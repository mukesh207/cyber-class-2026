# 🤝 Cybersecurity Meetups, Workshops & Community Events

> **Directory:** `meetups/`  
> **Purpose:** Technical logs, architectural analyses, laboratory investigations, and actionable takeaways from cybersecurity conferences, community meetups, and hands-on workshops.  
> **Navigation:** [🏠 Root Dashboard](../README.md)

---

## 🎯 Overview

Attending cybersecurity community meetups, technical summits, and hands-on workshops bridges academic concepts, CTF challenges, and real-world enterprise operations. This directory houses deep-dive write-ups, architecture breakdowns, lab observations, event photography, and certifications acquired through community participation.

Every event write-up strictly adheres to our core learning philosophy:
* **Understanding over memorization:** Deconstructing *why* technologies, architectures, and attack vectors behave the way they do.
* **Separation of theory and hands-on practice:** Differentiating observable facts, tool outputs, and telemetry from unverified assumptions.
* **Adversarial & defensive convergence:** Analyzing every topic through the dual lenses of a **penetration tester** (offensive exploitability) and a **SOC analyst** (defensive detection and telemetry).

---

## 🔄 Meetup Knowledge Transfer Loop

```text
+=============================================================================+
|                      COMMUNITY KNOWLEDGE INTEGRATION                        |
+=============================================================================+

   1. INDUSTRY MEETUP / WORKSHOP           2. DEEP TECHNICAL ANALYSIS
   [ Guest Speaker / Live Demo / CTF ] ==> [ Deconstruct Architecture, RFCs, ]
                                           [ TTPs, and Protocol Mechanics    ]
                                                          |
                                                          v
   4. PERMANENT KNOWLEDGE BASE             3. HANDS-ON LAB RECREATION
   [ Documented in Portfolio with     ] <== [ Validate in PentestGarage,      ]
   [ ASCII Diagrams & SOC Detections  ]     [ INE Labs, or Local Docker VMs  ]
```

---

## 📅 Events Log

| Date | Event / Workshop | Venue / Format | Key Speaker / Facilitator | Core Focus Areas | Artifacts & Credentials | Technical Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-10-24** | **OWASP Juice Shop Hands-On Workshop** | Apple Hall, Sri Sairam Engineering College, Chennai | **Björn Kimminich** (OWASP Juice Shop Project Leader; Product Group Lead at Kuehne+Nagel) | Modern SPA Architecture, Angular Routing, Server-Side Authorization Boundaries, MultiJuicer on Kubernetes, Client-Side Sensor Security | 🎓 Certificate of Participation (OWASP Chennai Chapter)<br>📸 Lab Photos | [Read Workshop Write-Up](./OWASP-Juice-Shop-Workshop-Chennai-2026/README.md) |
| **2026-07-26** | **Talent Talks Meetup** | Community Meetup / Industry Panel | Industry Panel & SOC / DFIR Practitioners | Networking Bedrock, NOC vs. SOC vs. SOR Operations, APT Threat Landscapes, RFC 3227 Order of Volatility, Bash Triage Automation | 📝 Practical Bash Scripts & Triage Checklists | [Read Meetup Notes](./2026-07-26-talent-talks.md) |

---

## 🌐 Thematic Synthesis Across Events

```text
+-----------------------------------------------------------------------------+
|                          MEETUP KNOWLEDGE DOMAINS                           |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [ Web & AppSec ]               [ Enterprise Operations ]  [ Threat Intel ] |
|  - Modern SPA Architecture       - NOC vs. SOC vs. SOAR    - APT Profiles   |
|  - Angular Client Routing        - Tier 1 -> Tier 3 Triage - Living-off-Land|
|  - Server-Side Access Control    - RFC 3227 Volatility     - C2 Channels    |
|                                                                             |
|  [ Cloud & Containers ]         [ Defense & Automation ]  [ Career Skills ] |
|  - MultiJuicer on Kubernetes     - Splunk / Sigma Rules    - Soft Skills    |
|  - Dynamic Pod Balancing         - Bash Log Parsers        - Risk Reporting |
|  - Multi-Tenant CTF State        - Rapid Subnet Sweeps     - Hands-on Proof |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### 1. Modern Web Application Security & Cloud Architecture
* **Single Page Applications (SPAs):** SPAs (Angular, React, Vue) fundamentally shift how clients interact with servers. Routing tables and internal module references are compiled into public JavaScript assets (`main.js`), demanding strict server-side authorization enforcement rather than relying on UI route hiding.
* **Containerized Training Environments:** Platforms like **MultiJuicer** demonstrate how Kubernetes, session cookies, and dynamic reverse-proxying eliminate database race conditions and allow scalable multi-tenant CTF deployments.
* *Detailed in:* [OWASP Juice Shop Hands-On Workshop (2026-10-24)](./OWASP-Juice-Shop-Workshop-Chennai-2026/README.md)

### 2. Enterprise Security Operations & The Incident Lifecycle
* **The Operational Triad:** Clear segregation of operational scopes between **NOC** (network uptime and availability), **SOC** (threat detection and alert triage), and **SOR/SOAR** (automated containment playbooks).
* **Incident Escalation:** Tier 1 SIEM triage feeding into Tier 2 deep analysis, supported by Tier 3 hypothesis-driven threat hunting.
* *Detailed in:* [Talent Talks Meetup (2026-07-26)](./2026-07-26-talent-talks.md)

### 3. Adversarial Mechanics & Digital Forensics
* **Advanced Persistent Threats (APTs):** State-sponsored actors rely on patience, dwell time, and living-off-the-land tools (`powershell.exe`, `wmic.exe`, `certutil.exe`) rather than noisy public exploits.
* **Evidence Preservation (RFC 3227):** Incident response must adhere strictly to the Order of Volatility (capturing live RAM, process states, and active sockets before touching persistent disk media).
* *Detailed in:* [Talent Talks Meetup (2026-07-26)](./2026-07-26-talent-talks.md)

### 4. Practical Automation & Command-Line Engineering
* **Scripting as a Force Multiplier:** Fluency in **Bash** and core utilities (`awk`, `grep`, `sort`, `uniq -c`) enables rapid log triage and host discovery directly on production Linux servers without installing bulky external tooling.
* *Detailed in:* [Talent Talks Meetup (2026-07-26)](./2026-07-26-talent-talks.md)

---

## 🔗 Cross-Repository References

The concepts explored during meetups directly intersect with coursework, labs, and exercises across this repository:

* **[Weekly Class Notes](../week-01/)**: Daily lectures covering fundamental TCP/IP networking, Linux administration, and web protocols.
* **[Week 04 — Web AppSec & OWASP Top 10](../week-04/2026-09-01.md)**: Complements the OWASP Juice Shop workshop with deep dives into SQL injection and broken access controls.
* **[INE Labs](../INE_labs/)**: Hands-on offensive, defensive, and DevSecOps labs validating enterprise architectures.
* **[Blue Team Labs](../blueteamlab/)**: SOC investigations, Sysmon log analysis, and phishing email triage exercises.
* **[Pentest Garage](../pentestgarage/)**: Practical machine exploitation, web challenge walkthroughs, and privilege escalation techniques.

---

## 📋 Action Items & Community Roadmap

- [x] Document Talent Talks meetup insights and establish operational frameworks.
- [x] Document OWASP Juice Shop workshop with Björn Kimminich, including architecture diagrams, access control tests, and participation certificate.
- [ ] Implement automated Bash log analysis script for Apache/Nginx web server access logs.
- [ ] Solve and document remaining OWASP Juice Shop multi-stage challenges in an authorized lab environment.
- [ ] Connect with local OWASP Chennai chapter members for future hands-on security sessions.
