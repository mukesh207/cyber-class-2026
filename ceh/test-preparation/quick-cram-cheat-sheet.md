# ⚡ CEH v13 Quick-Cram Exam Day Cheat Sheet

A concise, high-yield reference guide summarizing core formulas, protocol ports, CLI syntax, and technical matrices tested in CEH v13 (Modules 01 & 02).

---

## 📐 1. Quantitative Risk & Impact Formulas

$$\text{SLE} = \text{AV} \times \text{EF}$$
$$\text{ALE} = \text{SLE} \times \text{ARO} = (\text{AV} \times \text{EF}) \times \text{ARO}$$

- **AV (Asset Value):** Financial value of the asset in dollars.
- **EF (Exposure Factor):** Percentage of asset lost during an incident ($0.0 \text{ to } 1.0$).
- **SLE (Single Loss Expectancy):** Dollar amount lost in a single realization of the threat.
- **ARO (Annualized Rate of Occurrence):** Frequency of the incident per year (e.g., once every 2 years = $0.5$).
- **ALE (Annualized Loss Expectancy):** Expected annual financial loss.

### The Attack & Risk Formulas
$$\text{Attack} = \text{Motive (Goal)} + \text{Method (Skill/Exploit)} + \text{Vulnerability (Weakness)}$$
$$\text{Risk} = \text{Threat} \times \text{Vulnerability} \times \text{Impact}$$

### The 4 T's of Risk Management
1. **Tolerate (Accept):** Accept risk when cost of mitigation exceeds potential loss.
2. **Terminate (Avoid):** Eliminate the risky activity, asset, or business service.
3. **Treat (Mitigate):** Deploy security controls (firewalls, patching, MFA).
4. **Transfer (Share):** Shift financial impact to a third party (Cyber Insurance).

---

## 🔌 2. High-Yield Reconnaissance & Protocol Ports

| Port | Protocol | Service / Exam Significance |
| :---: | :---: | :--- |
| **43** | TCP | **WHOIS** — Registry and registrar query protocol. |
| **53** | UDP / TCP | **DNS** — Standard queries over UDP/53; **Zone Transfers (AXFR)** over TCP/53. |
| **67 / 68** | UDP | **DHCP** — Server (67) and Client (68). |
| **69** | UDP | **TFTP** — Trivial FTP (no authentication; cleartext). |
| **80** | TCP | **HTTP** — Web traffic; used in TCP traceroute. |
| **161 / 162** | UDP | **SNMP** — Queries on 161, Traps on 162 (target for community strings). |
| **389 / 636** | TCP | **LDAP / LDAPS** — Active Directory directory services. |
| **443** | TCP | **HTTPS** — TLS encrypted web traffic; used for `tcptraceroute` through firewalls. |
| **445** | TCP | **SMB** — Server Message Block (file sharing, null sessions). |
| **502** | TCP | **Modbus** — Industrial Control Systems (ICS/SCADA) queried via Shodan. |
| **5060 / 5061** | TCP/UDP | **SIP / SIPS** — VoIP signaling servers identified in SRV records. |

---

## 🌐 3. The 11 DNS Record Types Quick Matrix

| Record | Name | Core Technical Function & Attack Value |
| :---: | :--- | :--- |
| **A** | Host Address (IPv4) | Maps hostname to 32-bit IPv4 address. |
| **AAAA**| Host Address (IPv6) | Maps hostname to 128-bit IPv6 address (often bypasses IPv4 firewall rules). |
| **MX** | Mail Exchange | Identifies mail gateways with priority preference (lowest number = highest priority). |
| **NS** | Name Server | Authoritative nameservers governing the zone; target of AXFR. |
| **CNAME**| Canonical Name | Alias mapping. Risk: **Subdomain Takeover** if cloud endpoint deleted. |
| **SOA** | Start of Authority | Zone admin email, primary NS, Serial (`YYYYMMDDNN`), Refresh, Retry, Expire, Min TTL. |
| **SRV** | Service Locator | Maps specific services to hosts & ports (`_service._proto.domain Priority Weight Port Target`). |
| **PTR** | Pointer Record | Reverse DNS (`in-addr.arpa`) mapping IP to hostname. |
| **RP** | Responsible Person | Discloses administrative email and pointer to contact TXT record. |
| **HINFO**| Host Information | Discloses CPU and OS type (historical security leak; disabled on modern systems). |
| **TXT** | Text Strings | Anti-spoofing policies (**SPF**, **DKIM**, **DMARC**) and domain ownership tokens. |

---

## ✉️ 4. Email Security Trio (SPF, DKIM, DMARC)

```
+-----------------------------------------------------------------------------------+
| SPF Qualifiers  | +all (Pass Any - Spoofable) | ~all (SoftFail) | -all (HardFail) |
+-----------------+-----------------------------------------------------------------+
| DKIM Mechanics  | Private key signs email -> Public key published in TXT at       |
|                 | <selector>._domainkey.target.com verifies signature.            |
+-----------------+-----------------------------------------------------------------+
| DMARC Policies  | p=none (Monitor only) | p=quarantine (Spam) | p=reject (Drop)   |
+-----------------+-----------------------------------------------------------------+
```

---

## 🛠️ 5. Essential Command Flags Cheat Sheet

```bash
# DNS Zone Transfer (AXFR) over TCP 53
dig axfr @<Authoritative-NS> <Target-Domain>

# DNS Reverse Lookup
dig -x <Target-IP> +short

# Trace DNS Resolution Path from Root (.) down
dig <Target-Domain> +trace

# Query Specific RIR for Netblock Ownership
whois -h whois.arin.net <Target-IP>

# TCP Traceroute through Stateful Perimeter Firewall to HTTPS
traceroute -T -p 443 <Target-Domain>

# Strip HTML and harvest emails from web text via Lynx
lynx -dump https://<Target-Domain> | grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b"

# Harvest public emails, subdomains, and hosts
theHarvester -d <Target-Domain> -b google,bing,crtsh -l 500
```

---

## 🔍 6. 24 Specialized Search Engines Matrix (Quick-Match)

| Need / Target Asset | Primary Specialized Search Engine |
| :--- | :--- |
| Exposed IoT, SCADA (Modbus 502), IP Cams, Port Banners | **Shodan** |
| Certificate & TLS attack surface mapping | **Censys** |
| Global cyberspace assets / Asian internet perimeter | **FOFA** / **ZoomEye** |
| Hardcoded secrets & API keys in GitHub public repos | **Grep.app** / **Searchcode** |
| Shared Google Analytics IDs (`UA-XXXXX`) or JS widgets | **PublicWWW** |
| Corporate employee email formats and names | **Hunter.io** |
| Worldwide wireless access points & GPS mapping | **WiGLE** |
| Leaked breach data, paste sites, historical WHOIS | **Intelligence X (IntelX)** / **DeHashed** |
| Certificate Transparency (CT) logs for subdomains | **crt.sh** |
| Live DOM rendering, web cookies, outbound connections | **URLScan.io** |
| Distinguishing targeted scans from internet background noise | **GreyNoise** |
| Exposed Docker daemons, open `.git`, Elasticsearch leaks | **LeakIX** / **BinaryEdge** |

---

*Navigation:* [🏠 CEH Master Hub](../README.md) | [📝 Practice Questions](./mod-01-and-02-practice-questions.md)
