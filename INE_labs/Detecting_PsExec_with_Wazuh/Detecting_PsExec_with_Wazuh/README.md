# Detecting PsExec with Wazuh

A hands-on Blue Team lab documenting Sysmon telemetry, custom Wazuh detection rules, PsExec execution, and alert validation.

## Lab overview

- **Objective:** Detect PsExec-related activity on a Windows endpoint using Wazuh.
- **SOC:** Ubuntu-based Wazuh manager
- **Endpoint:** Windows Server 2019 with Wazuh agent and Sysmon
- **Technique context:** PsExec can be used for remote administration, lateral movement, and SYSTEM-level execution. Its presence alone is not proof of malicious activity.
- **Evidence:** Screenshots in [`evidence/`](evidence/)

> Run this workflow only in an authorized lab. Lab IP addresses and hostnames are environment-specific and should not be reused in other environments.

## Repository contents

- [`Detecting_PsExec_with_Wazuh.md`](Detecting_PsExec_with_Wazuh.md) — full walkthrough
- [`rules/local_rules.xml`](rules/local_rules.xml) — custom detection rules from the lab
- [`configs/sysmon-agent-ossec-snippet.xml`](configs/sysmon-agent-ossec-snippet.xml) — Sysmon event-channel collection snippet
- [`evidence/`](evidence/) — screenshots of the observed lab results

## Key outcomes

- Configured the Windows Wazuh agent to collect Sysmon Operational events.
- Added custom rules to identify PsExec EULA registry activity, service registry activity, and named-pipe activity.
- Executed PsExec in the isolated lab and verified the resulting PowerShell process ran as `NT AUTHORITY\\SYSTEM`.
- Observed matching custom alerts in the Wazuh Security Events dashboard.

## Important detection notes

- Repeated alerts can represent multiple matching events from one execution; do not automatically interpret each alert as a separate intrusion.
- Validate the event fields and endpoint context before classifying an alert as malicious.
- Test custom rules against representative benign and suspicious events before deploying them to production.
- The rules in this repository reflect the lab exercise and should be reviewed for the Sysmon configuration, Wazuh version, field normalization, and regex behavior in your environment.

## References

- [Wazuh: Detecting PsExec usage](https://wazuh.com/blog/detecting-psexec-usage-with-wazuh/)
- [Microsoft Sysinternals PsExec](https://learn.microsoft.com/en-us/sysinternals/downloads/psexec)
- [MITRE ATT&CK: PsExec (S0029)](https://attack.mitre.org/software/S0029/)
- [MITRE ATT&CK: Modify Registry (T1112)](https://attack.mitre.org/techniques/T1112/)
- [MITRE ATT&CK: Windows Service (T1543.003)](https://attack.mitre.org/techniques/T1543/003/)
- [MITRE ATT&CK: Lateral Tool Transfer (T1570)](https://attack.mitre.org/techniques/T1570/)
