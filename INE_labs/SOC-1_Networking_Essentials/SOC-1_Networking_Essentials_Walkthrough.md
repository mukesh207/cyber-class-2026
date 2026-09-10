# INE SOC-1: Networking Essentials — Detailed Walkthrough

> **Course:** INE – Core Skills for SOC Analysts  
> **Lab:** SOC-1: Networking Essentials  
> **Purpose:** Build practical networking and SOC investigation fundamentals.

---

## 1. Lab Overview

Networking knowledge is one of the most important foundations for a SOC analyst.

In this lab, we work from both the **system perspective** and the **network perspective**:

```text
Network Configuration
        ↓
Routing & DNS
        ↓
Listening Services
        ↓
Network Scanning
        ↓
Authentication / Web Activity
        ↓
Packet Capture
        ↓
Firewall Logs
        ↓
SOC Investigation
```

The main goal is not just to run commands. The goal is to understand:

- What is happening on a system?
- Which network services are exposed?
- Where is the traffic coming from?
- What does the activity look like in packets?
- What evidence is recorded in logs?
- How can a SOC analyst correlate these observations?

> **Note:** IP addresses, usernames, passwords, ports and other values can differ between lab instances. Use the values provided by your own INE lab.

---

# 2. Identifying Network Configuration

## Step 1: Analyze Network Interfaces and IP Addresses

Run:

```bash
ip a
```

This displays information about network interfaces, including:

- Interface names
- IP addresses
- MAC addresses
- Interface state
- IPv4 addresses
- IPv6 addresses

### Ubuntu

A typical system may contain:

```text
lo
ens5
```

### Kali Attacker

The Kali machine may have multiple interfaces, for example:

```text
eth0
eth1
```

If Kali has two active interfaces, it means the machine is connected to two different network segments.

This is common in security labs because the attacker machine may need connectivity to multiple networks.

### Important Interfaces

#### Loopback — `lo`

The loopback interface allows a computer to communicate with itself.

The IPv4 loopback range is:

```text
127.0.0.0/8
```

The most commonly used address is:

```text
127.0.0.1
```

Applications commonly use loopback addresses to communicate with services running on the same machine.

#### Main Network Interface

An interface such as `ens5`, `eth0`, or `wlan0` connects the system to a network.

It may provide connectivity to:

- LAN
- Other systems
- Servers
- Internet
- Other network segments

---

## Understanding the MAC Address

In the output of `ip a`, you may see something similar to:

```text
link/ether 06:6d:e6:87:9f:b7
```

This is the **MAC address** of the network interface.

A MAC address is a Layer 2 hardware/link-layer identifier used for communication on a local network.

> In virtual machines, the MAC address is usually assigned to the virtual network adapter.

---

## Understanding IPv4

You may see an address such as:

```text
10.0.17.231/20
```

IPv4 addresses are 32-bit logical network addresses.

The `/20` is the CIDR prefix length and tells us how much of the address represents the network portion.

---

## Understanding IPv6

You may also see an address similar to:

```text
fe80::46d:e6ff:fe87:9fb7/64
```

This is an IPv6 address.

Addresses beginning with:

```text
fe80::
```

are IPv6 link-local addresses.

They are normally used for communication on the local network segment.

---

# 3. Display the Host IP Address

Run:

```bash
hostname -I
```

This displays the IP addresses assigned to the host, generally excluding the loopback address.

Example:

```text
10.0.17.231
```

On a machine with multiple interfaces, multiple addresses may be displayed.

### Why is this useful for a SOC analyst?

It provides a quick way to determine:

- Which IP addresses belong to the system
- Which networks the system may be connected to
- Which address should be used when testing connectivity

---

# 4. Understanding the Routing Table

Run:

```bash
ip route
```

The routing table determines **where network traffic should be sent**.

A typical output may contain:

```text
default via 10.0.16.1 dev ens5
10.0.16.0/20 dev ens5 proto kernel scope link src 10.0.17.231
10.0.16.1 dev ens5 proto dhcp scope link
```

## Default Route

The important part is:

```text
default via 10.0.16.1 dev ens5
```

The default route is used when no more specific route matches the destination.

In simple terms:

```text
Unknown destination
       ↓
Default gateway
       ↓
10.0.16.1
```

The default gateway acts as the next-hop router for traffic leaving the local network.

---

## Local Network Route

For example:

```text
10.0.16.0/20 dev ens5
```

This tells the system that destinations belonging to that network are directly reachable through `ens5`.

Traffic to a local destination does **not** need to use the default gateway.

---

## Check the Route to a Specific Destination

A useful command is:

```bash
ip route get 8.8.8.8
```

This asks Linux:

> "Which route would you use to reach 8.8.8.8?"

This is useful when troubleshooting connectivity and routing problems.

---

# 5. DNS Configuration and Resolution

DNS translates domain names into IP addresses.

For example:

```text
google.com
     ↓
DNS
     ↓
IP address
```

## Step 1: Check DNS Configuration

Run:

```bash
cat /etc/resolv.conf
```

You may see:

```text
nameserver 127.0.0.53
```

or another resolver address.

### What does `127.0.0.53` mean?

It is a local DNS stub resolver commonly associated with `systemd-resolved`.

The application sends the DNS request to the local resolver, which then forwards it to an upstream DNS server.

---

## Step 2: Find the Upstream DNS Server

Run:

```bash
resolvectl status
```

Look for:

```text
DNS Servers
```

The output may show an address such as:

```text
10.0.0.2
```

The exact address depends on the lab environment.

---

## DNS in Containerized Environments

In some Docker environments, `/etc/resolv.conf` may show:

```text
nameserver 127.0.0.11
```

Docker provides an internal DNS resolver for containers.

This demonstrates an important SOC concept:

> DNS behavior can differ depending on whether a system is a traditional host, virtual machine, or container.

---

# 6. Ports and Services

## Step 1: Identify Listening Services

Run:

```bash
ss -tulnp
```

The command displays network sockets and listening services.

### Understanding the options

```text
-t  → TCP
-u  → UDP
-l  → Listening sockets
-n  → Numeric addresses and ports
-p  → Process information
```

Therefore:

```bash
ss -tulnp
```

means:

> Show TCP and UDP listening sockets with numeric addresses and the processes using them.

You may see:

```text
LISTEN 0 128 0.0.0.0:22
```

This indicates that a service is listening on TCP port `22`.

---

## Important SOC Observation: Bind Address

Compare:

```text
127.0.0.1:5432
```

with:

```text
0.0.0.0:5432
```

### `127.0.0.1`

The service is listening only on the local machine.

Other network hosts normally cannot directly connect to it.

### `0.0.0.0`

The service is listening on all IPv4 interfaces.

This can make the service reachable from other network hosts, depending on routing and firewall rules.

This distinction is important when identifying attack surface.

---

# 7. Network Scanning with Nmap

From the Kali attacker machine, scan the target:

```bash
nmap -sS <TARGET_IP>
```

Example:

```bash
nmap -sS 10.0.17.231
```

> Replace `<TARGET_IP>` with the IP address assigned by your lab.

## What is Nmap?

Nmap (Network Mapper) is commonly used to:

- Discover hosts
- Identify open ports
- Identify services
- Perform security auditing
- Understand network exposure

---

## What does `-sS` mean?

```bash
-sS
```

performs a TCP SYN scan.

The scanner sends a TCP SYN packet and analyzes the response.

Simplified behavior:

```text
SYN
 ↓
Target
 ↓
SYN/ACK → Port likely open
RST     → Port closed
```

The scan does not normally complete a full TCP connection for every discovered port.

---

## Understanding the Nmap Output

If Nmap reports:

```text
Host is up
```

the target is reachable.

You may see results such as:

```text
22/tcp    open    ssh
80/tcp    open    http
3389/tcp  open    ms-wbt-server
5910/tcp  open    ...
```

The exact ports may differ between lab instances.

### Closed Ports

Nmap may report that many ports are closed.

A TCP RST response generally indicates that the host received the connection attempt but no service is listening on that port.

This is different from a filtered port, where a firewall or filtering device may prevent the scanner from determining the port state.

---

# 8. Mapping Ports to Services

Common examples:

| Port | Service | Purpose |
|---|---|---|
| 22/TCP | SSH | Secure remote administration |
| 80/TCP | HTTP | Web traffic |
| 3389/TCP | RDP | Remote desktop access |
| 5910/TCP | Often VNC-related | Remote graphical access |

> Service identification from a port number alone is not guaranteed. Tools such as Nmap can perform service detection for additional information.

For example:

```bash
nmap -sV <TARGET_IP>
```

The `-sV` option attempts to identify service versions.

---

# 9. Network Traffic Generation

Now we generate normal and suspicious-looking traffic and observe the evidence it creates.

---

# 10. Connectivity Testing with Ping

From Kali:

```bash
ping -c 4 <TARGET_IP>
```

Example:

```bash
ping -c 4 10.0.27.36
```

The `-c 4` option sends four ICMP packets.

## How Ping Works

Ping uses **ICMP**.

The basic process is:

```text
Kali
 |
 | ICMP Echo Request
 ↓
Ubuntu
 |
 | ICMP Echo Reply
 ↓
Kali
```

Ping can help determine whether a host is reachable and whether there is packet loss or latency.

### SOC Perspective

ICMP traffic can be legitimate, but it can also be useful during reconnaissance.

Therefore, context matters.

---

# 11. SSH Connection and Authentication Logs

From Kali:

```bash
ssh sshuser@<TARGET_IP>
```

Use the credentials provided by the INE lab.

After connecting, switch to the Ubuntu machine and inspect the authentication log:

```bash
sudo tail -f /var/log/auth.log
```

You may see an entry similar to:

```text
sshd[9171]: Accepted password for sshuser from <SOURCE_IP> port 41194 ssh2
```

## Understanding the Log

```text
Accepted password
```

The authentication was successful.

```text
sshuser
```

The account that authenticated.

```text
<SOURCE_IP>
```

The source IP address of the connection.

```text
41194
```

The client's ephemeral source port.

```text
ssh2
```

The SSH protocol version.

---

## SOC Investigation Perspective

An analyst can use this information to ask:

- Who logged in?
- Was the login successful?
- Where did the connection originate?
- When did it happen?
- Was the source IP expected?
- Were there previous failed attempts?

This is a simple example of **log-based investigation**.

---

# 12. Testing the HTTP Service

From Kali:

```bash
curl http://<TARGET_IP>/
```

You can also request another endpoint:

```bash
curl http://<TARGET_IP>/admin
```

`curl` sends an HTTP request to the web server.

The request is essentially:

```text
GET /
```

or:

```text
GET /admin
```

---

# 13. Analyze Apache Web Logs

On Ubuntu:

```bash
sudo tail -f /var/log/apache2/access.log
```

Apache access logs can contain information such as:

- Source IP
- Timestamp
- HTTP method
- Requested path
- HTTP status code
- User-Agent
- Response size

For example, a request generated by `curl` may have a User-Agent containing:

```text
curl
```

### SOC Perspective

A SOC analyst can identify patterns such as:

```text
Same source IP
      ↓
Many requests
      ↓
Different URLs
      ↓
404 / 403 responses
      ↓
Possible enumeration
```

Logs become evidence that can be correlated with network traffic.

---

# 14. Simulate a TCP Connection with Netcat

> Perform this only inside the authorized INE lab environment.

On Ubuntu:

```bash
nc -lnvp 4444
```

This starts a Netcat listener.

### Options

```text
-l  → Listen
-n  → Do not perform DNS resolution
-v  → Verbose output
-p  → Specify local port
```

The system is now listening on TCP port `4444`.

Check it with:

```bash
ss -tulnp
```

You should see the listener.

---

## Connect from Kali

```bash
nc <TARGET_IP> 4444
```

This initiates a TCP connection to port `4444`.

You can now observe the TCP connection using:

```bash
ss -tnp
```

You may see:

```text
LISTEN
ESTABLISHED
```

### What is happening?

The original listening socket remains:

```text
LISTEN
```

When Kali connects, a separate connection becomes:

```text
ESTABLISHED
```

This demonstrates an important TCP concept:

```text
Listening Socket
       ↓
Incoming Connection
       ↓
Established Socket
```

---

# 15. Packet Capture with Wireshark

Wireshark allows us to inspect network packets directly.

## Step 1: Start Wireshark

Open Wireshark and select the appropriate network interface.

Start the capture.

---

# 16. Capture an Nmap Scan

Start the Wireshark capture.

From Kali:

```bash
nmap -sS <TARGET_IP>
```

Stop the capture after the scan finishes.

A SYN scan can generate traffic similar to:

```text
SYN
 ↓
Target
 ↓
SYN/ACK
```

for open ports.

For closed ports, the response may be:

```text
SYN
 ↓
Target
 ↓
RST
```

---

## SOC Perspective

An Nmap scan can generate a recognizable pattern:

```text
One source IP
     ↓
Many destination ports
     ↓
Many SYN packets
     ↓
SYN/ACK or RST responses
```

This can be an indicator of reconnaissance.

However, a SOC analyst should not automatically classify every port scan as malicious. Context, source, timing and environment matter.

---

# 17. Simulating SSH Login Attempts

Start a new Wireshark capture.

From Kali:

```bash
ssh sshuser@<TARGET_IP>
```

Use incorrect passwords for the lab exercise if the lab asks you to simulate failed authentication.

Stop the capture.

Apply:

```text
tcp.port == 22
```

This display filter isolates TCP traffic associated with SSH.

---

## What Can Wireshark Show?

You can observe:

- Source IP
- Destination IP
- TCP handshake
- SSH traffic
- Packet timing
- Connection attempts

SSH payload is encrypted, so the password itself should not be visible in the packet capture.

This is an important security concept:

> Packet capture can reveal metadata and connection behavior even when application data is encrypted.

---

# 18. Directory Enumeration with DIRB

Start a Wireshark capture.

From Kali:

```bash
dirb http://<TARGET_IP>
```

DIRB attempts to discover web directories and files using a wordlist.

It generates many HTTP requests.

Example pattern:

```text
GET /admin
GET /login
GET /backup
GET /test
GET /...
```

The actual paths depend on the target and wordlist.

---

# 19. Analyze Directory Enumeration in Wireshark

Stop the capture and apply:

```text
http
```

You may see many HTTP GET requests.

Common responses may include:

```text
404 Not Found
403 Forbidden
200 OK
```

### SOC Perspective

Repeated requests to many different paths in a short period can indicate automated enumeration.

For example:

```text
Source IP
   ↓
GET /admin
GET /backup
GET /test
GET /login
GET /...
   ↓
Many 404/403 responses
```

This pattern is more suspicious than a normal user requesting one or two pages.

---

# 20. Follow an HTTP Stream

Right-click an HTTP packet and select:

```text
Follow → HTTP Stream
```

This reconstructs the HTTP conversation.

It helps analysts inspect:

- HTTP request
- HTTP response
- Headers
- Requested path
- Server response

This is useful when investigating suspicious web activity.

---

# 21. Firewall Logging with UFW

UFW stands for **Uncomplicated Firewall**.

## Step 1: Enable UFW

On Ubuntu:

```bash
sudo ufw enable
```

> Be careful when enabling a firewall on a remote system. In real environments, ensure required management access is allowed first.

---

## Step 2: Check Firewall Status

Run:

```bash
sudo ufw status verbose
```

This shows:

- Firewall status
- Default policies
- Configured rules
- Logging information

---

# 22. Generate Blocked Traffic

From Kali, attempt a connection to a port that should be blocked:

```bash
nc -v <TARGET_IP> 23
```

Port `23` is traditionally associated with Telnet.

If no service is intentionally exposed and the firewall blocks the traffic, UFW can generate a log entry.

---

# 23. Inspect UFW Logs

On Ubuntu:

```bash
sudo cat /var/log/ufw.log
```

You may see something similar to:

```text
[UFW BLOCK] IN=ens5 OUT=
SRC=10.10.38.19 DST=10.0.17.231
PROTO=TCP SPT=53958 DPT=23
```

## Important Fields

### Action

```text
[UFW BLOCK]
```

The firewall blocked the packet.

### Interface

```text
IN=ens5
```

The interface through which the packet arrived.

### Source IP

```text
SRC=<SOURCE_IP>
```

The system that initiated the traffic.

### Destination IP

```text
DST=<DESTINATION_IP>
```

The system receiving the traffic.

### Protocol

```text
PROTO=TCP
```

The transport protocol.

### Source Port

```text
SPT=53958
```

The ephemeral source port.

### Destination Port

```text
DPT=23
```

The destination service/port being targeted.

---

# 24. SOC Correlation

This is where the lab becomes especially useful from a SOC perspective.

Imagine an analyst sees:

### Event 1 — Nmap

```text
Source → Many destination ports
```

Possible reconnaissance.

### Event 2 — SSH Attempts

```text
Source IP → TCP/22
Multiple authentication attempts
```

Possible credential attack.

### Event 3 — Web Enumeration

```text
Source IP → Many HTTP GET requests
Many 404/403 responses
```

Possible directory enumeration.

### Event 4 — Firewall Block

```text
Source IP → TCP/23
UFW BLOCK
```

A blocked connection attempt.

These events can be correlated:

```text
Reconnaissance
      ↓
Service discovery
      ↓
Authentication attempts
      ↓
Web enumeration
      ↓
Blocked connection
      ↓
SOC investigation
```

The key skill is **correlation**, not looking at one log entry in isolation.

---

# 25. Important Commands from the Lab

| Command | Purpose |
|---|---|
| `ip a` | Display network interfaces and addresses |
| `hostname -I` | Display host IP addresses |
| `ip route` | Display routing table |
| `ip route get <IP>` | Determine route to a destination |
| `cat /etc/resolv.conf` | View DNS resolver configuration |
| `resolvectl status` | View DNS configuration and upstream servers |
| `ss -tulnp` | Display listening TCP/UDP services |
| `nmap -sS <IP>` | Perform TCP SYN scan |
| `nmap -sV <IP>` | Attempt service/version detection |
| `ping -c 4 <IP>` | Test ICMP connectivity |
| `ssh user@<IP>` | Test SSH connectivity |
| `curl http://<IP>/` | Send an HTTP request |
| `tail -f /var/log/auth.log` | Monitor authentication logs |
| `tail -f /var/log/apache2/access.log` | Monitor Apache access logs |
| `nc -lnvp 4444` | Start a Netcat listener |
| `nc <IP> 4444` | Connect to a Netcat listener |
| `dirb http://<IP>` | Perform web directory enumeration |
| `sudo ufw status verbose` | View firewall status |
| `sudo cat /var/log/ufw.log` | View UFW firewall logs |

---

# 26. Key Concepts Learned

## Networking

- Network interfaces
- MAC addresses
- IPv4
- IPv6
- Loopback
- CIDR
- Routing
- Default gateway

## DNS

- `/etc/resolv.conf`
- Local DNS stub resolvers
- Upstream DNS servers
- DNS in containerized environments

## Services

- TCP and UDP
- Listening sockets
- Ports
- Bind addresses
- Service exposure
- Attack surface

## Reconnaissance

- Nmap
- TCP SYN scans
- Port states
- Service identification

## Authentication Monitoring

- SSH
- Authentication logs
- Source IP
- Successful and failed login attempts

## Web Monitoring

- HTTP
- Apache access logs
- HTTP status codes
- Directory enumeration
- User-Agent information

## Network Analysis

- Wireshark
- TCP handshake
- SYN/SYN-ACK/RST
- Display filters
- HTTP streams
- Traffic patterns

## Firewall Monitoring

- UFW
- Blocked traffic
- Source/destination IP
- Source/destination port
- Firewall logs

---

# 27. SOC Analyst Perspective

The most important lesson from this lab is that **network activity generates multiple types of evidence**.

For example:

```text
              Network Activity
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
     Packets        Logs       Services
        │            │            │
    Wireshark    auth.log     ss / Nmap
        │            │            │
        └────────────┼────────────┘
                     ↓
               Event Correlation
                     ↓
               SOC Investigation
```

A SOC analyst should learn to answer:

1. **Who** generated the activity?
2. **What** happened?
3. **When** did it happen?
4. **Where** did it originate?
5. **Which service or port** was targeted?
6. **Was the activity successful?**
7. **Is the behavior normal or suspicious?**
8. **What additional evidence should be investigated?**

---

# 28. Final Takeaway

This lab demonstrates the relationship between **networking fundamentals and SOC operations**.

A strong SOC analyst needs to understand not only security tools, but also the underlying network behavior.

The practical workflow demonstrated here is:

```text
Understand the Network
        ↓
Identify Services
        ↓
Generate / Observe Traffic
        ↓
Capture Packets
        ↓
Review Logs
        ↓
Correlate Evidence
        ↓
Identify Suspicious Behavior
        ↓
Investigate
```

The biggest takeaway is:

> **Learn what normal network behavior looks like first. Then suspicious behavior becomes much easier to recognize.**

---

## Lab Reference

INE – Core Skills for SOC Analysts  
**SOC-1: Networking Essentials**

For the official step-by-step lab instructions and screenshots, refer to the **Solution** tab in the INE lab.
