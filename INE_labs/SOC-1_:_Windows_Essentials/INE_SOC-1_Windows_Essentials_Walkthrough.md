# INE SOC-1: Windows Essentials --- Simple Walkthrough

## 1. Introduction

This lab introduces important Windows administration and security
concepts that are useful for a SOC analyst.

The main areas covered are:

-   User and account management
-   Windows groups and privileges
-   Password and account lockout policies
-   Process and service investigation
-   Startup folders
-   Task Scheduler
-   Windows Event Viewer
-   Windows Security logs
-   Sysmon logs
-   PowerShell commands
-   Windows Registry basics
-   Registry-based persistence

The main idea is simple:

> A SOC analyst needs to know how Windows normally works so suspicious
> activity can be identified.

------------------------------------------------------------------------

# 2. User & Account Management

## 2.1 Windows Account Types

Windows supports different types of accounts.

### Local User Account

A local account exists only on the individual Windows machine.

### Administrator Account

An administrator has extensive control over the system.

Administrators can:

-   Install and remove software
-   Change system settings
-   Manage users and groups
-   Access system files

### Service Account

Service accounts are used by services and applications.

------------------------------------------------------------------------

## 2.2 View Local Users

We can use the **Local Users and Groups** console to inspect local
accounts.

### Open it

Press:

``` text
Win + R
```

Type:

``` text
lusrmgr.msc
```

Press **Enter**.

Then navigate to:

``` text
Local Users and Groups
└── Users
```

Here we can see the local users on the machine.

### SOC perspective

When investigating a Windows machine, look for:

-   Unexpected accounts
-   Unknown accounts
-   Accounts that should not exist
-   Accounts with suspicious privileges

------------------------------------------------------------------------

## 2.3 View Local Groups

In the same console, navigate to:

``` text
Local Users and Groups
└── Groups
```

This displays the local groups.

Important groups include:

### Administrators

The most powerful built-in group.

Members have extensive control over the system.

### Remote Desktop Users

Members can connect to the system using Remote Desktop Protocol (RDP).

### Remote Management Users

These users can perform certain remote management activities using
technologies such as WinRM and PowerShell Remoting.

### Users

The standard group for normal user accounts.

### Backup Operators

Members can perform backup and restore operations and can access files
that may normally be restricted.

------------------------------------------------------------------------

## 2.4 Check Whether an Account Is Disabled

To check an account:

1.  Open `lusrmgr.msc`
2.  Go to **Users**
3.  Right-click the user
4.  Select **Properties**
5.  Check whether **Account is disabled** is selected

In the lab, the `student` account is shown as **not disabled**.

------------------------------------------------------------------------

# 3. Password Policy

Password policies determine how strong Windows passwords must be.

## 3.1 Open Password Policy

Press:

``` text
Win + R
```

Type:

``` text
secpol.msc
```

Press **Enter**.

Navigate to:

``` text
Local Security Policy
└── Account Policies
    └── Password Policy
```

Here we can inspect the configured password policies.

------------------------------------------------------------------------

## 3.2 What to Look For

Important password settings include:

-   Minimum password length
-   Password complexity requirements
-   Maximum password age
-   Minimum password age

In the lab, the password policy is intentionally very weak.

The minimum password length is configured as:

``` text
0 characters
```

This means blank passwords can potentially be created.

Password complexity is also disabled.

The maximum and minimum password ages are both configured as:

``` text
0 days
```

This means passwords do not expire.

### Security impact

Weak password policies increase the risk of:

-   Password guessing
-   Credential attacks
-   Brute-force attacks
-   Long-term use of compromised passwords

### Security recommendation

Use strong password policies with:

-   Appropriate minimum password length
-   Password complexity requirements
-   Suitable password lifetime policies

------------------------------------------------------------------------

# 4. Account Lockout Policy

Account lockout policies help protect against repeated failed login
attempts.

## 4.1 Open Account Lockout Policy

Open:

``` text
secpol.msc
```

Navigate to:

``` text
Local Security Policy
└── Account Policies
    └── Account Lockout Policy
```

------------------------------------------------------------------------

## 4.2 Account Lockout Threshold

The lab shows:

``` text
Account lockout threshold = 0
```

A value of `0` means accounts will not be locked out because of failed
login attempts.

### Security impact

An attacker can repeatedly attempt passwords without triggering account
lockout.

This increases exposure to:

-   Password guessing
-   Brute-force attacks
-   Repeated login attempts

### Security recommendation

Configure an appropriate account lockout policy so repeated failed
authentication attempts trigger a defensive response.

------------------------------------------------------------------------

# 5. Process Investigation

Processes are programs currently running on the Windows system.

A SOC analyst may investigate processes to identify suspicious or
unexpected activity.

## 5.1 Open Task Manager

Press:

``` text
Ctrl + Shift + Esc
```

This opens **Task Manager**.

Task Manager provides information about:

-   Running processes
-   CPU usage
-   Memory usage
-   Users
-   Process IDs

------------------------------------------------------------------------

## 5.2 View Process Details

Go to the **Details** section.

You can inspect:

-   Process name
-   PID
-   CPU/resource usage
-   User name

### What is PID?

PID means:

``` text
Process ID
```

It is a unique identifier assigned to a running process.

------------------------------------------------------------------------

## 5.3 Inspect Process Properties

Right-click a process and select **Properties**.

You can inspect information such as:

-   File location
-   File properties
-   Digital signature

### SOC perspective

When investigating a suspicious process, ask:

1.  What is the process?
2.  Who started it?
3.  What user is running it?
4.  Where is the executable located?
5.  Is it digitally signed?
6.  Does the location make sense?
7.  Is the process expected?

------------------------------------------------------------------------

# 6. Windows Services

Windows services are background components that perform different system
and application functions.

## 6.1 Open Services

Press:

``` text
Win + R
```

Type:

``` text
services.msc
```

Press **Enter**.

This displays Windows services and their:

-   Status
-   Startup type

------------------------------------------------------------------------

## 6.2 Service Startup Types

### Automatic

The service starts automatically during system boot.

### Automatic (Delayed Start)

The service starts automatically, but after the system has finished the
initial boot process.

### Manual

The service does not automatically start during boot.

It can start when required by Windows, an application, or an
administrator.

### Disabled

The service cannot start until it is enabled again.

------------------------------------------------------------------------

## 6.3 SOC Investigation

Suspicious services can sometimes be used for persistence.

When investigating a service, check:

-   Service name
-   Display name
-   Startup type
-   Running status
-   Executable path
-   Account used to run the service

------------------------------------------------------------------------

# 7. Startup Folder

Windows has startup folders that can automatically launch programs when
a user logs in.

## 7.1 Open Startup Folder

Press:

``` text
Win + R
```

Type:

``` text
shell:startup
```

Press **Enter**.

------------------------------------------------------------------------

## 7.2 Why Startup Folders Matter to a SOC Analyst

Startup folders are legitimate Windows functionality.

However, attackers can abuse them for persistence.

For example, a malicious program placed in a startup folder could
execute automatically when the user logs in.

There are:

-   User-specific startup locations
-   System-wide startup locations

### SOC investigation

Look for:

-   Unknown executables
-   Suspicious scripts
-   Unexpected shortcuts
-   Recently added startup items

------------------------------------------------------------------------

# 8. Task Scheduler

Windows Task Scheduler allows programs or commands to run automatically
based on triggers.

## 8.1 Open Task Scheduler

Press:

``` text
Win + R
```

Type:

``` text
taskschd.msc
```

Press **Enter**.

------------------------------------------------------------------------

## 8.2 Inspect Existing Tasks

Navigate through:

``` text
Task Scheduler Library
└── Microsoft
    └── Windows
```

Tasks can have different triggers, such as:

-   System startup
-   User logon
-   Time-based schedules
-   Other system events

------------------------------------------------------------------------

## 8.3 Create a Scheduled Task

Click:

``` text
Create Task
```

The task configuration contains several important sections.

### General

Used to configure:

-   Task name
-   Description
-   User/security context
-   Whether the user must be logged in

### Triggers

Defines:

-   When the task starts
-   How often it runs
-   What event triggers it

### Actions

Defines:

-   Program to execute
-   Script to execute
-   Arguments

### Conditions

Defines conditions under which the task should run.

For example:

``` text
Run only if the computer is idle
```

------------------------------------------------------------------------

## 8.4 SOC Perspective

Scheduled tasks are legitimate administrative features but can also be
abused for persistence.

Investigate:

-   Unknown task names
-   Tasks running unusual programs
-   Tasks created recently
-   Tasks triggered at suspicious times
-   Tasks executing scripts from unusual locations

------------------------------------------------------------------------

# 9. Windows Logging & Event Viewer

Windows does not automatically log every possible security event.

Auditing needs to be configured so important security activity can be
monitored.

Examples include:

-   Logon activity
-   Account changes
-   Security group changes
-   Process creation

------------------------------------------------------------------------

# 10. Audit Policy

## 10.1 Open Local Security Policy

Press:

``` text
Win + R
```

Type:

``` text
secpol.msc
```

Press **Enter**.

Navigate to:

``` text
Local Policies
└── Audit Policy
```

------------------------------------------------------------------------

## 10.2 Advanced Audit Policy

The more detailed auditing configuration is available under:

``` text
Security Settings
└── Advanced Audit Policy Configuration
    └── Audit Policies
```

Advanced Audit Policy provides more detailed control over security
auditing.

It can include specific activities such as:

-   Credential validation
-   Logon events
-   Privilege use
-   Process creation
-   File access

------------------------------------------------------------------------

## 10.3 Important Audit Categories

For this lab, enable **Success and Failure** for important categories
such as:

-   Logon / Authentication
-   Credential Validation
-   User Account Management
-   Security Group Management

This provides better visibility during security investigations.

------------------------------------------------------------------------

# 11. Event Viewer

## 11.1 Open Event Viewer

Press:

``` text
Win + R
```

Type:

``` text
eventvwr.msc
```

Press **Enter**.

------------------------------------------------------------------------

## 11.2 Windows Logs

Navigate to:

``` text
Event Viewer
└── Windows Logs
```

Important logs include:

-   Application
-   Security
-   System

------------------------------------------------------------------------

# 12. Security Event Logs

Open:

``` text
Windows Logs
└── Security
```

The Security log contains security-related events.

## Important Event IDs

  Event ID   Meaning
  ---------- ----------------------------------------------
  `4624`     Successful logon
  `4625`     Failed logon
  `4720`     User account created
  `4732`     User added to a security-enabled local group
  `4634`     Logoff

------------------------------------------------------------------------

## 12.1 Event ID 4720 --- New User

Event ID:

``` text
4720
```

indicates that a new user account was created.

In the lab example:

-   The account was created by `Administrator`
-   The new account was `John123`

### SOC question

If you see a new account being created, investigate:

``` text
Who created it?
When was it created?
Why was it created?
What privileges does it have?
Was the account expected?
```

------------------------------------------------------------------------

## 12.2 Event ID 4624 --- Successful Logon

Event ID:

``` text
4624
```

indicates a successful logon.

The event contains information about the account involved in the login.

------------------------------------------------------------------------

## 12.3 Event ID 4732 --- User Added to Group

Event ID:

``` text
4732
```

indicates that an account was added to a security-enabled local group.

The event can show:

-   Account that performed the action
-   User that was added
-   Target group

### SOC importance

Adding an account to a privileged group can increase its permissions.

------------------------------------------------------------------------

## 12.4 Event ID 4634 --- Logoff

Event ID:

``` text
4634
```

indicates that an account logged off.

The event can help establish when a session ended.

------------------------------------------------------------------------

# 13. Application Logs

Navigate to:

``` text
Windows Logs
└── Application
```

Application logs contain events generated by applications and services.

They can contain:

-   Information events
-   Warnings
-   Errors
-   Application crashes

These logs can help investigate application problems and abnormal
behavior.

------------------------------------------------------------------------

# 14. System Logs

Navigate to:

``` text
Windows Logs
└── System
```

System logs can contain information related to:

-   System startup
-   System shutdown
-   Services
-   System components

------------------------------------------------------------------------

## Important System Events

### Event ID 7045

Indicates that a new service was created or installed.

This can be important during an investigation because attackers may
abuse services for persistence.

### Event ID 6006

Indicates that the Windows Event Log service was stopped.

This commonly occurs during a clean system shutdown or restart.

------------------------------------------------------------------------

# 15. Sysmon

Sysmon is a Microsoft Sysinternals system monitoring component that
provides detailed security telemetry.

Open:

``` text
Applications and Services Logs
└── Microsoft
    └── Windows
        └── Sysmon
            └── Operational
```

------------------------------------------------------------------------

## Important Sysmon Events

### Sysmon Event ID 1 --- Process Creation

Logged when a new process is created.

Useful for investigating:

-   Malware execution
-   Suspicious programs
-   Unexpected processes

### Sysmon Event ID 6 --- Driver Loaded

Logged when a kernel-mode driver is loaded.

Useful for investigating suspicious or unsigned drivers.

### Sysmon Event ID 22 --- DNS Query

Logged when a process performs a DNS query.

Useful for investigating:

-   Suspicious domains
-   Malware communications
-   Unusual network activity

------------------------------------------------------------------------

# 16. Filtering Event Logs

Large Windows logs can contain thousands of events.

Instead of manually checking everything, filter the log.

## 16.1 Filter Current Log

Right-click a log and select:

``` text
Filter Current Log
```

You can filter based on:

-   Event ID
-   Time range
-   Event level
-   User
-   Task category

------------------------------------------------------------------------

## 16.2 Example: Find New User Accounts

Filter the Security log using:

``` text
Event ID: 4720
```

This displays events related to user account creation.

------------------------------------------------------------------------

# 17. PowerShell Essentials

PowerShell is extremely useful for Windows administration and SOC
investigation.

------------------------------------------------------------------------

## 17.1 List Local Users

``` powershell
Get-LocalUser
```

This displays local user accounts.

Use it to identify unexpected accounts.

------------------------------------------------------------------------

## 17.2 List Local Groups

``` powershell
Get-LocalGroup
```

This displays local security groups.

------------------------------------------------------------------------

## 17.3 Check Group Membership

``` powershell
Get-LocalGroupMember <group_name>
```

Example:

``` powershell
Get-LocalGroupMember Administrators
```

This helps identify which accounts have membership in a group.

------------------------------------------------------------------------

## 17.4 List Running Processes

``` powershell
Get-Process
```

This displays currently running processes.

------------------------------------------------------------------------

## 17.5 Find a Specific Process

``` powershell
Get-Process -Name "<process-name>"
```

Replace `<process-name>` with the process you want to investigate.

------------------------------------------------------------------------

## 17.6 List Services

``` powershell
Get-Service
```

This displays Windows services and their current states.

------------------------------------------------------------------------

## 17.7 Find a Specific Service

``` powershell
Get-Service -Name "<service_name>"
```

------------------------------------------------------------------------

## 17.8 Get Detailed Service Information

``` powershell
Get-CimInstance Win32_Service |
Where-Object {$_.Name -eq "<service_name>"} |
Select-Object Name, DisplayName, State, StartMode, StartName, PathName
```

This can show:

-   Service name
-   Display name
-   State
-   Startup mode
-   Account used to run the service
-   Executable path

------------------------------------------------------------------------

# 18. Scheduled Tasks with PowerShell

## List All Scheduled Tasks

``` powershell
Get-ScheduledTask
```

------------------------------------------------------------------------

## Search Tasks by Name

Example:

``` powershell
Get-ScheduledTask |
Where-Object {$_.TaskName -like "*update*"}
```

This searches for tasks containing:

``` text
update
```

in their task name.

### SOC perspective

A task called something like `Update` is not automatically malicious.

Always investigate the task's:

-   Action
-   Trigger
-   Author
-   Executable path
-   Creation/modification details

------------------------------------------------------------------------

# 19. List Windows Event Logs

Use:

``` powershell
Get-WinEvent -ListLog *
```

This lists the Event Logs available on the system.

------------------------------------------------------------------------

# 20. Search Security Events with PowerShell

## Find User Creation Events

Use:

``` powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4720} -MaxEvents 20 |
Select-Object TimeCreated, Id, ProviderName, Message
```

### What it does

The command:

1.  Searches the `Security` log
2.  Looks for Event ID `4720`
3.  Limits the result to 20 events
4.  Displays:
    -   Time
    -   Event ID
    -   Provider
    -   Event message

This is useful when investigating newly created accounts.

------------------------------------------------------------------------

# 21. Search Logons for a Specific Account

The lab demonstrates searching for successful logons for the
`administrator` account.

``` powershell
Get-WinEvent -LogName Security -FilterXPath "*[System[(EventID=4624)]] and *[EventData[Data[@Name='TargetUserName']='administrator']]" |
Select-Object TimeCreated, Id, Message
```

This searches for:

``` text
Event ID = 4624
TargetUserName = administrator
```

It can help build a timeline of successful logons for a particular
account.

------------------------------------------------------------------------

# 22. Windows Registry Basics

The Windows Registry is a hierarchical database used by Windows and
applications.

It stores information such as:

-   System configuration
-   User settings
-   Application behavior
-   Security settings
-   Startup configuration

------------------------------------------------------------------------

# 23. Open Registry Editor

Press:

``` text
Win + R
```

Type:

``` text
regedit
```

Press **Enter**.

------------------------------------------------------------------------

# 24. Important Registry Hives

  Hive                           Purpose
  ------------------------------ --------------------------
  `HKEY_LOCAL_MACHINE (HKLM)`    System-wide settings
  `HKEY_CURRENT_USER (HKCU)`     Current user's settings
  `HKEY_USERS (HKU)`             Loaded user profiles
  `HKEY_CLASSES_ROOT (HKCR)`     File associations
  `HKEY_CURRENT_CONFIG (HKCC)`   Current hardware profile

------------------------------------------------------------------------

# 25. Registry Data Types

## REG_SZ

String value.

Commonly used for:

-   File paths
-   Commands
-   Text configuration

## REG_DWORD

32-bit numeric value.

Often used for:

-   Enable/disable settings
-   Numeric configuration

## REG_BINARY

Binary data.

## REG_MULTI_SZ

Multiple string values.

Often used for lists of paths or strings.

------------------------------------------------------------------------

# 26. Registry Run Keys

Run keys are Registry locations that can automatically start programs
when Windows starts or when a user logs in.

They are legitimate Windows functionality.

However, attackers can abuse them for persistence.

------------------------------------------------------------------------

## 26.1 HKCU Run Key

``` text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

Programs stored here run in the context of the current user.

------------------------------------------------------------------------

## 26.2 HKLM Run Key

``` text
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
```

This affects users more broadly and generally requires higher privileges
to modify.

------------------------------------------------------------------------

## 26.3 RunOnce

Related Registry keys such as `RunOnce` can execute a program once
during the next logon.

------------------------------------------------------------------------

# 27. Check Autoruns Using PowerShell

To inspect the system-wide Run key:

``` powershell
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
```

Look for:

-   Unknown programs
-   Suspicious paths
-   Unexpected scripts
-   Recently added entries

Do not assume that every unknown entry is malicious. Investigate the
executable and its location.

------------------------------------------------------------------------

# 28. Inspect a Windows Service in the Registry

First list services:

``` powershell
Get-Service
```

Then inspect a specific service:

``` powershell
Get-Item "HKLM:\SYSTEM\CurrentControlSet\Services\<ServiceName>"
```

Replace:

``` text
<ServiceName>
```

with the actual service name.

------------------------------------------------------------------------

# 29. SOC Investigation Mindset

The most important lesson from this lab is not simply memorizing
commands.

When investigating a Windows host, build a timeline.

For example:

``` text
1. A new account is created
        ↓
2. The account is added to a privileged group
        ↓
3. A suspicious service is created
        ↓
4. A scheduled task is created
        ↓
5. A suspicious process starts
        ↓
6. The process performs DNS queries
```

Each individual event might have a legitimate explanation.

But when multiple suspicious events occur close together, they can form
a much stronger indication of malicious activity.

------------------------------------------------------------------------

# 30. Quick SOC Cheat Sheet

## GUI Tools

  Purpose                 Command
  ----------------------- ----------------------
  Local Users & Groups    `lusrmgr.msc`
  Local Security Policy   `secpol.msc`
  Services                `services.msc`
  Startup Folder          `shell:startup`
  Task Scheduler          `taskschd.msc`
  Event Viewer            `eventvwr.msc`
  Registry Editor         `regedit`
  Task Manager            `Ctrl + Shift + Esc`

------------------------------------------------------------------------

## Important Event IDs

``` text
4624 → Successful logon
4625 → Failed logon
4634 → Logoff
4720 → User account created
4732 → User added to local security group
7045 → New service created/installed
6006 → Event Log service stopped
```

### Sysmon

``` text
1  → Process creation
6  → Driver loaded
22 → DNS query
```

------------------------------------------------------------------------

## Important PowerShell Commands

``` powershell
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember Administrators

Get-Process
Get-Service

Get-ScheduledTask
Get-WinEvent -ListLog *

Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"
```

------------------------------------------------------------------------

# 31. Final Takeaway

The **Windows Essentials** lab gives a foundation for Windows-based SOC
investigations.

The key areas to remember are:

-   **Users** → Who has access?
-   **Groups** → What privileges do they have?
-   **Processes** → What is running?
-   **Services** → What runs in the background?
-   **Startup items** → What starts automatically?
-   **Scheduled Tasks** → What executes automatically?
-   **Event Logs** → What happened?
-   **Sysmon** → What detailed activity occurred?
-   **PowerShell** → How can we investigate quickly?
-   **Registry** → What configuration and persistence mechanisms exist?

A good SOC analyst connects these pieces together instead of
investigating each one in isolation.

> **Know what normal Windows activity looks like, then investigate what
> doesn't fit.**
