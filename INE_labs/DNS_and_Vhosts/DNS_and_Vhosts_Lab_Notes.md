# DNS and Vhosts --- INE / AttackDefense Lab

## Lab Objective

Learn DNS enumeration and identify multiple websites hosted on the same
web server using name-based virtual hosting.

**Lab network discovered:**

``` text
Kali        → 192.2.51.2
Web Server  → 192.2.51.3
DNS Server  → 192.2.51.4
Gateway     → 192.2.51.1  (Do not attack)
```

------------------------------------------------------------------------

## 1. Find the Kali IP

Command:

``` bash
ip a
```

Result:

``` text
eth1 → 192.2.51.2/24
```

Therefore:

``` text
X = 2
Y = 51
```

The lab targets become:

``` text
Web  = 192.2.51.3
DNS  = 192.2.51.4
```

------------------------------------------------------------------------

## 2. Enumerate the DNS Server

TCP:

``` bash
nmap -sV -p 53 192.2.51.4
```

Result:

``` text
53/tcp open domain ISC BIND 9.11.3
```

UDP:

``` bash
nmap -sU -p 53 192.2.51.4
```

Result:

``` text
53/udp open domain
```

**Lesson:** DNS commonly uses port 53 over UDP and can also use TCP.

------------------------------------------------------------------------

## 3. Initial DNS Queries

Commands tried:

``` bash
dig @192.2.51.4 ANY
dig @192.2.51.4 SOA
dig @192.2.51.4 NS
```

These returned `SERVFAIL` and did not reveal the useful domain
information.

The useful discovery came from reverse DNS.

------------------------------------------------------------------------

## 4. Reverse DNS Enumeration

Target web server:

``` text
192.2.51.3
```

Command:

``` bash
dig -x 192.2.51.3 +short
```

Result:

``` text
public.witrap.com.
promo.witrap.com.
witrap.com.
witrapper.com.
```

We discovered four domain names associated with the web server.

### Normal DNS vs Reverse DNS

``` text
Normal DNS:
Domain → IP

Reverse DNS:
IP → Domain
```

------------------------------------------------------------------------

## 5. DNS Zone Transfer / AXFR

The lab DNS server was intentionally misconfigured to allow zone
transfers.

General syntax:

``` bash
dig axfr <domain> @<dns-server>
```

Examples:

``` bash
dig axfr public.witrap.com @192.2.51.4
dig axfr promo.witrap.com @192.2.51.4
dig axfr witrapper.com @192.2.51.4
```

`public.witrap.com` failed, while `promo.witrap.com` succeeded.

The important transfer was:

``` bash
dig axfr witrapper.com @192.2.51.4
```

It returned about **95 records**.

### Save the result

``` bash
dig axfr witrapper.com @192.2.51.4 | tee witrapper-zone.txt
```

### Extract A records

``` bash
grep -E '\sIN\s+A\s+' witrapper-zone.txt
```

Cleaner:

``` bash
grep -E '\sIN\s+A\s+' witrapper-zone.txt | awk '{print $1, $5}'
```

Some discovered records included:

``` text
witrapper.com                  → 192.2.51.3
admin.witrapper.com            → 192.2.51.101
free.witrapper.com             → 192.2.51.210
internal.witrapper.com         → 192.2.51.100
ldap.witrapper.com             → 192.2.51.213
ns1.witrapper.com              → 192.2.51.5
ns3.witrapper.com              → 192.2.51.4
primary.witrapper.com          → 192.2.51.211
promo.witrapper.com            → 192.2.51.31
public.witrapper.com           → 192.2.51.30
reserved.witrapper.com         → 192.2.51.214
secondary.witrapper.com        → 192.2.51.212
secr3t-4-r3c0rd.witrapper.com  → 192.2.51.225
```

### Security lesson

An unrestricted AXFR can expose:

-   Hostnames
-   IP addresses
-   Nameservers
-   Mail servers
-   Internal infrastructure
-   Other DNS records

------------------------------------------------------------------------

## 6. Enumerate the Web Server

Scan:

``` bash
nmap -sV -p 80,443 192.2.51.3
```

HTTP headers:

``` bash
curl -I http://192.2.51.3
```

The server responded with Apache:

``` text
Apache/2.4.7 (Ubuntu)
```

The default page displayed:

``` text
Hello world!
```

------------------------------------------------------------------------

## 7. Understand Name-Based Virtual Hosting

The important concept of the lab is **name-based virtual hosting**.

One IP can host multiple websites:

``` text
                    192.2.51.3
                         |
                  Apache Web Server
                         |
                    Host Header
                         |
       +-----------------+-----------------+
       |                 |                 |
       ↓                 ↓                 ↓
  witrap.com       witrapper.com     promo.witrap.com
       |                 |                 |
   Website A          Website B          Website C
```

The browser/request sends a hostname using the HTTP `Host` header.

Example:

``` bash
curl -H "Host: example.com" http://192.2.51.3
```

This lets us test a particular virtual host without relying on public
DNS resolution.

------------------------------------------------------------------------

## 8. Test the Four Vhosts

### witrap.com

``` bash
curl -s -H "Host: witrap.com" http://192.2.51.3 | grep -i '<title>'
```

Result:

``` html
<title>Witrap.com - Unavailable</title>
```

### public.witrap.com

``` bash
curl -s -H "Host: public.witrap.com" http://192.2.51.3 | grep -i '<title>'
```

Result:

``` html
<title>Hello world!</title>
```

### witrapper.com

``` bash
curl -s -H "Host: witrapper.com" http://192.2.51.3 | grep -i '<title>'
```

Result:

``` html
<title>Course Server - Login</title>
```

It also redirected to:

``` text
/login.php
```

### promo.witrap.com

``` bash
curl -s -H "Host: promo.witrap.com" http://192.2.51.3 | grep -i '<title>'
```

Result:

``` html
<title>Witrap.com - Promo</title>
```

------------------------------------------------------------------------

## 9. Test All Four at Once

``` bash
for h in witrap.com public.witrap.com witrapper.com promo.witrap.com; do
    echo "===== $h ====="
    curl -s -H "Host: $h" http://192.2.51.3 | grep -i '<title>'
done
```

Observed:

``` text
===== witrap.com =====
<title>Witrap.com - Unavailable</title>

===== public.witrap.com =====
<title>Hello world!</title>

===== witrapper.com =====
<title>Course Server - Login</title>

===== promo.witrap.com =====
<title>Witrap.com - Promo</title>
```

This proves that different websites are being served from the same web
server depending on the requested hostname.

------------------------------------------------------------------------

# 10. What About login.php?

`witrapper.com` redirected to:

``` text
/login.php
```

The page contained a login form and JavaScript password hashing.

The application also displayed a database access error:

``` text
Tutor was unable to access the database.
```

For this particular lab, **do not continue into password attacks or
login bypasses**.

The official walkthrough ends after demonstrating the four different
websites and explaining that they are name-based virtual hosts.

------------------------------------------------------------------------

# 11. Complete Lab Workflow

``` text
ip a
  ↓
192.2.51.2
  ↓
Determine targets
  ↓
Web: 192.2.51.3
DNS: 192.2.51.4
  ↓
Nmap DNS
  ↓
BIND discovered
  ↓
Reverse DNS
  ↓
Four domains discovered
  ↓
AXFR / Zone Transfer
  ↓
DNS records exposed
  ↓
Web enumeration
  ↓
Host-header testing
  ↓
Four virtual hosts confirmed
  ↓
LAB COMPLETE
```

------------------------------------------------------------------------

# 12. Key Concepts

## DNS

**DNS = Domain Name System**

Maps names to IP addresses:

``` text
example.com → 192.168.1.10
```

## Reverse DNS

Maps an IP back to a hostname:

``` text
192.168.1.10 → example.com
```

Command:

``` bash
dig -x 192.168.1.10 +short
```

## AXFR

AXFR is a DNS zone-transfer mechanism.

Command:

``` bash
dig axfr example.com @192.168.1.1
```

If improperly restricted, it can disclose the DNS zone.

## Virtual Host

Multiple websites can share one IP:

``` text
192.2.51.3
├── witrap.com
├── public.witrap.com
├── witrapper.com
└── promo.witrap.com
```

## Host Header

The HTTP `Host` header tells the web server which virtual host is being
requested:

``` bash
curl -H "Host: witrap.com" http://192.2.51.3
```

------------------------------------------------------------------------

# 13. Command Cheat Sheet

``` bash
# Find IP
ip a

# Scan DNS
nmap -sV -p 53 192.2.51.4
nmap -sU -p 53 192.2.51.4

# Reverse DNS
dig -x 192.2.51.3
dig -x 192.2.51.3 +short

# Zone transfer
dig axfr witrapper.com @192.2.51.4

# Save zone
dig axfr witrapper.com @192.2.51.4 | tee witrapper-zone.txt

# Extract A records
grep -E '\sIN\s+A\s+' witrapper-zone.txt

# Web scan
nmap -sV -p 80,443 192.2.51.3

# HTTP headers
curl -I http://192.2.51.3

# Test vhost
curl -H "Host: witrap.com" http://192.2.51.3

# Extract title
curl -s -H "Host: witrap.com" http://192.2.51.3 | grep -i '<title>'
```

------------------------------------------------------------------------

# 14. What I Learned

-   How to identify the attacker/Kali IP address.
-   How to identify a DNS server with Nmap.
-   DNS uses port 53.
-   How to perform reverse DNS with `dig`.
-   How reverse DNS can reveal multiple domains.
-   What a DNS zone transfer (AXFR) is.
-   How a misconfigured DNS server can expose DNS records.
-   How to save and filter DNS enumeration results.
-   How Apache can host multiple websites on one IP.
-   How the HTTP `Host` header selects a name-based virtual host.
-   How to verify virtual hosts with `curl`.

------------------------------------------------------------------------

# 15. Lab Completion Checklist

``` text
[✓] Kali IP identified
[✓] Web server identified
[✓] DNS server identified
[✓] DNS service enumerated
[✓] Reverse DNS performed
[✓] Four domains discovered
[✓] AXFR successfully tested
[✓] DNS records extracted
[✓] Web server enumerated
[✓] Virtual hosts tested
[✓] Four different websites confirmed
[✓] Lab completed
```

## Final Takeaway

The main lesson is:

``` text
DNS Enumeration
      ↓
Domain Discovery
      ↓
Virtual Host Discovery
      ↓
Web Application Identification
```

**One IP address does not necessarily mean one website.**

The official walkthrough states that the four domains display different
pages even though they map to the same IP because they are served using
**name-based virtual hosts on a single server**.
