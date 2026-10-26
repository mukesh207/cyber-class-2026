# 🛰️ CEH v13 - Module 03: Scanning Networks

> **Course:** Certified Ethical Hacker (CEH v13) / Threat Hunting & SOC Engineering  
> **Topic:** Module 03 — Host Discovery, TCP/IP Flag Mechanics, Handshake Analysis, Port Scanning Anatomy (SYN, Connect, Inverse, Idle Zombie), Advanced Probing, Packet Fragmentation, Routing Manipulation, Proxy Chaining, Banner Grabbing & Defensive Detection Engineering  
> **Date:** 2026-10-26  
> **Navigation:** [🏠 CEH Dashboard](./README.md) | [⬅️ Module 02: Footprinting and Reconnaissance](./mod-02-footprinting-and-reconnaissance.md) | [➡️ Module 04: Enumeration (Upcoming)](#) | [Main Dashboard](../README.md)

---

## 🧭 Executive Navigation Map

1. [Network Scanning Core Architecture & Methodology](#1-network-scanning-core-architecture--methodology)
2. [Deep Mechanics of TCP/IP Flags & Handshakes](#2-deep-mechanics-of-tcpip-flags--handshakes)
3. [How Flags and Handshakes Act in Attacks](#3-how-flags-and-handshakes-act-in-attacks)
4. [Scanning Tools: Purpose, Architecture & Workflow](#4-scanning-tools-purpose-architecture--workflow)
5. [Host Discovery & Network Probes (Beyond Standard ICMP)](#5-host-discovery--network-probes-beyond-standard-icmp)
6. [Port Scanning Mechanics: Deep Dive into Scan Types](#6-port-scanning-mechanics-deep-dive-into-scan-types)
7. [The Idle Scan (Zombie Scan): Mechanics of Ultimate Stealth](#7-the-idle-scan-zombie-scan-mechanics-of-ultimate-stealth)
8. [IDS/Firewall Evasion I: Packet Fragmentation](#8-idsfirewall-evasion-i-packet-fragmentation)
9. [IDS/Firewall Evasion II: Routing Manipulations & Path Control](#9-idsfirewall-evasion-ii-routing-manipulations--path-control)
10. [Proxy Servers, Chaining & Anonymization Architecture](#10-proxy-servers-chaining--anonymization-architecture)
11. [Banner Grabbing, Service Probing & OS Fingerprinting](#11-banner-grabbing-service-probing--os-fingerprinting)
12. [Defensive Countermeasures & SOC Detection Engineering](#12-defensive-countermeasures--soc-detection-engineering)
13. [Big Picture: How It All Works Together](#13-big-picture-how-it-all-works-together)
14. [Real-Time Technical Scenario: Red Team Assessment vs. SOC Response](#14-real-time-technical-scenario-red-team-assessment-vs-soc-response)
15. [Hands-On Lab Methodology & Troubleshooting (Failed Attempts & Why)](#15-hands-on-lab-methodology--troubleshooting-failed-attempts--why)
16. [My Understanding Check](#16-my-understanding-check)

---

## 1. Network Scanning Core Architecture & Methodology

### What is Network Scanning?
**Network Scanning** is the second phase of the ethical hacking methodology, sitting directly between **Footprinting (Module 02)** and **Enumeration (Module 04)**. In terms of the MITRE ATT&CK framework, it maps to **Network Service Discovery (T1046)** and **System Network Configuration Discovery (T1016)** under the Discovery tactic (TA0007).

Where Footprinting provides a broad, high-level blueprint of the target organization's perimeter (CIDR ranges, ASN allocations, domain names, and public employee rosters), Scanning actively interrogates these specific networks and IP addresses to determine:
1. **Live Hosts:** Which IP addresses are actively powered on and connected to the network.
2. **Open Ports:** Which Layer 4 (TCP/UDP) listening ports are bound to accessible network sockets.
3. **Running Services & Versions:** The software application name, release version, and patch state running behind open sockets.
4. **Operating System & Architecture:** The underlying OS platform (Linux, Windows, BSD, embedded firmware) determined via protocol stack quirks.
5. **Perimeter Defenses:** The presence, filtering rules, statefulness, and bypass vectors of firewalls, IDS/IPS, and Web Application Firewalls (WAF).

```
+-----------------------------------------------------------------------------------+
|                        THE CEH SCANNING METHODOLOGY CYCLE                         |
+-----------------------------------------------------------------------------------+
|  [Step 1] Check for Live Systems (Host Discovery / Ping Sweeps)                   |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 2] Check for Open Ports (TCP/UDP Port Scanning Engines)                    |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 3] Scan Beyond IDS/Firewalls (Evasion: Fragmentation, Decoys, Spoofing)    |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 4] Banner Grabbing & Service Detection (Active/Passive Fingerprinting)      |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 5] Scan for Vulnerabilities (Targeted Scripts, NSE Engines, CVE Matching)  |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 6] Draw Network Topology Diagrams (Ingress/Egress, Subnets, Gateways)       |
|       │                                                                           |
|       ▼                                                                           |
|  [Step 7] Prepare Proxies & Pivots (Anonymization, Chaining, Tunneling)           |
+-----------------------------------------------------------------------------------+
```

### Why Scanning Works: The Deterministic Nature of RFCs
Every network operating system and firewall operates under standard networking specifications known as **RFCs (Requests for Comments)** published by the Internet Engineering Task Force (IETF). 

Network scanning exploits a core reality: **Operating systems are deterministic state machines.** When a host receives a packet conforming to or violating an RFC standard, its network stack *must* react in a mathematically predictable way unless specifically instructed otherwise by a firewall filter. By crafting custom packets with specific combinations of headers and flags, an attacker or pentester can force the target stack to generate responses that reveal its internal state.

---

## 2. Deep Mechanics of TCP/IP Flags & Handshakes

To master network scanning and understand how stealth, evasion, and denial-of-service attacks operate, you must understand the **Transmission Control Protocol (TCP)** at the raw byte and bit level.

### The RFC 793 TCP Header Structure
The TCP header is appended to the Layer 3 IP header. A standard TCP header without options is exactly **20 bytes (160 bits)** long:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |N|C|E|U|A|P|R|S|F|                         |
| Offset| Reserved  |S|W|E|R|C|S|S|Y|I|       Window Size       |
|       |           | |R| |G|K|H|T|N|N|                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |        Urgent Pointer         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options and Padding                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Critical Fields Explained
- **Source Port (16 bits):** Port on the sending host initiating or responding to traffic (0 to 65535).
- **Destination Port (16 bits):** Target service port on the destination host (e.g., 80 for HTTP, 443 for HTTPS, 22 for SSH).
- **Sequence Number (32 bits):** Tracks the byte stream position. In a SYN packet, this represents the **Initial Sequence Number (ISN)** generated by the operating system kernel.
- **Acknowledgment Number (32 bits):** If the ACK flag is set, this contains the next sequence number the receiver expects to receive ($ISN + 1$ or received sequence $+$ payload bytes).
- **Data Offset (4 bits):** Specifies the size of the TCP header in 32-bit (4-byte) words. Minimum value is 5 (which means $5 \times 4 = 20\text{ bytes}$). If options are used, this value increases.
- **Control Bits / Flags (9 bits):** 1-bit binary toggles (1 = ON, 0 = OFF) that dictate the operational state and handling instructions of the segment.

---

### Comprehensive Breakdown of All 9 TCP Control Flags

| Flag | Full Name | RFC Spec | Purpose & Kernel Mechanics | Offensive / Pentest Tactical Role |
| :---: | :--- | :---: | :--- | :--- |
| **SYN** | **Synchronize** | RFC 793 | Initiates a connection. Tells the remote host to synchronize its sequence numbering with the sender's Initial Sequence Number (**ISN**). | Used in **SYN Port Scanning** (`-sS`) to detect open ports without completing the connection, and in **SYN Flood DoS** attacks to exhaust connection state tables. |
| **ACK** | **Acknowledgment** | RFC 793 | Validates that the `Acknowledgment Number` field contains valid data confirming receipt of previous packets. Active in all packets after the initial SYN. | Used in **ACK Probing** (`-sA`) to map firewall rulesets and determine whether filtering is stateless or stateful. |
| **FIN** | **Finish** | RFC 793 | Signals that the sender has finished transmitting data and requests a graceful, bidirectional connection termination. | Used in **FIN Scans** (`-sF`) to probe Unix/Linux stacks where closed ports send a RST, but open ports drop the packet without reply. |
| **RST** | **Reset** | RFC 793 | Abruptly and immediately tears down a connection socket due to an unrecoverable error, packet mismatch, or attempt to connect to an unopened port. | Sent by targets when an attacker probes a closed port. Injected by attackers in **TCP Reset Hijacking** to kill active administrator sessions or BGP peerings. |
| **PSH** | **Push** | RFC 793 | Instructs the receiving TCP stack to bypass its internal buffering queues and immediately push all pending data directly to the user-space application. | Used in interactive shell sessions (SSH, Telnet) and in **Xmas Scans** (`-sX`) to stimulate specific kernel reactions. |
| **URG** | **Urgent** | RFC 793 | Declares that the segment contains high-priority data that must be processed out-of-band; activates the 16-bit **Urgent Pointer** field. | Used in telnet interrupt signals (`Ctrl+C`) and in crafted inverse scans to bypass primitive packet inspection engines. |
| **ECE** | **ECN-Echo** | RFC 3168 | **Explicit Congestion Notification**: Echoes back a network congestion warning. If SYN is 1, indicates the peer supports ECN; if SYN is 0, indicates congestion was detected in transit. | Manipulated in advanced network evasion tools and modern OS fingerprinting engines to evaluate RFC 3168 stack compliance. |
| **CWR** | **Congestion Window Reduced** | RFC 3168 | Sent by the transmitting host to confirm that it received an ECE packet and has throttled down its congestion transmission window. | Used alongside ECE in OS fingerprinting to observe how target kernels behave under non-standard congestion conditions. |
| **NS** | **Nonce Sum** | RFC 3540 | Experimental flag protecting against sender manipulation of ECN signaling (ECN-nonce concealment protection). | Rare in standard production traffic; used in research and deep protocol fingerprinting. |

---

### The TCP 3-Way Handshake (Step-by-Step Mechanical Flow)

Before any application data (HTTP, SSH, SMTP) can pass across a TCP stream, a 3-way connection synchronization sequence must occur between Client and Server.

```
       CLIENT (Attacker/User)                            SERVER (Target)
      [State: CLOSED]                                   [State: LISTEN]
             │                                                 │
             │           1. [SYN] Seq = 1000                   │
             │────────────────────────────────────────────────>│ (Allocates TCB / Buffer)
             │                                                 │ [State: SYN_RECEIVED]
             │                                                 │
             │           2. [SYN, ACK] Seq = 5000, Ack = 1001  │
             │<────────────────────────────────────────────────│
(Allocates TCB)                                                │
[State: ESTABLISHED]                                           │
             │                                                 │
             │           3. [ACK] Seq = 1001, Ack = 5001       │
             │────────────────────────────────────────────────>│
             │                                                 │ [State: ESTABLISHED]
             │                                                 │
             ▼                                                 ▼
      [DATA TRANSMISSION PHASE: PSH+ACK / Application Payload Follows]
```

#### Detailed State Transition Breakdown:
1. **Step 1: The SYN Probe (Client $\to$ Server)**
   - Client generates a pseudo-random **Initial Sequence Number (ISN)** (e.g., `Seq = 1000`).
   - Flags set: `[SYN = 1, ACK = 0]`.
   - Client transitions from `CLOSED` to `SYN_SENT`.
2. **Step 2: The Synchronization & Acknowledgment (Server $\to$ Client)**
   - Server receives the SYN. If the target port is bound to a listening service, the server's kernel allocates a **Transmission Control Block (TCB)** in memory.
   - Server generates its own independent **ISN** (e.g., `Seq = 5000`).
   - Server calculates the acknowledgment number by incrementing the client's sequence number by 1: `Ack = 1000 + 1 = 1001`.
   - Flags set: `[SYN = 1, ACK = 1]`.
   - Server transitions from `LISTEN` to `SYN_RECEIVED`.
3. **Step 3: The Final Handshake Acknowledgment (Client $\to$ Server)**
   - Client receives the SYN/ACK.
   - Client acknowledges receipt of the server's sequence by incrementing it: `Ack = 5000 + 1 = 5001`.
   - Client sets its sequence number to `Seq = 1001`.
   - Flags set: `[ACK = 1, SYN = 0]`.
   - Both client and server enter the `ESTABLISHED` state. Communication is now full-duplex.

---

### Connection Teardown: Graceful 4-Way vs. Abrupt RST

TCP connections terminate through one of two mechanisms:

#### Mechanism 1: Graceful 4-Way Teardown (FIN-ACK)
Each side independently closes its direction of the transmission stream:

```
       CLIENT                                            SERVER
[State: ESTABLISHED]                              [State: ESTABLISHED]
             │                                                 │
             │              1. [FIN, ACK]                      │
             │────────────────────────────────────────────────>│
[State: FIN_WAIT_1]                                            │ [State: CLOSE_WAIT]
             │              2. [ACK]                           │
             │<────────────────────────────────────────────────│
[State: FIN_WAIT_2]                                            │
             │              3. [FIN, ACK]                      │
             │<────────────────────────────────────────────────│
             │                                                 │ [State: LAST_ACK]
             │              4. [ACK]                           │
             │────────────────────────────────────────────────>│
[State: TIME_WAIT]                                             ▼
             │                                          [State: CLOSED]
(Waits 2 * MSL)
             ▼
      [State: CLOSED]
```

#### Mechanism 2: Abrupt RST Termination
If an unrecoverable mismatch occurs or an application crashes, a host sends a single packet with `[RST = 1]`. No acknowledgment is expected; both endpoints immediately purge their TCB buffers from memory and drop the socket.

---

### TCP vs. UDP: The Connectionless Reality

| Parameter | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Protocol Layer** | Layer 4 (Transport) | Layer 4 (Transport) |
| **Connection State** | **Stateful**: Requires 3-way handshake before data transfer. | **Connectionless**: Datagrams sent with zero prior negotiation. |
| **Reliability** | Guaranteed delivery via Sequence numbers, ACKs, retransmissions. | Unreliable: "Fire and forget." Packets may arrive out of order or drop. |
| **Header Overhead** | **20 Bytes minimum** (up to 60 bytes with options). | **8 Bytes fixed** (Source Port, Dest Port, Length, Checksum). |
| **Port Scanning Reaction** | Explicit: Responds with **SYN/ACK** (Open) or **RST** (Closed). | Implicit: Open services often **send no reply**; Closed ports trigger **ICMP Type 3 Code 3 (Port Unreachable)**. |

---

## 3. How Flags and Handshakes Act in Attacks

Understanding the state machine of TCP reveals why network protocols are systematically weaponized by attackers. The vulnerabilities lie in **resource asymmetry** and **trust assumptions**.

### 1. TCP SYN Flood Attack (Half-Open Queue Exhaustion)

```
       ATTACKER (Spoofed IPs)                           TARGET SERVER
             │                                                 │
             │  1. Spoofed SYN (Seq = A)                       │
             │────────────────────────────────────────────────>│ (Allocates TCB Slot 1)
             │  2. Spoofed SYN (Seq = B)                       │ [SYN_RECEIVED]
             │────────────────────────────────────────────────>│ (Allocates TCB Slot 2)
             │  3. Spoofed SYN (Seq = C)                       │ [SYN_RECEIVED]
             │────────────────────────────────────────────────>│ (Allocates TCB Slot 3)
             │                                                 │
             │     (Server sends SYN/ACKs to spoofed IPs;      │ [BACKLOG QUEUE FULL!]
             │      Legitimate clients receive no service)     │
             │                                                 │
       LEGITIMATE USER                                         │
             │  4. Valid SYN                                   │
             │────────────────────────────────────────────────>│ ❌ DROPPED!
             │                                                 │ (Memory Exhausted)
```

#### Why it Works:
- When a server receives a SYN packet, it must allocate a memory structure called a **Transmission Control Block (TCB)** and wait for the client's final ACK.
- This half-open state is held in a kernel structure called the **SYN Backlog Queue**.
- A standard server queue might only hold between 128 to 1,024 pending connections before saturating.
- By flooding thousands of SYN packets with random, spoofed source IP addresses, the attacker never sends the final ACK. The server retries sending SYN/ACKs repeatedly until the connection timer expires (typically 75 seconds).
- **Result:** Legitimate users attempting to establish connections are rejected because the server has zero free slots in its backlog queue.

#### Defensive Mechanism: SYN Cookies
Under a **SYN Cookie** defense (RFC 4987), the server **refuses to allocate a TCB buffer** upon receiving an initial SYN. Instead, it encodes the client's connection details (source IP, port, MSS, timestamp) into a cryptographic hash embedded directly inside the server's own Initial Sequence Number ($ISN_{cookie}$). 
Only when the client returns a legitimate final ACK containing $Ack = ISN_{cookie} + 1$ does the server decrypt the sequence number, verify the handshake integrity, and allocate memory for the connection.

---

### 2. TCP Reset (RST) Hijacking & Connection Teardown

```
     ATTACKER (Sniffing Wire)                         ACTIVE SESSION (Client <-> Server)
             │                                                 │
             │  1. Observe Client: Seq=45000, Ack=82000        │
             │< - - - - - - - - - - - - - - - - - - - - - - - -│
             │                                                 │
             │  2. Forged Packet: Src=Client_IP, Dst=Server_IP │
             │     Flags: [RST = 1], Seq = 45001               │
             │────────────────────────────────────────────────>│
             │                                                 │ 💥 TARGET KILLS SOCKET!
             │                                                 ▼ (Connection Terminated)
```

#### Why it Works:
- TCP endpoints must process an incoming RST packet immediately to avoid hanging sockets.
- If an attacker can sniff the active sequence number on an unencrypted connection (or accurately predict it within the receiving host's TCP sliding window), they forge a single TCP segment with the source IP of the client, the target port, and the **RST flag set**.
- When the server receives the RST segment with a valid in-window sequence number, it assumes the client crashed and forcefully terminates the active session.
- **Weaponization:** Used to terminate BGP routing peering sessions, sever long-running VPN tunnels, or disrupt active administrator SSH sessions.

---

### 3. State Table Exhaustion Floods (FIN, ACK, and PSH+ACK Floods)
- **Target:** Stateful firewalls and Deep Packet Inspection (DPI) appliances.
- **Mechanics:** Stateful firewalls maintain a **Connection Tracking Table** (e.g., Linux Netfilter's `conntrack`). Every packet must be compared against active state tables to verify whether it belongs to an existing, established connection.
- If an adversary floods high volumes of randomized **ACK** or **PSH+ACK** packets that do not correspond to any active session, the firewall must burn CPU cycles looking up every non-existent connection in its hash tables before dropping them.
- **Impact:** The firewall's CPU utilization hits 100%, causing state table saturation, dropping legitimate packets, or failing open (allowing traffic to pass uninspected).

---

## 4. Scanning Tools: Purpose, Architecture & Workflow

A common mistake in security certification study is memorizing command-line flags without understanding the underlying tool architecture. In enterprise penetration testing and SOC engineering, tools are selected based on **traffic generation mechanics**, **asynchronous performance**, and **protocol accuracy**.

```
+-----------------------------------------------------------------------------------+
|                        SCANNING TOOL TAXONOMY & ENGINE TYPES                      |
+-----------------------------------------------------------------------------------+
| Engine Architecture | Tools                       | Primary Tactical Use-Case     |
+---------------------+-----------------------------+-------------------------------+
| Stateful RAW Socket | Nmap                        | Precision, NSE scripting, OS/ |
| Packet Crafter      |                             | service version discovery.    |
| Custom Segment      | Hping3, Scapy               | Firewall rule interrogation,  |
| Fabricator          |                             | manual probe crafting, DoS.   |
| Asynchronous Kernel | Masscan, ZMap               | High-speed Internet-wide      |
| Bypass Engine       |                             | port scanning (10M+ pps).     |
| Raw Stream Worker   | Netcat (nc), Ncat, Socat    | Banner grabbing, raw socket   |
|                     |                             | testing, payload delivery.    |
| Asynchronous Stim   | Unicornscan                 | Low-noise UDP/TCP correlation |
| Response Correlator |                             | with independent listener.    |
+-----------------------------------------------------------------------------------+
```

---

### Tool 1: Nmap (Network Mapper)
**Core Purpose:** The industry standard for network exploration, vulnerability detection, and defense auditing.
- **Operational Workflow:** Uses raw sockets (requiring root/Administrator privileges) to craft customized Layer 3 and Layer 4 frames. Implements sophisticated adaptive round-trip-time (RTT) estimators, congestion control, and parallel host probing.
- **Nmap Scripting Engine (NSE):** Extends Nmap using Lua scripts for advanced service discovery, vulnerability exploitation, and brute forcing across 14 categories (`auth`, `vuln`, `safe`, `exploit`, etc.).

```
   +----------------------------------------------------------------------------+
   |                     NMAP TIMING TEMPLATES (T0 - T5)                        |
   +----------------------------------------------------------------------------+
   | Template | Designation | Delay Between Probes | Target Use-Case            |
   | :---     | :---        | :---                 | :---                       |
   | -T0      | Paranoid    | 5 minutes            | IDS evasion, covert red ops|
   | -T1      | Sneaky      | 15 seconds           | IDS evasion, slow circuits |
   | -T2      | Polite      | 0.4 seconds          | Reduces bandwidth / load   |
   | -T3      | Normal      | Dynamic (Adaptive)   | Standard default scan      |
   | -T4      | Aggressive  | Dynamic (Fast timeouts)| Modern reliable networks |
   | -T5      | Insane      | Extremely short delays| Extremely fast local LANs  |
   +----------------------------------------------------------------------------+
```

---

### Tool 2: Hping3 (Packet Crafting & Protocol Probing Engine)
**Core Purpose:** A command-line oriented TCP/IP packet assembler and analyzer. Unlike Nmap, which handles full scan automation, Hping3 gives the operator complete byte-by-byte manual control over IP, TCP, UDP, and ICMP headers.
- **Operational Workflow:** Crafts individual, customized datagrams to test specific firewall rules, evaluate packet filtering policies, fragment custom payloads, and perform covert channel analysis.

#### Essential Hping3 Tactical Workflows:
```bash
# 1. Send a customized TCP SYN to port 80 with a spoofed source IP
hping3 -S 192.168.1.50 -p 80 -a 10.0.0.99 -c 1

# 2. Interrogate firewall statefulness by sending an unprompted ACK packet
hping3 -A 192.168.1.50 -p 443 -c 1

# 3. Perform a TCP FIN scan with custom sequence numbering
hping3 -F 192.168.1.50 -p 22 -c 1

# 4. Probe path MTU and fragmentation handling (sets Don't Fragment bit)
hping3 -d 1400 -D 192.168.1.50 -p 80 --icmp -c 1
```

---

### Tool 3: Masscan (Asynchronous Internet-Scale Port Scanner)
**Core Purpose:** Masscan is designed to scan the entire public Internet in under 5 minutes.
- **Operational Workflow:** Masscan bypasses the operating system's native TCP/IP stack using its own custom user-space driver architecture (similar to `PF_RING`). It does not store connection state.
- It transmits raw, asynchronous SYN packets at rates exceeding **10 million packets per second (pps)**. Returning SYN/ACK packets are intercepted by an independent, asynchronous listener thread.

```bash
# Scan an entire /16 subnet for open port 443 at 100,000 packets per second
masscan 10.10.0.0/16 -p443 --rate=100000 -e eth0 --router-ip 10.10.0.1
```

---

### Tool 4: Netcat (The "Swiss Army Knife" of Networking)
**Core Purpose:** Reading and writing raw data across arbitrary TCP and UDP network connections.
- **Operational Workflow:** Operates as a simple socket connector or listener without complex packet crafting. Ideal for rapid banner grabbing, manual protocol interrogation, and setting up reverse shells.

```bash
# Connect directly to an open port and read the banner (verbose, no DNS)
nc -nv 192.168.1.50 21

# Set up an arbitrary listening port to capture incoming probes or payloads
nc -lvnp 4444
```

---

## 5. Host Discovery & Network Probes (Beyond Standard ICMP)

Host discovery (often termed a **Ping Sweep**) is the process of determining which IP addresses within a target CIDR block are associated with live, active systems.

### The Failure of Traditional ICMP Echo in Modern Enterprises
Historically, administrators and attackers relied on standard **ICMP Echo Requests** (`Ping`, Type 8). In modern enterprise networks, **pure ICMP discovery is completely ineffective**:
- Microsoft Windows Firewall has blocked inbound ICMP Echo requests by default since Windows Vista and Windows Server 2008.
- Enterprise edge routers and stateful firewalls routinely drop all incoming ICMP traffic at the perimeter.
- If an attacker scans using only ICMP (`nmap -sn -PE`), they will conclude that 95% of target hosts are "dead" when they are fully operational.

```
       ATTACKER                                          TARGET FIREWALL / WINDOWS HOST
          │                                                          │
          │  ICMP Echo Request (Type 8)                              │
          │─────────────────────────────────────────────────────────>│ ❌ SILENTLY DROPPED!
          │                                                          │ (No response)
          │                                                          │
          │  TCP SYN Probe (Port 443)                                │
          │─────────────────────────────────────────────────────────>│ ✅ PROCESSED!
          │                                                          │
          │  TCP SYN/ACK (Port Open) OR TCP RST (Port Closed)        │
          │<─────────────────────────────────────────────────────────│ (Host confirmed LIVE!)
```

---

### Probing Taxonomy & Mechanical Behavior

| Probe Type | Nmap Switch | Mechanics & Packet Flow | Why It Bypasses Defenses |
| :--- | :---: | :--- | :--- |
| **ARP Ping** | `-PR` | Sends raw Ethernet ARP requests (`Who has IP?`) directly to the broadcast address (`FF:FF:FF:FF:FF:FF`). | **100% Unblockable on local LANs.** Operating systems cannot filter ARP if they want to communicate on Layer 2. Nmap defaults to this automatically on local subnets. |
| **ICMP Echo** | `-PE` | Standard ICMP Type 8 Echo Request. Expects Type 0 Echo Reply. | Fast, but universally blocked by modern perimeter firewalls and endpoint security. |
| **ICMP Timestamp** | `-PP` | ICMP Type 13 query asking for current system time. Expects Type 14. | Bypasses administrators who blindly block Type 8 Echo but leave timestamp queries open. |
| **ICMP Address Mask** | `-PM` | ICMP Type 17 query asking for the subnet mask. Expects Type 18. | Archaic query type; frequently unmonitored by poorly configured egress firewalls. |
| **TCP SYN Ping** | `-PS<ports>` | Sends an empty TCP SYN to target ports (defaults to port 80). | If the port is open $\to$ server responds with **SYN/ACK**. If closed $\to$ server responds with **RST**. **Either response proves the host is ALIVE!** |
| **TCP ACK Ping** | `-PA<ports>` | Sends an empty TCP ACK directly to target ports (defaults to port 80). | Targets respond with a **RST** because no connection exists. Proves host is alive and effortlessly punches through stateless packet filters. |
| **UDP Ping** | `-PU<ports>` | Sends raw UDP datagrams to high, unlikely ports (defaults to 40125). | If the host is live and the port closed, RFC 792 mandates an **ICMP Type 3 Code 3 (Port Unreachable)** response. Proves the target is online. |
| **IP Protocol Ping**| `-PO<protocols>`| Sends raw IP packets with specific protocol numbers in the IP header (ICMP=1, IGMP=2, TCP=6, UDP=17). | Tests whether an operating system supports specific Layer 3 transport protocols. |

---

## 6. Port Scanning Mechanics: Deep Dive into Scan Types

Once live hosts are discovered, the attacker must determine which network sockets are actively listening for incoming connections.

### The RFC 793 Rule Matrix (The Ground Truth)
According to the official TCP specification (RFC 793, Page 65):
1. **Rule 1:** If an incoming segment arrives at a **CLOSED** port, and that segment does not contain a RST flag, the host **MUST** send an incoming segment with the **RST** flag set in response.
2. **Rule 2:** If an incoming segment arrives without a SYN, RST, or ACK flag set (e.g., FIN, NULL, or Xmas) at an **OPEN** port, the host **MUST DROP** the packet and return **NO RESPONSE**.

This fundamental RFC behavior gives rise to the entire family of **Inverse TCP Flag Scans**.

```
+-----------------------------------------------------------------------------------+
|                        TCP PORT SCANNING RESPONSE MATRIX                          |
+-----------------------------------------------------------------------------------+
| Scan Technique      | Open Port Response    | Closed Port Response| Filtered Response |
+---------------------+-----------------------+---------------------+-------------------+
| TCP Connect (-sT)   | SYN/ACK (Handshake)   | RST                 | No Reply / ICMP   |
| TCP SYN (-sS)       | SYN/ACK (Reset by us) | RST                 | No Reply / ICMP   |
| TCP FIN (-sF)       | No Reply (Dropped)    | RST                 | No Reply / ICMP   |
| TCP NULL (-sN)      | No Reply (Dropped)    | RST                 | No Reply / ICMP   |
| TCP Xmas (-sX)      | No Reply (Dropped)    | RST                 | No Reply / ICMP   |
| TCP ACK (-sA)       | RST (State Unfiltered)| RST (Unfiltered)    | No Reply / ICMP   |
| UDP Scan (-sU)      | App Response / No Rep | ICMP Type 3 Code 3  | ICMP Type 3 (1,2) |
+-----------------------------------------------------------------------------------+
```

---

### 1. TCP Connect Scan (`-sT`)
- **Mechanics:** Completes the entire 3-way handshake using the underlying operating system's native `connect()` system call.
- **Packet Flow:**
  - Attacker $\to$ `[SYN]` $\to$ Target
  - Target $\to$ `[SYN, ACK]` $\to$ Attacker
  - Attacker $\to$ `[ACK]` $\to$ Target (Connection is now `ESTABLISHED`)
  - Attacker $\to$ `[RST, ACK]` $\to$ Target (Gracefully tears down the connection)
- **Advantages:** Does not require raw socket access or administrative privileges (runs cleanly in non-root user spaces).
- **Disadvantages:** **Noisiest scan type.** Because the connection is fully established, user-space application daemons (Apache, Nginx, OpenSSH) log the connection attempt with the attacker's full IP address and timestamp.

---

### 2. Stealth Scan / TCP SYN Scan (`-sS`)
- **Mechanics:** Also known as the **Half-Open Scan**. It terminates the connection before the operating system kernel can transition the socket into an `ESTABLISHED` state.
- **Packet Flow:**
  ```
       ATTACKER (Raw Sockets)                            TARGET SERVER
             │                                                 │
             │           1. [SYN] Seq = 100                    │
             │────────────────────────────────────────────────>│ (Allocates TCB)
             │                                                 │
             │           2. [SYN, ACK] Seq = 800, Ack = 101    │
             │<────────────────────────────────────────────────│ (Port is OPEN!)
             │                                                 │
             │           3. [RST] Seq = 101                    │
             │────────────────────────────────────────────────>│ (TCB Immediately Purged!)
             ▼                                                 ▼
     (Connection Never Established; Service Daemon Never Logs Session)
  ```
- **Why it is Stealthy:** Most traditional application loggers (e.g., web server access logs) only write an entry when a connection reaches the `ESTABLISHED` state and payload data is received. Because the attacker resets the connection during the handshake, the target application never logs the intrusion.
- **Defensive Reality:** Modern Network Intrusion Detection Systems (Snort, Suricata, Zeek) and stateful firewalls track raw SYN/RST anomalies effortlessly. Stealth is relative only to application-layer logs.

---

### 3. Inverse TCP Flag Scans: FIN, NULL, and Xmas Scans

These scans invert standard logic by intentionally sending packets that violate normal connection-initiation protocols.

#### A. TCP FIN Scan (`-sF`)
- **Packet Sent:** A standalone segment with only the `[FIN = 1]` flag set.
- **Logic:** Under normal protocol flow, a FIN can only be sent *after* an established session. Sending a lone FIN to a port is illegal.
- If the port is **Closed**: Target kernel complies with RFC 793 Rule 1 and replies with a `[RST]`.
- If the port is **Open**: Target kernel complies with RFC 793 Rule 2, realizes no connection exists, and **silently drops** the packet.

#### B. TCP NULL Scan (`-sN`)
- **Packet Sent:** A completely empty segment with **zero flags set** (`000000000`).
- **Logic:** Identical to FIN scan. Closed ports return `[RST]`; open ports drop the packet without replying.

#### C. TCP Xmas Scan (`-sX`)
- **Packet Sent:** A segment with the **FIN, PSH, and URG** flags set simultaneously.
- **Naming Origin:** Named because the packet's control flags are "lit up like a Christmas tree" in packet analyzers (`000101001` binary).
- **Logic:** Closed ports reply with `[RST]`; open ports drop the packet.

```
       ATTACKER                                          TARGET SERVER
          │                                                    │
          │  FIN / NULL / Xmas Probe                           │
          │───────────────────────────────────────────────────>│
          │                                                    │
          │  CASE 1: Port is CLOSED                            │
          │<───────────────────────────────────────────────────│ [RST, ACK]
          │                                                    │
          │  CASE 2: Port is OPEN                              │
          │  (No Response; Packet Dropped by RFC 793)          │ 
          │  ................................................  │
```

> [!WARNING] The Microsoft Windows Non-Compliance Flaw
> The TCP/IP stack implementation in **Microsoft Windows (from NT through Windows 11/Server 2025)**, Cisco IOS, and many BSD printer engines violates RFC 793. When an unprompted FIN, NULL, or Xmas packet arrives at a Windows system, the Windows kernel sends a **RST packet regardless of whether the port is open or closed**.
> **Tactical Takeaway:** If a FIN, NULL, or Xmas scan against a host reports that *every single port is closed*, the host is almost certainly running Microsoft Windows. These scans only function reliably against POSIX/RFC-compliant systems (Linux, Solaris, HP-UX, FreeBSD).

---

### 4. TCP ACK Flag Scan (`-sA`)
- **Mechanics:** The attacker sends a packet with only the `[ACK = 1]` flag set.
- **Purpose:** The ACK scan **cannot determine whether a port is OPEN or CLOSED**. Its exclusive purpose is to **map firewall rulesets** and determine whether filtering is stateful or stateless.
- **Interpreting Results:**
  - If the firewall is **Stateless** (or no firewall exists): The ACK packet passes through. The target kernel receives an ACK for an unestablished session, generates a `[RST]`, and returns it. Nmap marks the port as **unfiltered**.
  - If the firewall is **Stateful** (or drops unprompted ACKs): The firewall inspects its state table, sees no matching SYN session, and silently drops the packet (or returns an ICMP Type 3 Destination Unreachable). Nmap marks the port as **filtered**.

---

### 5. TCP Window Scan (`-sW`)
- **Mechanics:** Identical to an ACK scan, but examines the **TCP Window Size** field inside the returning `[RST]` packet.
- **Exploited Stack Quirk:** In certain legacy or unpatched BSD-derived operating systems (AIX, FreeBSD, older macOS), open ports report a **positive, non-zero Window Size** in their RST packet, while closed ports return a RST with a **Window Size of exactly zero**.

---

## 7. The Idle Scan (Zombie Scan): Mechanics of Ultimate Stealth

The **Idle Scan** (`nmap -sI`) is the most technologically sophisticated port scan in cybersecurity. It allows an attacker to map open ports on a target **without sending a single packet from their own IP address to the target**.

### The Root Cause: The IP Identification (IPID) Field
Every IPv4 header contains a 16-bit **Identification (IPID)** field used to reassemble fragmented packets. 

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

Historically, many operating systems implemented a **global incremental counter** for the IPID: every time the host transmits any IPv4 packet, its kernel increments the IPID by exactly 1 ($IPID_{new} = IPID_{old} + 1$), regardless of who receives the packet.

### Requirements for a Zombie Host
To execute an Idle Scan, the attacker must first locate an unhardened third-party system on the Internet known as a **Zombie**:
1. It must generate predictable, sequentially incrementing IPID numbers (global counter).
2. It must be **truly idle**: Zero ambient network traffic. If other systems communicate with the zombie during the scan, its IPID counter will fluctuate unpredictably, corrupting the scan results.

---

### Step-by-Step Execution of the 3-Phase Idle Scan

```
===================================================================================
PHASE 1: ATTACKER PROBES ZOMBIE IPID BASELINE
===================================================================================
    ATTACKER                                  ZOMBIE HOST
       │                                           │
       │  1. [SYN, ACK]                            │
       │──────────────────────────────────────────>│ (Zombie sees unexpected SYN/ACK)
       │                                           │
       │  2. [RST] (Contains IPID = 31337)         │
       │<──────────────────────────────────────────│ (Attacker records baseline: x = 31337)
       │                                           │

===================================================================================
PHASE 2: ATTACKER FORGES SPOOFED SYN TO TARGET (SPOOFING ZOMBIE IP)
===================================================================================
    ATTACKER              ZOMBIE HOST                   TARGET SERVER
       │                       │                             │
       │  3. [SYN] (Src: ZOMBIE, Dst: TARGET, Port 80)       │
       │────────────────────────────────────────────────────>│
       │                       │                             │
       │                       │   CASE A: PORT IS OPEN      │
       │                       │   4a. [SYN, ACK]            │
       │                       │<────────────────────────────│
       │                       │                             │
       │                       │   5a. [RST] (IPID = 31338!) │ (Zombie increments IPID!)
       │                       │────────────────────────────>│
       │                       │                             │
       │                       │   CASE B: PORT IS CLOSED    │
       │                       │   4b. [RST]                 │
       │                       │<────────────────────────────│
       │                       │                             │
       │                       │   (Zombie drops RST;        │ (Zombie IPID DOES NOT
       │                       │    sends no packet)         │  increment!)
       │                       │                             │

===================================================================================
PHASE 3: ATTACKER RE-PROBES ZOMBIE TO MEASURE IPID DELTA
===================================================================================
    ATTACKER                                  ZOMBIE HOST
       │                                           │
       │  6. [SYN, ACK]                            │
       │──────────────────────────────────────────>│
       │                                           │
       │  7. [RST] (Contains New IPID)             │
       │<──────────────────────────────────────────│
       │                                           │
       ▼                                           ▼
[CALCULATION & VERDICT]
 - If New IPID == 31339 (Incremented by 2) ──> TARGET PORT IS OPEN!
 - If New IPID == 31338 (Incremented by 1) ──> TARGET PORT IS CLOSED / FILTERED!
```

#### Detailed Mathematical Breakdown:
1. **Phase 1 (Probe Zombie):** Attacker sends a SYN/ACK to the Zombie. The Zombie responds with a RST containing its current IPID: $x = 31337$.
2. **Phase 2 (Spoofed Attack):** Attacker crafts a raw SYN packet addressed to the Target, but **forges the Source IP address to match the Zombie's IP address**.
   - **If Port is OPEN:** Target sends a `[SYN/ACK]` to the Zombie. The Zombie receives an unexpected SYN/ACK, generates a `[RST]`, and transmits it to the Target. In doing so, the Zombie increments its global IPID to $x + 1$ ($31338$).
   - **If Port is CLOSED:** Target sends a `[RST]` to the Zombie. RFC 793 dictates that a host drops an incoming RST without responding. The Zombie sends nothing. Its IPID remains $x$ ($31337$).
   - **If Port is FILTERED:** Target drops the packet. The Zombie hears nothing. Its IPID remains $x$ ($31337$).
3. **Phase 3 (Measure Delta):** Attacker sends another SYN/ACK to the Zombie. The Zombie responds with a RST containing its new IPID:
   - **Open Port Delta:** $IPID_{final} = x + 2$ ($31339$). The Zombie incremented once for the target's probe, and once for the attacker's second probe.
   - **Closed/Filtered Delta:** $IPID_{final} = x + 1$ ($31338$). The Zombie only incremented once (for the attacker's second probe).

#### Practical Execution Syntax:
```bash
# Step 1: Use Nmap's ipidseq script to find a vulnerable zombie host
nmap -p80 --script ipidseq 192.168.1.100-200

# Step 2: Execute the Idle Scan using the validated zombie (192.168.1.150)
nmap -Pn -sI 192.168.1.150:80 10.0.0.50
```

---

## 8. IDS/Firewall Evasion I: Packet Fragmentation

### Why Packet Fragmentation Evades Firewalls
Traditional stateless firewalls and older Network Intrusion Detection Systems (NIDS) inspect network traffic on a packet-by-packet basis as segments traverse the interface.

**Packet Fragmentation** exploits the IP header's fragmentation mechanics to split the Layer 4 TCP header across multiple Layer 3 IP datagrams. If an IDS rule looks for signatures such as `TCP Port 22` paired with `Flags: SYN`, splitting the packet prevents the IDS from seeing the complete signature within a single frame.

```
       ORIGINAL UNFRAGMENTED PACKET (28 Bytes Total: 20 Byte IP + 8 Byte TCP)
      +-----------------------------+------------------------------------+
      |       IP Header (20B)       |          TCP Header (20B)          |
      |   Src, Dst, Protocol = 6    | Ports (4B) | Seq (8B) | Flags (1B) |
      +-----------------------------+------------------------------------+
                                      │
                         [FRAGMENTATION ENGINE SPLIT]
                                      ▼
      FRAGMENT #1 (Offset = 0, More Fragments = 1)
      +-----------------------------+--------------------------+
      |       IP Header (20B)       | TCP Ports (First 8 Bytes)|
      +-----------------------------+--------------------------+
      (Stateless firewall sees the ports, but CANNOT see TCP Flags!)

      FRAGMENT #2 (Offset = 1 [8 Bytes], More Fragments = 0)
      +-----------------------------+--------------------------+
      |       IP Header (20B)       | TCP Flags & Remaining (12B)|
      +-----------------------------+--------------------------+
      (Stateless firewall sees the flags, but CANNOT see Ports!)
```

### IP Fragmentation Fields:
1. **Identification (16 bits):** Binds fragments belonging to the same original datagram together.
2. **Flags (3 bits):**
   - Bit 0: Reserved (Must be 0).
   - Bit 1: **DF (Don't Fragment)**. If 1, intermediate routers must drop the packet if it exceeds MTU.
   - Bit 2: **MF (More Fragments)**. If 1, more fragments follow. If 0, this is the final fragment.
3. **Fragment Offset (13 bits):** Measured in **8-byte units (64 bits)**. Specifies the exact position of the fragment's payload relative to the beginning of the original unfragmented payload.

### Fragmentation Attack Variants:
- **Tiny Fragment Attack:** The attacker forces the first fragment to be so small that it only contains the IP header and the TCP source/destination ports (first 8 bytes). The TCP flags are pushed entirely into the second fragment. Stateless filters allowing established connections (checking for ACK) permit Fragment 1 (no flags) and Fragment 2 (no destination port), allowing malicious connections to slip through.
- **Overlapping Fragment Attack:** The attacker creates Fragment 2 with a manipulated Fragment Offset that causes it to overwrite the port data of Fragment 1 during reassembly inside the operating system kernel:
  - Fragment 1 contains: `Port 80 (Allowed by firewall)`.
  - Fragment 2 arrives with `Offset = 0`, overwriting the memory buffer with `Port 22 (SSH - Restricted)`.
  - The firewall validated Port 80, but the target server reassembles and executes traffic on Port 22!

```bash
# Split TCP header into 8-byte fragments
nmap -f 192.168.1.50

# Split TCP header into 16-byte fragments (double fragmentation)
nmap -ff 192.168.1.50

# Specify an explicit custom MTU (must be a multiple of 8)
nmap --mtu 24 192.168.1.50
```

---

## 9. IDS/Firewall Evasion II: Routing Manipulations & Path Control

Routing manipulation techniques alter the trajectory that IP datagrams travel across intermediate networks.

### Source Routing (RFC 791)
Under normal IP routing, the sending host only specifies the **Destination IP address**. Intermediate routers inspect their internal routing tables (BGP, OSPF) to independently decide the best hop-by-hop path to deliver the packet.

**Source Routing** allows the *sender* to explicitly specify the exact path (a list of intermediate router IP addresses) the packet must travel:
1. **Strict Source and Record Route (SSRR):** The sender specifies the exact, complete sequence of hops. If a router receives an SSRR packet and the next hop listed is not its directly connected neighbor, it **must drop the packet** with an ICMP routing error.
2. **Loose Source and Record Route (LSRR):** The sender specifies key "checkpoint" routers the packet must traverse, but allows intermediate routers to use standard routing algorithms to navigate between checkpoints.

```
       ATTACKER                                                  TARGET (Internal 10.0.0.5)
    (203.0.113.50)                                                     │
          │                                                            │
          │  1. Attacker crafts packet with Dst: 10.0.0.5             │
          │     LSRR Option: Traverse Trusted Router (198.51.100.1)    │
          │──────────────────────────┐                                 │
          │                          │                                 │
          ▼                          ▼                                 ▼
   [EDGE FIREWALL]          [TRUSTED PARTNER ROUTER]          [INTERNAL COMPUTE]
   (Blocks direct            (198.51.100.1)                    (10.0.0.5)
    inbound from              Traverses into internal           Accepts packet!
    203.0.113.50)             DMZ segment                       Returns traffic via
                              bypassing edge!                   specified reverse path!
```

#### Offensive Application:
- Bypassing perimeter firewalls by routing traffic through a trusted external partner or secondary network interface.
- Spoofing internal, private IP addresses (RFC 1918) while still receiving the return traffic by setting a reverse source-routed path.

#### Practical Syntax:
```bash
# Nmap Loose Source Routing through a specified gateway
nmap --ip-options "L 198.51.100.1 192.168.1.1" 10.0.0.50

# Nmap Strict Source Routing
nmap --ip-options "S 192.168.1.1 192.168.1.254" 10.0.0.50
```

#### Modern Countermeasure:
Under **RFC 1812 (Requirements for IP Version 4 Routers)**, modern network equipment drops source-routed packets by default. In Cisco IOS, this is enforced globally via:
```cisco
no ip source-route
```

---

## 10. Proxy Servers, Chaining & Anonymization Architecture

In offensive security assessments, direct scanning exposes the tester's public IP address to blacklisting, rate limiting, and defensive blocking. Pentesters employ **proxies** and **proxy chains** to obfuscate traffic origins and pivot through internal boundaries.

### Forward vs. Reverse vs. Transparent Proxies

```
+-----------------------------------------------------------------------------------+
|                        PROXY ARCHITECTURAL TAXONOMY                               |
+-----------------------------------------------------------------------------------+
| Proxy Type         | Position in Architecture       | Primary Function & Visibility|
+--------------------+--------------------------------+------------------------------+
| **Forward Proxy**  | Sits in front of the **client**| Client is explicitly aware;  |
|                    | (egress gateway).              | masks client identity from   |
|                    |                                | the external web.            |
| **Reverse Proxy**  | Sits in front of the **server**| Client is unaware; provides  |
|                    | (ingress gateway).             | load balancing, SSL/TLS      |
|                    |                                | termination, WAF protection. |
| **Transparent**    | Sits inline on the network     | Client is unaware; intercepts|
| **Proxy**          | cable / gateway router.        | traffic without client       |
|                    |                                | configuration (caching/DPI). |
+-----------------------------------------------------------------------------------+
```

---

### SOCKS4 vs. SOCKS5 Proxies

| Feature | SOCKS4 | SOCKS5 (RFC 1928) |
| :--- | :---: | :---: |
| **Layer of Operation** | Layer 5 (Session) | Layer 5 (Session) |
| **IPv6 Support** | ❌ No (IPv4 only) | ✅ Full IPv6 Support |
| **Authentication** | ❌ None | ✅ User/Password & GSS-API |
| **UDP Traffic Support** | ❌ TCP Streams Only | ✅ Supports UDP Datagrams |
| **Remote DNS Resolution** | ❌ No (Requires SOCKS4a extension)| ✅ Native Remote DNS Resolution |

---

### Proxy Chaining Mechanics
**Proxy Chaining** routes network traffic through a sequential series of intermediate proxies before reaching the ultimate destination. Each hop in the chain only knows the IP address of the node immediately preceding it.

```
+------------+       +------------+       +------------+       +------------+       +------------+
|  ATTACKER  | ----> |  PROXY #1  | ----> |  PROXY #2  | ----> |  PROXY #3  | ----> |   TARGET   |
|198.51.100.4|       | 104.28.1.5 |       | 45.33.22.8 |       | 185.19.0.2 |       | 203.0.113.8|
+------------+       +------------+       +------------+       +------------+       +------------+
                     (Knows Attacker      (Knows Proxy #1      (Knows Proxy #2      (Knows ONLY
                      & Proxy #2)          & Proxy #3)          & Target)            Proxy #3!)
```

#### Hands-On Configuration: `Proxychains-ng`
`Proxychains-ng` hooks dynamic library calls (`connect()`, `gethostbyname()`) via `LD_PRELOAD` to force any command-line tool's TCP connections through user-defined proxy chains.

File location: `/etc/proxychains4.conf` or `~/.proxychains/proxychains.conf`

```ini
# Chaining Mode Selection (Uncomment ONLY one mode)
# dynamic_chain: Traverses proxies in order; skips dead proxies automatically.
dynamic_chain

# strict_chain: Traverses proxies in exact order; fails entirely if one drops.
# strict_chain

# random_chain: Randomizes order from list; ideal for distributed fuzzing.
# random_chain

# CRITICAL SECURITY SETTING: Prevent DNS Leaking!
# Resolves domain names through the proxy list, not local ISP resolver!
proxy_dns

# Connection Timeouts
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
# Format: type host port [user] [pass]
# 1. Local Tor SOCKS5 Service
socks5  127.0.0.1  9050

# 2. Remote SSH Dynamic Port Forward (Pivot)
socks5  10.10.10.5 1080

# 3. Third-Party Egress Proxy
http    198.51.100.22 8080 admin P@ssw0rd123
```

#### Executing Scans through Proxychains:
```bash
# Execute an Nmap scan through the configured chain (MUST use -sT and -Pn)
proxychains4 nmap -Pn -sT -sV -p 80,443,22 203.0.113.8
```

> [!CAUTION] The Raw Socket Limitation of Proxies
> Proxies operate at Layer 5 (Session Layer). They handle completed TCP streams.
> **You CANNOT run raw packet scans (SYN `-sS`, FIN `-sF`, UDP `-sU`, OS detection `-O`) through standard SOCKS or HTTP proxies!**
> If you execute `proxychains nmap -sS target.com`, Nmap attempts to craft raw SYN packets which bypass the proxy hooks and leak your real IP address directly onto the wire! Always use `-sT -Pn` when routing through proxychains.

---

## 11. Banner Grabbing, Service Probing & OS Fingerprinting

Finding an open port is only the preliminary step; the attacker must identify the exact software daemon and operating system version running on that port to cross-reference with known CVEs.

### Active vs. Passive Banner Grabbing

```
+-----------------------------------------------------------------------------------+
|                      BANNER GRABBING & FINGERPRINTING TAXONOMY                    |
+-----------------------------------------------------------------------------------+
| Category | Mechanism                   | Tools Used        | Detection Risk       |
+----------+-----------------------------+-------------------+----------------------+
| **Active**| Establishes direct TCP/UDP  | Netcat, Telnet,   | High. Direct probe   |
|          | connection; transmits probe | Nmap (`-sV`),     | logged in target     |
|          | strings to elicit a banner. | OpenSSL, Curl.    | socket buffers.      |
| **Passive**| Sniffs ambient traffic on  | Wireshark, p0f,   | Zero. Transmits zero |
|          | the wire or queries cached  | NetworkMiner,     | packets to target;   |
|          | third-party intelligence.   | Shodan, Censys.   | reads packet headers.|
+-----------------------------------------------------------------------------------+
```

---

### Active Banner Grabbing Techniques & Syntax

#### 1. Raw Socket Probing with Netcat:
```bash
# Connect to FTP service (Port 21)
nc -nv 192.168.1.50 21
# Server Response: 220 (vsFTPd 2.3.4)

# Connect to HTTP service (Port 80) and send raw HTTP request
nc -nv 192.168.1.50 80
HEAD / HTTP/1.1
Host: 192.168.1.50

# Server Response:
# HTTP/1.1 200 OK
# Server: Apache/2.2.8 (Ubuntu) DAV/2
# X-Powered-By: PHP/5.2.4-2ubuntu5.10
```

#### 2. Encrypted Service Interrogation with OpenSSL:
```bash
# Connect to an SSL/TLS service (HTTPS/SMTPS) to extract SSL certificate & banner
openssl s_client -connect 192.168.1.50:443 -quiet
```

#### 3. Automated Service Fingerprinting with Nmap (`-sV`):
Nmap sends an array of complex probe strings defined in its `nmap-service-probes` database and compares responses against thousands of regular expression signatures.
```bash
# Service version detection with maximum probe intensity (0-9)
nmap -sV --version-intensity 9 192.168.1.50
```

---

### OS Fingerprinting: How Systems Leak Their Identity

#### Active OS Fingerprinting Mechanics (`nmap -O`)
Nmap transmits up to 16 engineered TCP, UDP, and ICMP probes containing rare or illegal flag combinations:
1. Probe with undefined TCP options.
2. Probe with `SYN|FIN|URG|PSH` set simultaneously.
3. UDP probe to a closed port to elicit an ICMP Port Unreachable.
4. Calculation of **ISN predictability** (how random the sequence numbers are).

Nmap compares the target's bitwise responses against its database of over 2,600 known operating system footprints (`nmap-os-db`).

#### Passive OS Fingerprinting Mechanics (p0f)
Passive fingerprinting analyzes packets generated by the target during normal operations without transmitting a single query. It relies on four key header fields:

```
+-----------------------------------------------------------------------------------+
|                        PASSIVE FINGERPRINTING SIGNATURE MATRIX                    |
+-----------------------------------------------------------------------------------+
| Operating System Family | Initial TTL | Default Window Size | Don't Fragment (DF)|
+-------------------------+-------------+---------------------+--------------------+
| **Linux (Kernel 3.x - 6.x)**| 64      | 5840 or 29200       | Set (1)            |
| **Microsoft Windows 10/11** | 128     | 8192 or 65535       | Set (1)            |
| **Cisco IOS / Solaris** | 255         | 4128                | Not Set (0)        |
| **FreeBSD / OpenBSD**   | 64          | 65535               | Set (1)            |
+-----------------------------------------------------------------------------------+
```

```bash
# Passively sniff interface eth0 for passing OS signatures using p0f
p0f -i eth0 -s /tmp/p0f.sock
```

---

## 12. Defensive Countermeasures & SOC Detection Engineering

Every scanning technique generates distinctive telemetry. A mature Security Operations Center (SOC) detects and neutralizes scanning activities long before an adversary transitions into exploitation.

### 1. Intrusion Detection Signatures (Snort & Suricata)

#### Rule A: Detect Inbound TCP Xmas Tree Scans
```snort
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"SCAN Xmas Scan Attempt Detected"; flags:FPU; flow:stateless; reference:arachnids,144; classtype:attempted-recon; sid:1000001; rev:1;)
```
- **Mechanics:** Inspects the TCP control bits for the simultaneous occurrence of `F` (FIN), `P` (PSH), and `U` (URG).

#### Rule B: Detect Inbound TCP NULL Scans
```snort
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"SCAN NULL Scan Attempt (Zero Flags)"; flags:0; flow:stateless; classtype:attempted-recon; sid:1000002; rev:1;)
```
- **Mechanics:** Flags set to `0` matches segments where all control bits are deactivated.

#### Rule C: Detect Rapid Port Sweeps (Horizontal & Vertical)
```snort
alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:"SCAN Potential Nmap Port Sweep"; flags:S; threshold:type both, track by_src, count 20, seconds 5; classtype:attempted-recon; sid:1000003; rev:1;)
```
- **Mechanics:** Triggers if an external IP sends more than 20 raw SYN packets across distinct ports within 5 seconds.

---

### 2. SIEM Telemetry & Threat Hunting Correlation (Splunk SPL)

#### Detecting Abnormal RST Spike Ratios (Indicator of Stealth SYN Scanning)
When an attacker runs an Nmap SYN scan across a subnet, closed ports return RSTs and open ports return SYN/ACKs which the attacker immediately resets. This generates an abnormally high volume of outbound RST packets relative to normal traffic:

```spl
index=firewall action=allowed
| stats count(eval(tcp_flags="RST")) as RST_Count, count(eval(tcp_flags="SYN")) as SYN_Count by src_ip, dest_ip
| eval Ratio = RST_Count / SYN_Count
| where Ratio > 5 AND RST_Count > 50
| table src_ip, dest_ip, SYN_Count, RST_Count, Ratio
```

---

### 3. Linux Kernel & Host Hardening Countermeasures

```bash
# 1. Enable TCP SYN Cookies (Mitigates SYN Flood queue exhaustion)
sysctl -w net.ipv4.tcp_syncookies=1

# 2. Ignore all incoming ICMP Echo Broadcasts (Smurf attack defense)
sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=1

# 3. Drop all IP Source Routed Packets at the Kernel level
sysctl -w net.ipv4.conf.all.accept_source_route=0
sysctl -w net.ipv4.conf.default.accept_source_route=0

# 4. Strip Web Server Banners (Apache Hardening: /etc/apache2/conf-enabled/security.conf)
# ServerTokens Prod
# ServerSignature Off
```

---

## 13. Big Picture: How It All Works Together

Network scanning does not occur in a vacuum. It represents the critical transition point where passive OSINT intelligence is converted into active tactical attack paths.

```
+-----------------------------------------------------------------------------------+
|                        THE COMPREHENSIVE SCANNING PIPELINE                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [PHASE 1: RECONNAISSANCE BLUEPRINT] (From Module 02 Footprinting)                |
|  - Validated CIDR: 198.51.100.0/24                                                |
|  - Target Perimeter: 254 IP addresses                                            |
|                                                                                   |
|                                       │                                           |
|                                       ▼                                           |
|  [STEP 1: HOST DISCOVERY / PROBING]                                               |
|  - ICMP Echo universally blocked.                                                 |
|  - Execute TCP SYN/ACK Probing: nmap -sn -PS443,80 -PA80 198.51.100.0/24          |
|  - Discover 3 Live Systems: 198.51.100.10, 198.51.100.25, 198.51.100.50         |
|                                                                                   |
|                                       │                                           |
|                                       ▼                                           |
|  [STEP 2: FIREWALL RULESET MAPPING]                                               |
|  - Send ACK Probes (-sA) to map stateful boundaries.                              |
|  - Identify that 198.51.100.50 has an unmonitored legacy stateless firewall.     |
|                                                                                   |
|                                       │                                           |
|                                       ▼                                           |
|  [STEP 3: STEALTH PORT SCANNING & EVASION]                                        |
|  - Apply Fragmentation (-f) and Source Port Masking (-g 53).                      |
|  - Run Half-Open SYN Scan: nmap -sS -p 1-1024 -g 53 -f 198.51.100.50             |
|  - Identify Open Ports: 21 (FTP), 80 (HTTP), 3306 (MySQL).                        |
|                                                                                   |
|                                       │                                           |
|                                       ▼                                           |
|  [STEP 4: SERVICE FINGERPRINTING & BANNER GRABBING]                               |
|  - Connect and elicit service greeting: nc -nv 198.51.100.50 21                   |
|  - Banner Revealed: "220 vsFTPd 2.3.4"                                            |
|                                                                                   |
|                                       │                                           |
|                                       ▼                                           |
|  [STEP 5: TRANSITION TO ENUMERATION & EXPLOITATION]                               |
|  - Cross-reference banner with CVE-2011-2523 (vsFTPd Smiley Backdoor).           |
|  - Target verified vulnerable; Red Team initiates Phase 4 Enumeration!            |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 14. Real-Time Technical Scenario: Red Team Assessment vs. SOC Response

### Engagement Context
- **Target Organization:** `Vanguard Health Systems` (`vanguard-health.lab`)
- **Authorized Scope:** External network penetration test against primary DMZ (`198.51.100.0/28`).
- **Red Team Objective:** Map perimeter infrastructure, identify an entry vector into the DMZ, and evade detection by the organization's Palo Alto Next-Gen Firewall (NGFW).
- **Blue Team Objective:** Detect unauthorized scanning patterns, correlate IOCs, and implement automated firewall shunning.

---

### Step-by-Step Scenario Progression

#### Step 1: Initial Discovery & Probe Evasion (Red Team)
1. **The Trap:** The Red Team initially fires a standard ping sweep:
   ```bash
   nmap -sn 198.51.100.0/28
   ```
   - *Result:* All 16 hosts report down. The Palo Alto firewall silently drops all external ICMP Type 8 Echo Requests.
2. **The Pivot:** The Red Team switches to a multi-vector TCP SYN/ACK discovery probe targeting standard enterprise ports (80, 443, 8080, 445):
   ```bash
   nmap -sn -PS80,443,8080 -PA445 198.51.100.0/28
   ```
   - *Result:* Host `198.51.100.12` returns a `[SYN/ACK]` on port 443; Host `198.51.100.14` returns a `[RST]` on port 445. Both hosts are confirmed **live**!

#### Step 2: Covert Scanning via Zombie Host (Red Team)
1. **Hunting for an Idle Host:** The Red Team discovers an unmanaged, legacy multifunction office printer on an adjacent staging subnet (`198.51.100.200`) exhibiting predictable global IPID increments:
   ```bash
   nmap -p80 --script ipidseq 198.51.100.200
   ```
   - *Result:* `IP ID Sequence Generation: Incremental! Valid Zombie candidate.`
2. **Executing the Idle Scan:** The Red Team scans target `198.51.100.14` through the zombie:
   ```bash
   nmap -Pn -sI 198.51.100.200:80 -p 21,22,80,443,3389 198.51.100.14
   ```
   - *Result:* Port 22 (SSH) and Port 80 (HTTP) return an IPID delta of $+2$ (**OPEN**).
   - *Critical Telemetry:* The target firewall logs incoming connection probes originating **exclusively from the internal printer (`198.51.100.200`)**. The Red Team's true IP never appears in the target's perimeter access logs!

#### Step 3: Banner Grabbing via Proxy Chaining (Red Team)
1. The Red Team routes a service version interrogation through Tor and an internal compromised pivot using `proxychains4`:
   ```bash
   proxychains4 curl -s -I http://198.51.100.14/
   ```
   - *Banner Extracted:*
     ```http
     HTTP/1.1 200 OK
     Server: Apache/2.4.49 (Unix)
     X-Backend-Server: web-node-01.internal
     ```
   - *Vulnerability Correlation:* Apache 2.4.49 is immediately flagged for **CVE-2021-41773** (Path Traversal & Remote Code Execution).

#### Step 4: SOC Detection, Correlation & Containment (Blue Team)
1. **SIEM Anomaly Detection:** Vanguard's Splunk SIEM fires a high-priority alert triggered by an unusual internal traffic flow:
   - `Alert: High Volume RST Packets from Internal Asset (198.51.100.200 - Office Printer) targeting DMZ Server (198.51.100.14)`.
2. **Suricata Network Telemetry Analysis:**
   - The SOC analyst pivots into Zeek/Suricata connection logs. They observe that `198.51.100.200` has established zero prior HTTP/DNS requests, yet suddenly fired alternating SYN/ACK and RST sequences across 5 consecutive destination ports.
   - The analyst immediately recognizes the signature of an **Idle (Zombie) Scan**.
3. **Forensic Traceback & Containment:**
   - The analyst inspects network switches and isolates the vulnerable printer port onto a dead VLAN.
   - Perimeter firewall logs are queried for external systems probing the printer's IPID on port 80 just prior to the attack. The query isolates the Red Team's real external IP address (`203.0.113.88`).
   - The SOC issues an automated block rule on the Palo Alto NGFW for `203.0.113.88`.
   - The web server administrator is notified to patch Apache 2.4.49 to 2.4.51 immediately, mitigating the imminent RCE vulnerability before exploitation occurs.

---

## 15. Hands-On Lab Methodology & Troubleshooting (Failed Attempts & Why)

When learning network scanning in an authorized laboratory environment, scans will frequently fail or produce misleading data. Use this scientific troubleshooting framework to diagnose issues:

### Failure Scenario 1: The "Everything is Open" Inverse Scan
- **What was tried:** Executing a FIN scan (`nmap -sF 192.168.1.75`) or Xmas scan against a remote target.
- **Result:** Nmap reports all 1,000 scanned ports are `open|filtered`.
- **Fact:** RFC 793 states open ports drop the packet without replying, while closed ports reply with RST.
- **Observation:** Target sent zero packets back across all 1,000 ports.
- **Hypothesis:** A stateful perimeter firewall is dropping all incoming non-SYN packets, OR the host is running Microsoft Windows.
- **Test:** Run an active OS detection probe (`nmap -O 192.168.1.75`) or check TTL via a ping (`ping -c 1 192.168.1.75`).
- **Conclusion:** TTL returns 128 (Windows). Windows kernels reply with RST to closed ports, but firewalls drop them. If a firewall drops them, Nmap cannot distinguish between an open port dropping the packet and a firewall dropping the packet. **Inverse scans are invalid against this target.**

---

### Failure Scenario 2: Proxychains Leaks the Attacker's True IP
- **What was tried:** The operator configured `/etc/proxychains4.conf` and executed:
  ```bash
  proxychains nmap -sS -p 80,443 10.0.0.15
  ```
- **Result:** The target firewall logged the scan as originating directly from the operator's real IP address, completely bypassing the proxy chain.
- **Root Cause (Why it failed):** Proxies function at Layer 5/7 using the OS `connect()` API. The `-sS` flag instructs Nmap to craft **raw Layer 3/4 Ethernet and IP frames** via AF_PACKET/libpcap. Raw sockets bypass the user-space socket wrappers hooked by `LD_PRELOAD`.
- **What that tells us:** You cannot execute raw socket operations through standard user-space proxy wrappers.
- **Corrective Action:** Always specify the full TCP connect scan switch:
  ```bash
  proxychains nmap -Pn -sT -p 80,443 10.0.0.15
  ```

---

### Failure Scenario 3: Idle Scan Returns False "All Ports Closed"
- **What was tried:** Executing an Idle scan using an identified zombie host (`nmap -Pn -sI 192.168.1.105 10.0.0.20`).
- **Result:** Every single port on the target is reported as `closed`.
- **Root Cause (Why it failed):** The zombie host was not truly "idle." Background processes (NTP updates, Windows telemetry, browsing) were generating ambient traffic, causing the IPID to increment by unpredictable numbers (e.g., $+5, +12$).
- **What that tells us:** Nmap's delta calculations require a clean $+1$ vs $+2$ mathematical difference. High ambient noise invalidates the zombie.
- **Corrective Action:** Validate the zombie's absolute silence using Hping3 before launching the scan:
  ```bash
  hping3 -S -r 192.168.1.105 -p 80 -c 10
  ```
  Ensure the IPID increments strictly by $+1$ per packet with zero gaps.

---

## 16. My Understanding Check

Test your mastery of the concepts covered in this module. Review each scenario thoroughly and formulate your technical justification:

1. **TCP State Machine Nuance:** You send a crafted TCP segment with `[SYN = 1, FIN = 1]` to an open port on a target server. According to RFC 793, what should the target do, and what does it tell you if the target returns a `[SYN, ACK]` versus a `[RST]`?
2. **SYN Cookie Cryptographic Impact:** If a target web server has TCP SYN Cookies enabled (`net.ipv4.tcp_syncookies = 1`), how does this alter the outcome of an attacker running a traditional TCP SYN Flood attack using spoofed IP addresses? What specific kernel data structure is protected?
3. **Firewall Filter Mapping:** During an assessment, you execute an ACK scan (`nmap -sA -p 22,80,443 target.com`). For port 22, you receive a `[RST]` packet with `TTL = 64` and `Window Size = 0`. For port 80, you receive no response. What is the exact filtering posture of port 22 versus port 80?
4. **The Idle Scan Math:** In an Idle Scan, suppose the zombie host's initial IPID is 4000. The attacker forges 5 SYN packets to 5 distinct closed ports on the target spoofing the zombie. The attacker then probes the zombie again. What will the zombie's new IPID be? What would it be if 2 of those ports had been open?
5. **Fragmentation vs. Stateful Reassembly:** Why does standard packet fragmentation (`nmap -f`) fail to evade a modern Next-Generation Firewall (such as a Fortinet FortiGate or Palo Alto NGFW) configured with full stream inspection?
6. **Proxychains DNS Leakage:** An analyst runs `proxychains curl http://internal-payroll.corp` on an external engagement. Even though proxychains is routing HTTP through a remote SOCKS5 proxy, the corporate SOC immediately detects the analyst's real home IP. What exact misconfiguration occurred in `proxychains.conf`?
7. **OS Fingerprinting via TTL:** You ping two hosts on the same local subnet. Host A returns `TTL = 64`, while Host B returns `TTL = 128`. What can you deduce about the underlying operating systems of Host A and Host B before running any port scan?
8. **TCP Connect vs. SYN Stealth Logging:** Why does a TCP Connect scan (`-sT`) generate log entries in `/var/log/apache2/access.log` while a TCP SYN scan (`-sS`) against port 80 generates zero log entries in that same file?

---

*End of Module 03 Study Notes. Continue to Module 04: Enumeration.*
