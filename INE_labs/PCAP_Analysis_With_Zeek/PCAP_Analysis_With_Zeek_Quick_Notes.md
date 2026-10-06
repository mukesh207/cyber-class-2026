# PCAP Analysis With Zeek — Quick Notes

> **Goal:** Analyze malware PCAP files with **Zeek**, extract useful network evidence, and identify suspicious IPs, domains, users, files, and malware activity.

---

## 1. What is Zeek?

**Zeek** is a network security monitoring and traffic analysis tool.

Instead of looking at thousands of raw packets manually, Zeek reads a PCAP and creates useful logs such as:

| Log | Purpose |
|---|---|
| `conn.log` | Connections, IPs, ports, protocols |
| `dns.log` | DNS queries and answers |
| `http.log` | HTTP requests, URLs, User-Agent, files |
| `files.log` | Files seen in network traffic |
| `dhcp.log` | MAC addresses, hostnames, DHCP information |
| `kerberos.log` | Kerberos authentication activity |
| `ssl.log` | TLS/SSL information and server names |
| `x509.log` | Certificate information |

---

# 2. PCAP → Zeek Logs

### Technique
Convert raw packet traffic into structured Zeek logs.

### Command

```bash
zeek -Cr ~/Desktop/Investigation/Malware1/infected.pcap
```

### Remember

```text
PCAP → Zeek → Multiple logs
```

This makes the investigation much easier than manually reading packets.

---

# 3. Generate JSON Logs

### Technique
JSON makes Zeek logs easier to process with tools such as `jq`.

### Command

```bash
zeek -Cr ~/Desktop/Investigation/Malware1/infected.pcap LogAscii::use_json=T
```

### Why?

JSON is useful for:

- Filtering
- Searching
- Automation
- SIEM pipelines
- Script-based analysis

---

# 4. Read JSON With jq

### Technique
Pretty-print a JSON Zeek log.

### Command

```bash
jq . http.log
```

### Meaning

```text
jq . file
   │
   └── Display the JSON in readable format
```

---

# 5. Find Unique Destination IPs

### Technique
Identify IP addresses that the host communicated with.

### Command

```bash
cat conn.log | zeek-cut id.resp_h | sort | uniq
```

### Breakdown

```text
cat conn.log
     ↓
zeek-cut id.resp_h
     ↓
sort
     ↓
uniq
```

- `id.resp_h` = destination/responding host
- `sort` = sort the results
- `uniq` = remove duplicates

### SOC Use

Useful for finding:

- C2 servers
- Suspicious external IPs
- Malware infrastructure

---

# 6. Find HTTP Response MIME Types

### Technique
Determine what type of content was returned by HTTP servers.

### Command

```bash
cat http.log | zeek-cut resp_mime_types | sort | uniq
```

### Example

```text
application/ocsp-response
```

MIME types can help identify:

- Documents
- Executables
- Images
- Scripts
- API responses

---

# 7. Search HTTP Requests

### Technique
Search HTTP logs for a specific domain.

### Command

```bash
cat http.log | grep ocsp.digicert.com
```

### SOC Use

Useful when investigating:

- Known IOCs
- Suspicious domains
- Malware callbacks
- Download locations

---

# 8. Find the User-Agent

### Technique
Identify the application/browser that generated the HTTP request.

### Command

```bash
jq . json/http.log | grep user_agent
```

### Example

```text
Microsoft-CryptoAPI/10.0
```

### Why?

A User-Agent can help identify:

- Browser/application
- Malware communication
- Unusual software
- Automated requests

---

# 9. Find Cobalt Strike Infrastructure

### Technique
Use TLS/SSL logs to identify suspicious domain names.

### Command

```bash
cat ssl.log | zeek-cut server_name | sort | uniq
```

Then search DNS:

```bash
cat dns.log | grep ceyuvigi.com
```

### Lab Finding

```text
Domain: ceyuvigi.com
IP:     23.108.57.213
```

### SOC Concept

```text
SSL/TLS → Domain
DNS     → IP
IP      → IOC
```

This is useful for connecting a suspicious domain to its resolved IP address.

---

# 10. Find Bumblebee C2 Traffic

### Technique
Search connection logs for a known IOC.

### Command

```bash
cat conn.log | grep 139.177.146.137
```

### Lab Finding

```text
Bumblebee C2: 139.177.146.137
```

### SOC Concept

If an IOC is provided:

```text
IOC → Search Zeek logs → Find matching traffic → Investigate
```

---

# 11. Find a Client MAC Address

### Technique
Use DHCP logs to connect an IP address with a MAC address.

### Command

```bash
cat dhcp.log | zeek-cut mac client_addr
```

### Lab Finding

```text
172.17.1.129
        ↓
00:1e:67:4a:d7:5c
```

### Why?

Useful for identifying the physical/network device associated with an IP.

---

# 12. Find the Hostname

### Technique
Use DHCP information to identify the machine name.

### Command

```bash
cat dhcp.log | zeek-cut client_addr host_name | sort | uniq
```

### Lab Finding

```text
Nalyvaiko-PC
```

---

# 13. Find the Windows User

### Technique
Use Kerberos traffic to identify the authenticated user.

### Command

```bash
cat kerberos.log | zeek-cut id.orig_h client service | awk '$3~"krbtgt"' | grep -vi nalyvaiko-pc
```

### Lab Finding

```text
innochka.nalyvaiko
```

### SOC Concept

Kerberos traffic can provide useful evidence about:

- User accounts
- Authentication
- Domain activity
- Possible lateral movement

---

# 14. Find Downloaded Word Documents

### Technique

First identify Word documents in `files.log`.

### Command

```bash
cat files.log | zeek-cut mime_type filename | grep msword
```

Then search `http.log` for the filename:

```bash
cat http.log | zeek-cut ts id.orig_h id.resp_h method host uri resp_filenames | grep "2018_11Details_zur_Transaktion.doc"
```

### Lab Finding

```text
ifcingenieria.cl/QpX8It/BIZ/Firmenkunden/
```

### Investigation Method

```text
files.log
   ↓
Find suspicious filename
   ↓
http.log
   ↓
Find URL
```

---

# 15. Find Executable Downloads

### Technique
Search HTTP traffic for Windows executable MIME types and file size.

### Command

```bash
cat http.log | zeek-cut -d ts method host uri resp_filenames resp_mime_types response_body_len | awk '$6=="application/x-dosexec"'
```

### Lab Finding

```text
URL:  timlinger.com/nmw/6169583.exe
Size: 429056 bytes
```

### Important Fields

| Field | Meaning |
|---|---|
| `method` | HTTP method |
| `host` | Web server |
| `uri` | Requested path |
| `resp_filenames` | Returned filename |
| `resp_mime_types` | Returned file type |
| `response_body_len` | Response size |

---

# 16. Malware Identification

The lab contains two major malware investigations.

### Malware 1

```text
Bumblebee
   ↓
C2 communication
   ↓
Cobalt Strike
   ↓
Post-exploitation activity
```

Important IOCs:

```text
ceyuvigi.com
23.108.57.213
139.177.146.137
```

### Malware 2

```text
Phishing
   ↓
Malicious Word document
   ↓
Emotet infection
   ↓
Executable download
```

The lab identifies the infection as:

```text
Phishing — Emotet Campaign
```

---

# 17. The SOC Investigation Workflow

When given an unknown malware PCAP, follow this order:

```text
             PCAP
               │
               ▼
          Run Zeek
               │
               ▼
      ┌────────┼────────┐
      ▼        ▼        ▼
    conn      DNS      HTTP
      │        │        │
      ▼        ▼        ▼
     IPs     Domains   URLs
                        │
                        ▼
                  files.log
                        │
                        ▼
                Downloaded files
                        │
                        ▼
                 Malware / IOC
```

---

# 18. Quick Command Cheat Sheet

```bash
# PCAP → Zeek logs
zeek -Cr infected.pcap

# PCAP → JSON logs
zeek -Cr infected.pcap LogAscii::use_json=T

# Read JSON
jq . http.log

# Unique destination IPs
cat conn.log | zeek-cut id.resp_h | sort | uniq

# HTTP MIME types
cat http.log | zeek-cut resp_mime_types | sort | uniq

# Search HTTP traffic
cat http.log | grep "domain.com"

# User-Agent
jq . json/http.log | grep user_agent

# DNS investigation
cat dns.log | grep "domain.com"

# TLS server names
cat ssl.log | zeek-cut server_name | sort | uniq

# DHCP / MAC / hostname
cat dhcp.log | zeek-cut mac client_addr host_name

# Kerberos users
cat kerberos.log | zeek-cut id.orig_h client service

# Files
cat files.log | zeek-cut mime_type filename

# Search for an executable
cat http.log | zeek-cut method host uri resp_filenames resp_mime_types response_body_len | \
awk '$5=="application/x-dosexec"'
```

---

# 19. Key Techniques to Remember

| Technique | Main Log |
|---|---|
| Find communicating IPs | `conn.log` |
| Find DNS/domain activity | `dns.log` |
| Investigate web traffic | `http.log` |
| Find downloaded files | `files.log` |
| Find MAC/hostname | `dhcp.log` |
| Investigate Windows authentication | `kerberos.log` |
| Find TLS domains | `ssl.log` |
| Parse JSON | `jq` |
| Extract Zeek fields | `zeek-cut` |
| Search known IOCs | `grep` |
| Remove duplicates | `sort \| uniq` |
| Filter complex results | `awk` |

---

# 20. One-Line Mental Model

> **Zeek turns PCAP into searchable evidence.**

Remember:

```text
PCAP
 ↓
Zeek
 ↓
Logs
 ↓
Filter
 ↓
IOC
 ↓
Investigate
 ↓
Identify Malware
```

## References

- Zeek: https://zeek.org/
- Zeek Documentation: https://docs.zeek.org/
- Malware Traffic Analysis: https://www.malware-traffic-analysis.net/
