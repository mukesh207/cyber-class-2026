# 🔬 INE Labs

A collection of detailed walkthroughs and technical notes from my INE (eLearnSecurity) practical labs. These labs focus on offensive security, network enumeration, defensive detection, log analysis, and DevSecOps workflows.

> ℹ️ **Note on Content:** The `.pdf` files found within these lab directories are the official lab manuals provided by INE. The `.md` files (walkthroughs) are my personal step-by-step solutions, technical notes, and key takeaways created while completing the labs.

---

## 📂 Typical Lab Structure

Each individual lab folder generally follows this format:

```text
Lab_Name/
├── Lab_Walkthrough.md     ← Personal detailed walkthrough and technical notes
├── walkthrough-XXXX.pdf   ← Official INE lab manual/walkthrough
└── screenshots/ / *.png   ← Associated evidence, screenshots, and architecture diagrams
```

---

## 📚 Contents

- [Reconnaissance & Enumeration](#-reconnaissance--enumeration)
- [System Security & Exploitation](#-system-security--exploitation)
- [Authentication & Access Control](#-authentication--access-control)
- [SOC, SIEM & Threat Analysis](#-soc-siem--threat-analysis)
- [Git & DevSecOps](#-git--devsecops)

---

## 🔎 Reconnaissance & Enumeration

- [DNS Enumeration](./DNS_Enumeration/) — Step-by-step DNS record enumeration and zone transfers.
- [DNS and Vhosts](./DNS_and_Vhosts/) — Virtual host discovery and DNS mapping.
- [Windows: Enumerating Processes and Services](./Enumerating_Processes_and_Services/) — Local process inspection and service auditing on Windows.
- [Automating Windows Local Enumeration](./Automating_WindowsLocal_Enumeration/) — Automated script-based enumeration on Windows targets.
- [Intro to EyeWitness](./Intro_to_EyeWitness/) — Automated web application screenshotting and fingerprinting.
- [Radius Recon: Dictionary Attacks](./Radius_Recon:_Dictionary_Attacks/) — RADIUS authentication service enumeration and dictionary attacks.
- [Service Discovery and Fingerprinting with Nmap](./Service%20Discovery%20and%20Fingerprinting%20with%20Nmap/) — Comprehensive Nmap scanning, service versioning, and OS fingerprinting.
- [SNMP Recon: Basics](./SNMP_Recon:Basics/) — SNMP community string enumeration and MIB walking.
- [SNMP Recon: Basics II](./SNMP_Recon:_Basics_II/) — Hostname and email address extraction via SNMP.
- [Squid Recon: Dictionary Attack](./Squid_Recon:_Dictionary_Attack/) — Proxy service enumeration and credential brute-forcing.

---

## 💻 System Security & Exploitation

- [Transferring Files To Windows Targets](./Transferring_Files_To_Windows_Targets/) — Techniques for transferring payloads and binaries to Windows targets.

---

## 🔑 Authentication & Access Control

- [Windows: NTLM Hash Cracking](./Windows:_NTLM_HashCracking/) — Extracting and cracking Windows NTLM hashes using offline tools.

---

## 🛡️ SOC, SIEM & Threat Analysis

- [Advanced Threat Analysis](./Advance_threat_analysis/) — Dissecting multi-stage threat indicators and payload analysis.
- [Kibana: Windows Event Logs I](./Kibana:_Windows_Event_Logs_I/) — Querying Windows event telemetry and security logs in Kibana.
- [Kibana: Windows Event Logs II](./Kibana:_Windows_Event_Logs_II/) — Advanced Kibana queries and authentication log analysis.
- [Kibana: Windows Event Logs III](./Kibana:_Windows_Event_Logs_III/) — Investigating complex process execution and lateral movement events in Kibana.
- [Log Anomaly Detection Basics](./Log_Anomaly_Detection_Basics/) — Identifying baseline deviations and log anomalies.
- [SOC-1: Windows Essentials](./SOC-1_:_Windows_Essentials/) — Core Windows security log monitoring and SOC analyst workflows.
- [SOC-1: Linux Essentials](./SOC-1_Linux_Essentials/) — Linux audit log analysis, syslog investigation, and bash history telemetry.
- [SOC-1: Networking Essentials](./SOC-1_Networking_Essentials/) — Packet analysis, network telemetry, and traffic flow analysis.

---

## 🛠️ Git & DevSecOps

- [Automated Git Repo Recovery](./Automated_Git_Repo_Recovery/) — Scripting recovery of dangling objects and lost commits.
- [Exploring a Git Repo](./Exploring_a_Git_Repo/) — Inspecting commit history, branches, and hidden metadata for sensitive data.
- [Recovering Key Git Repo Files](./Recovering_Key_Git_Repo_Files/) — Extracting deleted files and credentials from Git object storage.
