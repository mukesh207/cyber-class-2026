# 🛡️ Certified Ethical Hacker (CEH v13) Master Study Hub

Comprehensive technical study notes for the EC-Council **Certified Ethical Hacker (CEH v13)** curriculum. This dedicated study hub bridges offensive penetration testing methodologies with defensive Security Operations Center (SOC) detection engineering, prioritizing **deep mechanical understanding over rote memorization**.

---

## 🗺️ Master Curriculum Roadmap

| Module | Title | Status | Focus / Core Competencies | Study Notes |
| :---: | :--- | :---: | :--- | :---: |
| **01** | **Introduction to Ethical Hacking** | ✅ Completed | CIA Triad, Security Frameworks, Threat Attribution, AI in Pentesting, Defense-in-Depth, CVSS | [View Notes](./mod-01-introduction-to-ethical-hacking.md) |
| **02** | **Footprinting and Reconnaissance** | ✅ Completed | Passive/Active OSINT, 24 Search Engines, DNS Interrogation, AXFR, Email Header Forensics, Splunk Detection | [View Notes](./mod-02-footprinting-and-reconnaissance.md) |
| **03** | **Scanning Networks** | ⏳ Next Up | Host Discovery, Port Scanning Mechanics (SYN, FIN, NULL, Xmas), Nmap Scripting Engine (NSE), IDS Evasion | *Queued* |
| **04** | **Enumeration** | 📋 Planned | NetBIOS, SNMP, LDAP, NTP, SMTP, RPC, DNS Zone Enumeration, Active Directory Initial Probing | *Planned* |
| **05** | **Vulnerability Analysis** | 📋 Planned | Vulnerability Scoring (CVSS v4), Nessus/OpenVAS scanning, False Positive Validation | *Planned* |
| **06** | **System Hacking** | 📋 Planned | Password Cracking (Hashcat, John), Privilege Escalation (Linux/Windows), Steganography, Log Clearing | *Planned* |
| **07** | **Malware Threats** | 📋 Planned | Trojans, Backdoors, Polymorphic Viruses, Ransomware, Static & Dynamic Analysis, YARA | *Planned* |
| **08** | **Sniffing** | 📋 Planned | Wireshark Packet Analysis, ARP Poisoning, MAC Flooding, DHCP Starvation, Rogue Gateways | *Planned* |
| **09** | **Social Engineering** | 📋 Planned | Human Vector OSINT, Phishing Frameworks (GoPhish), Pretexting, USB drops, MFA Fatigue | *Planned* |
| **10** | **Denial-of-Service** | 📋 Planned | Volumetric & Application DoS/DDoS, SYN Floods, Slowloris, Amplification Attacks, Cloudflare/WAF Defenses | *Planned* |
| **11** | **Session Hijacking** | 📋 Planned | Layer 4 & Layer 7 Hijacking, TCP Sequence Prediction, Cookie Manipulation, Cross-Site Scripting (XSS) | *Planned* |
| **12** | **Evading IDS, Firewalls, & Honeypots** | 📋 Planned | Fragmentation, Decoy Scans, Protocol Tunneling, Honeypot Fingerprinting (Kippo/Cowrie) | *Planned* |
| **13** | **Hacking Web Servers** | 📋 Planned | Web Server Architecture, Apache/Nginx Misconfigurations, Directory Traversal, Web Shell Injection | *Planned* |
| **14** | **Hacking Web Applications** | 📋 Planned | OWASP Top 10, SSRF, SSTI, IDOR, Broken Authentication, API Security | *Planned* |
| **15** | **SQL Injection** | 📋 Planned | In-Band (Union-based), Inferential (Blind/Time-based), Out-of-Band (OOB), SQLMap Automation & Defense | *Planned* |
| **16** | **Hacking Wireless Networks** | 📋 Planned | 802.11 Protocols, WPA2/WPA3 4-Way Handshake Capture, PMKID Cracking, Rogue APs, Evil Twins | *Planned* |
| **17** | **Hacking Mobile Platforms** | 📋 Planned | Android APK Reverse Engineering, iOS Sandboxing, Frida Hooking, Mobile Device Management (MDM) | *Planned* |
| **18** | **IoT and OT Hacking** | 📋 Planned | Firmware Analysis, Hardware Debugging (JTAG/UART), Modbus/DNP3 SCADA protocols | *Planned* |
| **19** | **Cloud Computing** | 📋 Planned | AWS/Azure/GCP IAM Misconfigurations, S3 Bucket Takeover, Privilege Escalation in Cloud, CloudTrail Forensics | *Planned* |
| **20** | **Cryptography** | 📋 Planned | Symmetric/Asymmetric Ciphers, PKI, Diffie-Hellman Key Exchange, Cryptanalysis, Hash Collisions | *Planned* |

---

## 🎯 [Exam Test Preparation Hub](./test-preparation/)

A dedicated preparation area equipped with EC-Council exam-style question banks, quantitative risk formulas, protocol port cram sheets, and elimination strategies:

- 🎯 **[Comprehensive 19-Question MCQ Revision Test](./test-preparation/comprehensive-mcq-revision-test.md)** — In-depth technical breakdowns, ASCII attack flows, distractor analysis, and SOC engineering countermeasures for all 19 multi-domain exam scenarios.
- 📝 **[Modules 01 & 02 High-Yield Practice Exam](./test-preparation/mod-01-and-02-practice-questions.md)** — 15 realistic scenario-based questions with interactive expandable explanations.
- ⚡ **[Quick-Cram Exam Day Cheat Sheet](./test-preparation/quick-cram-cheat-sheet.md)** — High-yield formulas (ALE, SLE, ARO), port matrices, DNS record types, and command cheat sheets.
- 📋 **[Exam Blueprint & Trap Elimination Protocol](./test-preparation/README.md)** — Domain weightings, time-management tips, and question qualifier strategies.

---

## 📑 Completed Module Catalog

### 📘 [Module 01: Introduction to Ethical Hacking and Information Security](./mod-01-introduction-to-ethical-hacking.md)
- **Security Foundations:** The CIA Triad, Non-Repudiation, Digital Signatures, and the AAA Architecture.
- **The Attack Equation:** $\text{Attack} = \text{Motive} + \text{Method} + \text{Vulnerability}$.
- **Hacker Archetypes & Warfare:** White, Black, Grey, Script Kiddies, APTs, Hacktivists; Defensive (6 Pillars) vs. Offensive Information Warfare (5 Domains).
- **AI in Security:** LLMs in offensive reconnaissance (HackerGPT, PentestGPT, burpgpt) vs. Defensive SOC acceleration.
- **Frameworks & Attribution:** Lockheed Martin Cyber Kill Chain, Unified Kill Chain (UKC), CEH 5-Phase Hacking Cycle, MITRE ATT&CK, Pyramid of Pain, Diamond Model.
- **Defensive Strategy & Risk:** Defense-in-Depth (7 Concentric Rings), CVSS v3.1/v4.0 scoring calculation, Quantitative vs. Qualitative Risk (ALE, SLE, ARO).
- **Hands-on Labs:** OpenSSL cryptographic verification, ARP spoofing telemetry, CVSS calculation exercises.

### 📙 [Module 02: Footprinting and Reconnaissance](./mod-02-footprinting-and-reconnaissance.md)
- **Methodology & Blueprinting:** Passive vs. Active reconnaissance taxonomy; building the comprehensive Target Security Blueprint.
- **Search Engine OSINT & Google Dorking:** Advanced operators (`site:`, `inurl:`, `intitle:`, `filetype:`), Exploit-DB GHDB, CLI extraction with `lynx -dump` and ShellGPT prompt chaining.
- **24-Tool Specialized Search Engine Matrix:** Shodan, Censys, FOFA, ZoomEye, Grep.app, Searchcode, PublicWWW, Hunter.io, WiGLE, IntelX, Netlas, URLScan, FullHunt, SOCRadar, BinaryEdge, IVRE, crt.sh, Vulners, Pulsedive, GreyNoise, LeakIX, Onyphe, DeHashed, and Criminal IP.
- **Corporate & Human OSINT:** Tech-stack blueprinting through job board parsing, SEC EDGAR filings, and Wayback Machine CDX API enumeration.
- **Whois & RIR Infrastructure:** RFC 3912 protocol mechanics, ARIN/RIPE/APNIC queries, and post-GDPR privacy proxies.
- **DNS Deep-Dive:** Complete mechanics and tactical value of all **11 DNS Record Types** (A, AAAA, MX, NS, CNAME, SOA, SRV, PTR, RP, HINFO, TXT).
- **DNS Zone Transfers (AXFR):** RFC 5936 master-slave replication mechanics, exploitation syntax, and mitigation ACLs.
- **Network & Email Forensics:** Layer 3 TTL decrementing mechanics (ICMP vs. UDP vs. TCP SYN traceroutes), RFC 5322 bottom-to-top header tracing, and SPF/DKIM/DMARC anti-spoofing governance.
- **Automation & Tooling:** Maltego, Recon-ng, FOCA, theHarvester, SpiderFoot, and a custom Python reconnaissance automation script.
- **SOC Detection & Defense:** Split-Horizon DNS, BIND ACL configuration, and Splunk SIEM detection rules for unauthorized AXFR requests and NXDOMAIN enumeration spikes.
- **Real-Time Technical Scenario & Knowledge Check:** End-to-end Red Team recon vs. Blue Team SOC triage with 7 scenario-based validation questions.

---

## 🏛️ Study Methodology & Mentor Principles

All notes within this directory adhere to the following strict engineering standards:

```
+-----------------------------------------------------------------------------------+
|                        CEH STUDY NOTE ENGINEERING PRINCIPLES                      |
+-----------------------------------------------------------------------------------+
| 1. Mechanics Over Memorization | Explain WHY underlying protocols and tools act.  |
| 2. ASCII Flow Diagrams Only   | Architecture, packet flows, and attack chains.   |
| 3. Dual Red / Blue Perspective| Every attack paired with defenses & SIEM rules.  |
| 4. Tool Purpose & Workflows   | Focus on mechanics, data ingestion, and pipes.   |
| 5. Real-Time Scenarios        | Grounded technical scenarios for practical trial.|
| 6. Understanding Checks       | Scenario-driven challenges with hidden spoilers. |
+-----------------------------------------------------------------------------------+
```

---

## 📚 Local References & Courseware
- Official EC-Council PDF Courseware: `../References/CEH_REF/`
- OSINT Search Engines Taxonomy: `../References/search_engines_for_pentester.jpeg`
- DNS Record Types Reference: `../References/recordtypes.jpeg`
- CEH Footprinting Taxonomy: `../References/WhatsApp Image 2026-10-23 at 9.53.54 AM.jpeg`
