# 🔐 Cybersecurity Class Notes (2026)

## 📚 Contents

- [About](#-about)
- [Learning Path](#-learning-path)
- [Topics](#-topics)
- [Tools & Technologies](#-tools--technologies)
- [Repository Structure](#-repository-structure)
- [Current Focus](#-current-focus)
- [Progress & Key Milestones](#-progress--key-milestones)

---

## 👨‍💻 About

Welcome to **cyber-class-2026**! This is my personal cybersecurity learning repository and technical journal. It contains my daily class notes, practical lab walkthroughs, assignments, and hands-on offensive/defensive security exercises.

The purpose of this repository is to document my journey, solidify my understanding of complex topics, and serve as a structured knowledge base for my cybersecurity career.

**Connect with me on LinkedIn:** [Mukesh Raja](https://www.linkedin.com/in/mukeshraja207/)

> 📚 **Learning → Practicing → Documenting → Improving**

---

## 🛤️ Learning Path

My journey covers both offensive (Red Team) and defensive (Blue Team) security, with a strong focus on practical, hands-on learning. I am progressing through fundamental networking and web architectures, moving into vulnerability assessment, exploitation, and enterprise defense, SIEM/SOC engineering, and post-quantum cryptanalysis.

---

## 🎯 Topics

- **Reconnaissance & Enumeration**: Network scanning, service enumeration, OSINT, and active reconnaissance across 24 search engines.
- **Web Application Security**: OWASP Top 10, the full catalog of 35 web attacks, SQLi/NoSQLi, SSRF, SSTI, Path Traversal, and proxy architectures.
- **Network & Perimeter Security**: IP addressing, subnetting, pivoting, port forwarding, wireless pentesting, and firewall/IDS evasion.
- **System Security & Exploitation**: Privilege escalation, Active Directory Kerberos mechanics (AS-REP Roasting, Kerberoasting, Golden/Silver tickets), and buffer overflows.
- **SOC & Detection Engineering**: Unified Kill Chain, Sysmon log telemetry, SIEM (Kibana/Splunk/Wazuh), YARA rule creation, Zeek network monitoring, and log anomaly baselining.
- **Mobile, IoT & OT / SCADA**: OWASP Mobile Top 10, Janus vulnerability, Frida SSL pinning bypass, hardware reversing (UART/JTAG), Purdue Model, and Modbus TCP.
- **Cloud & Container Security**: Shared responsibility, envelope encryption (KMS), Docker socket escapes, privileged breakouts, and Microsoft Graph Entra ID abuse.
- **DevSecOps & Forensics**: Git repository exploration, dangling object recovery, Linux kernel `auditd` forensics, and CVE-2021-3156 investigation.

---

## 🛠️ Tools & Technologies

- **Offensive Tools**: Burp Suite, Caido, OWASP ZAP, Nmap, EyeWitness, Socat, Metasploit, Hashcat, John the Ripper, Hydra, SQLMap, NoSQLMap, Frida
- **Defensive & SIEM Tools**: Sysmon, Wireshark, Tshark, Zeek, Kibana, Splunk, Wazuh, YARA, Falco, Elastic Endgame (Defend)
- **Infrastructure & Scripting**: Git, Bash, Python, Linux/Windows native auditing, Docker

---

## 📂 Repository Structure

Detailed navigation and walkthrough indexes are available within each section's README.

- 📁 **[CEH Master Study Hub](./ceh/)** — Certified Ethical Hacker (CEH v13) modules (01–20), attack taxonomy, and exam preparation.
  - 🚀 **[Interactive Web Exam Simulator](./ceh/test-preparation/exam-simulator.html)** — Offline proctored testing app with persistent browser database.
  - 📝 **[Official 125-Question Mock Paper](./ceh/test-preparation/ceh-v13-mock-exam-125q.md)** — Full 125Q blueprint mock paper with self-scoring grid.
  - 🎯 **[Test Preparation Dashboard](./ceh/test-preparation/)** — 153 scenario teardowns, formula sheets, score reports, and exam strategy.
- 📁 **[Weekly Notes](./week-01/)** — Daily class notes categorized by week:
  - [Week 01](./week-01/) | [Week 02](./week-02/) | [Week 03](./week-03/) | [Week 04](./week-04/) | [Week 05](./week-05/) | [Week 06](./week-06/) | [Week 07](./week-07/) | [Week 08](./week-08/)
- 📁 **[INE Labs](./INE_labs/)** — 37 practical lab walkthroughs from INE (Offensive, Defensive, SIEM, Malware Analysis & DevSecOps).
- 📁 **[Blue Team Labs](./blueteamlab/)** — Blue team investigations, Linux kernel `auditd` forensics (`paranoid`), Sysmon log analysis, and phishing email triage.
- 📁 **[Pentest Garage](./pentestgarage/)** — Independent pentesting practice, web exploitation, privilege escalation, container labs, and AI prompt security.
- 📁 **[Assignments](./assignments/)** — CTF cheat sheets, PTES penetration testing reports, network recon walkthroughs, and Cyber Kill Chain analysis.
- 📁 **[Meetups & Events](./meetups/)** — Takeaways, architecture diagrams, and certifications from cybersecurity community events (e.g., OWASP Juice Shop Workshop).
- 📁 **[References](./References/)** — Official EC-Council CEH courseware, NIST guidelines, SOC architecture documentation, and visual cheat sheets.

---

## 🔭 Current Focus

Currently, I am consolidating the complete **EC-Council Certified Ethical Hacker (CEH v13)** curriculum across all 20 modules—synthesizing advanced domains including Cloud IAM & container breakouts, OT/SCADA Modbus security, mobile malware engineering, and post-quantum cryptanalysis—alongside deep-dive **Blue Team forensics** (Linux kernel `auditd` analysis, Baron Samedit privilege escalation, and Sysmon/Wazuh lateral movement detection).

---

## 📈 Progress & Key Milestones

- 🎓 **CEH v13 Full Curriculum Coverage**: Completed comprehensive notes across all 20 modules ([Modules 01–03](./ceh/), [Modules 04–14 Master Class](./ceh/2026-10-27-ceh-master-class-notes.md), and [Modules 15–20 Master Class](./ceh/2026-10-31-ceh-advanced-domains-notes.md)).
- 🎯 **Exam Preparation Hub & Web Simulator**: Engineered an interactive [Web-Based Exam Simulator](./ceh/test-preparation/exam-simulator.html) with persistent database tracking, alongside a [125-Question Blueprint Mock Paper](./ceh/test-preparation/ceh-v13-mock-exam-125q.md) and [153 high-yield scenario teardowns](./ceh/test-preparation/comprehensive-mcq-revision-test.md).
- 🏆 **Official Blueprint Exam Milestone**: Achieved **92.0% (115/125)** on the Official 125-Question Blueprint Exam ([Scorecard Report](./ceh/test-preparation/reports/2026-11-17-ceh-v13-mock-exam-92pct-scorecard.md)).
- 🔬 **Practical Defensive Telemetry**: Documented 37 [INE practical labs](./INE_labs/) and hands-on [Blue Team investigations](./blueteamlab/), including custom Wazuh rules for PsExec and Mimikatz.
- 🤝 **Community & Hands-On Workshops**: Active participation in industry events including the OWASP Juice Shop Workshop Chennai ([Meetup Notes](./meetups/)).

---
*Generated and maintained as a structured learning portfolio.*
