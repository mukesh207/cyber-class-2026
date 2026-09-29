# Local Network Reconnaissance: SSH & RDP Enumeration

> **Assessment Type:** Authorized Local Network Reconnaissance  
> **Network:** `192.168.1.0/24`  
> **Primary Target:** `192.168.1.105`  
> **Tools:** Nmap, Netcat, SSH, SCP  
> **Focus:** Host discovery, service enumeration, SSH analysis, RDP analysis, and authorized access

---

## 1. Overview

This walkthrough documents a local network reconnaissance exercise performed as part of a cybersecurity assignment.

The objective was to:

- Discover active hosts on the local network
- Identify exposed TCP services
- Enumerate SSH
- Enumerate RDP
- Investigate an unidentified service on port `1716`
- Identify supported authentication methods
- Perform authorized SSH access
- Transfer files using SCP
- Understand the difference between network connectivity and application-level access

The target host used during the exercise was:

```text
192.168.1.105
```

The target belonged to another participant in the assignment. The owner was informed about the activity, and the exercise was approved by the mentor.

---

# 2. Network Discovery

The first step was identifying hosts on the local network.

The initial command was:

```bash
nmap 192.168.1.0
```

This returned a host-down result because `192.168.1.0` is the network address rather than an individual host.

Therefore, the entire `/24` subnet was scanned:

```bash
nmap 192.168.1.0/24
```

The scan identified several hosts.

Among the discovered systems was:

```text
192.168.1.105
```

At this stage, the goal was simply to identify which machines were reachable and which services they exposed.

---

# 3. Searching for SSH

Because SSH is commonly exposed on TCP port `22`, the next step was to search the subnet specifically for systems with an open SSH port.

```bash
nmap -p 22 --open 192.168.1.0/24
```

The result identified:

```text
192.168.1.105
22/tcp open ssh
```

This made `192.168.1.105` a primary host for further enumeration.

---

# 4. SSH Version Enumeration

The SSH service was enumerated using:

```bash
nmap -sV -p 22 192.168.1.105
```

The result identified:

```text
OpenSSH 10.4p1 Debian 5
```

The service was running SSH protocol version:

```text
SSH-2.0
```

### Why use `-sV`?

The `-sV` option attempts to determine the service and version running behind an open port.

This is useful because knowing the exact service version can help with:

- Identifying software
- Understanding the target environment
- Checking configuration
- Researching known vulnerabilities
- Selecting appropriate enumeration techniques

---

# 5. SSH Default Script Enumeration

Nmap's default scripts were executed against SSH:

```bash
nmap -sC -sV -p 22 192.168.1.105
```

The SSH service was again identified as:

```text
OpenSSH 10.4p1 Debian 5
```

No immediate vulnerability was reported by the default scripts.

---

# 6. SSH Algorithm Enumeration

The supported SSH cryptographic algorithms were enumerated using:

```bash
nmap -sV -p 22 --script ssh2-enum-algos 192.168.1.105
```

The server supported several key-exchange algorithms, including:

```text
mlkem768x25519-sha256
sntrup761x25519-sha512
curve25519-sha256
curve25519-sha256@libssh.org
ecdh-sha2-nistp256
ecdh-sha2-nistp384
ecdh-sha2-nistp521
```

Host-key algorithms included:

```text
rsa-sha2-512
rsa-sha2-256
ecdsa-sha2-nistp256
ssh-ed25519
```

Encryption algorithms included:

```text
chacha20-poly1305@openssh.com
aes128-gcm@openssh.com
aes256-gcm@openssh.com
aes128-ctr
aes192-ctr
aes256-ctr
```

### Why enumerate SSH algorithms?

SSH algorithm enumeration helps determine:

- Which cryptographic algorithms are enabled
- Whether legacy algorithms are supported
- What cryptographic options are available to clients
- Whether the server configuration follows modern SSH practices

---

# 7. SSH Banner Grabbing with Netcat

The SSH service was also tested using Netcat:

```bash
nc -nv 192.168.1.105 22
```

The server returned:

```text
SSH-2.0-OpenSSH_10.4p1 Debian-5
```

This is known as the SSH banner.

The banner provides basic information about the SSH implementation.

### Important observation

Typing:

```text
ls
```

did not produce a shell.

Instead, the server responded with:

```text
Invalid SSH identification string.
```

This happens because Netcat only establishes a raw TCP connection. It does not perform the SSH protocol negotiation required to obtain an SSH shell.

### Key lesson

```text
TCP connection != application session
```

A port being open does not automatically mean that commands can be executed through a simple TCP connection.

---

# 8. Enumerating SSH Authentication Methods

The supported SSH authentication mechanisms were checked with:

```bash
nmap --script ssh-auth-methods -p 22 192.168.1.105
```

The server supported:

```text
publickey
password
```

### Why is this useful?

SSH commonly supports authentication through:

- Passwords
- SSH public/private keys
- Other configured authentication mechanisms

Knowing which mechanisms are enabled helps understand the authentication surface of the service.

---

# 9. Full TCP Port Scan

The next step was identifying services running on ports other than the default SSH port.

A full TCP port scan was performed:

```bash
nmap -p- --open 192.168.1.105
```

The scan identified:

```text
22/tcp    open    ssh
1716/tcp  open    xmsg
3389/tcp  open    ms-wbt-server
```

The target therefore exposed three TCP services:

| Port | Service | Description |
|------|---------|-------------|
| 22 | SSH | Secure remote administration |
| 1716 | xmsg | Unidentified/tcpwrapped service |
| 3389 | RDP | Remote Desktop Protocol |

---

# 10. Service Enumeration

The discovered ports were enumerated using:

```bash
nmap -sC -sV -p 22,1716,3389 192.168.1.105
```

The results showed:

```text
22/tcp
OpenSSH 10.4p1 Debian 5

1716/tcp
tcpwrapped

3389/tcp
ms-wbt-server
```

The RDP service also returned NTLM information.

Important information included:

```text
Target_Name: KALI
NetBIOS_Domain_Name: KALI
NetBIOS_Computer_Name: KALI
DNS_Domain_Name: KALI
DNS_Computer_Name: KALI
Product_Version: 10.0.22631
```

This provided useful information about the remote desktop environment.

---

# 11. Investigating Port 1716

Port `1716` was identified as:

```text
1716/tcp open tcpwrapped
```

A more focused service scan was performed:

```bash
nmap -sV -p 1716 192.168.1.105
```

The result remained:

```text
1716/tcp open tcpwrapped
```

A direct TCP connection was then attempted:

```bash
nc -nv 192.168.1.105 1716
```

The connection succeeded.

However, entering commands such as:

```text
ls
pwd
hostname
```

did not result in shell output.

### Important lesson

An open port only confirms that a TCP service is accepting connections.

It does **not** mean that the service provides:

- A command shell
- Interactive terminal access
- A text-based protocol
- Remote command execution

The application protocol must still be identified.

---

# 12. RDP Enumeration

The RDP service was running on:

```text
3389/tcp
```

The following Nmap scripts were used:

```bash
nmap --script rdp-enum-encryption,rdp-ntlm-info -p 3389 192.168.1.105
```

The scan confirmed RDP functionality and returned NTLM information.

The important host information included:

```text
Target_Name: KALI
NetBIOS_Computer_Name: KALI
DNS_Computer_Name: KALI
Product_Version: 10.0.22631
```

---

# 13. Checking RDP Security Configuration

RDP encryption and security configuration were examined using:

```bash
nmap --script rdp-enum-encryption,rdp-ntlm-info -p 3389 192.168.1.105
```

The result indicated:

```text
Security layer: CredSSP (NLA): SUCCESS
```

This means Network Level Authentication (NLA) was enabled.

### What is NLA?

Network Level Authentication requires authentication before a full RDP session is established.

This provides an additional authentication layer compared with older RDP configurations.

---

# 14. RDP Vulnerability Check

An Nmap script for checking the historical MS12-020 RDP vulnerability was executed:

```bash
nmap --script rdp-vuln-ms12-020 -p 3389 192.168.1.105
```

The result showed:

```text
3389/tcp open ms-wbt-server
```

No positive MS12-020 vulnerability result was reported.

### Important note

A single vulnerability script not reporting a vulnerability does not prove that the service is completely secure.

It only means that this particular check did not identify the tested condition.

---

# 15. Aggressive Service Enumeration

An aggressive Nmap scan was performed:

```bash
sudo nmap -A -p 22,1716,3389 192.168.1.105
```

This provided additional information about:

- Services
- Versions
- OS fingerprinting
- RDP information
- Network distance
- Traceroute

The traceroute showed:

```text
1  192.168.0.1
2  192.168.1.105
```

Nmap also reported that OS detection could be unreliable because the scan did not have enough open/closed ports for high-confidence fingerprinting.

### Lesson

Nmap's OS detection is an estimation based on network responses.

It should not automatically be treated as definitive.

---

# 16. Authorized SSH Access

During the authorized assignment, credentials were provided for the target account.

The SSH connection was established using:

```bash
ssh kali@192.168.1.105
```

The provided credentials were:

```text
Username: kali
Password: kali
```

The credentials were used only with the permission of the target owner and mentor as part of the assignment.

After the exercise, the password was changed by the account owner.

### Important security lesson

Using simple credentials such as:

```text
kali / kali
```

creates a significant authentication weakness if such credentials are used in a real environment.

Credentials should be:

- Unique
- Strong
- Difficult to guess
- Protected from disclosure
- Changed when exposed during testing

---

# 17. Verifying SSH Access

After connecting through SSH, basic commands can be used to understand the session:

```bash
whoami
```

```bash
id
```

```bash
hostname
```

```bash
sudo -l
```

These commands help determine:

### `whoami`

The current username.

### `id`

User ID, group membership, and supplementary groups.

### `hostname`

The name of the remote system.

### `sudo -l`

The commands the current user may execute through `sudo`, depending on the configured permissions.

---

# 18. File Transfer with SCP

After authorized SSH access, files from the remote machine were transferred for the assignment.

For example:

```bash
scp -r kali@192.168.1.105:/home/kali/Pictures .
```

The `-r` option means recursive copying.

This allows an entire directory and its contents to be transferred.

The `.` means:

```text
Copy the files into the current local directory.
```

---

# 19. SCP Path Issue

An initial SCP attempt used:

```bash
\~/Downloads/furkhan
```

This resulted in an error similar to:

```text
scp: mkdir /root/Downloads/furkhan: No such file or directory
```

The problem was related to the local shell path and the meaning of `~`.

The tilde:

```bash
~
```

represents the home directory of the current local user.

For example:

```text
/home/st4rk
```

for the local user `st4rk`.

It does not automatically refer to:

```text
/home/kali
```

on the remote machine.

---

# 20. Correct SCP Approach

A simpler approach was to copy the files into the current directory:

```bash
scp -r kali@192.168.1.105:/home/kali/Pictures .
```

This avoids confusion between the local and remote home directories.

The basic SCP structure is:

```text
scp [options] user@remote_host:/remote/path /local/path
```

Example:

```bash
scp -r kali@192.168.1.105:/home/kali/Pictures .
```

Where:

```text
kali
    ↓
Remote username

192.168.1.105
    ↓
Remote host

/home/kali/Pictures
    ↓
Remote source directory

.
    ↓
Current local directory
```

---

# 21. Final Attack Surface

The final identified attack surface of the target was:

```text
                    192.168.1.105
                          |
          +---------------+---------------+
          |               |               |
        22/tcp         1716/tcp        3389/tcp
          |               |               |
         SSH           tcpwrapped        RDP
          |                               |
    OpenSSH 10.4p1                  CredSSP / NLA
          |
   +------+------+
   |             |
password       publickey
   |
authorized
access
```

---

# 22. Key Findings

## Finding 1 — SSH exposed

```text
22/tcp open ssh
```

The host exposed an OpenSSH service.

Version:

```text
OpenSSH 10.4p1 Debian 5
```

---

## Finding 2 — Password authentication enabled

SSH supported:

```text
password
publickey
```

Password authentication increases the importance of strong credentials and appropriate authentication controls.

---

## Finding 3 — RDP exposed

```text
3389/tcp open ms-wbt-server
```

RDP was accessible and supported Network Level Authentication.

---

## Finding 4 — Port 1716 exposed

```text
1716/tcp open tcpwrapped
```

The service accepted TCP connections but did not provide a shell through Netcat.

Further protocol identification would be required to understand the service.

---

## Finding 5 — Weak credentials were available during the exercise

The authorized credentials provided for the assignment were:

```text
kali:kali
```

The password was changed after the exercise.

This demonstrates why default or easily guessable credentials should never be used on systems exposed to a network.

---

# 23. Lessons Learned

This exercise provided practical experience with several important penetration-testing concepts.

### 1. Start with discovery

```text
What hosts exist?
        ↓
Which ports are open?
        ↓
Which services are running?
        ↓
Which versions are running?
        ↓
What authentication methods are available?
```

---

### 2. Scan all ports when necessary

A default Nmap scan checks only the most common ports.

Using:

```bash
nmap -p- --open <target>
```

can reveal additional services running on uncommon ports.

---

### 3. An open port does not mean a shell

For example:

```bash
nc -nv 192.168.1.105 1716
```

successfully connected to the service.

But:

```text
ls
pwd
hostname
```

did not execute.

The service was not a command shell.

---

### 4. Service enumeration matters

Different services require different enumeration techniques.

For SSH:

```text
ssh-auth-methods
ssh2-enum-algos
```

For RDP:

```text
rdp-enum-encryption
rdp-ntlm-info
rdp-vuln-ms12-020
```

---

### 5. Authentication is part of the attack surface

Finding:

```text
password
```

as an SSH authentication method tells us that credential security matters.

A service can be technically secure while still being exposed through weak credentials.

---

### 6. Authorization comes first

Network reconnaissance should only be performed when there is permission to test the target.

In this exercise:

```text
Target owner informed
        ↓
Mentor approval
        ↓
Authorized testing
        ↓
Controlled access
        ↓
Password changed afterward
```

This kept the activity within the assignment's scope.

---

# 24. Commands Used

For quick reference, the main commands used during the exercise were:

```bash
nmap 192.168.1.0/24
```

```bash
nmap -p 22 --open 192.168.1.0/24
```

```bash
nmap -sV -p 22 192.168.1.105
```

```bash
nmap -sC -sV -p 22 192.168.1.105
```

```bash
nmap -sV -p 22 --script ssh2-enum-algos 192.168.1.105
```

```bash
nc -nv 192.168.1.105 22
```

```bash
nmap --script ssh-auth-methods -p 22 192.168.1.105
```

```bash
nmap -p- --open 192.168.1.105
```

```bash
nmap -sC -sV -p 22,1716,3389 192.168.1.105
```

```bash
nmap -sV -p 1716 192.168.1.105
```

```bash
nc -nv 192.168.1.105 1716
```

```bash
nmap --script rdp-enum-encryption,rdp-ntlm-info -p 3389 192.168.1.105
```

```bash
nmap --script rdp-vuln-ms12-020 -p 3389 192.168.1.105
```

```bash
sudo nmap -A -p 22,1716,3389 192.168.1.105
```

```bash
ssh kali@192.168.1.105
```

```bash
scp -r kali@192.168.1.105:/home/kali/Pictures .
```

---

# 25. Tools Used

| Tool | Purpose |
|------|---------|
| Nmap | Host and service discovery |
| Netcat | TCP connectivity and banner testing |
| SSH | Authorized remote access |
| SCP | Secure file transfer |
| Linux CLI | Command execution and investigation |

---

# 26. Skills Practiced

This assignment helped practice:

- Network discovery
- TCP port scanning
- Service enumeration
- Version detection
- SSH enumeration
- SSH authentication enumeration
- SSH cryptographic algorithm enumeration
- Banner grabbing
- RDP enumeration
- RDP security analysis
- Vulnerability script usage
- OS fingerprinting
- SSH authentication
- SCP file transfer
- Linux command-line troubleshooting
- Understanding network services
- Responsible security testing

---

# 27. Conclusion

This exercise demonstrated a practical reconnaissance workflow against a host on a local network.

The process started with:

```text
Network Discovery
        ↓
Port Discovery
        ↓
Service Enumeration
        ↓
SSH Enumeration
        ↓
RDP Enumeration
        ↓
Additional Port Investigation
        ↓
Authorized Authentication
        ↓
File Transfer
```

The target exposed SSH, RDP, and an additional service on port `1716`.

SSH provided useful information through version detection, authentication-method enumeration, algorithm enumeration, and banner grabbing.

RDP enumeration revealed Network Level Authentication and additional NTLM information.

The exercise also demonstrated an important penetration-testing principle:

> **Finding an open port is only the beginning. Understanding what is actually running behind that port is the real objective of enumeration.**

All testing documented in this walkthrough was performed with authorization as part of the assignment.
