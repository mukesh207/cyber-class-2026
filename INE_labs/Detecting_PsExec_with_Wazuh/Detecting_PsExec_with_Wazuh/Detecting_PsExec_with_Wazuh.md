# Detecting PsExec with Wazuh

## 1. Objective

Build and validate a detection workflow for PsExec-related activity using Sysmon telemetry and custom Wazuh rules. PsExec is a legitimate Sysinternals administration utility, but attackers may also abuse it for remote execution, lateral movement, or SYSTEM-level execution. Detection should therefore be based on context and correlated events rather than the tool name alone.

## 2. Lab architecture

- **SOC machine:** Ubuntu with Wazuh manager and dashboard
- **Target machine:** Windows Server 2019 with Wazuh agent and Sysmon
- **Tools:** Wazuh, Sysmon, PowerShell, PsExec
- **Evidence:** See the `evidence/` directory.

The IP address shown during a lab run is temporary and specific to that environment. Use the address assigned to your current SOC machine rather than copying addresses from another walkthrough.

## 3. Connect the Wazuh agent

1. Open the Wazuh dashboard on the SOC machine and confirm the manager is running.
2. Find the SOC machine's current private IP address:

   ```bash
   ip addr
   ```

3. On the Windows target, open **Wazuh Agent Manager** and set the Wazuh manager address to the SOC machine's current IP.
4. Start the agent from an elevated PowerShell prompt:

   ```powershell
   Start-Service -Name WazuhSvc
   Get-Service -Name WazuhSvc
   ```

5. In the Wazuh dashboard, confirm the endpoint appears as active.

If the agent does not connect, verify network reachability and the lab firewall/security-group rules. Wazuh commonly uses TCP 1514 for agent communication and TCP 1515 for agent enrollment, though the actual configuration may differ.

## 4. Configure Sysmon event collection

Edit the Windows agent configuration file, typically:

`C:\Program Files (x86)\ossec-agent\ossec.conf`

Add the following block inside the configuration's existing `<ossec_config>` root element:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Install Sysmon using an approved Sysmon configuration. In the lab, Sysmon was already installed; a second install attempt reported that the service was already registered. Do not repeatedly reinstall it. If configuration changes are required, follow the Sysmon documentation and validate the current service/configuration first.

Restart the Wazuh agent after saving the configuration:

```powershell
Restart-Service -Name WazuhSvc
```

Evidence: [`evidence/03-sysmon-wazuh-agent-config.png`](evidence/03-sysmon-wazuh-agent-config.png)

## 5. Add custom Wazuh detection rules

On the SOC machine, edit:

`/var/ossec/etc/rules/local_rules.xml`

Review and add the lab rules from [`rules/local_rules.xml`](rules/local_rules.xml) inside a valid ruleset structure. Ensure the IDs do not conflict with existing custom rules.

Validate the rules before restarting the manager:

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

If validation succeeds, restart the manager:

```bash
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager --no-pager
```

### Rule intent

| Rule ID | Intended detection | MITRE ATT&CK mapping |
|---|---|---|
| `160010` | PsExec EULA registry value activity | T1112 — Modify Registry |
| `160011` | PsExec service registry activity associated with SYSTEM | T1543.003 — Windows Service |
| `160012` | PsExec service registry-key deletion activity | T1543.003 — Windows Service |
| `160013` | PsExec named-pipe activity associated with SYSTEM | T1570 — Lateral Tool Transfer |

These are the lab's custom rules. Their effectiveness depends on the Sysmon events generated, the event fields Wazuh receives, and the exact field values. Confirm that the regex patterns match your own decoded events. The rules are indicators, not definitive proof of malicious behavior.

## 6. Simulate PsExec execution in the authorized lab

On the Windows target, open PowerShell as an administrator and move to the lab's PsTools directory. The exercise uses PsExec to open a PowerShell process under the SYSTEM account:

```powershell
.\PsExec.exe -i -s powershell
```

In the newly opened PowerShell window, verify the effective account:

```powershell
whoami
```

The observed output in this run was:

```text
nt authority\system
```

This confirms that the launched process ran as the Windows SYSTEM account. SYSTEM-level execution is highly privileged, but the result alone does not establish malicious intent.

Evidence: [`evidence/02-psexec-system-privilege.png`](evidence/02-psexec-system-privilege.png)

## 7. Review Wazuh alerts

Open **Security events** in the Wazuh dashboard and review alerts associated with the custom rules.

The captured dashboard showed:

- Rule `160011`: PsExec service activity running as `NT AUTHORITY\\SYSTEM`
- Rule `160013`: PsExec named-pipe activity
- Rule `92650`: a suspicious Windows service creation alert
- Additional host and manager events unrelated to the core PsExec detection

Evidence: [`evidence/01-wazuh-security-events.png`](evidence/01-wazuh-security-events.png)

Expand an alert and inspect fields such as:

- `win.eventdata.targetObject`
- `win.eventdata.eventType`
- `win.eventdata.user`
- `win.system.computer`

Correlate timestamps, endpoint identity, process/service details, and surrounding events. Repeated alerts may be caused by multiple registry or named-pipe events from a single execution; do not count every alert as a distinct attack.

## 8. Troubleshooting and validation

- **Agent offline:** Check manager address, routing, firewall/security-group rules, agent service state, and manager logs.
- **No Sysmon events:** Confirm Sysmon is running and generating events, confirm the event channel spelling, and restart the Wazuh agent after editing `ossec.conf`.
- **No custom alerts:** Run `wazuh-analysisd -t`, inspect the decoded event fields, and verify the rule's field names and regex patterns against actual events.
- **Too many alerts:** Tune correlation and rule conditions using benign baseline activity; document expected false positives.
- **Duplicate-looking alerts:** Compare timestamps and event details before deciding whether they represent distinct actions.

## 9. Results

The lab demonstrated the full monitoring-to-detection workflow:

1. Connected the Windows endpoint to Wazuh.
2. Configured Sysmon Operational log collection.
3. Added custom PsExec-focused rules.
4. Executed PsExec in an isolated lab and verified SYSTEM-level execution.
5. Observed matching alerts in the Wazuh dashboard.

## 10. Defensive takeaways

- Monitor service installation and registry changes on Windows endpoints.
- Collect Sysmon telemetry centrally and preserve useful event fields.
- Correlate service activity, named pipes, account context, and process execution.
- Investigate PsExec use in context because it is also a legitimate administration tool.
- Validate custom rules against actual logs and measure false positives before production deployment.

## References

- [Wazuh: Detecting PsExec usage](https://wazuh.com/blog/detecting-psexec-usage-with-wazuh/)
- [Microsoft Sysinternals PsExec](https://learn.microsoft.com/en-us/sysinternals/downloads/psexec)
- [MITRE ATT&CK: PsExec (S0029)](https://attack.mitre.org/software/S0029/)
- [MITRE ATT&CK: Modify Registry (T1112)](https://attack.mitre.org/techniques/T1112/)
- [MITRE ATT&CK: Windows Service (T1543.003)](https://attack.mitre.org/techniques/T1543/003/)
- [MITRE ATT&CK: Lateral Tool Transfer (T1570)](https://attack.mitre.org/techniques/T1570/)
