#!/usr/bin/env python3
"""
Generate CEH v13 125-Question Mock Examination Markdown Paper
Creates: ceh/test-preparation/ceh-v13-mock-exam-125q.md
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "ceh_v13_question_bank.json")
OUT_MD = os.path.join(BASE_DIR, "ceh-v13-mock-exam-125q.md")

TARGET_COUNTS = {
    1: 7,   # InfoSec Overview & Governance (~6%)
    2: 12,  # Reconnaissance Techniques (~10%)
    3: 23,  # System Hacking Phases & Techniques (~18%)
    4: 20,  # Network & Perimeter Hacking (~16%)
    5: 22,  # Web Application Hacking (~18%)
    6: 8,   # Wireless Network Hacking (~6%)
    7: 12,  # Mobile Platform, IoT, and OT Hacking (~10%)
    8: 10,  # Cloud Computing & Containers (~8%)
    9: 11   # Cryptography & Cryptanalysis (~8%)
}

def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Group by domain
    by_domain = {}
    for q in questions:
        by_domain.setdefault(q["domain_id"], []).append(q)

    # Sample deterministically according to target counts
    selected_questions = []
    for d_id in sorted(TARGET_COUNTS.keys()):
        req = TARGET_COUNTS[d_id]
        available = by_domain[d_id]
        selected_questions.extend(available[:req])

    assert len(selected_questions) == 125, f"Expected 125 questions, got {len(selected_questions)}"

    lines = []
    lines.append("# 📝 EC-Council CEH v13 (312-50) Official 125-Question Mock Examination Paper")
    lines.append("")
    lines.append("> **Exam Code:** 312-50 (CEH v13) | **Total Questions:** 125 Multiple-Choice Questions  ")
    lines.append("> **Time Limit:** 4 Hours (240 Minutes) | **Passing Cut-Score:** Variable 70.0% (88 / 125 Correct)  ")
    lines.append("> **Format:** Scenario-Based Multiple Choice, Best Answer Selection | **Negative Marking:** None  ")
    lines.append("> **Navigation:** [🏠 CEH Master Hub](../README.md) | [🚀 Launch Web Simulator](./exam-simulator.html) | [📋 Test Prep Dashboard](./README.md)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📋 Blueprint Domain Weighting & Test Structure")
    lines.append("")
    lines.append("| Domain | Curriculum Domain Title | Official Weight | Mock Exam Questions | Question Range |")
    lines.append("| :---: | :--- | :---: | :---: | :---: |")
    lines.append("| **D1** | **Information Security & Ethical Hacking Overview** (Mod 01) | ~6% | 7 Questions | Q001 – Q007 |")
    lines.append("| **D2** | **Reconnaissance Techniques** (Mod 02) | ~10% | 12 Questions | Q008 – Q019 |")
    lines.append("| **D3** | **System Hacking Phases & Attack Techniques** (Mod 06) | ~18% | 23 Questions | Q020 – Q042 |")
    lines.append("| **D4** | **Network & Perimeter Hacking** (Mod 03, 08, 10, 11, 12) | ~16% | 20 Questions | Q043 – Q062 |")
    lines.append("| **D5** | **Web Application Hacking** (Mod 13, 14, 15) | ~18% | 22 Questions | Q063 – Q084 |")
    lines.append("| **D6** | **Wireless Network Hacking** (Mod 16) | ~6% | 8 Questions | Q085 – Q092 |")
    lines.append("| **D7** | **Mobile Platform, IoT, and OT Hacking** (Mod 17, 18) | ~10% | 12 Questions | Q093 – Q104 |")
    lines.append("| **D8** | **Cloud Computing & Containers** (Mod 19) | ~8% | 10 Questions | Q105 – Q114 |")
    lines.append("| **D9** | **Cryptography & Cryptanalysis** (Mod 20) | ~8% | 11 Questions | Q115 – Q125 |")
    lines.append("| **Total** | **Official Full-Length Simulation** | **100%** | **125 Questions** | **Q001 – Q125** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🧭 Test Instructions & Exam Strategy")
    lines.append("")
    lines.append("1. **Time Management:** You have 240 minutes for 125 questions (~1.9 minutes per scenario). Flag questions that require extensive deduction and return to them.")
    lines.append("2. **Qualifier Words:** Look carefully for qualifiers: **FIRST**, **BEST**, **LEAST**, **MOST**, and **NOT**.")
    lines.append("3. **Systematic Distractor Elimination:** Rule out options that state technical absolutes (\"always\", \"never\"), mix protocols (e.g. UDP vs TCP), or confuse active probing with passive intelligence gathering.")
    lines.append("4. **Self-Scoring:** Mark your answers on a blank sheet or in the provided answer grid below before checking the collapsible answer keys in Part 2.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📄 Part 1: The 125 Examination Questions")
    lines.append("")

    for i, q in enumerate(selected_questions, 1):
        q_num_str = f"{i:03d}"
        lines.append(f"<a id=\"mock-q{q_num_str}\"></a>")
        lines.append(f"### Question {q_num_str} [{q['domain_code']}: {q['domain_name']}]")
        lines.append(f"**Item Ref:** #{q['legacy_ref']} | **Focus:** {q['title']} | **Tier:** {q['tier_icon']} {q['tier']}")
        lines.append("")
        lines.append(f"> **Question:** {q['question']}")
        lines.append(">")
        for opt in q["options"]:
            lines.append(f"> - [ ] **{opt['key']}.** {opt['text']}")
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary><b>🔍 View Answer Key & Deep SOC Analysis for Question {q_num_str}</b></summary>")
        lines.append("")
        lines.append(f"**Correct Answer:** **{q['correct_key']}. {q['correct_text']}**")
        lines.append("")
        lines.append("#### 🔬 Deep Technical Mechanics")
        lines.append(q["mechanics"])
        lines.append("")
        if q["diagram"]:
            lines.append("```text")
            lines.append(q["diagram"])
            lines.append("```")
            lines.append("")
        lines.append("#### 🚫 Distractor Teardown")
        lines.append(q["distractor_teardown"])
        lines.append("")
        if q["defense"]:
            lines.append("#### 🛡️ Defense & SOC Countermeasures")
            lines.append(q["defense"])
            lines.append("")
        lines.append(f"📖 **Localized Study Reference:** [{q['module']} &mdash; {q['domain_name']}]({q['notes_ref']})")
        lines.append("</details>")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Self-Grading Score Sheet
    lines.append("## 📊 Part 2: Candidate Answer Sheet & Score Calculation")
    lines.append("")
    lines.append("Record your selected answers (A, B, C, D) below during self-testing:")
    lines.append("")
    lines.append("| Q# | Your Ans | Key | Result | Q# | Your Ans | Key | Result | Q# | Your Ans | Key | Result | Q# | Your Ans | Key | Result | Q# | Your Ans | Key | Result |")
    lines.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    # Generate 25 rows x 5 columns = 125 questions table
    for r in range(1, 26):
        row_cells = []
        for col in range(5):
            q_idx = r + (col * 25)
            q_data = selected_questions[q_idx - 1]
            row_cells.append(f"**{q_idx:03d}** | &nbsp;&nbsp;&nbsp; | **{q_data['correct_key']}** | &nbsp;&nbsp;&nbsp;")
        lines.append("| " + " | ".join(row_cells) + " |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎯 Part 3: Performance Scorecard & Cut-Score Evaluation")
    lines.append("")
    lines.append("Calculate your score using the formula below:")
    lines.append("")
    lines.append("$$\\text{Final Score (\\%)} = \\left( \\frac{\\text{Total Correct Answers}}{125} \\right) \\times 100$$")
    lines.append("")
    lines.append("| Score Range | Classification | Status | Next Recommendation |")
    lines.append("| :--- | :--- | :---: | :--- |")
    lines.append("| **85% – 100% (106–125 Q)** | 🟢 Elite Mastery | **STRONG PASS** | Ready for official Pearson VUE exam appointment. |")
    lines.append("| **70% – 84% (88–105 Q)** | 🟡 Certified Readiness | **PASS** | Review missed questions in low-scoring domains. |")
    lines.append("| **60% – 69% (75–87 Q)** | 🟠 Marginal Borderline | **BORDERLINE** | Drill domain-specific questions in Web Apps & System Hacking. |")
    lines.append("| **< 60% (0–74 Q)** | 🔴 Insufficient Readiness | **DID NOT PASS** | Re-read fundamental module notes (Mod 01 to Mod 06) before retaking. |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🧠 Part 4: My Understanding Check")
    lines.append("")
    lines.append("Answer these synthesis questions to reinforce core exam concepts:")
    lines.append("")
    lines.append("1. **Question 1:** In scenario questions dealing with enterprise network reconnaissance, why is passive DNS harvesting (e.g. `crt.sh`, Censys) legally and tactically preferred before issuing active DNS zone transfer (`dig axfr`) queries?")
    lines.append("2. **Question 2:** Explain the difference in operational impact between a **TCP SYN Flood** (half-open state table exhaustion) and a **Slowloris Attack** (Layer 7 application thread exhaustion). Which one bypasses standard stateful firewalls?")
    lines.append("3. **Question 3:** During Active Directory exploitation, what is the cryptographic distinction between an **AS-REP Roasting** attack and a **Kerberoasting** attack regarding required privileges?")
    lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[+] Successfully generated 125-question mock paper: {OUT_MD}")
    print(f"    - File size: {os.path.getsize(OUT_MD)} bytes")
    print(f"    - Total lines: {len(lines)}")

if __name__ == "__main__":
    main()
