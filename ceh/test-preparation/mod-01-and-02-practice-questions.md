# 📝 CEH v13 High-Yield Practice Exam: Modules 01 & 02

**Domain Focus:** Information Security Fundamentals, Frameworks, AI in Pentesting, Passive & Active Footprinting, DNS Interrogation, Network/Email Forensics, and Threat Mitigation.

> [!TIP]
> **Study Instructions:** Attempt each question independently before expanding the explanation. Analyze the question for qualifiers (**FIRST**, **BEST**, **LEAST**, **MOST**) and practice eliminating distractors systematically.

---

### Question 1
An ethical hacker has been engaged to conduct a black-box penetration test against an enterprise organization. Before generating any network traffic toward the client's public IP range, the tester queries public Certificate Transparency (CT) logs using `crt.sh`. What specific technical intelligence is the tester attempting to harvest?

- [ ] A) Internal Active Directory user accounts
- [ ] B) Subdomains and wildcard certificates issued for the target domain
- [ ] C) Exposed cleartext passwords from historical database breaches
- [ ] D) The primary master authoritative DNS server's private RFC 1918 IP

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** Certificate Transparency (CT) logs are publicly auditable logs where Certificate Authorities (CAs) append every issued TLS/SSL certificate. Querying CT logs (e.g., via `crt.sh/?q=%.target.com`) allows a tester to passively enumerate active and historical subdomains (e.g., `vpn.target.com`, `dev-api.target.com`) without sending a single packet to the target organization's infrastructure.
- **Why A is incorrect:** CT logs only record cryptographic certificate issuance metadata, not Active Directory identity objects.
- **Why C is incorrect:** Breached credentials are found on paste sites and breach search engines (e.g., DeHashed, IntelX), not in CA logs.
- **Why D is incorrect:** CT logs display public domain names; internal master DNS servers are uncovered via SOA records or internal zone transfers.
</details>

---

### Question 2
During a reconnaissance engagement, a tester executes the following command:
```bash
dig axfr @ns1.globex.com globex.com
```
The server responds with:
```text
; Transfer failed.
;; WARNING: recursion requested but not available
;; Transfer failed: REFUSED
```
What does this response indicate, and what is the tester's **BEST** next step?

- [ ] A) The nameserver is offline; re-run the query using UDP port 53.
- [ ] B) The domain does not exist; verify the target domain spelling.
- [ ] C) AXFR is restricted on `ns1`; repeat the zone transfer attempt against all remaining authoritative nameservers for the domain.
- [ ] D) The target is running DNSSEC; execute an NSEC zone walk immediately.

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **C**

**Technical Rationale:**
- **Why C is correct:** The `REFUSED` code means the nameserver software received the request over TCP port 53 but an Access Control List (ACL) blocked the zone transfer. However, organizations frequently configure secondary nameservers (e.g., `ns2.globex.com`, `ns3.globex.com`) inconsistently. The tester must query every identified NS record before concluding zone transfers are completely blocked.
- **Why A is incorrect:** Zone transfers (AXFR) require TCP port 53 due to data volume; switching to UDP will not bypass an ACL.
- **Why B is incorrect:** If the domain did not exist, the server would return `NXDOMAIN`, not `REFUSED`.
- **Why D is incorrect:** While NSEC walking is valid for DNSSEC, the immediate next step in standard DNS interrogation is completing the AXFR test across all designated nameservers.
</details>

---

### Question 3
An ethical hacker is evaluating the physical and human risk posture of a financial firm. The tester reviews discarded printed materials in the recycling bins located outside the target's corporate building and discovers shredded network topology diagrams and employee phone extensions. Which attack methodology was utilized?

- [ ] A) Shoulder Surfing
- [ ] B) Pretexting
- [ ] C) Dumpster Diving
- [ ] D) Eavesdropping

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **C**

**Technical Rationale:**
- **Why C is correct:** Dumpster diving is the physical reconnaissance practice of searching through an organization's discarded waste, dumpsters, or recycling bins to harvest proprietary documents, credentials, calendars, and hardware.
- **Why A is incorrect:** Shoulder surfing involves visually observing a victim's screen or keyboard over their shoulder.
- **Why B is incorrect:** Pretexting is an active social engineering technique where the attacker invents a fraudulent persona or scenario.
- **Why D is incorrect:** Eavesdropping involves secretly listening to verbal communications.
</details>

---

### Question 4
A penetration tester discovers the following DNS TXT record for `targetbank.com`:
```text
v=spf1 ip4:198.51.100.0/24 include:_spf.google.com +all
```
What is the primary vulnerability exposed by this record?

- [ ] A) The nameserver allows unauthenticated zone transfers to any host.
- [ ] B) Any external mail server on the internet can spoof emails from `@targetbank.com` and pass SPF validation.
- [ ] C) The SPF record reveals the internal Active Directory domain controller IP.
- [ ] D) The Google Workspace integration is invalid and will cause email delivery failure.

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** The `+all` qualifier at the end of an SPF record is a catastrophic misconfiguration that tells receiving mail servers: "Consider ANY sender IP as authorized (+Pass)". An attacker can forge emails appearing to originate from `@targetbank.com`, bypassing basic anti-spoofing controls. Hardened domains enforce `-all` (HardFail).
- **Why A is incorrect:** SPF records have no technical relationship with DNS zone transfers (AXFR).
- **Why C is incorrect:** `198.51.100.0/24` is a public routable netblock, not an RFC 1918 internal IP.
- **Why D is incorrect:** `include:_spf.google.com` is valid; the flaw is the permissive `+all` directive.
</details>

---

### Question 5
While conducting an external assessment, an ethical hacker uses a network utility to trace the path to a server behind a stateful perimeter firewall. Standard ICMP traceroute (`tracert`) drops all packets after hop 5 with asterisks (`* * *`). However, the target web application on port 443 responds normally. What command should the tester use to complete the hop trace?

- [ ] A) `ping -t -l 65500 target.com`
- [ ] B) `traceroute -T -p 443 target.com`
- [ ] C) `nslookup -type=ptr target.com`
- [ ] D) `dig target.com ANY`

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** Modern stateful perimeter firewalls frequently filter inbound ICMP Echo (Type 8) and high UDP probe packets. By utilizing TCP Traceroute (`traceroute -T -p 443` or `tcptraceroute`), the tool sends TCP SYN packets to port 443. Because the firewall permits HTTPS traffic, the packets traverse intermediary devices and the edge firewall, eliciting TTL Time Exceeded responses across the path.
- **Why A is incorrect:** This is a ping of death attempt (buffer overflow / oversized ping) which will not trace hops and will be dropped.
- **Why C is incorrect:** `nslookup -type=ptr` performs reverse DNS lookups, not packet route tracing.
- **Why D is incorrect:** `dig ANY` queries DNS records, not Layer 3 routing paths.
</details>

---

### Question 6
An organization calculates that the Asset Value (AV) of its customer database server is **$200,000**. Historical threat intelligence indicates that a successful ransomware attack causes an Exposure Factor (EF) of **40%**. The threat is estimated to occur once every two years (ARO = **0.5**). What is the Annualized Loss Expectancy (ALE)?

- [ ] A) $80,000
- [ ] B) $40,000
- [ ] C) $160,000
- [ ] D) $20,000

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** 
  1. $\text{Single Loss Expectancy (SLE)} = \text{Asset Value (AV)} \times \text{Exposure Factor (EF)}$
     $$\text{SLE} = \$200{,}000 \times 0.40 = \$80{,}000$$
  2. $\text{Annualized Loss Expectancy (ALE)} = \text{SLE} \times \text{Annualized Rate of Occurrence (ARO)}$
     $$\text{ALE} = \$80{,}000 \times 0.5 = \$40{,}000$$
- **Why A is incorrect:** $80,000 is the Single Loss Expectancy (SLE), not the annual expectancy.
- **Why C and D are incorrect:** Incorrect multiplication/division of factors.
</details>

---

### Question 7
Which search engine from the penetration tester's toolkit specializes in indexing global Internet of Things (IoT) devices, ICS/SCADA controllers, open databases, and web cameras by capturing service banners?

- [ ] A) PublicWWW
- [ ] B) Grep.app
- [ ] C) WiGLE
- [ ] D) Shodan

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **D**

**Technical Rationale:**
- **Why D is correct:** Shodan is the premier search engine for internet-connected hardware and services. It constantly sweeps IPv4/IPv6 spaces, grabbing banners from listening ports (e.g., Modbus port 502, RTSP cameras on 554, Elasticsearch on 9200).
- **Why A is incorrect:** PublicWWW indexes web source code (HTML, JS, CSS) to find code snippets and tracking IDs.
- **Why B is incorrect:** Grep.app searches across public GitHub repositories for source code and hardcoded secrets.
- **Why C is incorrect:** WiGLE is a database of wireless network access points and GPS coordinates.
</details>

---

### Question 8
In an RFC 5322 email header, an investigator is attempting to locate the IP address of the original machine that sent the message. In what sequence must the `Received:` headers be evaluated?

- [ ] A) Top to bottom; the top-most header represents the original sending client.
- [ ] B) Bottom to top; the bottom-most header represents the initial hop / originating MTA.
- [ ] C) Alphabetically by the hostname of the relay.
- [ ] D) By timestamp in descending chronological order from newest to oldest.

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** Each mail transfer agent (MTA) prepends a new `Received:` header to the top of the message as it forwards it toward the destination mailbox. Therefore, the very bottom `Received:` header represents the original sending client and the first mail submission server.
- **Why A is incorrect:** The top-most header represents the final hop that delivered the message to the recipient's mailbox.
- **Why C and D are incorrect:** RFC standards mandate sequential prepending; sorting alphabetically or randomly corrupts the hop chain.
</details>

---

### Question 9
During a reconnaissance phase, an ethical hacker identifies a DNS record:
```text
mail.partner.target.com.  IN  CNAME  unclaimed-bucket.s3.amazonaws.com.
```
When attempting to browse to `https://unclaimed-bucket.s3.amazonaws.com`, the AWS platform returns `NoSuchBucket: The specified bucket does not exist`. What specific vulnerability does this represent?

- [ ] A) DNS Amplification Attack
- [ ] B) Subdomain Takeover
- [ ] C) Cache Poisoning
- [ ] D) Zone Transfer Leakage

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** This is a classic **Subdomain Takeover**. The organization configured a CNAME record pointing to a third-party cloud resource (an AWS S3 bucket), but subsequently deleted the bucket without deleting the DNS record. An attacker can create an S3 bucket named `unclaimed-bucket` in their own AWS account, effectively serving arbitrary malicious content under `mail.partner.target.com`.
- **Why A is incorrect:** DNS amplification uses open resolvers to flood victims with large UDP responses.
- **Why C is incorrect:** Cache poisoning involves injecting fraudulent records into a resolver's cache.
- **Why D is incorrect:** Zone transfer leakage is retrieving a full zone file via AXFR.
</details>

---

### Question 10
Which of the following Google search operators is **BEST** suited for locating publicly accessible administrative login portals on a target domain while excluding the primary corporate website?

- [ ] A) `site:target.com inurl:login -www`
- [ ] B) `intitle:"index of /" target.com`
- [ ] C) `filetype:sql "target.com"`
- [ ] D) `related:target.com inurl:admin`

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **A**

**Technical Rationale:**
- **Why A is correct:** `site:target.com` restricts the search to the target domain, `inurl:login` matches login endpoints, and `-www` filters out the main public portal, forcing Google to return obscure or non-standard subdomains (e.g., `admin.target.com`, `vpn.target.com/login`).
- **Why B is incorrect:** This dork locates open directory listings, not administrative portals.
- **Why C is incorrect:** This searches for raw SQL database backups.
- **Why D is incorrect:** `related:` finds competitor or partner websites with similar profiles.
</details>

---

### Question 11
An investigator reviews a DNS record displaying:
```text
_sip._tcp.target.com. 86400 IN SRV 10 60 5060 pbx01.target.com.
```
What type of information did the attacker extract?

- [ ] A) The primary name server and administrative contact email.
- [ ] B) A Service Locator record identifying a Session Initiation Protocol (VoIP) server running on port 5060.
- [ ] C) The reverse PTR lookup mapping `pbx01` to an IPv6 address.
- [ ] D) The DKIM cryptographic signature selector.

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** An **SRV (Service Locator)** record defines the service (`_sip`), protocol (`_tcp`), domain, priority (`10`), weight (`60`), listening port (`5060`), and target hostname (`pbx01.target.com`). This directly discloses VoIP infrastructure.
- **Why A is incorrect:** That is the role of an SOA record.
- **Why C is incorrect:** Reverse lookups utilize PTR records under `in-addr.arpa`.
- **Why D is incorrect:** DKIM uses TXT records under `<selector>._domainkey`.
</details>

---

### Question 12
According to David Bianco's **Pyramid of Pain**, which category of indicator of compromise (IOC) causes the **MOST** disruption and operational cost to an advanced adversary when detected and denied by defenders?

- [ ] A) Hash Values (SHA-256)
- [ ] B) IP Addresses
- [ ] C) Domain Names
- [ ] D) Tactics, Techniques, and Procedures (TTPs)

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **D**

**Technical Rationale:**
- **Why D is correct:** The apex of the Pyramid of Pain is **TTPs**. Blocking hashes or IPs is trivial for attackers (they recompile code or rotate proxy IPs). However, forcing an adversary to change their fundamental Tactics, Techniques, and Procedures requires them to learn new tools, change behavioral habits, and redesign campaigns—costing maximum time and resources.
- **Why A, B, and C are incorrect:** Hash values are "Trivial", IP addresses are "Easy", and Domain Names are "Simple" for adversaries to modify.
</details>

---

### Question 13
An attacker sends thousands of rapid DNS queries to an organization's authoritative nameservers with fabricated hostnames such as `test1.target.com`, `test2.target.com`, and `staging99.target.com`. From a SOC perspective, which detection rule would **BEST** flag this activity in real-time?

- [ ] A) High count of DNS queries returning status code `NOERROR`.
- [ ] B) Spikes in DNS responses returning status code `NXDOMAIN` from a single source IP.
- [ ] C) Detection of ICMP Time Exceeded packets.
- [ ] D) Increased traffic on TCP port 443.

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** Subdomain dictionary brute-forcing generates hundreds or thousands of failed lookups because most guessed names do not exist. In DNS telemetry, non-existent domains trigger the `NXDOMAIN` (Non-Existent Domain) status code. A threshold alert (e.g., `>100 NXDOMAIN per minute per source IP`) provides high-fidelity detection of automated subdomain enumeration.
- **Why A is incorrect:** `NOERROR` represents successful resolutions.
- **Why C is incorrect:** ICMP Time Exceeded indicates traceroute activity, not DNS brute-forcing.
- **Why D is incorrect:** Port 443 is HTTPS web traffic.
</details>

---

### Question 14
Which document metadata harvesting tool is engineered to download corporate documents (`.pdf`, `.docx`, `.xlsx`) from public search engines and extract hidden usernames, operating system versions, and internal network printer paths?

- [ ] A) FOCA
- [ ] B) Wireshark
- [ ] C) Hping3
- [ ] D) John the Ripper

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **A**

**Technical Rationale:**
- **Why A is correct:** **FOCA (Fingerprinting Organizations with Collected Archives)** is specifically designed to crawl target websites, download document archives, and parse internal binary metadata to reveal usernames, software suites, printer share paths, and local drive mappings.
- **Why B is incorrect:** Wireshark is a packet capture and protocol analysis tool.
- **Why C is incorrect:** Hping3 is a packet crafting and network probing tool.
- **Why D is incorrect:** John the Ripper is an offline password cracking suite.
</details>

---

### Question 15
An enterprise wishes to prevent internal network topology and internal server IP addresses from leaking to external attackers while still allowing legitimate internal employees to resolve internal intranet hostnames. What is the **BEST** architectural countermeasure?

- [ ] A) Enable DNSSEC on public authoritative nameservers
- [ ] B) Deploy Split-Horizon (Split-Brain) DNS architecture
- [ ] C) Change public web servers to listen on non-standard ports
- [ ] D) Add a `Disallow: /` entry in `robots.txt`

<details>
<summary><b>View Explanation & Rationale</b></summary>

**Correct Answer:** **B**

**Technical Rationale:**
- **Why B is correct:** **Split-Horizon DNS** maintains two completely distinct DNS zone databases. External internet clients querying the organization's public DNS servers only receive public-facing IP records (e.g., public web server, external mail gateway). Internal clients querying internal DNS servers resolve internal hostnames to private RFC 1918 addresses. This prevents external enumeration of internal assets.
- **Why A is incorrect:** DNSSEC provides cryptographic authentication and data integrity, but it does not conceal zone data or create an internal/external split.
- **Why C is incorrect:** Obscurity via non-standard ports does not hide DNS records.
- **Why D is incorrect:** `robots.txt` is an advisory file for web search engines; adversaries actively read it to discover hidden paths.
</details>

---

*End of Practice Exam. Continue reviewing [Cheat Sheet](./quick-cram-cheat-sheet.md) or return to [CEH Hub](../README.md).*
