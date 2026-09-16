# SOC-1: Linux Essentials — Detailed SOC Analyst Study Guide & Lab Walkthrough

> **Platform:** INE  
> **Lab:** SOC-1: Linux Essentials  
> **Environment:** Ubuntu-based Linux  
> **Focus:** Linux administration, investigation, logging, persistence, and suspicious artifact detection

---

## 🧭 How to Use This Guide

This document is designed to be more than a record of commands.

The goal is to understand **what you are checking, why you are checking it, what the output means, and what could make a finding suspicious** from a SOC analyst perspective.

For every investigation, keep this mental model:

```text
WHAT happened?
      ↓
WHO was involved?
      ↓
WHEN did it happen?
      ↓
WHERE did it happen?
      ↓
HOW was it executed?
      ↓
WHAT happened before and after?
```

> ⚠️ **Important:** A suspicious-looking artifact is not automatically malicious. Always correlate it with users, timestamps, processes, services, logs, files, and expected system behavior.

---

# 🎯 1. Learning Objectives

By completing this lab, you learn how to investigate a Linux host using several sources of host-based visibility:

- 👤 User and account management
- 👥 Linux groups and privileges
- 🔐 Authentication controls
- ⚙️ Processes and process ancestry
- 🔧 System services
- ⏰ Cron and scheduled tasks
- 📝 Authentication and system logs
- 🌐 Apache web-server logs
- 📁 Suspicious files and binaries
- 🔑 SUID binaries
- 🔄 Startup persistence
- 🖥️ Systemd persistence
- 🔐 SSH authorized keys and configuration

The bigger objective is to develop a **host-based investigation mindset** rather than memorizing commands.

---

# 👤 2. User & Account Management

## 2.1 Why Does a SOC Analyst Care About Users?

Before investigating activity on a Linux machine, you need to know **who can actually use the machine**.

An attacker who gains access may:

- Use an existing account
- Create a new account
- Modify an existing account
- Add an account to a privileged group
- Enable interactive access for a service account

Therefore, user enumeration is one of the first things to examine during a host investigation.

---

## 2.2 Linux Account Types

Linux commonly contains three categories of accounts:

| Account Type | Purpose |
|---|---|
| `root` | Superuser with unrestricted access |
| Local user | Regular interactive user account |
| System/service account | Used by services and background processes |

### 🧠 Think Like a SOC Analyst

Suppose you discover:

```text
backupadmin
```

Ask:

```text
Was this account expected?
Who created it?
When was it created?
Does it have sudo privileges?
Can it log in interactively?
Has it authenticated recently?
```

The username itself does not prove anything. **Context matters.**

---

## 2.3 Identify Users

### Command

```bash
cat /etc/passwd
```

### What does this do?

`/etc/passwd` contains information about local user accounts.

A typical entry follows this structure:

```text
username:x:UID:GID:comment:home_directory:login_shell
```

### Understanding Each Field

| Field | Meaning |
|---|---|
| `username` | Account name |
| `x` | Password information is stored separately |
| `UID` | User ID |
| `GID` | Primary group ID |
| `comment` | Account description |
| `home_directory` | User's home directory |
| `login_shell` | Shell used for login |

### Example

```text
john:x:1001:1001:John:/home/john:/bin/bash
```

This tells us that:

- Username → `john`
- UID → `1001`
- GID → `1001`
- Home → `/home/john`
- Shell → `/bin/bash`

---

## 2.4 Interactive vs Non-Interactive Shells

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

### Why is this useful?

A service account normally does not need an interactive shell.

For example:

```text
www-data:x:33:33:...:/var/www:/usr/sbin/nologin
```

would generally make sense for a web-service account.

If a service account unexpectedly has:

```text
/bin/bash
```

that is worth investigating.

> ⚠️ This is an **investigation indicator**, not proof of compromise.

---

## 🔎 SOC Investigation Checklist

When reviewing `/etc/passwd`, look for:

- Unexpected accounts
- Unexpected login shells
- Newly created users
- Privileged users
- Service accounts with interactive shells

---

# 👥 3. Linux Groups & Privileges

## 3.1 Identify Groups

### Command

```bash
cat /etc/group
```

A group entry follows:

```text
group_name:password:GID:members
```

Important groups discussed in this lab include:

| Group | Relevance |
|---|---|
| `sudo` | Users can execute commands with elevated privileges |
| `adm` | Access to system logs and monitoring files |
| `root` | Associated with the root user |
| `sys` | Legacy system group |

---

## 3.2 Why Groups Matter During an Investigation

Instead of asking only:

> "Who logged in?"

also ask:

> "What could this account do?"

Unexpected membership in a privileged group may indicate:

- Unauthorized account modification
- Privilege escalation
- Persistence
- Misconfiguration

### Investigation Example

```text
New user discovered
       ↓
Check groups
       ↓
User belongs to sudo
       ↓
Check authentication logs
       ↓
Check sudo activity
       ↓
Build timeline
```

This is much more useful than looking at the account in isolation.

---

# 🔐 4. Account Status & Authentication

## 4.1 Check Whether an Account Is Locked

### Command

```bash
grep <user_name> /etc/shadow
```

Example:

```bash
grep news /etc/shadow
```

A locked account starts with:

```text
!
```

### Why `/etc/shadow` Matters

`/etc/shadow` contains sensitive authentication information and normally requires elevated privileges.

From a SOC perspective, account status can provide useful context when investigating authentication activity.

For example:

```text
Account is locked
       +
Authentication events exist
       ↓
Investigate how and when those events occurred
```

---

# 🔑 5. Password & Authentication Controls

Linux authentication behavior is primarily controlled through files such as:

```text
/etc/login.defs
/etc/pam.d/common-password
```

---

## 5.1 Inspect Login Policy

### Command

```bash
cat /etc/login.defs
```

The lab highlights settings related to:

- Failed login logging
- Successful login logging
- Password aging
- Password expiration
- Login/session controls

### `FAILLOG_ENAB`

Relates to failed login tracking.

This can support investigations involving:

- Brute-force attempts
- Credential abuse

The lab also notes that legacy `FAILLOG_ENAB` tracking can conflict with PAM-based mechanisms such as `pam_faillock`.

### `LOG_UNKFAIL_ENAB`

Controls logging of failed attempts involving nonexistent users.

If logging is disabled, visibility into activity such as:

- Username enumeration
- Password spraying

may be reduced.

### `LOG_OK_LOGINS`

Relates to successful login logging.

Reduced successful-login visibility can make authentication investigations more difficult.

---

# 🧩 6. PAM Password Configuration

## 6.1 Inspect PAM Configuration

### Command

```bash
cat /etc/pam.d/common-password
```

The lab highlights:

```text
password [success=1 default=ignore] pam_unix.so obscure sha512
```

---

## 6.2 Understand the Configuration

### `pam_unix.so`

Handles local user password authentication and interacts with password hashes stored in:

```text
/etc/shadow
```

### `sha512`

The lab describes this configuration as using SHA-512 password hashing.

### `obscure`

Helps reject weak password patterns.

### PAM Control Flag

```text
[success=1 default=ignore]
```

The lab explains that successful execution causes PAM to skip the next module, while failure continues according to the configuration.

---

## 6.3 Password Complexity

The lab discusses:

```text
pam_pwquality.so
```

This module can enforce requirements such as:

- Password length
- Uppercase characters
- Lowercase characters
- Digits
- Special characters
- Prevention of weak passwords

### 🔎 SOC Perspective

Authentication configuration should be considered together with authentication logs.

A weak or poorly monitored authentication configuration can increase the impact of compromised credentials.

---

# ⚙️ 7. Process Investigation

Processes are one of the most important sources of information during Linux host investigation.

A process represents a running program.

The key question is not simply:

> "Is this process running?"

Instead ask:

```text
Who started it?
What is its PID?
What is its parent?
Which user owns it?
What command was executed?
Where is the executable?
What else is it doing?
```

---

## 7.1 List Running Processes

### Command

```bash
ps aux
```

This displays useful information including:

- PID
- User
- CPU usage
- Memory usage
- Command
- Process start information

### 🔎 What Should You Look For?

Look for:

- Unknown processes
- Processes unexpectedly running as `root`
- Suspicious command-line arguments
- Processes executing from unusual directories
- Unexpected network-related processes

---

## 7.2 Investigate a Specific Process

First obtain the PID.

Then:

```bash
ps -p $PID -o pid,ppid,user,cmd
```

Example:

```bash
ps -p 1234 -o pid,ppid,user,cmd
```

This provides:

| Field | Meaning |
|---|---|
| PID | Process ID |
| PPID | Parent Process ID |
| USER | Account running the process |
| CMD | Command used to start it |

---

## 7.3 Why PPID Matters

The parent process helps establish **process ancestry**.

For example:

```text
sshd
  ↓
bash
  ↓
python
  ↓
suspicious_script
```

The chain may tell you how a suspicious process was launched.

During an investigation, process ancestry can help connect an alert to its origin.

---

## 7.4 Identify the Executable Path

### Command

```bash
readlink -f /proc/$PID/exe
```

Example:

```bash
readlink -f /proc/1234/exe
```

### Why Is This Important?

A process name can look legitimate while its actual executable is somewhere unexpected.

For example:

```text
Process name: systemd-like-name
Executable: /tmp/something
```

The executable path provides another piece of evidence.

---

## 7.5 Filter Processes

```bash
ps aux | grep -i <process_name>
```

Example:

```bash
ps aux | grep -i ssh
```

> 💡 `grep` itself may appear in the results. Do not mistake the search command for the target process.

---

# 🔧 8. Service Investigation

Linux services can start automatically and run continuously in the background.

A malicious service can therefore become a persistence mechanism.

---

## 8.1 List Running Services

```bash
systemctl list-units --type=service --state=running
```

This displays active system services.

---

## 8.2 Inspect a Service

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

---

## 🔎 SOC Investigation

Investigate services that are:

- Unknown
- Unexpectedly enabled
- Recently created
- Executing from unusual locations
- Executing scripts from:
  - `/tmp`
  - `/dev/shm`
  - Hidden directories

### Investigation Flow

```text
Unknown service
      ↓
systemctl status
      ↓
Find PID / command
      ↓
Find executable path
      ↓
Check file timestamps
      ↓
Check related logs
      ↓
Build timeline
```

---

# ⏰ 9. Startup Persistence & Cron

Persistence means establishing a mechanism that causes code, commands, scripts, or binaries to execute automatically.

Cron is a legitimate scheduling mechanism that can also be abused for persistence.

---

## 9.1 Find Enabled Services

```bash
systemctl list-unit-files --type=service | grep enabled
```

Enabled services are configured to start automatically.

Look for:

- Oddly named services
- Recently enabled services
- Services executing suspicious scripts
- Executables in temporary directories
- Hidden or unusual paths

---

## 9.2 Inspect System Cron Jobs

Move to the cron directory:

```bash
cd /etc/cron.d/
```

Then:

```bash
ls -la /etc/cron.d/
```

Other system cron locations include:

```text
/etc/cron.hourly/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

These contain scheduled tasks that execute at corresponding intervals.

---

## 9.3 Inspect Current User's Cron

```bash
crontab -l
```

This lists cron jobs for the current user.

For root:

```bash
sudo crontab -l
```

### 🔎 What Makes a Cron Entry Worth Investigating?

Look for:

- Unexpected scripts
- Commands running from `/tmp`
- Commands running from `/dev/shm`
- Encoded or obfuscated commands
- Remote downloads
- Unknown binaries
- Recently added entries

> ⚠️ Cron is not malicious by itself. It is a legitimate Linux automation mechanism.

---

# 📝 10. Linux Authentication Logs

Logs are where separate observations can become a timeline.

---

## 10.1 Review Authentication Activity

```bash
sudo tail -n 100 /var/log/auth.log
```

The lab identifies this as a source for events such as:

- SSH login attempts
- Failed passwords
- Successful logins
- `sudo` activity
- `su` activity

---

## 10.2 Find Failed Events

```bash
sudo grep -i "Failed" /var/log/auth.log | tail -n 50
```

This can reveal failed authentication and other events containing the word `failed`.

### ⚠️ Investigation Note

Searching only for:

```text
Failed
```

can produce false positives because unrelated log messages or command strings may contain that word.

Therefore, always inspect the complete log entry and surrounding context.

---

## 10.3 Investigate a Specific User

```bash
sudo grep -i "Failed .* John" /var/log/auth.log | tail -n 50
```

This focuses on failed events associated with the specified username.

---

## 🔎 Authentication Investigation Model

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

The objective is to turn individual log entries into an **authentication timeline**.

---

# 🛡️ 11. Sudo Activity

### Command

```bash
sudo grep -i "sudo" /var/log/auth.log | tail -n 50
```

This can show:

- sudo session opening
- sudo session closing
- User executing sudo
- Command executed

### Questions for a SOC Analyst

When you see unexpected sudo activity:

1. Who executed sudo?
2. What command was executed?
3. When did it happen?
4. Was the user expected to have sudo privileges?
5. What happened immediately before it?
6. What happened immediately after it?

---

# 📖 12. journalctl & systemd Logs

## 12.1 View the Systemd Journal

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

## 12.2 Filter SSH Logs

```bash
sudo journalctl -u ssh
```

This filters journal entries associated with the SSH service.

---

## 12.3 Time-Based Investigation

When investigating an incident, time is extremely important.

Example:

```bash
sudo journalctl --since "1 hour ago"
```

You can also inspect a specific service:

```bash
sudo journalctl -u ssh
```

### 🧠 Timeline Thinking

If an alert occurred at:

```text
14:30
```

do not only inspect the exact event.

Look around the event:

```text
14:15 ─ suspicious login
14:18 ─ shell created
14:20 ─ sudo command
14:22 ─ file modified
14:25 ─ service started
14:30 ─ security alert
```

The relationships between these events are often more valuable than any single event.

---

# 🖥️ 13. General System Logs

## 13.1 Inspect syslog

```bash
cat /var/log/syslog
```

The lab describes `/var/log/syslog` as a general system log containing events such as:

- Service activity
- Daemon activity
- Network changes
- Cron executions

---

## 13.2 Inspect Kernel Logs

```bash
cat /var/log/kern.log
```

The lab highlights:

- Kernel boot events
- Hardware detection
- Driver initialization
- CPU-related information

### 🔎 SOC Perspective

Kernel logs can provide context when investigating unusual hardware, drivers, or system-level behavior.

---

# 🌐 14. Apache Web Server Logging

Web logs are especially useful when investigating attacks against a Linux web server.

They can help connect:

```text
Source IP
+
Timestamp
+
HTTP request
+
Status code
+
User agent
```

---

## 14.1 Locate Apache Logs

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

The lab also includes:

```text
access.log.bak
```

---

## 14.2 Review Recent Access Logs

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

Repeated `404` responses can be an indicator of reconnaissance activity.

> ⚠️ A single `404` is normal. The **pattern** is what matters.

---

## 14.3 Command Injection Indicator

The lab demonstrates:

```text
GET /?cmd=whoami HTTP/1.1" 200
```

This simulates a command-injection-related request.

### 🔎 Investigate the Context

Check:

- Source IP
- Timestamp
- HTTP status
- User agent
- Other requests from the same source

A suspicious request becomes much more meaningful when correlated with other activity.

---

## 14.4 Path Traversal Indicator

The lab demonstrates:

```text
GET /etc/passwd HTTP/1.1" 404
```

This is used to demonstrate a directory/path traversal attempt.

Again, the request should be treated as an **indicator requiring investigation**, rather than automatic proof of successful exploitation.

---

## 14.5 Review Apache Errors

```bash
sudo tail -n 20 /var/log/apache2/error.log
```

Error logs can show:

- Service startup
- Server errors
- Permission problems
- Access-control failures

---

## 14.6 Filter HTTP 404 Responses

```bash
sudo grep " 404 " /var/log/apache2/access.log | tail -n 20
```

This filters requests returning HTTP `404` responses.

Repeated requests may help identify:

- Automated enumeration
- Reconnaissance
- Probing for hidden resources

---

# 📁 15. Suspicious File Investigation

Files can provide evidence of:

- Persistence
- Malware execution
- Tampering
- Privilege escalation
- Unauthorized changes

The important idea is to search for **anomalies**, not simply files that look unfamiliar.

---

## 15.1 Find Files Without Owners

```bash
sudo find / -xdev -nouser -o -nogroup 2>/dev/null | head -n 50
```

This searches for files whose user or group ownership does not map to an existing account/group.

Possible investigation areas include:

- Deleted users
- Filesystem issues
- Tampering

---

## 15.2 Find Executables in Writable/Temporary Locations

```bash
sudo find /tmp /var/tmp /dev/shm -type f -perm /111 -ls 2>/dev/null
```

This searches for executable files in:

```text
/tmp
/var/tmp
/dev/shm
```

These locations can be relevant during malware and persistence investigations.

### 🔎 Why?

Temporary/shared-memory locations may contain files that are created during execution and may not belong to the normal software installation structure.

But remember:

> An executable in `/tmp` is suspicious context, not automatic proof of malware.

---

# 🕒 16. Recently Modified System Binaries

### Command

```bash
sudo find /bin /sbin /usr/bin /usr/sbin /usr/local/bin -type f -mtime -15 -ls 2>/dev/null | head -n 50
```

### What does `-mtime -15` mean?

It searches for files modified within the last 15 days.

### 🔎 What Should You Compare?

For a recently modified binary, compare it with:

- Package installation/update activity
- Change-management records
- File ownership
- Timestamps
- Known-good versions

The lab recommends adjusting the time window when repeating the exercise.

---

# 🔐 17. SUID Binary Investigation

## 17.1 Find SUID Binaries

```bash
sudo find / -xdev -perm -4000 -type f -ls 2>/dev/null | head -n 100
```

### What is SUID?

SUID allows an executable to run with the privileges associated with its owner.

This is important because SUID binaries can become relevant during privilege-escalation investigations.

### ⚠️ Important

Do **not** treat every SUID binary as malicious.

A normal Linux installation can contain legitimate SUID binaries.

Instead compare:

```text
Is it expected?
Where is it located?
Who owns it?
Was it recently added?
Was it recently modified?
Is the location unusual?
```

---

# 🕵️ 18. Recently Modified Files in Risky Locations

### Command

```bash
sudo find /etc /var /tmp /dev/shm -type f -mtime -3 -ls 2>/dev/null | head -n 100
```

`-mtime -3` identifies files modified within the last 3 days.

| Location | Investigation relevance |
|---|---|
| `/etc` | System/service configuration |
| `/var` | Logs, caches, spool data, cron-related data |
| `/tmp` | Temporary files |
| `/dev/shm` | Shared-memory filesystem |

### Investigation Question

If you discover a recently modified file:

```text
Who modified it?
What process modified it?
Why was it modified?
Was there a legitimate update?
Does the timestamp match another event?
```

---

# 🔄 19. Startup Persistence Inspection

Persistence is one of the most important concepts in host-based investigation.

An attacker may attempt to survive:

```text
logout
      ↓
reboot
      ↓
service restart
      ↓
new login
```

by placing commands in startup locations.

---

# 🐚 20. User-Level Shell Persistence

Inspect:

```bash
ls -la /home/<user>/.bashrc /home/<user>/.bash_history /home/<user>/.profile
```

Then:

```bash
cat /home/<user>/.bashrc
```

---

## 20.1 `.bashrc`

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

## 20.2 `.profile`

Inspect:

```bash
cat /home/<user>/.profile
```

`.profile` is associated with login-shell initialization.

It can execute commands when a user starts a login session.

---

## 20.3 Bash History

```bash
cat /home/<user>/.bash_history
```

History can contain:

- Commands executed by the user
- Investigation activity
- Privilege-escalation attempts
- Administrative commands

### ⚠️ Evidence Limitation

Command history is useful evidence, but it is **not a complete audit trail**.

Users or malware can modify or delete it.

Therefore:

```text
History ≠ complete truth
```

Correlate it with system and authentication logs.

---

# 👻 21. Hidden Files in Home Directories

## 21.1 List Hidden Files

```bash
ls -la /home/<user>/
```

---

## 21.2 Search for Hidden Regular Files

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

### 🧠 Key Lesson

Hidden does not automatically mean malicious.

Linux legitimately uses many hidden configuration files such as:

```text
.bashrc
.profile
.bash_history
```

The question is:

> **Is the file expected, and is its content expected?**

---

# 🖥️ 22. System-Level Persistence

## 22.1 Inspect `/etc/profile`

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

## 22.2 Inspect `/etc/profile.d`

```bash
ls -la /etc/profile.d/
```

Shell scripts placed here can execute for users during login.

### 🔎 SOC Perspective

Unexpected scripts in:

```text
/etc/profile.d/
```

deserve investigation because they can provide system-wide login persistence.

---

# ⚙️ 23. Systemd Persistence

## 23.1 System Services

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

## 23.2 User Services

```bash
systemctl --user list-unit-files
```

User-level systemd services can provide persistence without requiring system-wide administrative configuration.

Pay attention to user services that:

- Execute scripts from temporary directories
- Have unusual names
- Execute unexpected binaries
- Appear recently

---

# 🔐 24. SSH Persistence & Configuration

SSH is both a legitimate remote administration mechanism and an important area to investigate during a Linux incident.

---

## 24.1 Inspect Authorized Keys

```bash
sudo cat /home/<user>/.ssh/authorized_keys 2>/dev/null
```

SSH authorized keys allow key-based authentication.

### 🔎 What Should You Verify?

For every key, ask:

- Which key is this?
- Which account owns it?
- Is the key expected?
- Was it recently added?
- Should this account have SSH access?

An unknown authorized key can be an important persistence indicator.

---

## 24.2 Inspect SSH Configuration

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

### 🔎 Correlate SSH Evidence

Do not inspect `sshd_config` alone.

Combine:

```text
authorized_keys
      +
auth.log
      +
journalctl
      +
user accounts
```

This provides a broader picture of SSH access and potential persistence.

---

# 🧠 25. SOC Investigation Workflow

When investigating a suspicious Linux host, avoid relying on a single command.

A practical workflow from this lab is:

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
                 ┌────────┴────────┐
                 ▼                 ▼
          ┌─────────────┐    ┌─────────────┐
          │ Persistence │    │ Web Logs    │
          │ Cron/systemd│    │ Apache      │
          └──────┬──────┘    └──────┬──────┘
                 │                  │
                 └─────────┬────────┘
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

# 🧩 26. How to Think During an Investigation

Instead of memorizing:

```bash
ps aux
```

remember:

> **"I am checking what is running."**

Instead of memorizing:

```bash
crontab -l
```

remember:

> **"I am checking whether this user has scheduled tasks that could provide automation or persistence."**

Instead of memorizing:

```bash
sudo tail -n 100 /var/log/auth.log
```

remember:

> **"I am looking for authentication activity that can help me reconstruct who accessed the system."**

Instead of memorizing:

```bash
readlink -f /proc/$PID/exe
```

remember:

> **"I want to know which actual executable is behind this process."**

That mindset is more valuable than memorizing syntax.

---

# 🗂️ 27. Quick Command Reference

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
| Recent journal | `sudo journalctl --since "1 hour ago"` |
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

# 🧪 28. Analyst Practice Checklist

Use this section when revising the lab.

## 👤 Identity

- [ ] Can I identify Linux users?
- [ ] Do I understand UID and GID?
- [ ] Can I identify interactive shells?
- [ ] Can I identify suspicious group membership?
- [ ] Can I check account status?

## ⚙️ Processes

- [ ] Can I list running processes?
- [ ] Can I identify a process PID?
- [ ] Can I identify its parent process?
- [ ] Can I identify its executable path?
- [ ] Can I explain why process ancestry matters?

## 🔧 Services

- [ ] Can I list running services?
- [ ] Can I inspect a service?
- [ ] Can I identify enabled services?
- [ ] Can I recognize an unusual service as an investigation indicator?

## ⏰ Persistence

- [ ] Can I inspect user cron?
- [ ] Can I inspect root cron?
- [ ] Can I inspect `/etc/cron.d/`?
- [ ] Can I inspect `.bashrc` and `.profile`?
- [ ] Can I inspect `/etc/profile.d/`?
- [ ] Can I inspect systemd user services?
- [ ] Can I inspect SSH authorized keys?

## 📝 Logs

- [ ] Can I inspect `auth.log`?
- [ ] Can I search failed authentication?
- [ ] Can I identify sudo activity?
- [ ] Can I use `journalctl`?
- [ ] Can I filter SSH logs?
- [ ] Can I build a basic timeline?

## 🌐 Web Investigation

- [ ] Can I locate Apache logs?
- [ ] Can I identify repeated 404s?
- [ ] Can I recognize enumeration patterns?
- [ ] Can I recognize command-injection indicators?
- [ ] Can I recognize path-traversal indicators?

## 📁 Files

- [ ] Can I find unowned files?
- [ ] Can I search for executables in temporary locations?
- [ ] Can I find recently modified binaries?
- [ ] Can I find SUID binaries?
- [ ] Can I investigate recently modified files?

---

# 🧠 29. Key Takeaways

## 👤 Identity

Know:

```text
Who exists?
Who can log in?
Who has privileges?
Who has SSH access?
```

The lab emphasizes reviewing unexpected accounts, privileges, and interactive shells. 

## ⚙️ Processes & Services

A process name alone is not enough.

Investigate:

```text
PID
+
PPID
+
USER
+
COMMAND
+
EXECUTABLE PATH
+
SERVICE
```

---

## 📝 Logs

Different logs provide different pieces of the investigation:

```text
auth.log      → authentication activity
journalctl    → systemd/service/system events
syslog        → general system activity
kern.log      → kernel-level context
Apache logs   → web activity
```

---

## 🔁 Persistence

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

---

## 🕵️ Suspicious Artifacts

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

But remember:

> **Suspicious ≠ malicious. Correlation is required.**

---

## 🌐 Web Investigation

Apache access logs can reveal patterns such as:

```text
Repeated 404 requests
Directory/resource enumeration
Command-injection indicators
Path-traversal indicators
```

The useful evidence comes from correlating those requests with:

```text
Source IP
Timestamp
HTTP status
User agent
Other activity
```

---

# 🧭 30. Final SOC Mindset

The most important lesson from this lab is not a particular command.

It is the ability to connect multiple artifacts.

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
NETWORK / WEB ACTIVITY
   ↓
INVESTIGATION TIMELINE
```

A single artifact does not automatically prove compromise.

Instead, build a story:

```text
Who?
 ↓
What happened?
 ↓
When?
 ↓
How?
 ↓
What changed?
 ↓
What happened next?
```

The core skill demonstrated by this lab is **host-based visibility**: understanding how Linux records users, processes, services, authentication activity, persistence mechanisms, and filesystem changes so that a SOC analyst can investigate suspicious activity systematically.

---

# 🖼️ 31. Suggested Screenshots

Add your lab screenshots under the relevant sections.

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

### 📸 Recommended Screenshot Structure

For each screenshot, try to capture:

```text
┌───────────────────────────────────────┐
│ Command executed                     │
├───────────────────────────────────────┤
│                                       │
│ Terminal output / evidence            │
│                                       │
├───────────────────────────────────────┤
│ What the output means                │
└───────────────────────────────────────┘
```

This makes the GitHub documentation easier to study later.

---

# 🏁 32. Lab Status

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

---

# 📌 One-Page Mental Map

```text
                    LINUX SOC INVESTIGATION
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
     IDENTITY             EXECUTION             LOGGING
        │                     │                     │
  Users / Groups       Processes / Services   auth.log
  sudo privileges      PID / PPID             journalctl
  Shells               Executable path        syslog
                                              kern.log
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                         PERSISTENCE
                              │
          ┌───────────────┬───┴────┬───────────────┐
          ▼               ▼        ▼               ▼
        Cron           systemd   Shell files    SSH keys
                              │
                              ▼
                       FILE INVESTIGATION
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
          /tmp             SUID            Modified files
        /dev/shm          binaries         Unowned files
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                         WEB ACTIVITY
                              │
                       Apache access.log
                              │
                              ▼
                       CORRELATE EVENTS
                              │
                              ▼
                     BUILD TIMELINE
                              │
                              ▼
                     ASSESS ACTIVITY
```

> 🎯 **Core takeaway:** A SOC analyst does not investigate commands. A SOC analyst investigates **evidence and relationships between evidence**.
