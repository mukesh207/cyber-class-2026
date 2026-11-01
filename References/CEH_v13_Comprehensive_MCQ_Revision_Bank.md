# CEH v13 – Comprehensive MCQ Revision Bank

**Format:** Question → options → correct answer  
**Note:** Repeated questions from the supplied material have been consolidated into one entry. Wording has been lightly cleaned where needed; the answer choices are retained in substance. A few technically nuanced items are flagged in the notes at the end.

---

## 1. Cloud, Containers, Serverless and Kubernetes

### 1. Serverless function-to-function injection
An attacker targets a serverless web app. They send a malicious payload from a Contact Form function to a Billing function that shares the same execution environment. What is the cloud risk?

- A. Insecure Cloud Configuration / Lack of Isolation
- B. SQL Injection
- C. Broken Authentication
- D. Phishing

**Answer: A — Insecure Cloud Configuration / Lack of Isolation**

### 2. AWS Lambda event injection and excessive permissions
An AWS Lambda function has permissive IAM roles that allow it to read any S3 bucket in the account. By exploiting event injection in the function's input, an attacker forces it to exfiltrate private logs. What attack is this?

- A. Broken Function Level Authorization
- B. Function Data Injection / Insecure Cloud Configuration
- C. Cross-Site Scripting
- D. SQL Injection

**Answer: B — Function Data Injection / Insecure Cloud Configuration**

### 3. Cloud metadata service access
In a microservices architecture, an attacker compromises one service and calls the metadata service at `169.254.169.254` to steal temporary IAM credentials. What vulnerability is being exploited?

- A. SSRF (Server-Side Request Forgery)
- B. Cross-Site Scripting
- C. Insecure Deserialization
- D. Directory Traversal

**Answer: A — SSRF (Server-Side Request Forgery)**

### 4. GCP metadata SSRF
A GCP Cloud Function accepts a URL and generates a PDF screenshot. An attacker supplies the Google metadata token endpoint, and the generated PDF contains the function's OAuth access token. What attack is this?

- A. Server-Side Request Forgery (SSRF) against Cloud Metadata Service
- B. Cross-Site Scripting
- C. SQL Injection
- D. Local File Inclusion

**Answer: A — SSRF against the Cloud Metadata Service**

### 5. IAM role hopping through an EC2 instance
An attacker compromises a developer laptop and obtains AWS credentials. The role cannot list S3 buckets but has `iam:PassRole` and `ec2:RunInstances`. The attacker launches an EC2 instance and attaches an AdminRole to it. What is this privilege escalation technique?

- A. Cloud Drift Injection
- B. IAM Role Hopping via Instance Profile
- C. S3 Bucket Policy Bypass
- D. Metadata Service Impersonation

**Answer: B — IAM Role Hopping via Instance Profile**

### 6. S3 policy manipulation
An attacker has `s3:PutBucketPolicy` permission and changes a bucket policy to deny legitimate administrators access, holding the data hostage without stealing it. What attack is this?

- A. Cloud Ransomware / Denial of Service via Policy Manipulation
- B. S3 Data Exfiltration
- C. Bucket Hopping
- D. Privilege Escalation

**Answer: A — Cloud Ransomware / Denial of Service via Policy Manipulation**

### 7. S3 resource metadata leakage
An attacker can inspect object tags and metadata in a publicly listable S3 bucket. A tag contains a plaintext staging password. What is this?

- A. S3 Bucket Policy Bypass
- B. Sensitive Data Exposure via Resource Metadata
- C. Insecure Direct Object Reference
- D. Cross-Stack Resource Sharing

**Answer: B — Sensitive Data Exposure via Resource Metadata**

### 8. Docker bind-mount escape
An attacker exploits a writable bind mount in a Docker container to write a malicious script into the host's `/etc/cron.d/`. What technique is this?

- A. Kernel Exploit
- B. Host Filesystem Escape / Privilege Escalation via Cron
- C. SQL Injection
- D. ARP Poisoning

**Answer: B — Host Filesystem Escape / Privilege Escalation via Cron**

### 9. Docker socket exposure
A web container has `/var/run/docker.sock` mounted. After compromising the container, an attacker communicates with the Docker daemon, creates a privileged container, and mounts the host filesystem. What is this?

- A. Directory Traversal
- B. Container Breakout via Socket Exposure
- C. Kernel Exploit
- D. Side-channel Attack

**Answer: B — Container Breakout via Socket Exposure**

### 10. Kubernetes privileged pod escape
A Kubernetes pod runs with `Privileged: true` and shares the `HostPID` namespace. An attacker uses this configuration to access worker-node processes. What is this called?

- A. Container Breakout / Pod Escape
- B. SQL Injection
- C. Cross-Site Request Forgery
- D. Bluejacking

**Answer: A — Container Breakout / Pod Escape**

### 11. Exposed Kubernetes etcd
An exposed etcd service on port 2379 contains Kubernetes Secrets and service-account tokens. What is the key security lesson?

- A. Etcd is only for storage
- B. Control-plane components must be isolated and encrypted at rest and in transit
- C. Kubernetes is inherently insecure
- D. Port 2379 should always be public

**Answer: B — Isolate and protect control-plane components**

### 12. Jenkins exposed without authentication
A Jenkins server is accessible without authentication. An attacker creates a build job that executes a Groovy script and reads `/etc/passwd`. What is the attack and implication?

- A. XSS; steals developer cookies
- B. Remote Code Execution (RCE); can compromise the software supply chain
- C. DoS; slows the build process
- D. Directory Traversal; only reads files

**Answer: B — RCE with software supply-chain impact**

### 13. CI/CD pipeline poisoning
An attacker modifies `.gitlab-ci.yml` to exfiltrate environment variables containing AWS secrets during a build. What is this attack?

- A. Software Supply Chain Attack / Pipeline Poisoning
- B. Shadow IT
- C. Reverse Engineering
- D. Man-in-the-Middle

**Answer: A — Software Supply Chain Attack / Pipeline Poisoning**

### 14. Zero Trust lateral movement through CI/CD
An attacker compromises a low-privilege managed desktop, accesses Jenkins, and modifies a build script to steal AWS deployment keys. What is this movement?

- A. Vertical Privilege Escalation
- B. Lateral Movement via CI/CD Pipeline
- C. Credential Stuffing
- D. Reverse Proxying

**Answer: B — Lateral Movement via CI/CD Pipeline**

---

## 2. Web Application and API Security

### 15. WAF normalization mismatch
A WAF checks only standard ASCII SQL keywords. An attacker uses double URL encoding and Unicode variants; the WAF does not normalize the input, but the database decodes and executes it. What is this evasion strategy?

- A. Improper Input Validation
- B. Normalization Impedance Mismatch
- C. SQL Map Hijacking
- D. XSS Filter Bypass

**Answer: B — Normalization Impedance Mismatch**

### 16. JWT `alg: none`
An attacker changes a JWT's `alg` header to `None`, removes the signature, and submits the token to gain administrative access. What flaw is this?

- A. SQL Injection
- B. Broken Object Level Authorization
- C. Cross-Site Scripting
- D. JWT Algorithm Confusion / Insecure JWT Implementation

**Answer: D — JWT Algorithm Confusion / Insecure JWT Implementation**

### 17. GraphQL deep-nesting DoS
An attacker sends a GraphQL query with deeply nested relationships, causing the server CPU to reach 100%. What attack is this?

- A. SQL Injection
- B. GraphQL Complexity/Depth Attack (DoS)
- C. Broken Object Level Authorization
- D. Insecure Deserialization

**Answer: B — GraphQL Complexity/Depth Attack (DoS)**

### 18. Blind SSRF timing reconnaissance
An attacker exploits blind SSRF and measures response times to infer which internal ports are open. What method is this?

- A. Inference-based Internal Reconnaissance
- B. Cross-Site Scripting
- C. SQL Injection
- D. Broken Authentication

**Answer: A — Inference-based Internal Reconnaissance**

### 19. Password-manager autofill abuse
A password manager fills credentials into any field named `password`. A malicious page creates a hidden password field and steals the autofilled credentials. What is the primary flaw?

- A. Lack of encryption for stored passwords
- B. Failure to verify the Origin or Domain before autofill
- C. Using JavaScript to fill forms
- D. Storing passwords in a local database

**Answer: B — Failure to verify the Origin or Domain**

### 20. Padding Oracle Attack
A web app encrypts session cookies using AES-CBC and returns different errors for valid and invalid padding. An attacker uses the error differences to recover plaintext. What is this attack?

- A. Birthday Attack
- B. Padding Oracle Attack
- C. Rainbow Table Attack
- D. Meet-in-the-middle

**Answer: B — Padding Oracle Attack**

### 21. HTTP Request Smuggling
A request contains both `Content-Length` and `Transfer-Encoding`. The front-end proxy and back-end server disagree about where the request ends. What can an attacker achieve?

- A. Change the server IP
- B. Delete CSS files
- C. Increase bandwidth
- D. Bypass security controls and poison the next user's request

**Answer: D — Bypass controls and poison subsequent requests**

### 22. Reflected XSS mitigation
A tester uses reflected XSS to hook a victim's browser to an exploit framework. Which header would most effectively restrict malicious script execution?

- A. Server: Apache
- B. Content-Security-Policy (CSP) with restricted `script-src`
- C. X-Powered-By: PHP
- D. Connection: keep-alive

**Answer: B — Content-Security-Policy (CSP)**

### 23. SSRF using Gopher
An attacker finds an internal database address in a leaked `wp-config.php` backup. A server-side health-check feature accepts arbitrary URLs. The attacker supplies a `gopher://` URL to interact with the internal database. What attack chain is this?

- A. SQL Injection via Command Injection
- B. SSRF using the Gopher protocol
- C. LFI to Remote Code Execution
- D. CSRF via internal pivoting

**Answer: B — SSRF using the Gopher protocol**

### 24. Broken function-level authorization and header bypass
A Guest user cannot access `/admin/delete` normally, but manipulates headers such as `X-Original-URL` so the backend processes the restricted route. What combination is exploited?

- A. SQL Injection and XSS
- B. Insecure Direct Object Reference with WAF Parameter Pollution
- C. Broken Functional Level Authorization and Header-based Bypassing
- D. CSRF

**Answer: C — Broken Functional Level Authorization and Header-based Bypassing**

### 25. SAML Signature Wrapping
A SAML implementation validates only a specific assertion rather than the entire signed XML document. An attacker wraps a valid signed assertion in a malicious XML structure that changes the effective NameID. What is this attack?

- A. XXE Injection
- B. SAML Signature Wrapping (SSW) Attack
- C. XML Denial of Service
- D. SOAP Action Spoofing

**Answer: B — SAML Signature Wrapping (SSW) Attack**

### 26. Insecure deserialization
A REST API accepts a serialized PHP object inside a JSON string. A gadget chain triggers remote code execution before business logic is processed. Why is this possible?

- A. It only works on Linux
- B. It exploits how the application handles data objects in memory before business logic
- C. It requires no network connection
- D. It bypasses the need for a database

**Answer: B — Unsafe object handling during deserialization**

### 27. CORS wildcard configuration
A developer sets `Access-Control-Allow-Origin: *`. Which statement best describes the risk?

- A. It deletes the database
- B. It allows any origin to read responses where the browser's CORS rules permit it; sensitive credentialed access is not safely enabled by wildcard
- C. It changes the user's password
- D. It crashes the server

**Answer: B — Overly permissive cross-origin access**

### 28. SQL injection countermeasure
An application safely separates user input from SQL statements and binds input as values. Which countermeasure is being used?

- A. Encoding the single quote
- B. Restrict database access
- C. Parameterized queries or prepared statements
- D. Input validation only

**Answer: C — Parameterized queries / prepared statements**

### 29. UNION SQL injection
A crafted numeric parameter causes the response to combine expected loan data with sensitive employee data from another table. Which SQL injection type is this?

- A. Second-Order SQL Injection
- B. Error-Based SQL Injection
- C. UNION SQL Injection
- D. Blind SQL Injection

**Answer: C — UNION SQL Injection**

### 30. SQL injection through inline comments
An attacker breaks SQL keywords apart with comment syntax so the database interprets them while a filter fails to detect them. Which evasion technique is being used?

- A. String Concatenation
- B. Null Byte
- C. In-line Comment
- D. Hex Encoding

**Answer: C — In-line Comment**

### 31. Blind SQLi using heavy queries
A WAF blocks common `OR 1=1` and `SLEEP()` payloads. The tester uses expensive joins that cause noticeable server delay when a condition is true. What is this method?

- A. Time-based Inference via Resource Exhaustion
- B. Boolean-based Injection
- C. Out-of-band Injection
- D. Error-based Injection

**Answer: A — Time-based Inference via Resource Exhaustion**

### 32. Shell injection
An application passes user-supplied input directly to system-level functions. Crafted input causes unexpected operating-system commands to execute. What is this flaw?

- A. Cross-Site Scripting
- B. LDAP Injection
- C. SQL Injection
- D. Shell Injection

**Answer: D — Shell Injection**

### 33. HTTP Response Splitting
A crafted request is processed as two separate HTTP responses/requests through improper handling of input, allowing injected data into server communication. Which attack is this?

- A. Web Cache Poisoning
- B. Directory Traversal
- C. Password Cracking
- D. HTTP Response Splitting

**Answer: D — HTTP Response Splitting**

### 34. Robots.txt information gathering
A tester finds a root-level crawler directive that reveals paths to restricted or sensitive resources. Which technique is being used?

- A. Vulnerability Scanning
- B. Web Server Footprinting / Banner Grabbing
- C. Directory Brute Forcing
- D. Information Gathering from `robots.txt`

**Answer: D — Information Gathering from robots.txt**

### 35. Document root
A web server component stores publicly accessible website content such as HTML, images, and client-side scripts. What is it?

- A. Document Root
- B. Application Server
- C. Virtual Document Tree
- D. HTTP Server Core

**Answer: A — Document Root**

---

## 3. Network, Wireless and Protocol Attacks

### 36. WPA3 Dragonblood
A tester targets the WPA3-SAE Dragonfly handshake's password-to-element mapping using timing and cache side channels. What is this attack called?

- A. KRACK Attack
- B. Dragonblood
- C. Pixie Dust
- D. Evil Twin

**Answer: B — Dragonblood**

### 37. WPA3 transition-mode downgrade
A rogue AP advertises a weaker WPA2 option and tricks a client into connecting using the weaker protocol, allowing offline handshake cracking. What is the key risk?

- A. WPA3 is uncrackable
- B. The user believes the connection is WPA3-secure but has been downgraded to a weaker protocol
- C. The phone battery drains
- D. Internet speed increases

**Answer: B — Downgrade to a weaker protocol**

### 38. PMKID clientless attack
An attacker captures a single RSN information element frame from an AP and attempts offline PSK cracking without waiting for a client to connect. What makes this different from a handshake capture?

- A. It encrypts the AP
- B. It requires a high-gain antenna
- C. It is a clientless attack that does not require waiting for a user to log in
- D. It only works at night

**Answer: C — Clientless attack**

### 39. WPA2 mask attack
An attacker knows a Wi-Fi password follows a pattern such as `CompanyYear!` and uses a mask attack rather than a full brute-force search. Why is this efficient?

- A. It requires more RAM
- B. It reduces the search space by targeting human password patterns
- C. It bypasses the MIC
- D. It only works on 5 GHz

**Answer: B — It reduces the search space**

### 40. MAC spoofing on captive portal Wi-Fi
An attacker changes their MAC address to impersonate a client already authenticated to an open captive-portal network. What is this technique?

- A. Session Hijacking via MAC Spoofing
- B. Warding
- C. Bluejacking
- D. Packet Sniffing

**Answer: A — Session Hijacking via MAC Spoofing**

### 41. Rogue access point
An unknown access point is physically connected to the internal switch, issues IP addresses on the corporate VLAN, relays internal traffic, and provides remote connectivity. What is it?

- A. Honeypot AP
- B. Rogue AP
- C. Misconfigured AP
- D. Evil Twin AP

**Answer: B — Rogue AP**

### 42. Evil Twin and EAP-TTLS certificate validation
A victim connects to a rogue AP and ignores an untrusted certificate warning. The inner authentication uses PAP, exposing the password. What failed?

- A. WPA2 itself
- B. The user failed to validate the server certificate, and the inner authentication method was insecure
- C. The use of an Evil Twin
- D. The password was too short

**Answer: B — Certificate validation and secure inner authentication failed**

### 43. MAC flooding
An attacker generates thousands of random MAC addresses, filling a switch's CAM table. The switch begins flooding traffic out multiple ports. What is this attack?

- A. ARP Spoofing
- B. MAC Flooding
- C. DHCP Starvation
- D. VLAN Hopping

**Answer: B — MAC Flooding**

### 44. STP root bridge manipulation
STP is enabled but BPDU Guard is disabled on access ports. A rogue switch sends a BPDU with priority 0. What may happen?

- A. The network becomes faster
- B. The rogue switch may become the Root Bridge, enabling traffic interception or redirection
- C. All ports automatically shut down
- D. The rogue switch is ignored

**Answer: B — Rogue switch may become the Root Bridge**

### 45. ARP spoofing
An attacker injects crafted messages into a LAN so traffic between a workstation and authentication server is routed through the attacker's machine. Which sniffing technique is most likely?

- A. ARP Spoofing
- B. IRDP Spoofing
- C. Switch Port Stealing
- D. STP Attack

**Answer: A — ARP Spoofing**

### 46. CAM-table exhaustion scenario
A switch's CAM table is overwhelmed and the attacker's system begins receiving packets not originally destined for it. Which sniffing technique most likely caused this?

- A. DNS Poisoning
- B. MAC Flooding
- C. VLAN Hopping
- D. ARP Poisoning

**Answer: B — MAC Flooding**

### 47. NetBIOS enumeration
A tester queries UDP ports 137/138 and TCP port 139 on older Windows systems and obtains machine names, logged-in usernames, and shared-folder information. Which enumeration method is this?

- A. NFS Enumeration
- B. NetBIOS Enumeration
- C. SNMP Enumeration
- D. SMB Enumeration

**Answer: B — NetBIOS Enumeration**

### 48. LDAP enumeration
A service on TCP port 389 accepts anonymous binds and reveals usernames, departments, and organizational units through search filters. What is this activity?

- A. SMTP Enumeration
- B. DNS Enumeration
- C. NTP Enumeration
- D. LDAP Enumeration

**Answer: D — LDAP Enumeration**

### 49. TCP port 1434
During an audit, TCP port 1434 is found open on a database node. Which service is most likely associated with this port?

- A. ms-sql-m
- B. ms-sql-s
- C. sql net
- D. sqlsrv

**Answer: A — ms-sql-m (Microsoft SQL Server Browser)**

### 50. SNMP traffic inspection
An analyst wants to capture live SNMP requests and responses and manually inspect OIDs, community strings, and variable bindings. Which tool should be used?

- A. Wireshark
- B. SnmpWalk
- C. Nmap
- D. SoftPerfect Network Scanner

**Answer: A — Wireshark**

### 51. NULL scan
A tester sends TCP packets with no flags to infer port states while attempting to be less visible than a full TCP handshake. Which scan is this?

- A. TCP Connect Scan
- B. ACK Scan
- C. NULL Scan
- D. FIN Scan

**Answer: C — NULL Scan**

### 52. Service version discovery
A tester analyzes network-level responses and application output to identify the underlying service and its software release without logging in. Which technique is this?

- A. Vulnerability Scanning
- B. OS Discovery
- C. Port Scanning
- D. Service Version Discovery

**Answer: D — Service Version Discovery**

### 53. Nmap MAC spoofing
Which Nmap option can set a vendor-associated MAC address for a scan?

- A. `nmap -sT -Pn --spoof-mac 0 10.10.1.11`
- B. `nmap -sT -Pn --spoof-mac 00:11:22 10.10.1.11`
- C. `nmap -sT -Pn --spoof-mac Dell 10.10.1.11`
- D. `nmap -sT -Pn --spoof-mac 00:01:02:25:56:AE 10.10.1.11`

**Answer: C — `--spoof-mac Dell`**

### 54. ICMP discovery countermeasure
A security team wants to disrupt ICMP-based host discovery by preventing error messages from being returned. Which action best matches the stated objective?

- A. Block inbound ICMP message types and all outbound ICMP type-3 unreachable messages
- B. Lock down the network and block unwanted ports
- C. Configure firewall and IDS rules to detect and block probes
- D. Block unwanted services and update service versions

**Answer: A — Filter the specified ICMP message types**

### 55. DNS tunneling
An attacker hides data in the ID field or encoded portions of DNS queries sent to a domain they control. What is this technique?

- A. DNS Tunneling
- B. DNS Poisoning
- C. DNS Hijacking
- D. DNSSEC

**Answer: A — DNS Tunneling**

### 56. DNS-over-HTTPS C2
An attacker uses DoH for C2 while external port 53 DNS is blocked. Why can this work?

- A. DoH uses port 53
- B. DoH is encrypted and commonly travels over HTTPS port 443, potentially blending with web traffic
- C. DoH is faster
- D. DoH does not require an IP address

**Answer: B — DoH can blend with HTTPS traffic on port 443**

### 57. Fast-Flux DNS
A phishing domain resolves to hundreds of changing IP addresses. Why does this challenge IP-based blacklists?

- A. It makes the website faster
- B. IP addresses change rapidly, making static blacklists difficult to maintain
- C. It encrypts DNS queries
- D. It prevents indexing

**Answer: B — Rapidly changing IP addresses undermine static blacklists**

### 58. TCP stream segmentation/overlap evasion
A tester splits a payload into tiny TCP segments and uses overlapping sequence ranges so a firewall and target reconstruct the stream differently. What is this?

- A. IP Fragmentation
- B. TCP Stream Segmentation/Overlap Evasion
- C. Protocol Tunneling
- D. Source Routing

**Answer: B — TCP Stream Segmentation/Overlap Evasion**

### 59. RST hijacking
An attacker sends spoofed TCP packets carrying the reset flag, terminating active sessions. What session-hijacking technique is being simulated?

- A. UDP Hijacking
- B. Blind Hijacking
- C. RST Hijacking
- D. TCP/IP Hijacking

**Answer: C — RST Hijacking**

### 60. Session fixation / donation
An attacker deliberately shares a pre-assigned session ID with a victim. The victim logs in using that session, allowing the attacker to retrieve activity associated with it. Which technique is this?

- A. Session Prediction
- B. Session Donation Attack
- C. Session Fixation Attack
- D. Session Replay Attack

**Answer: B — Session Donation Attack**

### 61. Active session hijacking
An attacker injects crafted TCP packets into a live client-server communication and takes over the connection. Which type is this?

- A. Man-in-the-Browser
- B. Active Session Hijacking
- C. Blind Hijacking
- D. Passive Session Hijacking

**Answer: B — Active Session Hijacking**

### 62. Blind hijacking
A tester injects packets into a session without being able to observe the full response stream. Which session hijacking type is this?

- A. Man-in-the-Browser
- B. Active Session Hijacking
- C. Blind Hijacking
- D. Passive Session Hijacking

**Answer: C — Blind Hijacking**

---

## 4. Malware, Exploitation and Host Security

### 63. API hooking
Malware modifies a legitimate process's Import Address Table so calls such as `CreateFileW` are redirected to malicious functions. Why is this useful?

- A. It makes malware run faster
- B. It lets malware intercept, modify, or block system calls made by legitimate software
- C. It deletes the Windows registry
- D. It only works on 32-bit systems

**Answer: B — Intercepts or modifies legitimate API calls**

### 64. Process hollowing
Malware starts a legitimate process in a suspended state, replaces its original code in memory, and resumes it. Why is this stealthy?

- A. It uses less CPU
- B. It appears as a trusted system process in Task Manager and basic tools
- C. It bypasses the need for a network connection
- D. It encrypts the hard drive

**Answer: B — Malicious code runs under the appearance of a legitimate process**

### 65. DLL side-loading
A malicious DLL is placed beside a signed application that searches its local directory first. Why is this deceptive?

- A. The signed app will not run
- B. The user sees a trusted application, while malicious code executes under its process identity
- C. The computer reboots
- D. Windows automatically deletes the DLL

**Answer: B — Malicious code executes under a trusted process**

### 66. DLL hijacking
A non-privileged process loads a malicious library from a directory searched before the legitimate library location. Which technique is this?

- A. Access Token Manipulation
- B. Privilege Escalation by Bypassing UAC
- C. Privilege Escalation by Exploiting Vulnerabilities
- D. Privilege Escalation Using DLL Hijacking

**Answer: D — Privilege Escalation Using DLL Hijacking**

### 67. Web shell network detection
A PHP web shell uses `eval(base64_decode($_POST['cmd']))`. If source code is unavailable, which detection approach is most useful among the options?

- A. Check for large image files
- B. Monitor outbound connections to unknown IPs from the web-server process
- C. Check server CPU temperature
- D. Change the root password

**Answer: B — Monitor suspicious outbound connections**

### 68. Web shell in User-Agent logs
A web shell is hidden in a User-Agent string and executed through log injection in a monitoring tool. Why is this difficult for SOC analysts?

- A. It resembles normal web traffic in access logs and is not in the URL parameters
- B. It deletes logs
- C. It requires a password
- D. It only works on Linux

**Answer: A — It blends into normal-looking web traffic**

### 69. Timestomping
An attacker changes a malicious DLL's created, modified, and accessed timestamps to match a legitimate 2018 system file. Why is this problematic for forensics?

- A. It makes the file invisible to antivirus
- B. It can place the file outside the timeline of interest in a standard investigation
- C. It encrypts the hard drive
- D. It deletes event logs

**Answer: B — It misleads timeline-based investigation**

### 70. Polymorphic malware
A virus changes its code using different encryption keys and decryption routines each time it replicates. What challenge does this create for signature-based antivirus?

- A. The virus is too large to scan
- B. Its hash and code pattern change with each infection, weakening static signatures
- C. It deletes antivirus software
- D. It only runs on weekends

**Answer: B — Changing code patterns defeat static signatures**

### 71. ROP
An exploit chains small snippets of existing code (gadgets) from system DLLs to execute malicious logic and bypass DEP. What is ROP's advantage?

- A. It allows malicious logic without introducing new executable code into memory
- B. It automatically disables the firewall
- C. It makes the exploit faster
- D. It bypasses the need for administrative privileges

**Answer: A — Reuses existing executable code**

### 72. Heap spraying mitigation
An exploit fills memory with NOP sleds and shellcode to increase the chance that a corrupted pointer lands in attacker-controlled code. Which OS-level mitigation is most relevant?

- A. Antivirus
- B. ASLR (Address Space Layout Randomization)
- C. Stronger passwords
- D. Disk encryption

**Answer: B — ASLR**

### 73. NOP sled
In a buffer overflow, an attacker places NOP instructions before shellcode. What is the purpose?

- A. Encrypt the shellcode
- B. Increase the chance execution reaches the shellcode even if the return address is imprecise
- C. Bypass firewall signatures
- D. Delete system logs

**Answer: B — Increase the landing area for execution**

### 74. Rubber Ducky / HID injection
A USB device emulates a keyboard and types commands that launch hidden PowerShell and download a reverse shell. Which control is most effective among the options?

- A. Stronger login password
- B. Antivirus only
- C. EDR monitoring unusual parent-child process relationships and Office/Explorer spawning PowerShell
- D. Disabling USB ports in BIOS

**Answer: C — EDR behavioral monitoring**

### 75. Office macro payload prevention
A Word macro launches a reverse shell. Which control most directly reduces the chance of initial execution?

- A. Block port 4444
- B. Attack Surface Reduction (ASR) rules that block Office applications from creating child processes
- C. Delete the Public folder
- D. Change the user's password

**Answer: B — ASR rules for Office child-process behavior**

### 76. WMI persistence
Malware creates a WMI Event Subscription that runs a PowerShell script when the Print Spooler service restarts. What persistence category is this?

- A. Registry Run Key
- B. WMI Event Subscription persistence
- C. Scheduled Task Injection
- D. Service Binary Hijacking

**Answer: B — WMI Event Subscription persistence**

### 77. SUID root editor
A text editor such as Vim has the SUID bit set and is owned by root. A local user launches it and uses `:sh`. What privilege may the shell have?

- A. Standard user
- B. Guest
- C. It will crash
- D. Root, because the binary runs with the file owner's effective privileges

**Answer: D — Root, if the SUID program preserves its effective UID when spawning the shell**

### 78. SUID backup script
A root-owned custom backup script has permissions `-rwsr-xr-x`. How could a low-privilege attacker abuse it?

- A. Delete the file
- B. Exploit the SUID bit to execute commands as the file owner (root)
- C. Change its owner
- D. Move it to `/tmp`

**Answer: B — Abuse SUID execution as root**

### 79. Arbitrary file read
A root-running local-socket application accepts a filename. Supplying `/dev/sda` causes it to dump raw disk data into an attacker-readable log. What vulnerability is this?

- A. Buffer Overflow in the logging module
- B. Insecure Resource Access / Arbitrary File Read
- C. Race Condition in the local socket
- D. Command Injection

**Answer: B — Insecure Resource Access / Arbitrary File Read**

### 80. TOCTOU
An application checks permission to read a file and opens it a moment later. How can an attacker exploit the time gap?

- A. Change their username
- B. Crash the server
- C. Delete the file
- D. Replace the file with a symbolic link to a sensitive file after the permission check

**Answer: D — Replace the checked file with a symlink before use**

### 81. Steganography and fileless execution
A PowerShell script is hidden in JPEG pixels and extracted by a small loader for in-memory execution. Why can this evade traditional signature-based antivirus?

- A. The image is too cute to scan
- B. The malicious code is not stored as a conventional executable file on disk and is hidden in non-executable data
- C. PowerShell is always encrypted
- D. Antivirus cannot read JPEGs

**Answer: B — Hidden payload and in-memory execution**

### 82. Logic bomb environmental keying
A logic bomb runs only when the hostname is `PROD-DB-01` and the date is after January 1. Otherwise, it deletes itself. What is this anti-analysis feature?

- A. Polymorphism
- B. Environmental Keying
- C. Anti-Debugging
- D. Obfuscation

**Answer: B — Environmental Keying**

### 83. DLL side-loading versus code signing
A legitimate, signed application loads a malicious DLL from its own directory. What is the key deception?

- A. The signed app cannot run
- B. A trusted-looking application hosts malicious code under its identity
- C. The system reboots
- D. The DLL is automatically removed

**Answer: B — Malicious code runs inside a trusted process**

### 84. RAT
A disguised attachment appears normal but gives an attacker persistent access to monitor emails, keystrokes, and files on a workstation. Which malware is most likely?

- A. Adware
- B. Spyware
- C. Botnet
- D. Remote Access Trojan (RAT)

**Answer: D — Remote Access Trojan (RAT)**

### 85. Spyware
Malware captures customer credentials and sells them for financial gain, while secretly monitoring victims. Which hacker/malware context best matches the described activity?

- A. White Hat hackers
- B. Script Kiddies
- C. Hacktivists
- D. Black Hat hackers

**Answer: D — Black Hat hackers**

### 86. Worm
Malware installed on one workstation automatically copies itself through shared folders and weak administrator credentials, infecting many computers without further user interaction. What type is it?

- A. Logic Bomb
- B. Backdoor
- C. Fileless Malware
- D. Worm

**Answer: D — Worm**

### 87. Botnet agents
Compromised endpoints communicate with a remote server and receive synchronized commands, including instructions to send bursts of outbound traffic. What are the malicious components?

- A. Potentially Unwanted Applications
- B. Scareware
- C. Botnet Agents
- D. Spyware

**Answer: C — Botnet Agents**

---

## 5. Identity, Authentication and Credential Attacks

### 88. NTLM relay
An attacker poisons LLMNR/NBT-NS, captures an NTLM authentication exchange, and relays it to a server where SMB signing is disabled. What is this lateral movement technique?

- A. Pass-the-Hash
- B. SMB Relay Attack
- C. Kerberoasting
- D. AS-REP Roasting

**Answer: B — SMB Relay Attack**

### 89. LDAP relay
A victim's NTLM authentication is relayed to a Domain Controller over LDAP because LDAP signing is not required. Why can this work with a complex password?

- A. The password is never revealed; the authentication exchange is forwarded
- B. LDAP signing only protects against eavesdropping, not relaying
- C. Kerberos TGT is exploited
- D. The attacker already has the Domain Admin hash

**Answer: A — The authentication exchange is relayed without cracking the password**

### 90. AS-REP Roasting
A domain account has “Do not require Kerberos preauthentication” enabled. An attacker requests an AS-REP response and cracks the encrypted material offline. What is this attack?

- A. Kerberoasting
- B. AS-REP Roasting
- C. Pass-the-Ticket
- D. Golden Ticket

**Answer: B — AS-REP Roasting**

### 91. Pass-the-Ticket
An attacker steals Kerberos tickets from a compromised workstation and reuses them to authenticate to other domain systems without plaintext credentials. What is this?

- A. LLMNR/NBT-NS Poisoning
- B. Pass-the-Ticket Attack
- C. Kerberoasting
- D. Pass-the-Hash

**Answer: B — Pass-the-Ticket**

### 92. Constrained delegation abuse
An Active Directory user has constrained delegation to a CIFS service. An attacker uses Rubeus to request a service ticket while impersonating a Domain Administrator. Why can this work?

- A. Delegation can allow a service to act as another user to a configured backend resource
- B. The password is weak
- C. Kerberos is broken
- D. The file server is unpatched

**Answer: A — Delegation permits impersonation to the configured backend service**

### 93. Internal Monologue
An attacker interacts with local NetNTLM authentication and forces a downgrade to NTLMv1, extracting hashes without sending network packets. Why is this stealthy?

- A. It bypasses network-based IDS/IPS visibility
- B. It requires no password
- C. It only works on Linux
- D. It deletes event logs

**Answer: A — It can bypass network-based detection**

### 94. Distributed rate-limit bypass
A password-reset feature allows five PIN attempts per minute per IP. An attacker rotates through 100 proxy IPs and sends four attempts from each. What strategy is this?

- A. Credential Stuffing
- B. Distributed Rate-Limit Bypass
- C. Session Fixation
- D. Slowloris

**Answer: B — Distributed Rate-Limit Bypass**

### 95. SIM swapping
An attacker uses social engineering at a mobile carrier to take over a victim's phone number and reset a banking password. What is the lesson?

- A. SMS is the most secure 2FA
- B. SMS-based 2FA can be defeated through carrier-level social engineering and is weaker than phishing-resistant methods
- C. Phones should not have SIM cards
- D. Passwords are no longer needed

**Answer: B — SMS 2FA is vulnerable to SIM swapping**

### 96. MFA fatigue
An attacker with a stolen password sends dozens of push notifications until a tired user approves one. What is this attack?

- A. Phishing
- B. MFA Fatigue / Push Spam
- C. Vishing
- D. Smishing

**Answer: B — MFA Fatigue / Push Spam**

### 97. OAuth authorization-code interception
A malicious mobile app registers the same custom URL scheme as a legitimate app and intercepts its authorization code. What mitigation prevents this?

- A. Stronger password
- B. PKCE (Proof Key for Code Exchange)
- C. Change the client ID
- D. Disable cookies

**Answer: B — PKCE**

### 98. Biometric Boolean bypass
An app checks only whether an OS biometric function returns `True`. An attacker hooks the function and forces a successful result. What should the app do instead?

- A. Use a more accurate fingerprint sensor
- B. Use a password instead
- C. Bind biometric success to unlocking a cryptographic key in the Secure Enclave or Keystore
- D. Prevent fingerprint theft

**Answer: C — Bind biometric authorization to a protected cryptographic key**

### 99. Password spraying versus mask attack
An attacker knows a target password pattern such as `CompanyYear!` and uses a mask attack. Why is it more efficient than exhaustive brute force?

- A. It uses more RAM
- B. It targets likely human password patterns and reduces the search space
- C. It bypasses the handshake MIC
- D. It only works on 5 GHz

**Answer: B — It reduces the search space**

### 100. Password hash collision
An attacker finds that a different password produces the same MD5 hash as the stored password and is accepted by the application. What cryptographic phenomenon is this?

- A. Encryption failure
- B. Hash Collision
- C. Salting
- D. Key Stretching

**Answer: B — Hash Collision**

---

## 6. Cryptography, Data Protection and Privacy

### 101. Perfect Forward Secrecy
An attacker steals a VPN server's long-term private key. Why might they still be unable to decrypt previously captured sessions?

- A. PFS requires a 100-character password
- B. PFS uses unique session keys for each connection, so the long-term key alone does not reveal past session keys
- C. PFS only works on Linux
- D. PFS doubles encryption speed

**Answer: B — PFS protects past sessions from long-term key compromise**

### 102. Base64 is not encryption
A developer stores an administrator password in Base64 and calls it secure. Why is this incorrect?

- A. Base64 is a cipher, not a hash
- B. Encoding is not encryption; it is reversible and provides no confidentiality
- C. Base64 is too slow
- D. Base64 only works on Windows

**Answer: B — Base64 is reversible encoding, not encryption**

### 103. XOR and DLP
A DLP system detects credit-card number patterns. An attacker XORs card numbers with a static key before sending them by email. Why might basic pattern-based DLP fail?

- A. DLP only works on Saturdays
- B. The transformed data no longer matches the expected credit-card regex pattern
- C. XOR is unbreakable
- D. The email was BCC

**Answer: B — XOR transformation defeats simple pattern matching**

### 104. Homomorphic encryption integrity
A cloud provider processes homomorphically encrypted data. An attacker modifies encrypted results to zero out fields. Which security property is attacked?

- A. Confidentiality
- B. Malleability / Integrity
- C. Availability
- D. Authentication

**Answer: B — Malleability / Integrity**

### 105. RSA/AES ransomware recovery
Ransomware creates a unique AES-256 key per file, encrypts each AES key with the attacker's RSA-4096 public key, appends the encrypted key, and securely deletes the AES key. What is true about recovery?

- A. Brute-force AES-256 for one file
- B. Recovery is generally impossible without the attacker's RSA private key or another recovery weakness
- C. Extract the RSA public key from the malware
- D. Use a known-plaintext attack on RSA

**Answer: B — Recovery requires the RSA private key or an independent flaw/backup**

### 106. Side-channel power analysis
A researcher monitors a smart card's power consumption during RSA operations and identifies the square-and-multiply pattern. What countermeasure is most effective?

- A. Use a longer 4096-bit key
- B. Implement blinding or add noise to the power-consumption profile
- C. Change the plastic casing
- D. Use a faster processor

**Answer: B — Blinding / power-analysis countermeasures**

### 107. HSTS tracking
An attacker sets different HSTS states across subdomains to create a binary identifier that tracks a user. What is this privacy attack?

- A. Cookie Poisoning
- B. HSTS Fingerprinting / Tracking
- C. Protocol Downgrade
- D. SSL Stripping

**Answer: B — HSTS Fingerprinting / Tracking**

### 108. Android Keystore authentication requirement
An app stores session tokens in Android Keystore but does not require user authentication for key use. What is the flaw?

- A. Insecure Key Generation
- B. Improper Hardware-Backed Storage Usage
- C. Sideloading
- D. Rooting

**Answer: B — Improper Hardware-Backed Storage Usage**

---

## 7. IoT, OT and Industrial Control Systems

### 109. UPnP automatic port forwarding
A smart camera uses UPnP to open a router port automatically, exposing its login page to the internet. What is the risk?

- A. Insecure Default Settings / Automatic Port Forwarding
- B. Physical Theft
- C. Slow Internet
- D. Battery Drain

**Answer: A — Insecure defaults / automatic port forwarding**

### 110. Hardcoded IoT secrets
A smart-home hub uses a hardcoded encryption key for firmware updates. An attacker decrypts an intercepted update and discovers the root password. What is the classification?

- A. Insecure Ecosystem Interfaces
- B. Use of Hardcoded Secrets / Weak Cryptography
- C. Insufficient Privacy Protection
- D. Lack of Physical Hardening

**Answer: B — Hardcoded secrets / weak cryptography**

### 111. Zigbee clear-text key exchange
A smart meter sends its network key in clear text during initial joining. What is the weakness?

- A. Use of AES-128
- B. Clear-text key exchange during association
- C. Physical access requirement
- D. Lack of a touchscreen

**Answer: B — Clear-text key exchange**

### 112. BLE characteristic protection
A smart lock exposes unencrypted GATT services, and an attacker writes to the Unlock characteristic. What is the flaw?

- A. Broken Key Management
- B. Unprotected BLE Characteristics
- C. Physical Bypass
- D. Social Engineering

**Answer: B — Unprotected BLE Characteristics**

### 113. Medical IoT replay
An attacker captures and replays an unauthenticated RF command to trigger an insulin pump dose. What is the primary failure?

- A. Lack of Message Integrity and Authentication
- B. Too much encryption
- C. Small battery
- D. Bright screen

**Answer: A — Lack of message integrity and authentication**

### 114. DNP3 command manipulation
An attacker modifies a DNP3 Control Relay Output Block command to switch off a circuit breaker. Why is this especially serious in ICS?

- A. ICS networks are faster
- B. It can cause physical consequences such as outages or equipment damage
- C. DNP3 is more secure than TCP/IP
- D. It can only happen once

**Answer: B — Physical-world consequences**

### 115. HMI spoofing
An attacker changes an HMI display to show a pump running normally while sending PLC commands that increase pressure to dangerous levels. What is this?

- A. Stuxnet-style Man-in-the-Middle / HMI Spoofing
- B. Replay Attack
- C. Bluejacking
- D. Eavesdropping

**Answer: A — HMI Spoofing / deceptive manipulation**

### 116. Data diddling / HMI spoofing
An attacker changes a centrifuge's HMI display to show 1000 RPM while the actual speed is 5000 RPM. What is this technique?

- A. Data Diddling / HMI Spoofing
- B. Man-in-the-Middle
- C. ARP Poisoning
- D. Replay Attack

**Answer: A — Data Diddling / HMI Spoofing**

### 117. Low-and-slow process disturbance
An attacker accesses a water-treatment PLC and changes the chemical feed rate by 0.5% per day, staying below alarm thresholds until water becomes unsafe. What is this?

- A. Denial of Service
- B. Low-and-Slow Integrity Attack / Process Disturbance
- C. Man-in-the-Middle
- D. Replay Attack

**Answer: B — Low-and-Slow Integrity Attack / Process Disturbance**

### 118. Distributed Control System
A manufacturing plant uses a centralized supervisory network coordinating multiple controllers that regulate temperature, pressure, and conveyor speed. Which OT concept is this?

- A. Closed loop
- B. Manual loop
- C. Distributed Control System (DCS)
- D. Open loop

**Answer: C — Distributed Control System (DCS)**

### 119. Exposed SNMP on UPS
An exposed UPS SNMP interface accepts the default community string `private`. A test command causes the server rack to shut down. What is the event's classification?

- A. Intentional Denial of Service via IoT/Infrastructure Misconfiguration
- B. SQL Injection
- C. Social Engineering
- D. MAC Flooding

**Answer: A — Infrastructure misconfiguration causing denial of service**

---

## 8. Denial of Service and Availability

### 120. Slow POST
An attacker sends an HTTP POST with a large Content-Length but transmits the body one byte every ten seconds, exhausting server threads. What is this variation?

- A. UDP Flood
- B. Slowloris / Layer 7 DoS
- C. Smurf Attack
- D. Fraggle Attack

**Answer: B — Slowloris / Layer 7 DoS**

### 121. Rate limiting
A portal caps how many requests a user can make per second, delaying or dropping excessive requests while preserving service for most users. Which countermeasure is this?

- A. Shutting Down Services
- B. Degrading Services
- C. Rate Limiting
- D. Absorb the Attack

**Answer: C — Rate Limiting**

### 122. HTTP GET/POST flood
Repeated GET and POST requests overload backend scripts that process searches and forms. Which DoS technique is being demonstrated?

- A. UDP Flood
- B. Peer-to-Peer Attack
- C. Slowloris
- D. HTTP GET/POST Attack

**Answer: D — HTTP GET/POST Attack**

### 123. WAF for HTTP flood
A company experiences an HTTP flood against its checkout page. Which tool inspects and filters malicious HTTP traffic while allowing legitimate requests?

- A. Firewall
- B. Web Application Firewall
- C. Load Balancer
- D. Intrusion Prevention System

**Answer: B — Web Application Firewall**

### 124. Distributed reflection DoS
An attacker forges requests to multiple open internet services. Those services send amplified responses to the victim, overwhelming it. What is this?

- A. Smurf Attack
- B. Botnet
- C. NTP Amplification Attack
- D. Distributed Reflection Denial-of-Service (DRDoS)

**Answer: D — Distributed Reflection Denial-of-Service (DRDoS)**

### 125. ICMP exfiltration
Ransomware sends small chunks of data inside ICMP Echo Request payloads to an attacker-controlled IP. Why use ICMP instead of HTTPS?

- A. ICMP is faster for large files
- B. To bypass egress filtering and DLP systems focused on common web ports such as 80 and 443
- C. ICMP is automatically encrypted
- D. To perform a DoS while exfiltrating

**Answer: B — Potentially bypasses egress filtering and web-port-focused monitoring**

---

## 9. Governance, Risk, Compliance and Professional Practice

### 126. ISO 27001 Statement of Applicability
An organization excludes physical entry controls for a remote storage facility from its SoA because it was considered low risk. An attacker breaks in and steals backup tapes. What failed?

- A. The SoA was too long
- B. A flawed risk assessment led to exclusion of a critical control
- C. The auditor was bribed
- D. The tapes were not encrypted

**Answer: B — Flawed risk assessment and control selection**

### 127. Untested Business Continuity Plan
An organization claims ISO 27001 compliance because it has a written BCP, but it has not tested it in three years. What is the issue?

- A. A plan is ineffective if it is not regularly tested and updated through exercises
- B. The plan must be 100 pages
- C. BCP is not part of ISO 27001
- D. Only IT needs a BCP

**Answer: A — BCP must be tested and maintained**

### 128. Cyber insurance and risk sharing
An organization buys cyber insurance but ignores technical controls. Why is this poor risk treatment?

- A. Insurance is illegal
- B. Insurance may cover financial losses but does not fix vulnerabilities or eliminate reputational harm
- C. Insurance only covers natural disasters
- D. ISO 27001 prohibits insurance

**Answer: B — Insurance transfers some financial impact, not the underlying risk**

### 129. Asset register and BYOD
An organization excludes employee BYOD phones used for work email from its asset inventory. Why is this a compliance weakness?

- A. Phones are not assets
- B. Assets within the ISMS scope that handle organizational information must be managed and protected
- C. Auditors only care about servers
- D. BYOD is illegal under ISO

**Answer: B — In-scope information assets must be managed**

### 130. Segregation of duties
The same employee writes application code and has privileged access to deploy it to production. What risk does this create?

- A. The application runs slower
- B. One person could introduce malicious code into production without oversight or secondary review
- C. The organization fails its financial audit
- D. The firewall cannot scan production code

**Answer: B — Unreviewed changes and abuse of privileged access**

### 131. ISO 27001 risk management guidance
An organization wants a framework for identifying, assessing, and treating information security risks as part of its ISMS. Which standard best matches this requirement?

- A. ISO/IEC 27001:2022
- B. ISO/IEC 27002:2022
- C. ISO/IEC 27701:2019
- D. ISO/IEC 27005:2022

**Answer: D — ISO/IEC 27005:2022**

### 132. ISO 27001 organizational control failure
A company has strong technical controls but fails to follow segregation of duties. What risk is created?

- A. Firewall cannot scan production code
- B. Financial audit failure only
- C. A single person can introduce malicious production code without independent review
- D. Application performance decreases

**Answer: C — Unreviewed production changes**

### 133. Acceptable Use Policy
An Acceptable Use Policy does not clearly prohibit cryptomining on company hardware. An employee sets up a mining farm in the data center. What is the auditor's concern?

- A. It is not a crime
- B. The AUP lacks clear rules and controls, making enforcement difficult
- C. Mining is good for hardware
- D. The employee owns the hardware

**Answer: B — The policy lacks clear enforceable controls**

### 134. Asset management and information classification
An asset register is stored in a public-read S3 bucket. An attacker identifies servers running legacy Windows versions. Which ISMS weakness is exploited?

- A. Internal Audit failure
- B. Information Classification and Asset Management weakness
- C. Lack of Management Commitment
- D. Poor Risk Treatment Plan

**Answer: B — Information Classification and Asset Management weakness**

### 135. Risk assessment report section
A vulnerability assessment report section describes methodology, targets, scope, scan types, and tools, but not individual findings. Which section is this?

- A. Assessment Overview
- B. Risk Assessment
- C. Findings
- D. Supporting Information

**Answer: A — Assessment Overview**

### 136. Professional ethics in reporting
After completing a client security assessment, what is the most professional reporting obligation?

- A. Keep vulnerabilities secret
- B. Report findings clearly and honestly, and handle sensitive data according to the NDA
- C. Sell findings to the highest bidder
- D. Use findings to attack competitors

**Answer: B — Honest reporting and confidentiality**

### 137. BYOD and ISMS scope
Work-related BYOD phones are omitted from the asset inventory. What is the correct principle?

- A. Phones are not assets
- B. All assets within scope that handle organizational information must be managed and protected
- C. Only servers matter
- D. BYOD is illegal

**Answer: B — Manage all in-scope information assets**

### 138. Vulnerability management verification
A team has applied patches and fixes, then runs follow-up scans to confirm that the remedies eliminated the risks. Which lifecycle phase is this?

- A. Verification
- B. Monitoring
- C. Remediation
- D. Risk Assessment

**Answer: A — Verification**

### 139. Credentialed vulnerability scan
A scanner is provided administrator credentials and discovers weak registry permissions, missing patches, and insecure configuration files. Which scan type is this?

- A. Non-Credentialed Scanning
- B. Internal Scanning
- C. Credentialed Scanning
- D. External Scanning

**Answer: C — Credentialed Scanning**

### 140. Patching and risk treatment
A company purchases cyber insurance but does not address technical weaknesses. What is the correct audit observation?

- A. Insurance is illegal
- B. Risk sharing transfers some financial impact but does not remove the vulnerability
- C. Insurance only covers natural disasters
- D. ISO 27001 does not permit insurance

**Answer: B — Risk sharing does not replace security controls**

---

## 10. Reconnaissance, Social Engineering and Mobile Security

### 141. Geotagged image reconnaissance
An investigator maps geotagged images from employees' public posts to understand physical movements and office routines. Which tool is best suited?

- A. Social Searcher
- B. Creepy
- C. Maltego
- D. Sherlock

**Answer: B — Creepy**

### 142. Vishing
An attacker calls a helpdesk agent, impersonates the CEO, and creates urgency to obtain a password reset. What is this vocal social-engineering attack?

- A. Phishing
- B. Vishing
- C. Smishing
- D. Whaling

**Answer: B — Vishing**

### 143. Social engineering reconnaissance
An attacker poses as a recruiter on a professional networking site and persuades employees to disclose internal software and VPN details. Which threat method is this?

- A. System and Network Attacks
- B. Social Engineering
- C. Information Leakage
- D. Corporate Espionage

**Answer: B — Social Engineering**

### 144. Shoulder surfing
An assessor watches employees' screens and hand movements as they log in, capturing usernames and partial passwords without touching devices. What technique is this?

- A. Tailgating
- B. Impersonation
- C. Shoulder Surfing
- D. Dumpster Diving

**Answer: C — Shoulder Surfing**

### 145. Dark-web search query
A researcher wants to passively search `.onion` sites for PDF documents with titles suggesting administrative access. Which query best matches?

- A. `filetype:docx intitle:"login credentials"`
- B. `filetype:pdf intitle:"admin access" site:onion`
- C. `filetype:pdf intitle:"secure login" site:onion`
- D. `filetype:docx intitle:"user accounts" site:onion`

**Answer: B — `filetype:pdf intitle:"admin access" site:onion`**

### 146. Mobile device location and wipe
A nurse loses a smartphone containing patient-management software. Which guideline most directly reduces the impact?

- A. Install device tracking software
- B. Register devices with a remote locate and wipe facility
- C. Use a VPN on public Wi-Fi
- D. Use antivirus and DLP

**Answer: B — Register devices with remote locate and wipe**

### 147. Mobile insecure data storage
A mobile case-tracking app stores confidential notes and client records locally without encryption or authentication. Which OWASP Mobile risk is present?

- A. Inadequate Privacy Controls
- B. Insecure Data Storage
- C. Improper Credential Usage
- D. Insecure Communication

**Answer: B — Insecure Data Storage**

### 148. Android WebView file access
An Android app enables `setAllowUniversalAccessFromFileURLs(true)`. A malicious local HTML file accesses app-private SharedPreferences and exfiltrates them. What is this vulnerability?

- A. Insecure Data Storage
- B. Cross-App Scripting / File-based XSS
- C. Root Detection Bypass
- D. Intent Spoofing

**Answer: B — Cross-App Scripting / File-based XSS**

### 149. iOS semi-untethered jailbreak
An iPhone boots normally without a computer, but elevated access is lost after reboot until the user launches an on-device app to reapply modifications. Which jailbreak type is this?

- A. Semi-tethered Jailbreaking
- B. Semi-untethered Jailbreaking
- C. Untethered Jailbreaking
- D. Tethered Jailbreaking

**Answer: B — Semi-untethered Jailbreaking**

### 150. KingoRoot APK
A tester installs KingoRoot.apk directly on an Android device. Which feature makes this rooting approach effective?

- A. Tethered jailbreak with patched kernel functions
- B. Weak SSL validation
- C. It is an APK that can run directly on the device without a PC
- D. Bluetooth pairing flaws

**Answer: C — It runs directly on the device without a PC**

---

## 11. Wireless Security, WIPS and Cloud Billing

### 151. Wireless intrusion prevention solution
A production wireless system performs passive scanning, aggregates alarms from multiple controllers, stores forensic data centrally, and can apply countermeasures across a campus. Which solution is most consistent?

- A. RFProtect
- B. Cisco Adaptive Wireless IPS
- C. WatchGuard Wi-Fi Cloud WIPS
- D. Fern WiFi Cracker

**Answer: B — Cisco Adaptive Wireless IPS**

### 152. Cloud measured service
A cloud provider tracks compute hours, storage, and bandwidth so customers pay for what they consume and can audit usage. Which cloud characteristic is this?

- A. Broad Network Access
- B. Resource Pooling
- C. Measured Service
- D. On-Demand Self-Service

**Answer: C — Measured Service**

### 153. Vulnerability scanner versus service discovery
A tester captures application output and network responses to determine a service's software release. Which technique is the best fit?

- A. Vulnerability Scanning
- B. OS Discovery
- C. Port Scanning
- D. Service Version Discovery

**Answer: D — Service Version Discovery**

---

## 12. Additional Security Concepts

### 154. Honeytokens
Fake files such as `passwords.xlsx` are placed on file servers. Opening one triggers a web beacon to the SOC. What is the primary purpose?

- A. Encrypt the attacker's laptop
- B. Catch the attacker's password
- C. Detect an intruder and alert the SOC that a breach may be in progress
- D. Back up real passwords

**Answer: C — Detect intruder activity and alert the SOC**

### 155. NOP sled
An attacker places NOP instructions before shellcode in a buffer overflow. What is the purpose?

- A. Encrypt shellcode
- B. Increase the chance execution reaches shellcode despite an imprecise return address
- C. Bypass firewall signatures
- D. Delete logs

**Answer: B — Increase the chance of reaching shellcode**

### 156. Ransomware ICMP exfiltration
An attacker sends data in ICMP Echo Request payloads before encrypting systems. Why might this be chosen?

- A. ICMP is faster for large files
- B. To bypass egress filters and DLP focused on common web ports
- C. ICMP is automatically encrypted
- D. To perform a DoS

**Answer: B — Potentially evade web-port-focused egress controls**

### 157. OS and application design flaws
A payroll app uses weak custom encryption and flawed session validation because of poor design decisions made during development. Which vulnerability category best describes the root cause?

- A. Design Flaws
- B. Misconfigurations / Weak Configurations
- C. Poor Patch Management
- D. Application Flaws

**Answer: A — Design Flaws**

### 158. Firewall traffic generation and replay
A tester needs a tool that can build and replay varied traffic patterns to test firewall rule enforcement and evasion handling. Which tool is most likely?

- A. Metasploit
- B. Colasoft Packet Builder
- C. Nmap
- D. Traffic IQ Professional

**Answer: B — Colasoft Packet Builder**

### 159. Vulnerability assessment follow-up
After fixes are applied, a team rescans systems to verify that vulnerabilities are resolved. Which phase is this?

- A. Verification
- B. Monitoring
- C. Remediation
- D. Risk Assessment

**Answer: A — Verification**

### 160. DDoS protection by rate limiting
A service caps requests per user per second and delays or drops excessive connections while preserving service for legitimate users. What is this?

- A. Shutting Down Services
- B. Degrading Services
- C. Rate Limiting
- D. Absorb the Attack

**Answer: C — Rate Limiting**

### 161. Web server hardening
A web server runs unnecessary services such as NetBIOS and SMB. Which hardening measure is most appropriate?

- A. Use a dedicated machine as a web server
- B. Conduct risk assessment for patching
- C. Block unnecessary ports, ICMP traffic, and protocols
- D. Eliminate unnecessary files

**Answer: C — Block unnecessary ports, protocols, and traffic**

### 162. Wireless rogue DHCP
A laptop connected to the corporate LAN begins issuing incorrect gateways and DNS settings, redirecting employees to fake login portals. What attack is this?

- A. DHCP Starvation Attack
- B. Rogue DHCP Server Attack
- C. DNS Cache Poisoning
- D. Packet Sniffing

**Answer: B — Rogue DHCP Server Attack**

### 163. Sniffer detection
An analyst sends specially crafted ICMP packets with a mismatched MAC address but correct IP destination. The suspected machine responds, suggesting promiscuous-mode sniffing. Which detection method is this?

- A. Nmap sniffer-detect (NSE)
- B. ARP Method
- C. Ping Method
- D. DNS Method

**Answer: C — Ping Method**

### 164. Blockchain eclipse attack
A merchant's node receives blocks from only a small fixed set of attacker-controlled peers and accepts a private chain that later reverses a payment. Which blockchain attack is this?

- A. 51% Attack
- B. DeFi Sandwich Attack
- C. Eclipse Attack
- D. Finney Attack

**Answer: C — Eclipse Attack**

### 165. Vulnerability report assessment overview
A report section documents the scanning methodology, target information, scan scope, and tools, without yet listing findings. Which section is this?

- A. Assessment Overview
- B. Risk Assessment
- C. Findings
- D. Supporting Information

**Answer: A — Assessment Overview**

---

## Quick Answer Index

| Q | Correct answer |
|---:|---|
| 1 | Insecure Cloud Configuration / Lack of Isolation |
| 2 | Function Data Injection / Insecure Cloud Configuration |
| 3–4 | SSRF |
| 5 | IAM Role Hopping via Instance Profile |
| 6 | Cloud Ransomware / Denial of Service via Policy Manipulation |
| 7 | Sensitive Data Exposure via Resource Metadata |
| 8 | Host Filesystem Escape / Privilege Escalation via Cron |
| 9 | Container Breakout via Socket Exposure |
| 10 | Container Breakout / Pod Escape |
| 11 | Isolate and protect Kubernetes control-plane components |
| 12 | RCE with software supply-chain impact |
| 13 | Software Supply Chain Attack / Pipeline Poisoning |
| 14 | Lateral Movement via CI/CD Pipeline |
| 15 | Normalization Impedance Mismatch |
| 16 | JWT Algorithm Confusion / Insecure JWT Implementation |
| 17 | GraphQL Complexity/Depth Attack |
| 18 | Inference-based Internal Reconnaissance |
| 19 | Failure to verify Origin/Domain before autofill |
| 20 | Padding Oracle Attack |
| 21 | HTTP Request Smuggling |
| 22 | Content-Security-Policy |
| 23 | SSRF using Gopher |
| 24 | Broken Functional Level Authorization and Header-based Bypassing |
| 25 | SAML Signature Wrapping |
| 26 | Insecure Deserialization |
| 27 | Overly permissive CORS |
| 28 | Parameterized queries / prepared statements |
| 29 | UNION SQL Injection |
| 30 | In-line Comment |
| 31 | Time-based Inference via Resource Exhaustion |
| 32 | Shell Injection |
| 33 | HTTP Response Splitting |
| 34 | Information Gathering from robots.txt |
| 35 | Document Root |
| 36 | Dragonblood |
| 37 | WPA3 downgrade to weaker protocol |
| 38 | Clientless PMKID attack |
| 39 | Mask attack reduces search space |
| 40 | Session Hijacking via MAC Spoofing |
| 41 | Rogue AP |
| 42 | Certificate validation failure / insecure PAP |
| 43 | MAC Flooding |
| 44 | Rogue switch may become Root Bridge |
| 45 | ARP Spoofing |
| 46 | MAC Flooding |
| 47 | NetBIOS Enumeration |
| 48 | LDAP Enumeration |
| 49 | ms-sql-m |
| 50 | Wireshark |
| 51 | NULL Scan |
| 52 | Service Version Discovery |
| 53 | `--spoof-mac Dell` |
| 54 | Filter specified ICMP types |
| 55 | DNS Tunneling |
| 56 | DoH over HTTPS/443 |
| 57 | Fast-Flux DNS |
| 58 | TCP Stream Segmentation/Overlap Evasion |
| 59 | RST Hijacking |
| 60 | Session Donation Attack |
| 61 | Active Session Hijacking |
| 62 | Blind Hijacking |
| 63 | API Hooking |
| 64 | Process Hollowing |
| 65–66 | DLL Side-Loading / DLL Hijacking |
| 67 | Monitor suspicious outbound connections |
| 68 | Web shell hidden in User-Agent/log injection |
| 69 | Timestomping |
| 70 | Polymorphic malware |
| 71 | ROP reuses existing code |
| 72 | ASLR |
| 73 | NOP sled |
| 74 | EDR behavioral monitoring |
| 75 | Office ASR rules |
| 76 | WMI Event Subscription persistence |
| 77–78 | SUID privilege abuse |
| 79 | Arbitrary File Read |
| 80 | TOCTOU symlink replacement |
| 81 | Steganography / in-memory execution |
| 82 | Environmental Keying |
| 83 | DLL Side-Loading |
| 84 | RAT |
| 85 | Black Hat hackers |
| 86 | Worm |
| 87 | Botnet Agents |
| 88–89 | SMB/LDAP Relay |
| 90 | AS-REP Roasting |
| 91 | Pass-the-Ticket |
| 92 | Constrained Delegation abuse |
| 93 | Internal Monologue |
| 94 | Distributed Rate-Limit Bypass |
| 95 | SIM Swapping risk |
| 96 | MFA Fatigue |
| 97 | PKCE |
| 98 | Bind biometric success to a protected cryptographic key |
| 99 | Mask attack |
| 100 | Hash Collision |
| 101 | Perfect Forward Secrecy |
| 102 | Base64 is encoding, not encryption |
| 103 | DLP regex evasion via XOR |
| 104 | Malleability / Integrity |
| 105 | RSA private key required for recovery absent another weakness |
| 106 | Blinding / power-analysis countermeasures |
| 107 | HSTS Fingerprinting |
| 108 | Improper Hardware-Backed Storage Usage |
| 109 | UPnP automatic port forwarding |
| 110 | Hardcoded Secrets / Weak Cryptography |
| 111 | Clear-text key exchange |
| 112 | Unprotected BLE Characteristics |
| 113 | Lack of Message Integrity and Authentication |
| 114 | Physical-world ICS consequences |
| 115–116 | HMI Spoofing / Data Diddling |
| 117 | Low-and-Slow Integrity Attack |
| 118 | Distributed Control System |
| 119 | Infrastructure misconfiguration / DoS |
| 120 | Slowloris / Layer 7 DoS |
| 121–122 | Rate Limiting / HTTP GET-POST Attack |
| 123 | Web Application Firewall |
| 124 | DRDoS |
| 125 | ICMP exfiltration to evade egress controls |
| 126 | Flawed risk assessment |
| 127 | Untested BCP |
| 128 | Insurance does not replace controls |
| 129, 137 | Manage in-scope BYOD assets |
| 130, 132 | Segregation of Duties failure |
| 131 | ISO/IEC 27005:2022 |
| 133 | Inadequate AUP controls |
| 134 | Asset management / information classification weakness |
| 135, 165 | Assessment Overview |
| 136 | Honest reporting and confidentiality |
| 138, 159 | Verification |
| 139 | Credentialed Scanning |
| 140 | Risk sharing does not remove vulnerabilities |
| 141 | Creepy |
| 142 | Vishing |
| 143 | Social Engineering |
| 144 | Shoulder Surfing |
| 145 | `filetype:pdf intitle:"admin access" site:onion` |
| 146 | Remote locate and wipe |
| 147 | Insecure Data Storage |
| 148 | Cross-App Scripting / File-based XSS |
| 149 | Semi-untethered Jailbreaking |
| 150 | On-device APK rooting |
| 151 | Cisco Adaptive Wireless IPS |
| 152 | Measured Service |
| 153 | Service Version Discovery |
| 154 | Honeytokens detect intruders |
| 155 | NOP sled |
| 156 | ICMP exfiltration |
| 157 | Design Flaws |
| 158 | Colasoft Packet Builder |
| 160 | Rate Limiting |
| 161 | Block unnecessary ports/protocols |
| 162 | Rogue DHCP Server Attack |
| 163 | Ping Method |
| 164 | Eclipse Attack |

---

## Important accuracy notes

1. **CORS wildcard:** `Access-Control-Allow-Origin: *` does not by itself allow credentialed cross-origin reads. Browsers do not permit credentialed responses with wildcard origin. The risk depends on the data and request design; the original quiz wording oversimplifies this.
2. **LDAP signing:** NTLM relay to LDAP depends on the target's LDAP signing/channel-binding protections and other configuration details. “LDAP signing not required” alone is not a complete description of every condition needed to create a Domain Admin.
3. **SUID shell behavior:** A SUID-root editor does not guarantee that a spawned shell retains root privileges. Some shells drop elevated privileges, and modern Vim builds may restrict shell escapes. The quiz's expected answer is root because the editor runs with the owner's effective UID, but the real outcome depends on implementation and shell behavior.
4. **WPA3 transition mode:** Dragonblood refers to vulnerabilities in WPA3-SAE implementations, including side-channel and downgrade-related issues. The exact exploit depends on the implementation and configuration.
5. **Password hash collision:** A collision means two different inputs produce the same hash, but a login accepting a colliding password depends on the specific hash function and authentication implementation. MD5 is broken and unsuitable for password storage; use salted, slow password hashing such as Argon2id.
6. **ISO risk standard:** ISO/IEC 27005 provides guidance for information security risk management. ISO/IEC 27001 specifies ISMS requirements; these standards are complementary, not interchangeable.
7. **Wireless IPS question:** The described centralized alarm aggregation and coordinated countermeasure behavior is closest to Cisco Adaptive Wireless IPS among the given choices; product capabilities vary by platform and version.
8. **Nmap MAC spoofing syntax:** `--spoof-mac Dell` is valid Nmap syntax for selecting a vendor prefix. MAC spoofing generally affects Ethernet/Wi-Fi local-link identity and does not make a scan anonymous.
9. **ICMP and DNS exfiltration:** These protocols are not automatically invisible or encrypted. Proper egress monitoring, protocol validation, and anomaly detection can identify tunneling.
10. **Ransomware recovery:** “Impossible without the private RSA key” is the intended answer for the described hybrid-encryption design, assuming sound cryptography, secure key deletion, and no implementation flaw or available backup.

