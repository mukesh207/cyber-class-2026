# 🔬 INE Labs

A collection of detailed walkthroughs and technical notes from my INE (eLearnSecurity) practical labs. These labs focus on offensive security, network enumeration, defensive detection, log analysis, malware investigation, and DevSecOps workflows.

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
  - [Wazuh & Host Telemetry Engineering](#wazuh--host-telemetry-engineering)
  - [Kibana & SIEM Log Analysis](#kibana--siem-log-analysis)
  - [Malware Analysis & Endpoint Forensics](#malware-analysis--endpoint-forensics)
  - [Network Traffic & Zeek Monitoring](#network-traffic--zeek-monitoring)
  - [Core SOC Essentials](#core-soc-essentials)
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

### Wazuh & Host Telemetry Engineering
- [Detecting Abnormal Network Connections with Wazuh](./Detecting_Abnormal_Network_Connections_With_Wazuh/) — Identifying unauthorized outbound connections, C2 callbacks, and anomalous socket bindings via Wazuh agents.
- [Detecting Incidents in Internet-Facing Environments](./Detecting_Incidents_in_Internet-Facing_Environments/) — Investigating web application compromises, reverse shell executions, and Apache access log anomalies.
- [Detecting Mimikatz Threat Using Sysmon & Wazuh](./Detecting_Mimikatz_Threat_Using_Sysmon_and_Wazuh/) — Capturing LSASS process memory access (`Sysmon Event ID 10`) and building custom Wazuh XML detection rules.
- [Detecting PsExec with Wazuh](./Detecting_PsExec_with_Wazuh/) — Tracking lateral movement via remote service installation (`Sysmon Event ID 11/12/13`), named pipes, and correlating Wazuh alerts.
- [Introduction to Wazuh](./Introduction_to_Wazuh/) — Wazuh manager/agent architecture, enrollment, ruleset customization, and dashboard navigation.
- [Threat Detection with Wazuh & Sysmon](./Threat_Detection_with_Wazuh_Sysmon/) — Telemetry correlation between Windows Sysmon events and Wazuh log pipelines.

### Kibana & SIEM Log Analysis
- [Kibana: DNS Log Analysis](./Kibana:_DNS_log_analysis/) — Querying DNS telemetry to identify malicious domain generation algorithms (DGA) and DNS tunneling.
- [Kibana: Windows Event Logs I](./Kibana:_Windows_Event_Logs_I/) — Querying Windows event telemetry and security logs in Kibana.
- [Kibana: Windows Event Logs II](./Kibana:_Windows_Event_Logs_II/) — Advanced Kibana Lucene/KQL queries and logon authentication auditing.
- [Kibana: Windows Event Logs III](./Kibana:_Windows_Event_Logs_III/) — Investigating complex process execution and lateral movement events in Kibana.
- [Log Anomaly Detection Basics](./Log_Anomaly_Detection_Basics/) — Python-driven statistical baselining (`detect.py`) and log anomaly identification.

### Malware Analysis & Endpoint Forensics
- [Advanced Threat Analysis](./Advance_threat_analysis/) — Dissecting multi-stage threat indicators, CyberChef decoding, and payload analysis.
- [Investigating Malware Infection](./Investigating_Malware_Infection/) — Endpoint compromise triage, rogue process tree reconstruction, and persistence inspection.
- [Malware Analysis: Trojan](./Malware_Analysis_Trojan/) — Behavioral and dynamic analysis of trojanized executables, API hooking, and artifact extraction.
- [Malware Fundamentals: LockBit 2.0 Analysis](./Malware_Fundamentals_LockBit_2_Analysis/) — Dissecting LockBit ransomware, VSS volume shadow copy deletion, multi-threaded encryption, and defensive IOC extraction.
- [SOC 1: Detecting Malware Walkthrough](./SOC1_Detecting_Malware_Walkthrough/) — Tier 1 triage, malicious hash reputation checking, payload quarantine, and incident response containment.

### Network Traffic & Zeek Monitoring
- [PCAP Analysis with Zeek](./PCAP_Analysis_With_Zeek/) — Network security monitoring with Zeek, protocol log triage (`conn.log`, `dns.log`, `http.log`), and suspicious stream carving.
- [SOC-1: Networking Essentials](./SOC-1_Networking_Essentials/) — Packet analysis, network telemetry, and traffic flow analysis.

### Core SOC Essentials
- [SOC-1: Windows Essentials](./SOC-1_:_Windows_Essentials/) — Core Windows security log monitoring and SOC analyst workflows.
- [SOC-1: Linux Essentials](./SOC-1_Linux_Essentials/) — Linux audit log analysis, syslog investigation, and bash history telemetry.
- [Introduction to Splunk](./Introduction_to_Splunk/) — Lab evidence and query snapshots for enterprise Splunk SIEM search processing language (SPL).
- [Malicious User Behaviour Analysis](./Malicious_User_Behaviour_Analysis/) — User and Entity Behavior Analytics (UEBA) evidence and anomalous insider activity tracking.

---

## 🛠️ Git & DevSecOps

- [Automated Git Repo Recovery](./Automated_Git_Repo_Recovery/) — Scripting recovery of dangling objects and lost commits.
- [Exploring a Git Repo](./Exploring_a_Git_Repo/) — Inspecting commit history, branches, and hidden metadata for sensitive data.
- [Recovering Key Git Repo Files](./Recovering_Key_Git_Repo_Files/) — Extracting deleted files and credentials from Git object storage.
