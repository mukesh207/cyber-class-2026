import re

# 1. Update README.md
with open('README.md', 'r') as f:
    readme = f.read()

readme = readme.replace('Sessions Completed:** 8', 'Sessions Completed:** 9')
readme = readme.replace('Labs Completed:** 3', 'Labs Completed:** 4')

new_row = "| 2026-09-01 | Week 04 | 09      | OWASP Top 10 (2025 vs 2021), SQL Injection, Oracle vs Non-Oracle, SQLmap, Dirbuster, Gobuster, Curl, Blind SQLi | [week-04/2026-09-01.md](week-04/2026-09-01.md) |\n"
# Find where to insert it in the table
# The last row of the table currently ends with week-04/2026-08-31.md) |
readme = readme.replace("| 2026-08-31 | Week 04 | 08      | Web Apps, HTTP, Network Security (Firewall, WAF, IDS/IPS), Honeypots | [week-04/2026-08-31.md](week-04/2026-08-31.md) |\n", "| 2026-08-31 | Week 04 | 08      | Web Apps, HTTP, Network Security (Firewall, WAF, IDS/IPS), Honeypots | [week-04/2026-08-31.md](week-04/2026-08-31.md) |\n" + new_row)

with open('README.md', 'w') as f:
    f.write(readme)

# 2. Update week-04/2026-08-31.md next links
with open('week-04/2026-08-31.md', 'r') as f:
    prev_note = f.read()

# Replace the top navigation
prev_note = prev_note.replace("[🏠 Dashboard](../README.md) | [◀ Previous Session](../week-03/2026-08-27.md)\n", "[🏠 Dashboard](../README.md) | [◀ Previous Session](../week-03/2026-08-27.md) | [Next Session ▶](2026-09-01.md)\n")
# Replace the bottom navigation
prev_note = prev_note.replace("[🏠 Dashboard](../README.md) | [◀ Previous Session](../week-03/2026-08-27.md)\n", "[🏠 Dashboard](../README.md) | [◀ Previous Session](../week-03/2026-08-27.md) | [Next Session ▶](2026-09-01.md)\n")

with open('week-04/2026-08-31.md', 'w') as f:
    f.write(prev_note)

print("Updated README and previous note.")
