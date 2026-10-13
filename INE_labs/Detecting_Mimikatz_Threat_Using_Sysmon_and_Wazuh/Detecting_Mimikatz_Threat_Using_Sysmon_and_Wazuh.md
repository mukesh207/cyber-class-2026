# Detecting Mimikatz Threat Using Sysmon and Wazuh

> **Lab:** INE Skill Dive — Detecting Mimikatz Threat Using Sysmon and Wazuh  
> **Category:** Cybersecurity / Blue Team / SOC  
> **Difficulty:** Advanced  
> **Status:** Completed in the INE lab environment  
> **Focus:** Windows telemetry, Sysmon, Wazuh agent integration, custom detection rules, and alert investigation

## 1. Objective

Configure a Windows endpoint to send Sysmon events to Wazuh, create custom rules for suspicious Mimikatz-related process activity, and investigate the resulting alerts in the Wazuh dashboard.

Perform testing only in the authorized INE practice environment. Do not use credential-dumping tools on systems without explicit authorization.

## 2. Lab environment

| Component | Role |
|---|---|
| Kali Linux | Attacker / simulation workstation |
| Ubuntu with Wazuh | SOC machine and Wazuh manager |
| Windows Server 2019 | Target endpoint with Wazuh agent and Sysmon |
| Sysmon | Windows event telemetry |
| Wazuh dashboard | Alert search and investigation |

Do not publish lab credentials. Redact network details if required by your course or organization.

## 3. Detection architecture

```text
Windows Server 2019
      |
      | Sysmon Operational events
      v
Wazuh Agent
      |
      v
Wazuh Manager
      |
      | Decoders + local custom rules
      v
Wazuh Security Events
      |
      v
SOC analyst investigates alert context
```

## 4. Implementation

### 4.1 Connect the Wazuh agent

On the Windows target, the Wazuh agent configuration was updated to point to the Wazuh manager in the lab network. The agent service was started and restarted after configuration changes.

PowerShell commands used:

```powershell
Start-Service -Name WazuhSvc
Restart-Service -Name WazuhSvc
Get-Service -Name WazuhSvc
```

The agent appeared in the Wazuh dashboard as agent ID `001`, named `AttackDefense`.

### 4.2 Configure Sysmon event collection

The Windows Wazuh agent configuration file was:

```text
C:\Program Files (x86)\ossec-agent\ossec.conf
```

The following event-channel configuration was added inside the existing agent configuration:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

This configures the Wazuh agent to collect events from the Sysmon Operational channel.

### 4.3 Configure Sysmon

Sysmon 14.14 was present in the lab. The provided XML configuration was saved as `sysmonconfig.xml` and applied using the Sysmon configuration update command from the Sysmon directory.

The command reported:

```text
Loading configuration file with schema version 4.10
Configuration file validated.
Configuration updated.
```

The configuration included process creation, remote-thread creation, and process-access filtering for image paths containing `mimikatz.exe`, along with other event categories. The events recorded depend on the Sysmon configuration and filters in effect.

### 4.4 Create custom Wazuh rules

Custom rules were added to:

```text
/var/ossec/etc/rules/local_rules.xml
```

Two configuration issues were encountered:

1. Rule ID `100001` conflicted with an existing local SSH rule.
2. The Event ID 10 group name did not match the installed Wazuh ruleset. The installed file `/var/ossec/ruleset/rules/0595-win-sysmon_rules.xml` showed the group `sysmon_event_10`.

The duplicate ID was addressed by assigning distinct IDs to custom rules. The group name was checked against the installed ruleset.

**Intended rule IDs:**

| Rule ID | Detection intent | Expected Sysmon event |
|---|---|---|
| `100010` | Process image contains `mimikatz.exe` | Event ID 1 |
| `100011` | Matching source process creates a remote thread | Event ID 8 |
| `100012` | Matching source process accesses another process | Event ID 10 |

> **Reproducibility note:** The captured dashboard screenshot shows alerts with IDs `100000` and `100012`. It does not show Rule `100011`. Confirm the final contents of `local_rules.xml` before publishing the rule configuration, so the documentation matches the configuration that generated the evidence.

Example rule structure (confirm field and group names against the installed ruleset before use):

```xml
<group name="local,sysmon,">
  <rule id="100010" level="12">
    <if_group>sysmon_event1</if_group>
    <field name="win.eventdata.image" type="pcre2">(?i)mimikatz\.exe</field>
    <description>Sysmon: suspicious process image contains mimikatz.exe</description>
  </rule>

  <rule id="100011" level="12">
    <if_group>sysmon_event8</if_group>
    <field name="win.eventdata.sourceImage" type="pcre2">(?i)mimikatz\.exe</field>
    <description>Sysmon: mimikatz-like process created a remote thread</description>
  </rule>

  <rule id="100012" level="12">
    <if_group>sysmon_event_10</if_group>
    <field name="win.eventdata.sourceImage" type="pcre2">(?i)mimikatz\.exe</field>
    <description>Sysmon: mimikatz-like process accessed another process</description>
  </rule>
</group>
```

Do not replace the whole existing `local_rules.xml` with this snippet: merge custom rules into the existing file and preserve the original SSH rule and outer XML structure.

### 4.5 Validate and restart Wazuh

Configuration validation:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

After correcting duplicate IDs and the Event ID 10 group name, restart the manager:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl is-active wazuh-manager
```

The expected service status is `active`. Check validation output and manager logs if startup fails.

## 5. Results

The Wazuh Security Events dashboard displayed two custom-rule alerts for agent `001` (`AttackDefense`).

| Observed rule ID | Alert description in dashboard | Level | Interpretation |
|---|---|---:|---|
| `100000` | `Sysmon - Suspicious Process - mimikatz.exe` | 12 | The configured process-creation detection matched |
| `100012` | `Sysmon: mimikatz-like process accessed another process` | 12 | The configured process-access detection matched |

The dashboard showed the alerts at approximately `05:22:37` and `05:32:35` on October 13, 2026, according to the displayed lab timestamps.

**Evidence-based limitation:** Rule `100011` was not visible in the captured dashboard screenshot. No claim is made that remote-thread detection triggered. The screenshot demonstrates that the two listed alerts were generated; it does not by itself prove credential theft or compromise.

## 6. Investigation notes

When opening each alert, review these fields where available:

- Timestamp and timezone
- Agent ID and endpoint name
- Rule ID, description, and severity
- Sysmon event ID
- Process image and command line
- Parent process and user context
- Source and target process for Event ID 10
- Nearby endpoint events and corroborating telemetry

A matching filename or a single process-access event is not proof of successful credential compromise. Correlate endpoint context and additional telemetry before assigning a final incident verdict.

## 7. Troubleshooting lessons

### Duplicate rule ID

Wazuh warned that rule ID `100001` was duplicated because the existing SSH example rule already used that ID. Custom rules needed unique IDs.

### Invalid Event ID 10 group

The installed ruleset defined the group as `sysmon_event_10`, with an underscore before `10`. The custom rule initially referenced `sysmon_event10`, which Wazuh could not find.

Useful inspection command:

```bash
grep -n -A 10 -B 3 'sysmon_event10\|sysmon_event_10' \
  /var/ossec/ruleset/rules/0595-win-sysmon_rules.xml
```

### Configuration validation

Use `wazuh-analysisd -t` before restarting the manager. Investigate warnings rather than assuming rules loaded correctly.

## 8. Defensive recommendations

- Apply least privilege and restrict administrative access.
- Maintain Windows updates and endpoint protection.
- Collect appropriate Sysmon and Windows security telemetry.
- Investigate unusual access to sensitive processes in context.
- Use credential-protection controls appropriate to the environment.
- Follow incident-response procedures if evidence supports suspected credential theft.
- Keep custom rules version-controlled and validate them after ruleset or Wazuh upgrades.
- Avoid publishing credentials, credential material, or sensitive event data.

## 9. Conclusion

This lab provided hands-on practice with Windows endpoint telemetry, Sysmon configuration, Wazuh agent integration, custom rule troubleshooting, and SOC alert investigation. The captured dashboard confirmed two alerts associated with the configured process-creation and process-access detections. The main lesson is to validate rules against the installed Wazuh ruleset and interpret alerts using event context rather than treating a single alert as definitive proof of compromise.

## 10. Evidence

Place screenshots captured from your own INE run in an `evidence/` directory. Suggested filenames:

```text
evidence/
├── 01-wazuh-security-events-overview.png
├── 02-process-creation-alert.png
└── 03-process-access-alert.png
```

The overview screenshot captured during this run shows Rule IDs `100000` and `100012`. Capture the expanded alert views separately for field-level evidence. Redact sensitive details before publishing.

## 11. References

- [Wazuh documentation — Ruleset testing](https://documentation.wazuh.com/current/user-manual/ruleset/testing.html)
- [Wazuh documentation — Rules and decoders](https://documentation.wazuh.com/current/user-manual/ruleset/)
- [Wazuh documentation — Log data collection](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html)
- [Wazuh project repository](https://github.com/wazuh/wazuh)
- [Mimikatz project repository](https://github.com/gentilkiwi/mimikatz)
