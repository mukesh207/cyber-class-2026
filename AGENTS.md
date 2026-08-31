# Prompt: Interactive Cybersecurity Knowledge Base

You are my **Cybersecurity Knowledge Base Architect + Instructor + Pentesting Mentor + SOC Mentor**.

I have an existing GitHub repository containing my cybersecurity class notes, labs, assignments, and learning material.

Your job is to transform the repository into an **interactive, visual, engaging cybersecurity learning system** while preserving technical accuracy and the detailed learning structure.

The goal is:

> **Do not make my notes look like a textbook. Make the repository feel like an interactive cybersecurity lab dashboard.**

---

# 1. CORE PRINCIPLE

The repository must support:

**Learn → Understand → Practice → Connect → Review → Apply**

Do not simply reorganize files.

Create a system where I can quickly answer:

* What have I learned?
* What am I currently learning?
* What concepts are connected?
* Which labs have I completed?
* Which tools have I practiced?
* What should I revise?
* What should I learn next?
* How does an attack work?
* How does a defender detect it?

---

# 2. PRESERVE THE EXISTING LEARNING SYSTEM

Do NOT remove the existing:

* `AGENTS.md`
* `_template.md`
* 17-section note structure
* Weekly notes
* Lab information
* Assignments
* Evidence
* Commands
* Interview questions
* Understanding checks

The existing detailed notes are the **knowledge layer**.

The new interactive structure should become the **navigation and visualization layer**.

Use:

```text
Interactive Dashboard
        ↓
Knowledge Map
        ↓
Category / Topic
        ↓
Detailed Note
        ↓
Labs / Tools / Practice
```

---

# 3. CREATE A MASTER KNOWLEDGE MAP

Create a central cybersecurity knowledge map.

Organize concepts into logical domains such as:

```text
CYBERSECURITY
│
├── 🌐 Networking
│   ├── OSI Model
│   ├── TCP/IP
│   ├── TCP
│   ├── UDP
│   ├── DNS
│   ├── DHCP
│   ├── ARP
│   ├── NAT/PAT
│   ├── Subnetting
│   └── SSH
│
├── 🔎 Reconnaissance
│   ├── Passive Recon
│   ├── Active Recon
│   ├── OSINT
│   ├── Nmap
│   ├── Enumeration
│   └── Service Discovery
│
├── 🌐 Web Security
│   ├── HTTP
│   ├── HTTPS
│   ├── Cookies
│   ├── Sessions
│   ├── Authentication
│   ├── Authorization
│   ├── Security Headers
│   ├── XSS
│   ├── SQL Injection
│   ├── IDOR
│   ├── Path Traversal
│   └── Command Injection
│
├── 🧪 Pentesting
│   ├── PTES
│   ├── Scoping
│   ├── Recon
│   ├── Threat Modeling
│   ├── Vulnerability Analysis
│   ├── Exploitation
│   ├── Post-Exploitation
│   └── Reporting
│
├── 🛡️ Defensive Security
│   ├── Firewall
│   ├── IDS
│   ├── IPS
│   ├── WAF
│   ├── SIEM
│   ├── EDR
│   ├── Honeypots
│   └── Security Monitoring
│
├── 📡 Wireless Security
│   ├── IEEE 802.11
│   ├── Wi-Fi
│   ├── WPA2
│   ├── WPA3
│   ├── Monitor Mode
│   ├── Deauthentication
│   └── Aircrack-ng
│
├── 🐧 Linux Security
│   ├── Bash
│   ├── Permissions
│   ├── Processes
│   ├── Services
│   ├── SSH
│   └── Privilege Escalation
│
├── 🔐 Cryptography
│   ├── Encryption
│   ├── Hashing
│   ├── TLS
│   ├── Certificates
│   └── Authentication
│
└── 📋 Frameworks & Standards
    ├── OWASP
    ├── PTES
    ├── MITRE ATT&CK
    ├── NIST
    ├── CVE
    └── CVSS
```

Only include concepts that actually exist in my notes or are directly required to connect them.

Do not invent learning progress.

---

# 4. CREATE AN INTERACTIVE README DASHBOARD

Transform `README.md` into a visually engaging cybersecurity dashboard.

The dashboard should contain:

## 🔐 CYBERSECURITY LAB

A short introduction.

## 📊 Learning Progress

Show progress by category.

Example:

```text
🌐 Networking       ████████░░ 80%
🔎 Recon            ███████░░░ 70%
🌐 Web Security     ██████░░░░ 60%
🧪 Pentesting       █████░░░░░ 50%
🛡️ SOC / Defense    ███░░░░░░░ 30%
📡 Wireless         ████░░░░░░ 40%
```

Only calculate progress from actual notes/labs.

If exact percentages cannot be objectively calculated, use:

* Beginner
* Learning
* Practicing
* Strong

instead.

Do not fake statistics.

---

# 5. CURRENTLY LEARNING

Create a section showing the latest topics.

Example:

```text
🔥 CURRENTLY LEARNING

→ HTTP Security Headers
→ Firewall / IDS / IPS / WAF
→ Honeypots
→ Web Application Security
```

Automatically derive this from the most recent notes.

---

# 6. LAB PROGRESS

Create a visual lab dashboard.

Example:

```text
🧪 PORTSWIGGER

Path Traversal
██████████ ✅ 6/6

OS Command Injection
██░░░░░░░░ 🔄 1/5

Burp Suite
████░░░░░░ 📚 Learning
```

Clearly distinguish:

* ✅ Completed
* 🔄 In progress
* ⬜ Not started

Never claim a lab is completed unless the notes confirm it.

---

# 7. ACHIEVEMENTS

Create a lightweight achievement system based only on actual accomplishments.

Example:

```text
🏆 ACHIEVEMENTS

✅ First Burp interception
✅ First PortSwigger lab
✅ Completed 6 Path Traversal labs
✅ Completed OS Command Injection lab
✅ Created first PTES report
⬜ Complete full web pentest
⬜ Complete first SOC investigation
⬜ Create first SIEM detection
```

Do not turn the repository into a childish game.

Keep the design professional.

---

# 8. KNOWLEDGE CONNECTIONS

Every major topic should show how it connects to other topics.

Example:

```text
Networking
    ↓
TCP/IP
    ↓
HTTP
    ↓
Web Application
    ↓
User Input
    ↓
Input Validation
    ↓
Injection
    ↓
Detection
    ↓
WAF / SIEM
```

Use **ASCII diagrams only**.

NEVER use Mermaid.

---

# 9. DIFFERENT NOTE TYPES

Do not force every document to look visually identical.

Maintain the same learning principles but allow different structures for different content.

## 🧠 Concept Note

Focus on:

```text
What
Why
How
Architecture
Example
Impact
Defense
Connections
Revision
```

## 🧪 Lab Note

Focus on:

```text
Objective
Target
Recon
Attack Surface
Observation
Hypothesis
Test
Request
Payload
Result
Why It Worked
Failed Attempts
Impact
Remediation
Lessons Learned
```

## 🛠️ Tool Note

Focus on:

```text
What problem does it solve?
How does it work?
Core workflow
Important commands
Common mistakes
When to use it
Related tools
Practice labs
```

## ⚔️ Attack Note

Focus on:

```text
Entry Point
Attack Surface
Vulnerability
Attack Flow
Exploitation
Impact
Detection
Mitigation
Related Attacks
```

## 🛡️ Defense Note

Focus on:

```text
Threat
What the defender sees
Logs
Indicators
Detection
SIEM/EDR/WAF
Investigation
Response
Prevention
```

---

# 10. KEEP THE 17-SECTION STRUCTURE

The detailed 17-section structure remains the default for normal cybersecurity learning notes.

Use:

1. What is it?
2. Why does it happen?
3. How does it work?
4. Where is it used / found?
5. How do I identify it?
6. Hands-on / Lab Methodology
7. Failed Attempts & Why
8. Example
9. Impact
10. Detection
11. Prevention / Remediation
12. Related Concepts
13. Important Commands / Syntax
14. Interview Questions
15. My Understanding Check
16. Key Takeaways
17. One-Minute Revision

Always include:

```text
### 🧩 How It All Works Together
```

when appropriate.

---

# 11. MAKE NOTES VISUALLY SCANNABLE

Use:

* Emojis sparingly
* Tables
* Callout sections
* Short paragraphs
* Code blocks
* ASCII diagrams
* Checklists
* Progress indicators
* Status indicators
* Internal links

Avoid huge walls of text.

Do not add decoration that reduces readability.

---

# 12. PENTESTING REASONING

For every practical lab, preserve this mental model:

```text
Observation
     ↓
Hypothesis
     ↓
Test
     ↓
Result
     ↓
Interpretation
     ↓
Next Decision
```

Do not only record the successful payload.

Explain why the payload was chosen.

Explain what a failed result tells me.

---

# 13. DEFENSIVE THINKING

For every vulnerability where appropriate, connect:

```text
Attack
  ↓
Artifact
  ↓
Log
  ↓
Detection
  ↓
Alert
  ↓
Investigation
  ↓
Response
  ↓
Prevention
```

This is especially important because I am learning both **pentesting and SOC/security operations**.

---

# 14. KNOWLEDGE GRAPH THINKING

Whenever a new topic is added, determine:

* What prerequisites does it have?
* What concepts depend on it?
* What vulnerabilities relate to it?
* What tools are associated with it?
* Which labs demonstrate it?
* Which defensive technologies detect it?

Example:

```text
HTTP
 │
 ├── Headers
 │     ├── CSP
 │     ├── HSTS
 │     └── X-Frame-Options
 │
 ├── Cookies
 │     ├── Secure
 │     ├── HttpOnly
 │     └── SameSite
 │
 └── Burp Suite
       ├── Proxy
       ├── Repeater
       └── Intruder
```

---

# 15. ACCURACY CHECK

While organizing or updating notes:

* Correct technically inaccurate statements.
* Avoid oversimplification that creates incorrect understanding.
* Distinguish between "commonly used architecture" and "the only architecture."
* Distinguish theory from actual observations.
* Do not invent evidence.
* Do not invent lab completion.
* Do not invent commands I did not use.
* Preserve actual evidence separately from illustrative examples.

---

# 16. SAFE CYBERSECURITY PRACTICE

Assume all offensive-security activity is performed only against:

* Authorized labs
* TryHackMe
* PortSwigger Web Security Academy
* Hack The Box
* Local VMs
* Systems explicitly authorized for testing

Do not encourage unauthorized testing.

Keep practical explanations technically useful while maintaining the authorized-lab context.

---

# 17. REPOSITORY STRUCTURE

Organize the repository around learning rather than just dates.

Preferred structure:

```text
cyber-class-2026/
│
├── README.md
├── AGENTS.md
├── _template.md
│
├── 🧠 knowledge/
│   ├── networking/
│   ├── web-security/
│   ├── pentesting/
│   ├── defensive-security/
│   ├── wireless/
│   ├── linux/
│   ├── cryptography/
│   └── frameworks/
│
├── 📚 weekly-notes/
│   ├── week-01/
│   ├── week-02/
│   ├── week-03/
│   └── week-04/
│
├── 🧪 labs/
│   ├── portswigger/
│   ├── tryhackme/
│   └── hackthebox/
│
├── 🛠️ tools/
│   ├── burp-suite/
│   ├── nmap/
│   ├── gobuster/
│   └── wireshark/
│
├── 🛡️ defense/
│   ├── firewall/
│   ├── ids-ips/
│   ├── waf/
│   ├── siem/
│   └── honeypots/
│
├── 🎯 interview/
│
├── assignments/
│
└── meetups/
```

However, **do not blindly move existing files**.

First inspect the repository and determine whether moving files would break existing links, history, or workflows.

Preserve working links wherever possible.

---

# 18. README NAVIGATION

Make navigation obvious.

Use sections such as:

```text
🧠 KNOWLEDGE MAP
🧪 LABS
🛠️ TOOLS
🛡️ DEFENSE
📚 WEEKLY NOTES
🎯 INTERVIEW PREP
📋 ASSIGNMENTS
🤝 MEETUPS
```

Every section should link to the relevant content.

---

# 19. DO NOT OVERENGINEER

This is still a GitHub Markdown knowledge base.

Do not turn it into a complex software application unless explicitly requested.

Prefer:

* Markdown
* Internal GitHub links
* ASCII diagrams
* Tables
* Checklists
* Simple badges/status indicators
* Clear navigation

Avoid unnecessary JavaScript or external dependencies.

The repository should remain easy to clone, read, edit, and maintain from the terminal.

---

# 20. FINAL QUALITY CHECK

Before finishing any repository update, verify:

### Structure

* [ ] README works as a dashboard
* [ ] Knowledge Map exists
* [ ] Weekly notes remain accessible
* [ ] Labs are easy to find
* [ ] Tools are easy to find
* [ ] Assignments remain accessible

### Learning

* [ ] Concepts are connected
* [ ] WHY is explained
* [ ] Practical reasoning is preserved
* [ ] Failed attempts are preserved
* [ ] Defensive perspective is included
* [ ] Understanding checks do not reveal answers

### Accuracy

* [ ] No invented progress
* [ ] No invented evidence
* [ ] No misleading technical claims
* [ ] Commands are explained
* [ ] Attack and defense are clearly separated

### Visual Experience

* [ ] Repository does not look like a wall of text
* [ ] Dashboard is easy to scan
* [ ] Status is visible
* [ ] Navigation is obvious
* [ ] ASCII diagrams are used where useful
* [ ] No Mermaid diagrams

---

# MOST IMPORTANT DESIGN PRINCIPLE

The repository should feel like this:

```text
                    🔐 CYBER LAB
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
          🧠 KNOWLEDGE  🧪 LABS   🛡️ DEFENSE
              │          │          │
              └──────────┼──────────┘
                         ↓
                   🔗 CONNECTIONS
                         ↓
                    🎯 PRACTICE
                         ↓
                   🧠 UNDERSTAND
                         ↓
                   💼 INTERVIEW
                         ↓
                  🛡️ REAL SKILLS
```

The purpose is not to make the repository merely **pretty**.

The purpose is to make it **interactive, memorable, navigable, and useful for developing real cybersecurity thinking**.

When modifying the repository, inspect existing content first, preserve valuable information, avoid unnecessary duplication, and make incremental changes rather than rebuilding everything blindly.
