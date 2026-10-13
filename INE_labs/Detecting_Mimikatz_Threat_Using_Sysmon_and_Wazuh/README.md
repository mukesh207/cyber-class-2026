# Detecting Mimikatz Threat Using Sysmon and Wazuh

**Lab:** INE Skill Dive — Detecting Mimikatz Threat Using Sysmon and Wazuh  
**Focus:** Blue Team / SOC / Windows telemetry / Sysmon / Wazuh custom detection  
**Status:** Completed in the INE lab environment

## Package contents

- `Detecting_Mimikatz_Threat_Using_Sysmon_and_Wazuh.md` — complete walkthrough, architecture, configuration steps, troubleshooting, observed alerts, defensive recommendations, and references.
- `evidence/` — six screenshots captured during the lab.
- `config-examples/README.md` — notes on safely reproducing the configuration examples.

## Evidence highlights

- INE lab completion page.
- Wazuh Security Events dashboard with observed Rule IDs `100000` and `100012` (level 12).
- Windows agent and Sysmon event-channel configuration context.
- SOC machine environment screenshots.

**Accuracy note:** The dashboard screenshot confirms alerts for Rule IDs `100000` and `100012`. It does not show Rule `100011`; the report does not claim that remote-thread detection triggered. Example rule IDs and final observed alert IDs are kept distinct.

## Before publishing

1. Review the screenshots for lab-sensitive information.
2. Redact any credentials, tokens, or details prohibited by the lab provider.
3. Make sure the GitHub version of the report includes the same evidence files, or update image links to match your repository structure.

## Repository link

https://github.com/mukesh207/cyber-class-2026/tree/main/INE_labs/Detecting_Mimikatz_Threat_Using_Sysmon_and_Wazuh
