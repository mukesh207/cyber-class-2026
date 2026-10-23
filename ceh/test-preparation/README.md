# 🎯 CEH v13 Exam Test Preparation Hub

Welcome to the **Certified Ethical Hacker (CEH v13 — Exam 312-50)** test preparation dashboard. This space is engineered to transform theoretical and hands-on knowledge into exam readiness through structured question banks, scenario analysis, formula drill sheets, and test-taking strategies.

---

## 📋 CEH v13 (312-50) Official Exam Blueprint

| Exam Parameter | Official Specification |
| :--- | :--- |
| **Exam Code** | 312-50 (ECC EXAM) / 312-50 (VUE) |
| **Total Questions** | 125 Multiple-Choice Questions |
| **Time Limit** | 4 Hours (240 Minutes) |
| **Passing Score** | Variable Cut Score: **60% to 85%** (Determined dynamically via Item Response Theory based on exam form complexity) |
| **Question Format** | Scenario-based, Technical Multiple Choice, Best Answer Selection |

---

## ⚖️ EC-Council Domain Weightings & Curriculum Mapping

The 20 modules of CEH v13 map into **9 primary exam domains**. Notice that **Reconnaissance (Module 02)** is the highest weighted single domain on the entire exam!

```
+-----------------------------------------------------------------------------------+
|                        CEH v13 EXAM DOMAIN DISTRIBUTION                           |
+-----------------------------------------------------------------------------------+
| Domain 1: Information Security & Ethical Hacking Overview (Mod 01)        | ~6%   |
| Domain 2: Reconnaissance Techniques (Mod 02)                             | ~21%  |
| Domain 3: System Hacking Phases & Attack Techniques (Mod 06)              | ~17%  |
| Domain 4: Network & Perimeter Hacking (Mod 03, 08, 10, 11, 12)            | ~14%  |
| Domain 5: Web Application Hacking (Mod 13, 14, 15)                        | ~16%  |
| Domain 6: Wireless Network Hacking (Mod 16)                               | ~6%   |
| Domain 7: Mobile Platform, IoT, and OT Hacking (Mod 17, 18)               | ~8%   |
| Domain 8: Cloud Computing (Mod 19)                                        | ~6%   |
| Domain 9: Cryptography (Mod 20)                                           | ~6%   |
+-----------------------------------------------------------------------------------+
| Total                                                                     | 100%  |
+-----------------------------------------------------------------------------------+
```

---

## 📚 Test Prep Materials Directory

1. 🎯 **[Comprehensive 19-Question MCQ Revision Test](./comprehensive-mcq-revision-test.md)**
   - In-depth technical teardowns for all 19 multi-domain exam scenarios.
   - ASCII architecture diagrams, distractor analysis, and SOC engineering mitigations.
2. 📝 **[Module 01 & 02 High-Yield Practice Exam](./mod-01-and-02-practice-questions.md)**
   - 15 scenario-based questions matching EC-Council examination style.
   - Expandable explanations detailing *why* the correct answer is right and *why* distractors fail.
3. ⚡ **[Quick-Cram Exam Day Cheat Sheet](./quick-cram-cheat-sheet.md)**
   - Risk management formulas ($\text{ALE} = \text{SLE} \times \text{ARO}$, CVSS metrics).
   - Core reconnaissance ports, DNS record types, and email authentication tables.
   - Essential CLI tools & operational command flags.

---

## 🧠 EC-Council Test-Taking Strategies & Traps

```
+-----------------------------------------------------------------------------------+
|                         EXAM TRAP ELIMINATION PROTOCOL                            |
+-----------------------------------------------------------------------------------+
| 1. Watch for Qualifier Words | "FIRST", "BEST", "LEAST", "MOST", "NOT".           |
|                              | For example: What should a pentester do FIRST?     |
|                              | Always check scope / authorization / passive recon |
|                              | before initiating active scans!                    |
+-----------------------------------------------------------------------------------+
| 2. Eliminate Extremes        | Answers stating "always", "never", or "impossible" |
|                              | are almost always incorrect in security contexts.  |
+-----------------------------------------------------------------------------------+
| 3. Distinguish Passive vs    | Probes directed at the target's IP = ACTIVE.       |
|    Active Tools              | Queries against third parties (Censys, crt.sh,     |
|                              | Google, Whois) = PASSIVE.                          |
+-----------------------------------------------------------------------------------+
| 4. Contextualize the Role    | Read if the question asks from the perspective of  |
|                              | a Pen Tester (authorized lab/ROE), an Attacker,    |
|                              | or a Security Administrator / CISO.                |
+-----------------------------------------------------------------------------------+
```

---

*Navigation:* [🏠 CEH Master Hub](../README.md) | [📘 Module 01 Notes](../mod-01-introduction-to-ethical-hacking.md) | [📙 Module 02 Notes](../mod-02-footprinting-and-reconnaissance.md)
