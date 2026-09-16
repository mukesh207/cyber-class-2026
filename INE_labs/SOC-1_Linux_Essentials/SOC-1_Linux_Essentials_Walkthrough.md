# SOC-1: Linux Essentials — Lab Walkthrough

> **Platform:** INE  
> **Lab:** SOC-1: Linux Essentials  
> **Environment:** Ubuntu-based Linux  
> **Focus:** Linux administration, investigation, logging, persistence, and suspicious artifact detection

---

## 🎯 Objectives

By completing this lab, we cover:

- User and account management
- Linux groups and authentication controls
- Process and service investigation
- Cron and scheduled tasks
- Linux authentication and system logs
- Apache web-server logging
- Suspicious file and binary inspection
- Startup persistence mechanisms
- SSH authorized keys and SSH configuration

---

# 1. User & Account Management

## 1.1 Understanding Linux Accounts

Linux commonly contains three categories of accounts:

| Account Type | Purpose |
|---|---|
| Root | Superuser with unrestricted access |
| Local User | Regular interactive user account |
| System/Service Account | Used by services and background processes |

From a SOC perspective, unusual user accounts, unexpected privileges, or accounts capable of interactive login can be useful investigation indicators.

---

## 1.2 Identify Users

```bash
cat /etc/passwd
```

Each entry follows:

```text
username:x:UID:GID:comment:home_directory:login_shell
```

### Important fields

- **UID** → User ID
- **GID** → Primary Group ID
- **Home directory** → User's home location
- **Login shell** → Determines whether an interactive shell can normally be obtained

Common interactive shells:

```text
/bin/bash
/bin/sh
/bin/zsh
```

Non-interactive shells:

```text
/usr/sbin/nologin
/bin/false
```

### 🔎 SOC Perspective

When investigating a compromised Linux host, review:

- Unexpected accounts
- Unexpected login shells
- Newly created users
- Privileged users
- Service accounts that unexpectedly have interactive shells

---

## 1.3 Identify Groups

```bash
cat /etc/group
```

Format:

```text
group_name:password:GID:members
```

Important groups discussed in the lab:

- **sudo** → Users can execute commands with elevated privileges
- **adm** → Access to system logs and monitoring files
- **root** → Associated with the root user
- **sys** → Legacy system group

### 🔎 SOC Perspective

Unexpected membership in privileged groups can indicate privilege escalation or unauthorized account modification.

---

## 1.4 Check Whether an Account Is Locked

```bash
grep <user_name> /etc/shadow
```

A locked account starts with:

```text
!
```

Example investigation:

```bash
grep news /etc/shadow
```

### 🔎 SOC Perspective

Account status is important when investigating suspicious authentication activity. A locked account appearing in authentication logs may require further investigation.

> `/etc/shadow` contains sensitive authentication information and normally requires elevated privileges.

---

# 2. Password & Authentication Controls

Linux authentication behavior is primarily controlled through:

```text
/etc/login.defs
/etc/pam.d/common-password
```

---

## 2.1 Inspect Login Policy

```bash
cat /etc/login.defs
```

The lab highlights settings related to:

- Failed login logging
- Successful login logging
- Password aging
- Password expiration
- Login/session controls

### Important security considerations

`FAILLOG_ENAB` relates to failed login tracking.

This can support investigations involving:

- Brute-force attempts
- Credential abuse

The lab also notes that legacy `FAILLOG_ENAB` tracking can conflict with PAM-based mechanisms such as `pam_faillock`.

`LOG_UNKFAIL_ENAB` controls logging of failed attempts involving nonexistent users.

Disabled logging can reduce visibility into:

- Username enumeration
- Password spraying

`LOG_OK_LOGINS` relates to successful login logging.

Reduced successful-login visibility can make authentication investigations more difficult.

---

## 2.2 Inspect PAM Password Configuration

```bash
cat /etc/pam.d/common-password
```

The lab highlights:

```text
password [success=1 default=ignore] pam_unix.so obscure sha512
```

### `pam_unix.so`

Handles local user password authentication and interacts with password hashes stored in `/etc/shadow`.

### `sha512`

The lab describes this configuration as using SHA-512 password hashing.

### `obscure`

Helps reject weak password patterns.

### PAM control flag

```text
[success=1 default=ignore]
```

The lab explains that successful execution causes PAM to skip the next module, while failure continues according to the configuration.

---

## 2.3 Password Complexity

The lab discusses:

```text
pam_pwquality.so
```

This module can enforce password strength requirements such as:

- Password length
- Uppercase characters
- Lowercase characters
- Digits
- Special characters
- Prevention of weak passwords

### 🔎 SOC Perspective

Authentication configuration should be considered alongside authentication logs. A weak or poorly monitored authentication configuration can increase the impact of compromised credentials.

---

# 3. Process Investigation

## 3.1 List Running Processes

```bash
ps aux
```

This displays running processes and useful information such as:

- PID
- User
- CPU usage
- Memory usage
- Command
- Process start information

### 🔎 SOC Perspective

Look for:

- Unknown processes
- Processes running as root unexpectedly
- Suspicious command-line arguments
- Processes executing from unusual directories
- Unexpected network-related processes

---

## 3.2 Investigate a Specific Process

First obtain a PID, then:

```bash
ps -p $PID -o pid,ppid,user,cmd
```

Example:

```bash
ps -p 1234 -o pid,ppid,user,cmd
```

This provides:

- PID
- Parent PID
- User
- Command

### Why PPID matters

The parent process can help establish process ancestry during an investigation.

---

## 3.3 Identify the Executable Path

```bash
readlink -f /proc/$PID/exe
```

Example:

```bash
readlink -f /proc/1234/exe
```

### 🔎 SOC Perspective

The executable path is particularly useful when a process name looks legitimate but the binary is running from an unexpected location.

---

## 3.4 Filter Processes

```bash
ps aux | grep -i <process_name>
```

Example:

```bash
ps aux | grep -i ssh
```

> Note: `grep` itself may appear in the results.

---

# 4. Service Investigation

## 4.1 List Running Services

```bash
systemctl list-units --type=service --state=running
```

This shows active system services.

---

## 4.2 Inspect a Service

```bash
systemctl status <service_name>
```

Example:

```bash
systemctl status ssh
```

Useful information includes:

- Service state
- PID
- Resource usage
- Recent service messages

### 🔎 SOC Perspective

Investigate services that are:

- Unknown
- Unexpectedly enabled
- Recently created
- Executing from unusual locations
- Executing scripts from `/tmp`, `/dev/shm`, or hidden directories

---

# 5. Startup Persistence & Cron

Persistence allows commands, scripts, or binaries to execute automatically after reboot or login.

---

## 5.1 Find Enabled Services

```bash
systemctl list-unit-files --type=service | grep enabled
```

Enabled services are configured to start automatically.

### 🔎 SOC Perspective

Look for:

- Oddly named services
- Recently enabled services
- Services executing suspicious scripts
- Executables located in temporary directories
- Hidden or unusual paths

---

## 5.2 Inspect System Cron Jobs

```bash
cd /etc/cron.d/
```

You can then inspect the files:

```bash
ls -la /etc/cron.d/
```

System cron locations also include:

```text
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

These directories contain scheduled tasks that execute at their corresponding intervals.

---

## 5.3 Inspect Current User's Cron

```bash
crontab -l
```

This lists cron jobs for the current user.

For root's crontab when using another account:

```bash
sudo crontab -l
```

### 🔎 SOC Perspective

Cron is useful for both legitimate automation and persistence.

Investigate:

- Unexpected scheduled scripts
- Commands running from `/tmp`
- Encoded or obfuscated commands
- Remote downloads
- Unknown binaries
- Recently added cron entries

---

# 6. Linux Authentication Logs

## 6.1 Review Authentication Activity

```bash
sudo tail -n 100 /var/log/auth.log
```

The lab identifies this log as a source for authentication-related events such as:

- SSH login attempts
- Failed passwords
- Successful logins
- sudo activity
- su activity

---

## 6.2 Find Failed Events

```bash
sudo grep -i "Failed" /var/log/auth.log | tail -n 50
```

This can reveal failed authentication and other events containing the word `failed`.

### ⚠️ Investigation Note

Searching only for the word `Failed` can produce false positives because unrelated log messages or command strings may also contain that word.

---

## 6.3 Investigate a Specific User

```bash
sudo grep -i "Failed .* John" /var/log/auth.log | tail -n 50
```

This focuses on failed events associated with the specified username.

### 🔎 SOC Perspective

Correlate:

```text
Username
↓
Source IP
↓
Timestamp
↓
Authentication result
↓
Follow-up activity
```

This helps build an authentication timeline.

---

# 7. Sudo Activity

```bash
sudo grep -i "sudo" /var/log/auth.log | tail -n 50
```

This can show:

- sudo session opening
- sudo session closing
- User executing sudo
- Command executed

### 🔎 SOC Perspective

Unexpected sudo activity can be important when investigating privilege escalation.

Questions to ask:

1. Who executed sudo?
2. What command was executed?
3. When did it happen?
4. Was the user expected to have sudo privileges?
5. What happened immediately before and after it?

---

# 8. journalctl & Systemd Logs

## 8.1 View Systemd Journal

```bash
sudo journalctl
```

The journal can contain:

- Boot messages
- Kernel logs
- Service events
- Authentication events
- sudo activity
- SSH activity
- Cron activity
- Application logs

---

## 8.2 Filter SSH Logs

```bash
sudo journalctl -u ssh
```

This filters journal entries for the SSH service.

### 🔎 SOC Perspective

Use time-based filtering when building an incident timeline:

```bash
sudo journalctl --since "1 hour ago"
```

or inspect a specific service:

```bash
sudo journalctl -u ssh
```

---

# 9. General System Logs

## 9.1 Inspect syslog

```bash
cat /var/log/syslog
```

The lab describes `/var/log/syslog` as a general system log containing events such as:

- Service activity
- Daemon activity
- Network changes
- Cron executions

---

## 9.2 Inspect Kernel Logs

```bash
cat /var/log/kern.log
```

The lab highlights:

- Kernel boot events
- Hardware detection
- Driver initialization
- CPU-related information

### 🔎 SOC Perspective

Kernel logs can provide useful context when investigating unusual hardware, drivers, or system-level behavior.

---

# 10. Apache Web Server Logging

## 10.1 Locate Apache Logs

```bash
ls -la /var/log/apache2/
```

Important files include:

```text
access.log
error.log
access.log.1
other_vhosts_access.log
```

The lab also includes a demonstration backup:

```text
access.log.bak
```

---

## 10.2 Review Recent Access Logs

```bash
sudo tail -n 50 /var/log/apache2/access.log.bak
```

The lab contains simulated requests such as:

```text
GET /admin HTTP/1.1" 404
GET /secret HTTP/1.1" 404
GET /test.php HTTP/1.1" 404
```

These demonstrate:

- Directory probing
- Resource enumeration

Repeated 404 responses can be an indicator of reconnaissance activity.

---

## 10.3 Command Injection Indicator

The lab demonstrates:

```text
GET /?cmd=whoami HTTP/1.1" 200
```

This simulates a command-injection-related request.

### 🔎 SOC Perspective

A suspicious parameter containing command-like input deserves investigation alongside:

- Source IP
- Timestamp
- HTTP status
- User agent
- Other requests from the same source

---

## 10.4 Path Traversal Indicator

The lab demonstrates:

```text
GET /etc/passwd HTTP/1.1" 404
```

This is used to demonstrate a directory/path traversal attempt.

---

## 10.5 Review Apache Errors

```bash
sudo tail -n 20 /var/log/apache2/error.log
```

Error logs can show:

- Service startup
- Server errors
- Permission problems
- Access-control failures

---

## 10.6 Filter HTTP 404 Responses

```bash
sudo grep " 404 " /var/log/apache2/access.log | tail -n 20
```

This filters requests returning HTTP 404 responses.

### 🔎 SOC Perspective

Repeated 404 requests can help identify automated enumeration or reconnaissance.

---

# 11. Suspicious File Indicators

## 11.1 Files Without Owners

```bash
sudo find / -xdev -nouser -o -nogroup 2>/dev/null | head -n 50
```

This searches for files whose user or group ownership does not map to an existing account/group.

Possible investigation areas include:

- Deleted users
- Filesystem issues
- Tampering

---

## 11.2 Executables in Writable Directories

```bash
sudo find /tmp /var/tmp /dev/shm -type f -perm /111 -ls 2>/dev/null
```

This searches for executable files in common temporary/shared-memory locations.

### 🔎 SOC Perspective

Pay attention to executables in:

```text
/tmp
/var/tmp
/dev/shm
```

These locations can be relevant during malware and persistence investigations.

---

## 11.3 Recently Modified System Binaries

```bash
sudo find /bin /sbin /usr/bin /usr/sbin /usr/local/bin -type f -mtime -15 -ls 2>/dev/null | head -n 50
```

`-mtime -15` searches for files modified within the last 15 days.

### 🔎 SOC Perspective

Recently modified binaries should be compared with:

- Package installation/update activity
- Change-management records
- File ownership
- Timestamps
- Known-good versions

The lab recommends adjusting the time window when repeating the exercise.

---

## 11.4 Find SUID Binaries

```bash
sudo find / -xdev -perm -4000 -type f -ls 2>/dev/null | head -n 100
```

SUID binaries execute with the privileges associated with their owner.

### 🔎 SOC Perspective

SUID binaries are important in privilege-escalation investigations.

Do not treat every SUID binary as malicious. Compare findings against expected system binaries and investigate unusual additions or locations.

---

## 11.5 Recently Modified Files in Risky Locations

```bash
sudo find /etc /var /tmp /dev/shm -type f -mtime -3 -ls 2>/dev/null | head -n 100
```

`-mtime -3` identifies files modified within the last 3 days.

Locations:

| Location | Investigation relevance |
|---|---|
| `/etc` | System/service configuration |
| `/var` | Logs, caches, spool data, cron-related data |
| `/tmp` | Temporary files |
| `/dev/shm` | Shared-memory filesystem |

---

# 12. Startup Persistence Inspection

## 12.1 User-Level Shell Persistence

Inspect common shell files:

```bash
ls -la /home/<user>/.bashrc /home/<user>/.bash_history /home/<user>/.profile
```

Then:

```bash
cat /home/<user>/.bashrc
```

---

## 12.2 `.bashrc`

`.bashrc` is a user-level shell configuration file used by interactive Bash shells.

Attackers may attempt to abuse it for persistence by adding commands that execute when a user starts a shell.

Look for:

- Unexpected scripts
- Commands referencing `/tmp`
- Commands referencing `/dev/shm`
- Remote URLs
- Unexpected PATH modifications
- Suspicious command execution

---

## 12.3 `.profile`

Inspect:

```bash
cat /home/<user>/.profile
```

`.profile` is associated with login-shell initialization.

It can execute commands when a user starts a login session.

---

## 12.4 Bash History

```bash
cat /home/<user>/.bash_history
```

The history file can contain:

- Commands executed by the user
- Investigation activity
- Privilege escalation attempts
- Administrative commands

### ⚠️ SOC Note

Command history is useful evidence, but it is not a complete audit trail. Users or malware can modify or delete it.

---

# 13. Hidden Files in Home Directories

## 13.1 List Hidden Files

```bash
ls -la /home/<user>/
```

## 13.2 Search for Hidden Regular Files

```bash
find /home/<user> -type f -name ".*"
```

Look for:

- Recently created files
- Recently modified files
- Executable hidden files
- Scripts referencing `/tmp`
- Scripts referencing `/dev/shm`
- Remote URLs

The lab notes that the observed hidden files were standard configuration files.

---

# 14. System-Level Persistence

## 14.1 Inspect `/etc/profile`

```bash
cat /etc/profile
```

`/etc/profile` is a system-wide login shell configuration file.

The lab identifies login contexts including:

- SSH login
- TTY login
- `su - username`
- Terminal sessions following graphical login

---

## 14.2 Inspect `/etc/profile.d`

```bash
ls -la /etc/profile.d/
```

Shell scripts placed here can execute for users during login.

### 🔎 SOC Perspective

Unexpected scripts in `/etc/profile.d/` deserve investigation because they can provide system-wide login persistence.

---

# 15. Systemd Persistence

## 15.1 System Services

```bash
systemctl list-unit-files --type=service | grep enabled
```

Investigate:

- Unknown services
- Odd service names
- Recently created services
- Recently enabled services
- Services executing from unusual directories

---

## 15.2 User Services

```bash
systemctl --user list-unit-files
```

User-level systemd services can provide persistence without requiring system-wide administrative configuration.

### 🔎 SOC Perspective

Pay attention to user services that:

- Execute scripts from temporary directories
- Have unusual names
- Execute unexpected binaries
- Appear recently

---

# 16. SSH Persistence & Configuration

## 16.1 Inspect Authorized Keys

```bash
sudo cat /home/<user>/.ssh/authorized_keys 2>/dev/null
```

SSH authorized keys allow key-based authentication.

### 🔎 SOC Perspective

During an investigation, verify:

- Which keys are present
- Which account owns them
- Whether the keys are expected
- Whether a key was recently added
- Whether the associated account should have SSH access

An unknown authorized key can be an important persistence indicator.

---

## 16.2 Inspect SSH Configuration

```bash
sudo cat /etc/ssh/sshd_config
```

Review settings related to:

- Root login
- Password authentication
- Key-based authentication
- Authentication retries
- Maximum sessions

The lab demonstrates configurations where SSH key authentication and password authentication are enabled and where root SSH login is permitted.

### 🔎 SOC Perspective

SSH configuration should be evaluated together with:

```text
authorized_keys
+
auth.log
+
journalctl
+
user accounts
```

This gives a broader picture of SSH access and potential persistence.

---

# 17. SOC Investigation Workflow

When investigating a suspicious Linux host, correlate multiple artifacts instead of relying on one command.

A practical workflow from the concepts in this lab:

```text
                ┌──────────────────┐
                │ Suspicious Alert │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Identify User    │
                │ / Account        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Processes &      │
                │ Services         │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Authentication   │
                │ & System Logs    │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │ Persistence │       │ Web Logs    │
       │ Cron/systemd│       │ Apache      │
       └──────┬──────┘       └──────┬──────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                ┌──────────────────┐
                │ Suspicious Files │
                │ / Binaries       │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Build Timeline & │
                │ Assess Activity  │
                └──────────────────┘
```

---

# 18. Quick Command Reference

| Investigation | Command |
|---|---|
| List users | `cat /etc/passwd` |
| List groups | `cat /etc/group` |
| Check account status | `grep <user> /etc/shadow` |
| Password policy | `cat /etc/login.defs` |
| PAM password config | `cat /etc/pam.d/common-password` |
| Running processes | `ps aux` |
| Process details | `ps -p $PID -o pid,ppid,user,cmd` |
| Executable path | `readlink -f /proc/$PID/exe` |
| Find process | `ps aux \| grep -i <name>` |
| Running services | `systemctl list-units --type=service --state=running` |
| Service details | `systemctl status <service>` |
| Enabled services | `systemctl list-unit-files --type=service \| grep enabled` |
| Root cron | `sudo crontab -l` |
| User cron | `crontab -l` |
| Authentication logs | `sudo tail -n 100 /var/log/auth.log` |
| Failed events | `sudo grep -i "Failed" /var/log/auth.log` |
| Sudo events | `sudo grep -i "sudo" /var/log/auth.log` |
| SSH journal | `sudo journalctl -u ssh` |
| System log | `cat /var/log/syslog` |
| Kernel log | `cat /var/log/kern.log` |
| Apache logs | `ls -la /var/log/apache2/` |
| Apache 404s | `sudo grep " 404 " /var/log/apache2/access.log` |
| Unowned files | `sudo find / -xdev -nouser -o -nogroup 2>/dev/null` |
| Executables in temp | `sudo find /tmp /var/tmp /dev/shm -type f -perm /111 -ls 2>/dev/null` |
| Recent binaries | `sudo find /bin /sbin /usr/bin /usr/sbin /usr/local/bin -type f -mtime -15 -ls` |
| SUID binaries | `sudo find / -xdev -perm -4000 -type f -ls 2>/dev/null` |
| Recent risky files | `sudo find /etc /var /tmp /dev/shm -type f -mtime -3 -ls` |
| Inspect `.bashrc` | `cat /home/<user>/.bashrc` |
| Inspect `.profile` | `cat /home/<user>/.profile` |
| Bash history | `cat /home/<user>/.bash_history` |
| Hidden files | `find /home/<user> -type f -name ".*"` |
| Login scripts | `cat /etc/profile` |
| Profile scripts | `ls -la /etc/profile.d/` |
| User systemd units | `systemctl --user list-unit-files` |
| SSH keys | `sudo cat /home/<user>/.ssh/authorized_keys` |
| SSH configuration | `sudo cat /etc/ssh/sshd_config` |

---

# 19. Key Takeaways

### 👤 Identity

Know who exists on the system, what groups they belong to, and whether their accounts can obtain interactive sessions.

### ⚙️ Processes & Services

A process name alone is not enough. Investigate its PID, parent process, user, command line, executable path, and associated service.

### 📝 Logs

Authentication, systemd, kernel, system, and Apache logs provide different pieces of the investigation.

### 🔁 Persistence

Check:

```text
cron
systemd
.bashrc
.profile
/etc/profile
/etc/profile.d/
SSH authorized_keys
```

### 🕵️ Suspicious Artifacts

Pay particular attention to:

```text
/tmp
/var/tmp
/dev/shm
unexpected SUID binaries
recently modified system binaries
unowned files
unknown services
unknown SSH keys
```

### 🌐 Web Investigation

Apache access logs can reveal patterns such as:

```text
Repeated 404 requests
Directory/resource enumeration
Command-injection indicators
Path-traversal indicators
```

---

# 20. Final SOC Mindset

A single suspicious artifact does not automatically prove compromise.

Instead, correlate:

```text
ACCOUNT
   +
PROCESS
   +
SERVICE
   +
LOG
   +
PERSISTENCE
   +
FILE
   +
NETWORK/WEB ACTIVITY
   =
INVESTIGATION TIMELINE
```

The core skill demonstrated by this lab is **host-based visibility**: understanding how Linux records users, processes, services, authentication activity, persistence mechanisms, and filesystem changes so that a SOC analyst can investigate suspicious activity systematically.

---

## 🖼️ Suggested Screenshots

Add your lab screenshots under the relevant sections:

```markdown
![Users and Groups](images/users-groups.png)

![Process Investigation](images/process-investigation.png)

![Running Services](images/services.png)

![Cron Jobs](images/cron.png)

![Authentication Logs](images/auth-log.png)

![Apache Access Logs](images/apache-access.png)

![Suspicious Files](images/suspicious-files.png)

![SUID Binaries](images/suid.png)

![SSH Configuration](images/ssh-config.png)
```

---

## 🏁 Lab Status

**SOC-1: Linux Essentials — COMPLETED ✅**

Topics covered:

- [x] User & Account Management
- [x] Authentication Controls
- [x] Process Investigation
- [x] Service Investigation
- [x] Cron & Scheduled Tasks
- [x] Linux Logging
- [x] Apache Logging
- [x] Suspicious File Detection
- [x] SUID Investigation
- [x] Startup Persistence
- [x] SSH Persistence & Configuration
