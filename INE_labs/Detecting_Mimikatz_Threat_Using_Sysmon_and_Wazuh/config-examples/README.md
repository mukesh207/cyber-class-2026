# Configuration examples and reproducibility notes

The main walkthrough contains the relevant Wazuh agent event-channel XML, validation commands, and an illustrative custom-rule structure. These are documentation examples, not a guaranteed export of the exact final configuration used in the lab.

Before applying them:

- Back up the existing Wazuh configuration.
- Merge custom rules into the existing `local_rules.xml`; do not overwrite the file.
- Preserve existing rules and use unique rule IDs.
- Confirm event group names against the installed Wazuh ruleset.
- Validate with `sudo /var/ossec/bin/wazuh-analysisd -t` before restarting the manager.
- Test only in an authorized lab environment.

The captured dashboard showed Rule IDs `100000` and `100012`. It did not show Rule `100011` firing.
