# 🛡️ Certified Ethical Hacker (CEH v13) Master Study Hub

Comprehensive technical study notes for the EC-Council **Certified Ethical Hacker (CEH v13)** curriculum. This dedicated study hub bridges offensive penetration testing methodologies with defensive Security Operations Center (SOC) detection engineering, prioritizing **deep mechanical understanding over rote memorization**.

---

## 🗺️ Master Curriculum Roadmap

| Module | Title | Status | Focus / Core Competencies | Study Notes |
| :---: | :--- | :---: | :--- | :---: |
| **01** | **Introduction to Ethical Hacking** | ✅ Completed | CIA Triad, Security Frameworks, Threat Attribution, AI in Pentesting, Defense-in-Depth, CVSS | [View Notes](./mod-01-introduction-to-ethical-hacking.md) |
| **02** | **Footprinting and Reconnaissance** | ✅ Completed | Passive/Active OSINT, 24 Search Engines, DNS Interrogation, AXFR, Email Header Forensics, Splunk Detection | [View Notes](./mod-02-footprinting-and-reconnaissance.md) |
| **03** | **Scanning Networks** | ✅ Completed | Host Discovery, TCP Flags/Handshakes, Port Scanning (SYN, FIN, Xmas, Idle Zombie), Fragmentation, Routing Manipulation, Proxy Chaining, Banner Grabbing | [View Notes](./mod-03-scanning-networks.md) |
| **04–14** | **Master Class: Enumeration to Web Attacks** | ✅ Completed | Protocols (SMB, SNMP, NetBIOS, LDAP, NTP, NFS, SMTP), Qualys VMDR, Kerberos (AS-REP, Roasting, Tickets), Buffer Overflow, YARA in SOC, Bettercap MITM, Botnets, Palo Alto NGFW, 35 Web Attacks | [View Notes](./2026-10-27-ceh-master-class-notes.md) |
| **04** | **Enumeration** | ✅ Completed | NetBIOS suffixes, SNMP OIDs, LDAP trees, NTP monlist, SMTP commands, SMB-to-John pipeline | [View Notes](./2026-10-27-ceh-master-class-notes.md#2-module-04-advanced-protocol-enumeration) |
| **05** | **Vulnerability Analysis** | ✅ Completed | CVSS v3.1 vs v4.0, Qualys VMDR vs Nessus architecture, assessment lifecycles | [View Notes](./2026-10-27-ceh-master-class-notes.md#3-module-05-vulnerability-analysis--enterprise-assessment) |
| **06** | **System Hacking** | ✅ Completed | Password cracking, Active Directory, Kerberos flows, Golden/Silver tickets, Buffer Overflows, CI/CD | [View Notes](./2026-10-27-ceh-master-class-notes.md#4-module-06-system-hacking-active-directory--kerberos-exploitation) |
| **07** | **Malware Threats** | ✅ Completed | APT lifecycle, LOLBins, YARA rule structure & SOC production detection rules | [View Notes](./2026-10-27-ceh-master-class-notes.md#5-module-07-malware-threats-apt-lifecycle--soc-yara-engineering) |
| **08** | **Sniffing** | ✅ Completed | Snooping vs Sniffing vs Spoofing vs Poisoning, Wireshark, Tshark, Bettercap, ARP/DHCP attacks | [View Notes](./2026-10-27-ceh-master-class-notes.md#6-module-08-sniffing-snooping-spoofing--network-attacks) |
| **09** | **Social Engineering** | ✅ Completed | Cialdini's triggers, Evilginx2 MFA bypass, Synthetic identity theft | [View Notes](./2026-10-27-ceh-master-class-notes.md#7-module-09-social-engineering-identity-theft--psychological-manipulation) |
| **10** | **Denial-of-Service** | ✅ Completed | Botnet C2, Volumetric vs State vs L7 (Slowloris deep mechanics), Amplification | [View Notes](./2026-10-27-ceh-master-class-notes.md#8-module-10-denial-of-service-dos-ddos--botnets) |
| **11** | **Session Hijacking** | ✅ Completed | Layer 4 vs Layer 7, Caido vs Burp Suite comparative architecture, Token defenses | [View Notes](./2026-10-27-ceh-master-class-notes.md#9-module-11-session-hijacking--web-proxies) |
| **12** | **Evading IDS, Firewalls, & Honeypots** | ✅ Completed | Network zones, Snort rules, Palo Alto NGFW (App-ID, User-ID, Content-ID), Tor | [View Notes](./2026-10-27-ceh-master-class-notes.md#10-module-12-evading-ids-firewalls--honeypots) |
| **13** | **Hacking Web Servers** | ✅ Completed | Web architectures, misconfigurations, AI prompt engineering in pentesting | [View Notes](./2026-10-27-ceh-master-class-notes.md#11-modules-13--14-web-servers-applications--owasp-top-10) |
| **14** | **Hacking Web Applications** | ✅ Completed | OWASP Top 10 (2017 vs 2021 evolution), Full Catalog of 35 Web Application Attacks | [View Notes](./2026-10-27-ceh-master-class-notes.md#12-the-complete-catalog-of-35-web-application-attacks) |
| **15–20** | **Master Class: Advanced Domains & Specialized Vectors** | ✅ Completed | SQLMap/NoSQLMap, URL Encodings, Tool Matrix (ZAP, Burp, Caido, Snort), OWASP Mobile M1-M10, Agent Smith, IoT Hardware/Firmware, OT/SCADA/PLC Modbus, Cloud IaaS/PaaS/SaaS, Docker Escapes, Microsoft Graph, Endgame EDR, Cryptanalysis | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md) |
| **15** | **SQL & NoSQL Injection** | ✅ Completed | BEUSTQ detection techniques, NoSQLMap operator injection, WAF impedance mismatch | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md#3-data-tier-exploitation--character-encoding-mechanics) |
| **16** | **Hacking Wireless Networks** | 📋 Planned | 802.11 Protocols, WPA2/WPA3 4-Way Handshake Capture, PMKID Cracking, Rogue APs, Evil Twins | *Planned* |
| **17** | **Hacking Mobile Platforms** | ✅ Completed | OWASP Mobile Top 10 (2024), Janus Flaw (CVE-2019-2107), Agent Smith, Frida SSL Bypass | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md#5-module-17-mobile-platform-security--malware-engineering) |
| **18** | **IoT and OT Hacking** | ✅ Completed | UART/JTAG reversing, Binwalk firmware extraction, Purdue Model (L0-L5), Modbus TCP, Fortinet & Defender for IoT | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md#6-module-18-iot--operational-technology-ot--scada--plc-security) |
| **19** | **Cloud Computing & Containers** | ✅ Completed | Shared Responsibility Matrix, Envelope Encryption, Docker Socket & Privileged Breakouts, Microsoft Graph Abuse | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md#7-module-19-cloud-computing-containers--identity-graph-exploitation) |
| **20** | **Cryptography & Cryptanalysis** | ✅ Completed | COA/KPA/CPA/CCA models, Shor's/Grover's algorithms, NIST PQC Standards (ML-KEM, ML-DSA) | [View Notes](./2026-10-31-ceh-advanced-domains-notes.md#9-module-20-cryptanalysis--post-quantum-cryptography) |

---

## 🎯 [Exam Test Preparation Hub](./test-preparation/)

A dedicated preparation area equipped with EC-Council exam-style question banks, quantitative risk formulas, protocol port cram sheets, and elimination strategies:

- 🎯 **[Comprehensive 153-Question Master MCQ Revision Test](./test-preparation/comprehensive-mcq-revision-test.md)** — In-depth technical breakdowns, ASCII attack flows, distractor analysis, and SOC engineering countermeasures for all 153 multi-domain exam scenarios.
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

### 📗 [Module 03: Scanning Networks](./mod-03-scanning-networks.md)
- **Scanning Methodology & Architecture:** The 7-step scanning sequence; active vs. passive discovery; why RFC determinism enables network scanning.
- **TCP/IP Flag & Handshake Mechanics:** Complete bitwise breakdown of all 9 TCP control flags (SYN, ACK, FIN, RST, PSH, URG, ECE, CWR, NS); mathematical mechanics of the 3-way handshake ($ISN$, $Ack = ISN + 1$) and graceful 4-way teardown vs. abrupt RST.
- **Protocol Weaponization & Attacks:** TCP SYN Flooding (TCB and backlog queue exhaustion, SYN cookie cryptography), TCP Reset (RST) hijacking, and stateful firewall table exhaustion (ACK/PSH+ACK floods against `conntrack`).
- **Scanning Tool Engines & Taxonomy:** Architecture and workflows of Nmap (raw socket timing T0-T5), Hping3 (custom header crafting), Masscan (10M+ pps asynchronous kernel bypass), ZMap, Netcat, and Unicornscan.
- **Host Discovery Probes:** Why modern ICMP fails against endpoint firewalls; ARP ping (`-PR`), TCP SYN Ping (`-PS`), TCP ACK Ping (`-PA`), and UDP ping (`-PU`).
- **Port Scanning Taxonomy:** TCP Connect (`-sT`), Stealth SYN (`-sS`), RFC 793 Inverse Scans (FIN, NULL, Xmas), ACK firewall mapping (`-sA`), and Window scanning (`-sW`), including the Microsoft Windows RFC non-compliance flaw.
- **The Idle Scan (Zombie Scan):** Deep 3-phase mathematical walkthrough of IP Identification (IPID) global counter abuse for 100% blind attribution scanning.
- **IDS/Firewall Evasion:** IP fragmentation fields (MF, DF, Fragment Offset), Tiny Fragment and Overlapping Fragment attacks; Strict/Loose Source Routing (SSRR/LSRR) manipulation.
- **Proxy Chaining & Anonymizers:** Forward vs. Reverse vs. Transparent proxies; SOCKS4 vs. SOCKS5 mechanics; `Proxychains-ng` configuration (Strict, Dynamic, Random) and resolving the raw socket proxy limitation.
- **Banner Grabbing & Fingerprinting:** Active raw socket interrogation (`nc`, `curl`, `openssl`, `nmap -sV`) vs. passive header sniffing (`p0f`, TTL and Window Size heuristic matrices).
- **SOC Detection & Defense:** Snort/Suricata rules for Xmas/NULL scans and SYN sweeps; Splunk SIEM SPL correlation for abnormal RST/SYN ratios; Linux kernel hardening (`sysctl` syncookies, source-route rejection).
- **Real-Time Technical Scenario & Troubleshooting:** Red Team DMZ assessment vs. SOC response; diagnosing failed inverse scans, proxychains raw leaks, and noisy idle zombies.

### 📕 [Modules 04–14: Comprehensive Master Class Notes (Enumeration to Web Attacks)](./2026-10-27-ceh-master-class-notes.md)
- **Protocol Enumeration:** Deep dive into SMB (null-sessions to John the Ripper cracking), NetBIOS suffixes, SNMP MIB/OIDs, LDAP directory trees, NTP monlist amplification, NFS root squashing, SMTP command verification, and IPsec aggressive-mode probing.
- **Enterprise Recon & AI Workflows:** OWASP Amass graph database mechanics and ShellGPT (`sgpt`) prompt chaining for automated reconnaissance and payload generation.
- **Vulnerability Analysis:** CVSS v3.1 vs v4.0 comparative scoring, Qualys VMDR cloud-agent architecture vs Tenable Nessus.
- **System Hacking & Active Directory:** Password cracking (Hashcat/John/pycrack), deep Kerberos 3-phase authentication flows, AS-REP Roasting, Kerberoasting, and an architectural comparison between Golden Tickets and Silver Tickets.
- **Memory Exploitation & CI/CD Security:** Buffer overflow stack anatomy (ESP, EBP, EIP overwrite), memory defenses (ASLR, DEP, Canaries), Poisoned Pipeline Execution (PPE), and offensive/defensive Bash scripts.
- **Malware & SOC YARA Engineering:** APT tradecraft, living-off-the-land techniques, and production-ready YARA rules for webshells and Cobalt Strike beacons.
- **Network Attacks & Traffic Analysis:** Snooping vs. Sniffing vs. Spoofing vs. Poisoning, Wireshark filters, headless `tshark` scripting, Bettercap MITM, ARP cache poisoning, and Layer 2 defenses (DAI, DHCP Snooping, Port Security).
- **Denial of Service & Session Hijacking:** Botnet C2 topologies, Slowloris thread exhaustion mechanics, Layer 4 TCP hijacking vs. Layer 7 token theft, and a comparative analysis of Caido vs. Burp Suite.
- **Perimeter Defense & Evasion:** Network segmentation zones (DMZ, LAN), Snort rule syntax, Palo Alto NGFW (App-ID, User-ID, Content-ID), and Anonymous Proxies/Tor onion routing.
- **Web Applications & The 35 Attacks:** Evolution of OWASP Top 10 (2017 vs. 2021) and the exhaustive catalog of all 35 Web Application Attacks from the CEH curriculum.

### 📓 [Modules 15–20: Advanced Domains & Specialized Attack Vectors](./2026-10-31-ceh-advanced-domains-notes.md)
- **Client-Side Exploitation:** Clickjacking (UI redressing) DOM mechanics, framebusting scripts and HTML5 sandbox bypasses, defensive response headers (`X-Frame-Options` and CSP `frame-ancestors`), and Watering Hole Attack (Strategic Web Compromise) lifecycles.
- **Data-Tier Attacks & Character Encodings:** Character conversion pipelines (ASCII vs. Hex vs. URL vs. Overlong UTF-8), WAF impedance mismatches, NoSQL injection mechanics in MongoDB/BSON, NoSQLMap automated extraction, and SQLMap's 6 detection techniques (`BEUSTQ`) with tamper script bypasses.
- **Security Tooling Ecosystem:** Comprehensive comparative matrix and operational workflows across OWASP ZAP (headless DAST), PortSwigger Burp Suite (Intruder attack modes & Collaborator OOB), Caido (next-gen Rust proxy architecture), Snort (signature grammar & preprocessors), and SQLMap.
- **Mobile Security (Module 17):** Updated OWASP Mobile Top 10 (M1 to M10), Android UID application sandboxing, Agent Smith malware dissecting the Janus vulnerability (CVE-2019-2107), and dynamic runtime instrumentation using Frida and Objection.
- **IoT & Operational Technology (Module 18):** 4-tier IoT architecture, hardware reversing (UART pinout discovery, JTAG boundary scanning), firmware extraction via `binwalk`, Purdue Model (Levels 0–5) IT/OT architectural contrast, Modbus TCP (Port 502) unauthenticated function code abuse, and enterprise defenses (Fortinet FortiGate Rugged vs. Microsoft Defender for IoT).
- **Cloud Computing & Containers (Module 19):** Cloud service models (IaaS, PaaS, SaaS) and the Shared Responsibility Matrix, envelope encryption with KMS, container privilege escalation (Docker socket `/var/run/docker.sock` and `--privileged` escapes), Linux namespaces/cgroups, Falco runtime auditing, and Microsoft Graph API Entra ID exploitation (illicit consent grant phishing & PRT extraction).
- **Endpoint Detection & Stealth Backdoors:** Elastic Endgame EDR (Elastic Defend) sensor architecture, user-space system call detours (`ntdll.dll`), Process Hollowing step-by-step injection, Windows persistence mechanisms (Run keys, services, WMI event subscriptions), and hunting unbacked executable memory.
- **Cryptanalysis & Quantum Threats (Module 20):** Classical cryptanalysis models (COA, KPA, CPA, CCA, side-channel leakage), Shor's algorithm (asymmetric destruction) vs. Grover's algorithm (symmetric halving), and NIST's standardized Post-Quantum Cryptography algorithms (ML-KEM, ML-DSA, SLH-DSA).

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
