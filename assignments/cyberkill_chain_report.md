# Understanding the Cyber Kill Chain

## What is a Kill Chain in Cybersecurity?
A cyber kill chain is a security framework designed to identify and stop sophisticated cyberattacks by breaking down the attack into multiple, distinct stages. Originating from military operations where an enemy attack is identified, broken down into stages, and preventive measures are deployed, this concept was adapted for cybersecurity by Lockheed Martin in 2011.

This model helps security teams recognize, intercept, or prevent attacks before they cause significant impact. Its primary purpose is to bolster an organization's defenses against Advanced Persistent Threats (APTs) and sophisticated attacks, which commonly include malware, ransomware, Trojan horses, phishing, and other social engineering techniques.

## The 7 Stages of a Cyber Kill Chain
The original framework defines the attacker's lifecycle through seven stages:

1. **Reconnaissance**: The attacker selects a target, researches it, and identifies vulnerabilities (e.g., scanning networks, harvesting emails).
2. **Weaponization**: The attacker creates a remote-access malware weapon tailored to exploit one or more identified vulnerabilities.
3. **Delivery**: The weapon is transmitted to the target (e.g., via phishing emails, infected USB drives, or malicious websites).
4. **Exploitation**: The malware weapon's code is triggered, taking action on the target network to exploit the vulnerability.
5. **Installation**: The malware installs an access point (like a backdoor) usable by the attacker to maintain presence.
6. **Command and Control (C2)**: The malware enables the attacker to establish a "hands-on-the-keyboard" persistent connection to the target network.
7. **Actions on Objectives**: The attacker takes final action to achieve their original goals, such as data encryption, data destruction, or deeper network infiltration.

## Is there an Eighth Step in the Cyber Kill Chain?
While Lockheed Martin's original model has seven steps, the modern cybersecurity community often adds an eighth step: **Monetization** (sometimes referred to as **Exfiltration**). As cybercrime has evolved to be highly financially motivated (especially with the rise of ransomware), this step specifically accounts for how the attacker extracts financial gain from the breach, such as selling stolen data or collecting a ransom.

## How Security Solutions Detect and Prevent Attacks
By leveraging the kill chain model alongside threat intelligence, automation, and unified security workflows, organizations can enable proactive defense:
- **Reconnaissance**: Firewalls and intrusion detection systems (IDS) can detect network scanning.
- **Delivery & Exploitation**: Email security filters block phishing, while endpoint detection and response (EDR) and antivirus solutions block malicious payloads from executing.
- **C2 & Actions on Objectives**: Network segmentation and outbound traffic monitoring can prevent malware from communicating with attacker servers or exfiltrating data.

## Weaknesses in the Cyber Kill Chain
While effective, the traditional Cyber Kill Chain has some critiques:
- **Limited Attack Detection Profile**: It is primarily focused on malware and external threats.
- **No Insider Threat Detection**: The framework struggles with detecting attacks that originate from within the organization or attacks using compromised legitimate credentials.
- **Web-Based Attacks**: It is less suited for identifying purely web-based attacks like Cross-Site Scripting (XSS), SQL Injection, or DoS/DDoS, as these don't always follow the traditional malware deployment stages (as seen in the 2017 Equifax breach).

---

## Example Scenario: Cyber Kill Chain in Action
*Based on the TryHackMe "Guided Pentest: Web" Room*

To understand how the Cyber Kill Chain is used, here is a simplified mapping of a web application penetration test:

1. **Reconnaissance**: The attacker scans the target website and discovers a hidden password reset page.
2. **Weaponization**: The attacker prepares an exploit strategy to manipulate the password reset flow and creates a malicious file (a web shell) to upload later.
3. **Delivery**: The attacker accesses the vulnerable password reset page and interacts with the web application.
4. **Exploitation**: The attacker bypasses security controls (using an Insecure Direct Object Reference - IDOR) to reset the administrator's password and logs into the admin panel.
5. **Installation**: Using their new admin access, the attacker uploads their malicious web shell to the server.
6. **Command and Control (C2)**: The attacker executes the web shell, gaining a direct command-line connection to the underlying server.
7. **Actions on Objectives**: The attacker uses their command-line access to locate and read sensitive files (the "flags") on the server, completing their goal.

---