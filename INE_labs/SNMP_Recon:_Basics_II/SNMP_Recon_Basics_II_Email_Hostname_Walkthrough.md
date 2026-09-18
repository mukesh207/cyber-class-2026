# SNMP Recon: Basics II --- Target Information Enumeration

## Lab Objective

This section documents two SNMP enumeration tasks performed against the
lab target:

1.  Find the email address from the target using `snmpwalk`
2.  Find the hostname of the target machine

> **Lab Target:** `192.164.123.3`\
> **SNMP Version:** SNMPv2c\
> **Community String:** `public`

------------------------------------------------------------------------

## 1. Find the Email Address from the Target Using `snmpwalk`

### Objective

The goal is to retrieve the **system contact information** from the
target using SNMP.

The SNMP `sysContact` value is stored under the following OID:

``` text
1.3.6.1.2.1.1.4
```

### Command

``` bash
snmpwalk -v2c -c public 192.164.123.3 1.3.6.1.2.1.1.4
```

### Command Breakdown

  -----------------------------------------------------------------------
  Option / Value                      Description
  ----------------------------------- -----------------------------------
  `snmpwalk`                          Queries a target through SNMP and
                                      walks the selected OID

  `-v2c`                              Uses SNMP version 2c

  `-c public`                         Uses `public` as the SNMP community
                                      string

  `192.164.123.3`                     IP address of the lab target

  `1.3.6.1.2.1.1.4`                   OID for `sysContact`
  -----------------------------------------------------------------------

### Output

The command returned:

``` text
SNMPv2-MIB::sysContact.0 = STRING: admin <admin@pentesteracademylabs.xyz>
```

### Result

The email address associated with the target is:

``` text
admin@pentesteracademylabs.xyz
```

### Screenshot

![SNMP sysContact Enumeration](screenshots/snmpwalk%20-v2c%20-c%20public%20192.164.123.3%201.3.6.1.2.1.1.4.png)

------------------------------------------------------------------------

## 2. Find the Hostname of the Target Machine

### Objective

The goal is to retrieve the hostname of the target system through SNMP.

The target hostname is stored in the SNMP `sysName` object, which uses
the following OID:

``` text
1.3.6.1.2.1.1.5
```

### Command

``` bash
snmpwalk -v2c -c public 192.164.123.3 1.3.6.1.2.1.1.5
```

### Command Breakdown

  Option / Value      Description
  ------------------- -----------------------------------------
  `snmpwalk`          Queries the target through SNMP
  `-v2c`              Uses SNMP version 2c
  `-c public`         Uses the `public` SNMP community string
  `192.164.123.3`     IP address of the lab target
  `1.3.6.1.2.1.1.5`   OID for `sysName`

### Output

The command returned:

``` text
SNMPv2-MIB::sysName.0 = STRING: victim-1
```

### Result

The hostname of the target machine is:

``` text
victim-1
```

### Screenshot

![SNMP sysName Enumeration](screenshots/snmpwalk%20-v2c%20-c%20public%20192.164.123.3%201.3.6.1.2.1.1.5.png)

------------------------------------------------------------------------

## Final Answers

  Question        Answer
  --------------- ----------------------------------
  Email address   `admin@pentesteracademylabs.xyz`
  Hostname        `victim-1`

## Key Takeaways

-   `snmpwalk` can retrieve individual SNMP objects by querying their
    OIDs.
-   `1.3.6.1.2.1.1.4` corresponds to the target's **system contact
    (`sysContact`)** information.
-   `1.3.6.1.2.1.1.5` corresponds to the target's **system name
    (`sysName`)**.
-   In this lab, the target was `192.164.123.3` and accepted the
    `public` SNMP community string.
