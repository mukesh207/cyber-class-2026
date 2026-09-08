# DNS Enumeration Lab --- Detailed Walkthrough

## 1. Lab Overview

**Lab:** DNS Enumeration\
**Platform:** INE / Skill Dive\
**Category:** Network Pentesting / DNS Enumeration

### Objective

The objective of this lab was to use DNS enumeration tools to discover
as much information as possible about the domains configured on the
target DNS server.

The main tools used were:

-   `dnsenum`
-   `dnsrecon`
-   Metasploit `auxiliary/gather/enum_dns`

The lab environment provided a Kali machine and a target DNS server.

### Lab Network

From the lab machine:

```
Kali / Attacker: 192.203.203.2
DNS Target:      192.203.203.3
Gateway:         192.203.203.1
```

> **Important:** `192.203.203.1` was the gateway and was not the target.
> The enumeration was performed against `192.203.203.3`.

------------------------------------------------------------------------

# 2. Understanding DNS Enumeration

DNS (Domain Name System) translates domain names into IP addresses and
also stores different types of DNS records.

During enumeration, we can discover records such as:

  -----------------------------------------------------------------------
  Record                              Purpose
  ----------------------------------- -----------------------------------
  A                                   Maps a hostname to an IPv4 address

  NS                                  Identifies authoritative name
                                      servers

  MX                                  Identifies mail servers

  SOA                                 Contains authoritative zone
                                      information

  TXT                                 Stores text information and other
                                      metadata

  CNAME                               Alias from one hostname to another

  SRV                                 Identifies services and their ports

  AXFR                                DNS zone transfer; can expose the
                                      entire zone if misconfigured
  -----------------------------------------------------------------------

A particularly important finding in this lab was that the DNS server
allowed **zone transfers (AXFR)**.

------------------------------------------------------------------------

# 3. Step 1 --- Identify the Network Configuration

First, I checked the network interfaces on the lab Kali machine:

``` bash
ip a
```

The important interface was:

``` text
eth1
192.203.203.2/24
```

The target DNS server was:

``` text
192.203.203.3
```

I also checked the DNS resolver configuration:

``` bash
cat /etc/resolv.conf
```

It showed:

``` text
nameserver 192.203.203.3
```

This confirmed that the lab DNS server was being used for DNS queries.

------------------------------------------------------------------------

# 4. Step 2 --- Check DNS Tools

Before starting enumeration, I verified that the required tools were
installed.

### Check dnsenum

``` bash
which dnsenum
```

Output:

``` text
/usr/bin/dnsenum
```

### Check DNSRecon

``` bash
which dnsrecon
```

Output:

``` text
/usr/bin/dnsrecon
```

Both tools were available.

------------------------------------------------------------------------

# 5. Step 3 --- Reverse DNS Lookup

I performed a reverse DNS lookup against the target DNS server:

``` bash
dig -x 192.203.203.3
```

The response returned several hostnames associated with the target IP,
including:

``` text
ns3.witrapper.com
ns1.witrapper.com
promo.witrap.com
witrapper.com
public.witrap.com
witrap.com
ns2.witrapper.com
```

This was an important clue because it revealed the domains configured
around the DNS server.

The response also showed multiple name servers associated with
`witrapper.com`.

------------------------------------------------------------------------

# 6. Step 4 --- DNS Enumeration with dnsenum

The first main enumeration tool was `dnsenum`.

I started with:

``` bash
dnsenum witrapper.com
```

## Important Results

### Main domain

``` text
witrapper.com
192.203.203.3
```

### Name servers

``` text
ns1.witrapper.com
ns2.witrapper.com
ns3.witrapper.com
```

All three resolved to:

``` text
192.203.203.3
```

### Mail servers

Several MX records were discovered, including:

``` text
mx1.us.witrapper.com
mx2.sg.witrapper.com
mx3.sg.witrapper.com
mx4.ua.witrapper.com
mx5.ap.witrapper.com
mx6.ru.witrapper.com
mx7.uk.witrapper.com
```

### Interesting A records

The zone contained several useful hostnames:

``` text
admin.witrapper.com       192.203.203.101
internal.witrapper.com    192.203.203.100
ldap.witrapper.com        192.203.203.213
promo.witrapper.com       192.203.203.31
public.witrapper.com      192.203.203.30
reserved.witrapper.com    192.203.203.214
```

There were also records related to services such as SIP, SMB, LDAP and
Kerberos.

### CNAME records

Some aliases were discovered:

``` text
dev.witrapper.com   -> secondary.witrap.com
open.witrapper.com  -> free.witrap.com
prod.witrapper.com  -> primary.witrap.com
rsvd.witrapper.com  -> reserved.witrap.com
```

### Important TXT record

A particularly interesting TXT record was discovered:

``` text
secr3tAr3c0rd.witrapper.com
```

with the value:

``` text
Th!s_w4s_Th3_Secret_TXT_R3c0rd!
```

## Zone Transfer

The most important result from `dnsenum` was that **zone transfers were
successful** against the name servers.

This means the DNS server was incorrectly allowing an AXFR request.

A successful AXFR can expose a large amount of DNS information at once,
including:

-   Internal hostnames
-   Server names
-   IP addresses
-   Mail servers
-   Service records
-   Aliases
-   TXT records

------------------------------------------------------------------------

# 7. Step 5 --- DNSRecon Against witrapper.com

Next, I used DNSRecon with aggressive enumeration:

``` bash
dnsrecon -d witrapper.com -a
```

The `-a` option performs additional DNS enumeration, including
attempting zone transfers.

## Results

DNSRecon confirmed:

``` text
192.203.203.3 Has port 53 TCP Open
Zone Transfer was successful!!
```

The authoritative name servers included:

``` text
ns1.witrapper.com
ns2.witrapper.com
ns3.witrapper.com
```

The SOA record was:

``` text
witrapper.com SOA: ns1.witrapper.com
```

### TXT records

DNSRecon found:

``` text
Welcome to Witrapper.com - the parent company of witrap :)
```

and the secret TXT record:

``` text
Th!s_w4s_Th3_Secret_TXT_R3c0rd!
```

### Host records

DNSRecon confirmed hosts such as:

``` text
admin.witrapper.com       192.203.203.101
internal.witrapper.com    192.203.203.100
ldap.witrapper.com        192.203.203.213
promo.witrapper.com       192.203.203.31
public.witrapper.com      192.203.203.30
reserved.witrapper.com    192.203.203.214
```

It also discovered DNSSEC information and identified the DNS server as
running:

``` text
BIND 9.11.3-1ubuntu1.12-Ubuntu
```

------------------------------------------------------------------------

# 8. Step 6 --- Enumerate the Second Domain

The reverse lookup and previous enumeration revealed another domain:

``` text
witrap.com
```

I therefore ran:

``` bash
dnsrecon -d witrap.com -a
```

## Results

The zone transfer was again successful.

The name servers included:

``` text
ns1.witrapper.com
ns3.witrapper.com
```

The SOA record was:

``` text
ns1.witrapper.com
```

### TXT record

``` text
Welcome to Witrap.com!
```

### A records

DNSRecon discovered:

``` text
admin.witrap.com       192.203.203.41
training.witrap.com    192.203.203.40
public.witrap.com      192.203.203.3
info.witrap.com        192.203.203.43
static.witrap.com      192.203.203.44
demo.witrap.com        192.203.203.42
stats.witrap.com       192.203.203.44
```

Mail servers included:

``` text
mx1.us.witrap.com      192.203.203.200
mx3.us.witrap.com      192.203.203.201
```

A CNAME was also discovered:

``` text
labs.witrap.com -> witrapper.com
```

DNSRecon also reported a LOC record and indicated that DNSSEC was not
configured for `witrap.com`.

------------------------------------------------------------------------

# 9. Step 7 --- Metasploit DNS Enumeration

The final major tool required by the lab was Metasploit.

Start Metasploit:

``` bash
msfconsole -q
```

Load the DNS enumeration module:

``` text
use auxiliary/gather/enum_dns
```

Check the module options:

``` text
show options
```

The important options included:

``` text
DOMAIN
NS
ENUM_A
ENUM_AXFR
ENUM_CNAME
ENUM_MX
ENUM_NS
ENUM_SOA
ENUM_SRV
ENUM_TXT
ENUM_BRT
```

I configured the target DNS server:

``` text
setg NS 192.203.203.3
```

Then selected the first domain:

``` text
set DOMAIN witrap.com
```

and ran the module:

``` text
run
```

After that, I changed the domain:

``` text
set DOMAIN witrapper.com
```

and ran it again:

``` text
run
```

------------------------------------------------------------------------

# 10. Metasploit Results

Metasploit successfully queried the DNS server and returned records.

### NS records

``` text
witrapper.com NS: ns1.witrapper.com
witrapper.com NS: ns2.witrapper.com
witrapper.com NS: ns3.witrapper.com
```

### MX records

The module discovered multiple mail servers, including:

``` text
mx1.us.witrapper.com
mx2.sg.witrapper.com
mx3.sg.witrapper.com
mx4.ua.witrapper.com
mx6.ru.witrapper.com
mx7.uk.witrapper.com
```

### SOA

``` text
witrapper.com SOA: ns1.witrapper.com
```

### TXT

``` text
Welcome to Witrapper.com - the parent company of witrap :)
```

### SRV records

Metasploit discovered service records for:

``` text
Kerberos
LDAP
SIP
```

For example:

``` text
_ldap._tcp.witrapper.com
_sip._tcp.witrapper.com
```

### A records

Metasploit also confirmed:

``` text
admin.witrapper.com       192.203.203.101
internal.witrapper.com    192.203.203.100
ldap.witrapper.com        192.203.203.213
ns1.witrapper.com         192.203.203.3
ns2.witrapper.com         192.203.203.3
ns3.witrapper.com         192.203.203.3
promo.witrapper.com       192.203.203.31
public.witrapper.com      192.203.203.30
reserved.witrapper.com    192.203.203.214
```

The module finished with:

``` text
[*] Auxiliary module execution completed
```

This confirmed that Metasploit enumeration was successful.

------------------------------------------------------------------------

# 11. Step 8 --- Brute-Force Enumeration with Metasploit

I also performed the brute-force enumeration step.

Inside the Metasploit DNS enumeration module:

``` text
set ENUM_BRT true
```

Then:

``` text
set DOMAIN witrapper.com
```

Finally:

``` text
run
```

The module uses a default wordlist:

``` text
/usr/share/metasploit-framework/data/wordlists/namelist.txt
```

This attempts to discover additional subdomains and hostnames that may
not have been found through normal DNS record enumeration.

------------------------------------------------------------------------

# 12. Important Finding --- Zone Transfer

The biggest security issue identified during this lab was the successful
DNS zone transfer.

A normal DNS server should generally restrict AXFR requests to
authorized secondary DNS servers.

In this lab, the misconfiguration allowed the enumeration tools to
retrieve the zone.

Conceptually:

``` text
Attacker
   |
   | AXFR request
   v
DNS Server
   |
   | Full DNS zone
   v
Attacker
```

This exposed information such as:

``` text
Internal hosts
Server names
IP addresses
Mail servers
Service records
TXT records
Aliases
```

This demonstrates why DNS configuration is important from a security
perspective.

------------------------------------------------------------------------

# 13. Useful Manual Verification

The zone transfer can also be manually verified with `dig`.

For `witrapper.com`:

``` bash
dig @192.203.203.3 witrapper.com AXFR
```

For `witrap.com`:

``` bash
dig @192.203.203.3 witrap.com AXFR
```

These commands directly request a DNS zone transfer from the target DNS
server.

------------------------------------------------------------------------

# 14. Final Enumeration Summary

## Domains discovered

``` text
witrapper.com
witrap.com
```

## DNS server

``` text
192.203.203.3
```

## Name servers

``` text
ns1.witrapper.com
ns2.witrapper.com
ns3.witrapper.com
```

## Interesting hosts

``` text
admin.witrapper.com
internal.witrapper.com
ldap.witrapper.com
promo.witrapper.com
public.witrapper.com
reserved.witrapper.com
```

## Services discovered

``` text
Kerberos
LDAP
SIP
SMB
```

## Important DNS issue

``` text
Successful AXFR / Zone Transfer
```

## DNS server software

``` text
BIND 9.11.3-1ubuntu1.12-Ubuntu
```

## Interesting TXT record

``` text
Th!s_w4s_Th3_Secret_TXT_R3c0rd!
```

------------------------------------------------------------------------

# 15. Complete Command List

For quick revision, these were the main commands used:

``` bash
# Network information
ip a

# DNS resolver configuration
cat /etc/resolv.conf

# Check installed tools
which dnsenum
which dnsrecon

# Reverse DNS lookup
dig -x 192.203.203.3

# DNS enumeration
dnsenum witrapper.com

# DNSRecon
dnsrecon -d witrapper.com -a

# Enumerate second discovered domain
dnsrecon -d witrap.com -a

# Start Metasploit
msfconsole -q
```

Inside Metasploit:

``` text
use auxiliary/gather/enum_dns
show options
setg NS 192.203.203.3

set DOMAIN witrap.com
run

set DOMAIN witrapper.com
run

set ENUM_BRT true
set DOMAIN witrapper.com
run
```

Optional manual AXFR:

``` bash
dig @192.203.203.3 witrapper.com AXFR
dig @192.203.203.3 witrap.com AXFR
```

------------------------------------------------------------------------

# 16. What I Learned

### 1. DNS is valuable during reconnaissance

DNS can reveal much more than a domain's public IP address. Records can
expose:

-   Servers
-   Internal systems
-   Mail infrastructure
-   Network services
-   Subdomains
-   Aliases
-   Organizational information

### 2. Zone transfers can expose an entire DNS zone

A successful AXFR can provide a large amount of information without
needing to guess individual hostnames.

### 3. Multiple tools can validate the same finding

In this lab:

``` text
dnsenum
   ↓
DNSRecon
   ↓
Metasploit
```

All three approaches helped confirm the DNS information.

### 4. DNS records can reveal security-sensitive information

Records such as:

``` text
internal
admin
ldap
ad01
smb
```

can provide useful clues about the target's infrastructure.

### 5. Enumeration comes before exploitation

The lab demonstrates an important penetration-testing workflow:

``` text
Reconnaissance
      ↓
DNS Enumeration
      ↓
Identify Hosts / Services
      ↓
Analyze Attack Surface
      ↓
Further Testing
```

------------------------------------------------------------------------

# 17. Lab Completion

The INE lab displayed:

``` text
✓ Completed
```

The required DNS enumeration tasks were completed using:

``` text
dnsenum
DNSRecon
Metasploit auxiliary/gather/enum_dns
```

The lab successfully demonstrated DNS enumeration and the security
impact of an improperly configured DNS zone transfer.

------------------------------------------------------------------------

## Quick Revision

``` text
Target
192.203.203.3
        |
        v
Reverse DNS
        |
        v
Discover domains
        |
        +---- witrapper.com
        |
        +---- witrap.com
        |
        v
dnsenum
        |
        v
Zone Transfer successful
        |
        v
DNSRecon
        |
        v
Confirm records + AXFR
        |
        v
Metasploit enum_dns
        |
        v
NS / MX / SOA / TXT / SRV / A
        |
        v
Brute-force enumeration
        |
        v
LAB COMPLETED ✓
```

> **Practice note:** These commands should only be used against systems
> you own or have explicit permission to test, such as this authorized
> INE lab.
