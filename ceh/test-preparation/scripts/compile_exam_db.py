#!/usr/bin/env python3
"""
CEH v13 Question Database Compiler
Parses comprehensive-mcq-revision-test.md and produces:
- data/ceh_v13_question_bank.json
- data/exam_data.js
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_PATH = os.path.join(BASE_DIR, "comprehensive-mcq-revision-test.md")
OUT_JSON = os.path.join(BASE_DIR, "data", "ceh_v13_question_bank.json")
OUT_JS = os.path.join(BASE_DIR, "data", "exam_data.js")

DOMAIN_DEFINITIONS = {
    1: {"code": "D1", "name": "Information Security & Ethical Hacking Overview", "weight": 6, "module": "Module 01", "ref": "../mod-01-introduction-to-ethical-hacking.md"},
    2: {"code": "D2", "name": "Reconnaissance Techniques", "weight": 21, "module": "Module 02", "ref": "../mod-02-footprinting-and-reconnaissance.md"},
    3: {"code": "D3", "name": "System Hacking Phases & Attack Techniques", "weight": 17, "module": "Module 06", "ref": "../2026-10-27-ceh-master-class-notes.md#4-module-06-system-hacking-active-directory--kerberos-exploitation"},
    4: {"code": "D4", "name": "Network & Perimeter Hacking", "weight": 14, "module": "Modules 03, 08, 10, 11, 12", "ref": "../mod-03-scanning-networks.md"},
    5: {"code": "D5", "name": "Web Application Hacking", "weight": 16, "module": "Modules 13, 14, 15", "ref": "../2026-10-27-ceh-master-class-notes.md#11-modules-13--14-web-servers-applications--owasp-top-10"},
    6: {"code": "D6", "name": "Wireless Network Hacking", "weight": 6, "module": "Module 16", "ref": "../2026-10-31-ceh-advanced-domains-notes.md"},
    7: {"code": "D7", "name": "Mobile Platform, IoT, and OT Hacking", "weight": 8, "module": "Modules 17, 18", "ref": "../2026-10-31-ceh-advanced-domains-notes.md#6-module-18-iot--operational-technology-ot--scada--plc-security"},
    8: {"code": "D8", "name": "Cloud Computing & Containers", "weight": 6, "module": "Module 19", "ref": "../2026-10-31-ceh-advanced-domains-notes.md#7-module-19-cloud-computing-containers--identity-graph-exploitation"},
    9: {"code": "D9", "name": "Cryptography & Cryptanalysis", "weight": 6, "module": "Module 20", "ref": "../2026-10-31-ceh-advanced-domains-notes.md#9-module-20-cryptanalysis--post-quantum-cryptography"}
}

def classify_question(qnum, title, granular, concept):
    t = f"{title} {concept}".lower()
    g = granular.lower()
    
    # 6. Wireless
    if re.search(r'\b(wpa\d*|wireless|wifi|evil twin|rogue access|pmkid|captive portal|wips|dragonblood|802\.11\w*|aircrack)\b', t):
        return 6
    if 'wireless security' in g or 'wireless network security' in g:
        return 6
        
    # 8. Cloud
    if re.search(r'\b(cloud|aws|gcp|azure|lambda|s3|container|docker|kubernetes|k8s|serverless|iam role|microservices|ec2)\b', t) or 'cloud' in g or 'container' in g or 'serverless' in g:
        return 8
        
    # 7. Mobile & IoT/OT
    if re.search(r'\b(mobile|android|ios|apk|frida|iot|scada|plc|modbus|purdue|uart|jtag|firmware|agent smith|janus|zigbee)\b', t) or re.search(r'\b(mobile|iot|scada|industrial)\b', g):
        return 7
    if 'ot & industrial' in g or 'ot security' in g:
        return 7
        
    # 9. Cryptography
    if re.search(r'\b(crypt\w*|cipher|rsa|aes|des\b|ecc\b|quantum|pqc|shor|diffie|padding oracle|hash\w*|collision|hmac|pgp|blockchain)\b', t) or 'cryptography' in g:
        return 9
        
    # 5. Web App
    if re.search(r'\b(web|sql\w*|xss|csrf|ssrf|xxe|idor|deserializ\w*|clickjacking|lfi|rfi|nosql|graphql|api|cookie|session fixation|cors|sop|burp|owasp|traversal|tamper)\b', t) or 'web' in g or 'client-side' in g:
        return 5
        
    # 2. Reconnaissance
    if re.search(r'\b(recon\w*|footprint\w*|osint|dork|whois|dns|axfr|shodan|censys|email header|social engineering|phish\w*|vish\w*|shoulder surfing|pretext\w*|dumpster|banner grab\w*|subdomain|crt\.sh|service version|traceroute|amass|theharvester)\b', t) or 'footprinting' in g or 'reconnaissance' in g or 'social engineering' in g:
        return 2
        
    # 1. InfoSec Overview & Governance
    if re.search(r'\b(governance|iso 2700\d*|ethical hacking|threat actor|white hat|black hat|grey hat|cvss|risk|compliance|audit|sdlc|policy|aup|byod|isms|code of ethics|cia triad|vulnerability assessment|vulnerability management)\b', t) or 'governance' in g or 'vulnerability' in g or 'sdlc' in g:
        return 1
        
    # 4. Network & Perimeter
    if re.search(r'\b(scan\w*|nmap|sniff\w*|arp\b|icmp|tcp|udp|firewall|ids|ips|honeypot|dos\b|ddos|botnet|syn flood|slowloris|fragment\w*|proxy|snort|palo alto|session hijacking|tunneling|netbios|smb\b)\b', t) or 'scanning' in g or 'sniffing' in g or 'perimeter' in g or 'denial' in g:
        return 4
        
    # 3. System Hacking
    return 3

def parse_markdown():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse index rows
    index_rows = re.findall(
        r'\| (?:🟢|🟡|🔴) \*\*\[(\d+)\]\(\#q\d+\)\*\* \| \[\#(\d+)\]\(.*?\) \| (.*?) \| (.*?) \| (.*?) \|',
        content
    )
    meta_dict = {}
    for r in index_rows:
        qnum = int(r[0])
        meta_dict[qnum] = {
            "num": qnum,
            "legacy_ref": r[1].strip(),
            "focus": r[2].strip(),
            "domain_granular": r[3].strip(),
            "concept": r[4].strip()
        }

    # Split into question blocks
    sections = re.split(r'\n(?=<a id="q\d+"></a>)', content)
    questions = []

    for sec in sections:
        header_m = re.search(r'### Question (\d+): (.+?) \[Exam Ref: #(\d+)\]', sec)
        if not header_m:
            continue
        
        qnum = int(header_m.group(1))
        title = header_m.group(2).strip()
        legacy_ref = header_m.group(3).strip()

        # Determine Tier
        if qnum <= 44:
            tier_code, tier_name = "🟢", "Tier 1: Foundational"
        elif qnum <= 105:
            tier_code, tier_name = "🟡", "Tier 2: Core Applied"
        else:
            tier_code, tier_name = "🔴", "Tier 3: Advanced Exploitation"

        # Question prompt
        q_match = re.search(r'> \*\*Question:\*\* (.*?)(?=\n> -|\n>\n)', sec, re.DOTALL)
        question_text = q_match.group(1).strip() if q_match else ""

        # Options
        opts_matches = re.findall(r'> - \[[ x]\] \**([A-D])\.\s*(.+?)\**$', sec, re.MULTILINE)
        options = []
        for opt_key, opt_text in opts_matches:
            options.append({
                "key": opt_key,
                "text": opt_text.strip()
            })

        # Correct answer
        ans_match = re.search(r'> \*\*Correct Answer:\*\* \*\*([A-D])\.\s*(.*?)\*\*', sec)
        if ans_match:
            correct_key = ans_match.group(1)
            correct_text = ans_match.group(2).strip()
        else:
            # Fallback
            ans_match2 = re.search(r'> \*\*Correct Answer:\*\* \*\*([A-D])\b', sec)
            correct_key = ans_match2.group(1) if ans_match2 else "A"
            correct_text = ""
            for o in options:
                if o["key"] == correct_key:
                    correct_text = o["text"]

        # Deep Mechanics
        mech_match = re.search(r'#### 🔬 Deep Technical Mechanics.*?\n(.*?)(?=\n#### |$)', sec, re.DOTALL)
        mechanics = mech_match.group(1).strip() if mech_match else ""

        # Distractor Teardown
        dist_match = re.search(r'#### (?:🚫|❌) Distractor Teardown.*?\n(.*?)(?=\n#### |$)', sec, re.DOTALL)
        distractor_teardown = dist_match.group(1).strip() if dist_match else ""

        # Defense / Countermeasures
        def_match = re.search(r'#### 🛡️ (?:Defense & SOC Engineering|Pentesting & SOC Defensive Countermeasures).*?\n(.*?)(?=\n---|### |$)', sec, re.DOTALL)
        defense = def_match.group(1).strip() if def_match else ""

        # Extract ASCII diagram if present
        diagram_match = re.search(r'```(?:text)?\n(\+--+[\s\S]*?--+\+)\n```', sec)
        diagram = diagram_match.group(1).strip() if diagram_match else ""

        # Get metadata
        meta = meta_dict.get(qnum, {})
        granular_domain = meta.get("domain_granular", "")
        concept = meta.get("concept", "")

        # Classify into one of 9 domains
        domain_id = classify_question(qnum, title, granular_domain, concept)
        domain_info = DOMAIN_DEFINITIONS[domain_id]

        q_obj = {
            "id": f"q{qnum:03d}",
            "number": qnum,
            "legacy_ref": legacy_ref,
            "title": title,
            "tier": tier_name,
            "tier_icon": tier_code,
            "domain_id": domain_id,
            "domain_code": domain_info["code"],
            "domain_name": domain_info["name"],
            "domain_granular": granular_domain,
            "concept": concept,
            "module": domain_info["module"],
            "notes_ref": domain_info["ref"],
            "question": question_text,
            "options": options,
            "correct_key": correct_key,
            "correct_text": correct_text,
            "mechanics": mechanics,
            "distractor_teardown": distractor_teardown,
            "defense": defense,
            "diagram": diagram
        }
        questions.append(q_obj)

    return questions

def main():
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    questions = parse_markdown()
    print(f"[+] Successfully extracted {len(questions)} questions from comprehensive test bank.")

    # Domain summary
    counts = {}
    for q in questions:
        c = q["domain_name"]
        counts[c] = counts.get(c, 0) + 1
    
    print("\n[+] Domain Breakdown:")
    for d_id in sorted(DOMAIN_DEFINITIONS.keys()):
        d_name = DOMAIN_DEFINITIONS[d_id]["name"]
        print(f"    - Domain {d_id} ({d_name}): {counts.get(d_name, 0)} questions")

    # Save JSON
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Saved JSON database: {OUT_JSON} ({os.path.getsize(OUT_JSON)} bytes)")

    # Save JS for direct browser import
    js_content = f"// CEH v13 (312-50) Official Question Bank Payload\n// Total Questions: {len(questions)}\nwindow.CEH_EXAM_DATA = {json.dumps(questions, ensure_ascii=False)};\n"
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[+] Saved JS database: {OUT_JS} ({os.path.getsize(OUT_JS)} bytes)")

if __name__ == "__main__":
    main()
