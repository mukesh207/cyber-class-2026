# INE Skill Dive --- Log Anomaly Detection Basics

> **Lab:** Log Anomaly Detection Basics\
> **Category:** Forensics --- Webserver Log Analysis\
> **Difficulty:** Beginner / Novice\
> **Estimated time:** \~30 minutes\
> **Objective:** Identify the normal pattern in a large web-access log
> and locate the 5 anomalous entries.

------------------------------------------------------------------------

## 1. Lab Overview

This lab is an introduction to **webserver log anomaly detection**.

The lab provides a pre-parsed `logs.txt` file containing **more than one
million log entries**. Most entries follow the same hidden rules, but
**5 entries have been deliberately modified**.

Your job is to:

1.  Understand the structure of a normal log entry.
2.  Identify the rules followed by normal entries.
3.  Write or use a Python script to extract useful attributes.
4.  Detect values that do not follow the established pattern.
5.  Recover the complete anomalous log entries with `grep`.

The official walkthrough describes the same overall approach: inspect
several log entries, identify the pattern, tokenize the records with
Python, inspect the resulting sets/lists, and then use `grep` to
retrieve the complete suspicious records.

------------------------------------------------------------------------

## 2. What the Log Looks Like

A representative normal entry is:

``` text
CONNECT http://example.net/access_object.php?param1=1350&param2=brachy&param3=20APR2013
```

Break it into its components:

``` text
HTTP Method
    │
    ▼
CONNECT
    │
    └── URL
         │
         ├── param1 = 1350
         ├── param2 = brachy
         └── param3 = 20APR2013
```

So every record has four useful pieces of information:

  -----------------------------------------------------------------------
  Component               Example                 What we investigate
  ----------------------- ----------------------- -----------------------
  HTTP method             `CONNECT`               Is it one of the normal
                                                  methods?

  `param1`                `1350`                  Does the number belong
                                                  to the normal range?

  `param2`                `brachy`                Does it contain the
                                                  required `brac` prefix?

  `param3`                `20APR2013`             Is the date made from
                                                  valid day/month/year
                                                  patterns?
  -----------------------------------------------------------------------

> **Note:** The supplied PDF calls the final field "Param4" in one
> place, but the actual sample and supplied `detect.py` use `param3`.
> This walkthrough follows the actual log format and script.

------------------------------------------------------------------------

# 3. First Step --- Inspect the Log

Before writing detection logic, inspect a small sample.

### Display the first few entries

``` bash
head logs.txt
```

Or inspect around 10--15 entries:

``` bash
head -n 15 logs.txt
```

You can also use:

``` bash
less logs.txt
```

Inside `less`:

``` text
Space     → next page
b         → previous page
q         → quit
```

The important thing is **not to manually inspect all one million+
records**.

Instead, look for a pattern shared by normal records.

------------------------------------------------------------------------

# 4. Identify the Normal Pattern

From the sample records, the walkthrough identifies these rules:

### Rule 1 --- HTTP methods vary

Different records can use different HTTP methods.

For example:

``` text
GET
POST
PUT
DELETE
HEAD
TRACE
OPTIONS
CONNECT
PATCH
```

Therefore, simply seeing a different HTTP method does **not
automatically mean the entry is anomalous**.

The script collects all observed methods into a Python `set`.

------------------------------------------------------------------------

### Rule 2 --- `param1` is a number

Example:

``` text
param1=1350
```

The values belong to a normal numerical range/sequence.

This makes an unusually large or otherwise out-of-range number
suspicious.

The supplied walkthrough specifically identifies:

``` text
8119
```

as an outlier after sorting the `param1` values.

------------------------------------------------------------------------

### Rule 3 --- `param2` starts with `brac`

Examples of normal-looking values include:

``` text
brachy
brachi
brac...
```

The check is case-insensitive.

In Python:

``` python
if "brac" not in str(p2[1]).lower():
```

means:

> Convert the value to lowercase and verify that `brac` occurs in it.

Therefore:

``` text
brachy   → normal
brachi   → normal
bracxyz  → normal
crachy   → anomalous
```

------------------------------------------------------------------------

### Rule 4 --- `param3` follows `DDMMMYYYY`

Example:

``` text
20APR2013
```

Breakdown:

``` text
20   APR   2013
│     │      │
DD   MMM    YYYY
```

The script separates these into three sets:

``` python
set_dates
set_mon
set_year
```

This lets us notice unusual day, month, or year values.

Examples:

``` text
33JAN2013
20XYZ2019
```

contain suspicious date components.

------------------------------------------------------------------------

# 5. Why Python Is Useful Here

The log contains more than one million entries.

Manually checking them is impractical.

Python allows us to:

``` text
Read
  ↓
Tokenize
  ↓
Extract fields
  ↓
Store unique values
  ↓
Sort numerical values
  ↓
Identify outliers
```

The supplied `detect.py` implements exactly this basic strategy.

------------------------------------------------------------------------

# 6. Understanding the Supplied `detect.py`

The script starts by creating containers for the values we want to
analyze:

``` python
set_methods = set()
set_dates = set()
set_mon = set()
set_year = set()
num_list = []
```

### Why use a `set`?

A set stores **unique values**.

For example:

``` python
{"GET", "POST", "GET", "DELETE"}
```

becomes:

``` python
{"GET", "POST", "DELETE"}
```

This is useful when we only care about which distinct values appeared.

### Why use a list for `param1`?

Because we eventually want to sort the numerical values:

``` python
num_list.sort()
```

------------------------------------------------------------------------

# 7. Reading `logs.txt`

The script opens the log:

``` python
with open("logs.txt", "r") as f:
    file_content = f.readlines()
```

This reads the lines into memory.

Then:

``` python
file_content = [x.strip() for x in file_content]
```

removes newline and surrounding whitespace characters.

For example:

``` text
"GET http://example.net/...\n"
```

becomes:

``` text
"GET http://example.net/..."
```

------------------------------------------------------------------------

# 8. Processing Each Log Entry

The script loops through every record:

``` python
for line_item in file_content:
```

Each line is processed independently.

------------------------------------------------------------------------

## 8.1 Extract the HTTP Method

The log is split at spaces:

``` python
token_string = line_item.split(' ')
```

For:

``` text
CONNECT http://example.net/...
```

the result is conceptually:

``` python
[
    "CONNECT",
    "http://example.net/..."
]
```

The first element is the HTTP method:

``` python
set_methods.add(token_string[0])
```

So `CONNECT` is added to the set of observed methods.

------------------------------------------------------------------------

# 9. Extract the URL Parameters

The second token contains the URL and parameters.

The script splits it on `&`:

``` python
params = token_string[1].split('&')
```

For:

``` text
http://example.net/access_object.php?param1=1350&param2=brachy&param3=20APR2013
```

we get approximately:

``` text
param1=1350
param2=brachy
param3=20APR2013
```

This gives us the three parameters to analyze.

------------------------------------------------------------------------

# 10. Analyze `param1`

The script extracts `param1`:

``` python
p1 = params[0].split('=')
```

Conceptually:

``` python
["...param1", "1350"]
```

The value is then converted to an integer:

``` python
num_list.append(int(p1[1]))
```

This is important because numerical sorting should be numerical.

For example, strings could sort like:

``` text
100
20
3
```

while integers sort correctly:

``` text
3
20
100
```

------------------------------------------------------------------------

# 11. Analyze `param2`

Next:

``` python
p2 = params[1].split('=')
```

For:

``` text
param2=brachy
```

we get:

``` python
["param2", "brachy"]
```

The validation is:

``` python
if "brac" not in str(p2[1]).lower():
    print("[!] Anomalous entry found in param2: " + str(p2[1]))
```

### Why `.lower()`?

Because the normal rule is case-insensitive.

For example:

``` text
BRACHY
Brachy
brachy
```

can all contain the required sequence:

``` text
brac
```

After converting to lowercase:

``` text
BRACHY → brachy
```

------------------------------------------------------------------------

# 12. Analyze `param3`

The script extracts the final parameter:

``` python
p3 = params[2].split('=')
date_str = p3[1]
```

For:

``` text
param3=20APR2013
```

we have:

``` text
20APR2013
```

The script slices the string:

``` python
set_dates.add(date_str[0:2])
set_mon.add(date_str[2:5])
set_year.add(date_str[5:])
```

So:

``` text
20APR2013
```

becomes:

``` text
date = 20
month = APR
year = 2013
```

This gives us three separate collections to inspect.

------------------------------------------------------------------------

# 13. Print the Observed Values

At the end, the script prints:

``` python
print("\n--- Result Analysis ---")
print("[*] HTTP Methods observed: " + str(set_methods))
print("[*] Days observed: " + str(set_dates))
print("[*] Months observed: " + str(set_mon))
print("[*] Years observed: " + str(set_year))
```

This gives us a compact summary of what occurred throughout the huge
log.

Instead of displaying one million records, we can inspect the unique
values.

------------------------------------------------------------------------

# 14. Detect the `param1` Outlier

The script sorts the numerical values:

``` python
num_list.sort()
```

The supplied script initially keeps the complete list commented:

``` python
# print("[*] Sorted Param1 values: " + str(num_list))
```

This is intentional.

Printing a million+ values creates a huge amount of terminal output.

For the second run, uncomment it if necessary:

``` python
print("[*] Sorted Param1 values: " + str(num_list))
```

Then run:

``` bash
python3 detect.py
```

Because the list is sorted, an unusual value can stand out from the
normal range.

The official walkthrough identifies:

``` text
8119
```

as the numerical outlier.

------------------------------------------------------------------------

# 15. Run the Detection Script

Make sure the files are in the same directory:

``` bash
ls
```

You should have something similar to:

``` text
detect.py
logs.txt
```

Run:

``` bash
python3 detect.py
```

The supplied Python 3 version reports an anomalous `param2` value and
then prints the observed sets.

A result can look conceptually like:

``` text
[!] Anomalous entry found in param2: crachy

--- Result Analysis ---
[*] HTTP Methods observed: {...}
[*] Days observed: {...}
[*] Months observed: {...}
[*] Years observed: {...}
```

The exact ordering of values inside Python sets is not important.

------------------------------------------------------------------------

# 16. Find the Five Anomalies

The anomalies come from different fields.

The five suspicious records identified by the supplied walkthrough are:

  -------------------------------------------------------------------------------------------------------------------------------------------------
  \#                HTTP Method       Suspicious Field  Complete Entry
  ----------------- ----------------- ----------------- -------------------------------------------------------------------------------------------
  1                 `HEADER`          HTTP method       `HEADER http://example.net/access_object.php?param1=2828&param2=brachy&param3=22JUL2018`

  2                 `DELETE`          Day `33`          `DELETE http://example.net/access_object.php?param1=2931&param2=brachy&param3=33JAN2013`

  3                 `DELETE`          Month `XYZ`       `DELETE http://example.net/access_object.php?param1=2823&param2=brachi&param3=20XYZ2019`

  4                 `CONNECT`         `param1=8119` and `CONNECT http://example.net/access_object.php?param1=8119&param2=brachm&param3=23JUL2011`
                                      `param2=brachm`   

  5                 `POST`            `param2=crachy`   `POST http://example.net/access_object.php?param1=3970&param2=crachy&param3=08SEP2013`
  -------------------------------------------------------------------------------------------------------------------------------------------------

> The table above reproduces the five anomalous entries listed in the
> supplied lab walkthrough. The lab's intended purpose is to discover
> these by analyzing the normal rules rather than simply reading the
> answer list.

------------------------------------------------------------------------

# 17. Why Each Entry Is Anomalous

## Anomaly 1 --- Invalid HTTP method

``` text
HEADER http://example.net/access_object.php?param1=2828&param2=brachy&param3=22JUL2018
```

The observed normal method set does not contain:

``` text
HEADER
```

Therefore:

``` text
HEADER
```

is the anomaly.

Notice that the other fields look structurally normal:

``` text
param1=2828
param2=brachy
param3=22JUL2018
```

This demonstrates why checking only one field at a time is useful.

------------------------------------------------------------------------

## Anomaly 2 --- Invalid day

``` text
DELETE http://example.net/access_object.php?param1=2931&param2=brachy&param3=33JAN2013
```

The date is:

``` text
33JAN2013
```

Breakdown:

``` text
33 | JAN | 2013
```

The day value:

``` text
33
```

is outside the normal calendar-day range.

The anomaly is therefore:

``` text
33
```

------------------------------------------------------------------------

## Anomaly 3 --- Invalid month

``` text
DELETE http://example.net/access_object.php?param1=2823&param2=brachi&param3=20XYZ2019
```

Breakdown:

``` text
20 | XYZ | 2019
```

The month:

``` text
XYZ
```

does not match a normal three-letter month abbreviation.

The suspicious component is:

``` text
XYZ
```

------------------------------------------------------------------------

## Anomaly 4 --- Numerical outlier

``` text
CONNECT http://example.net/access_object.php?param1=8119&param2=brachm&param3=23JUL2011
```

The important value is:

``` text
param1=8119
```

After sorting all `param1` values, the walkthrough identifies `8119` as
being far outside the normal range.

The entry also contains:

``` text
param2=brachm
```

which still contains `brac`, so it passes the supplied `param2` check.

The intended detection method for this anomaly is the numerical outlier
analysis.

------------------------------------------------------------------------

## Anomaly 5 --- Invalid `param2`

``` text
POST http://example.net/access_object.php?param1=3970&param2=crachy&param3=08SEP2013
```

The normal rule requires `param2` to contain:

``` text
brac
```

But this value is:

``` text
crachy
```

It does not contain:

``` text
brac
```

Therefore the Python condition triggers:

``` python
if "brac" not in str(p2[1]).lower():
```

------------------------------------------------------------------------

# 18. Recover the Complete Log Entries with `grep`

Once you know a suspicious value, use `grep` to locate the complete
record.

### Find the invalid HTTP method

``` bash
grep '^HEADER ' logs.txt
```

### Find the invalid day

``` bash
grep 'param3=33JAN2013' logs.txt
```

### Find the invalid month

``` bash
grep 'param3=20XYZ2019' logs.txt
```

### Find the numerical outlier

``` bash
grep 'param1=8119' logs.txt
```

### Find the invalid `param2`

``` bash
grep 'param2=crachy' logs.txt
```

You can also search using the distinctive value alone:

``` bash
grep 'crachy' logs.txt
```

The lab walkthrough specifically recommends using `grep` after
identifying the anomalous values to recover the complete log entries.

------------------------------------------------------------------------

# 19. Useful `grep` Options

If you want cleaner output:

### Show line numbers

``` bash
grep -n 'param1=8119' logs.txt
```

Example:

``` text
123456:CONNECT http://example.net/...
```

The number before the colon is the line number.

------------------------------------------------------------------------

### Ignore case

``` bash
grep -i 'crachy' logs.txt
```

------------------------------------------------------------------------

### Show only the number of matches

``` bash
grep -c 'param1=8119' logs.txt
```

------------------------------------------------------------------------

### Search several patterns

You can use extended regular expressions:

``` bash
grep -E 'HEADER|33JAN2013|20XYZ2019|8119|crachy' logs.txt
```

This is useful for quickly validating the five anomalies.

------------------------------------------------------------------------

# 20. A Better Python 3 Version

The supplied `detect.py` is intentionally simple and educational.

For learning purposes, we can make it slightly more robust while
preserving the same detection logic.

``` python
#!/usr/bin/env python3

set_methods = set()
set_dates = set()
set_mon = set()
set_year = set()
num_list = []

with open("logs.txt", "r") as f:
    file_content = [line.strip() for line in f]

for line_item in file_content:

    # Split method from URL
    token_string = line_item.split(" ", 1)

    if len(token_string) != 2:
        continue

    method = token_string[0]
    url = token_string[1]

    set_methods.add(method)

    # Split URL parameters
    params = url.split("&")

    if len(params) != 3:
        continue

    # Param1
    p1 = params[0].split("=", 1)

    if len(p1) == 2:
        try:
            num_list.append(int(p1[1]))
        except ValueError:
            pass

    # Param2
    p2 = params[1].split("=", 1)

    if len(p2) == 2:
        value = p2[1]

        if "brac" not in value.lower():
            print("[!] Anomalous entry found in param2:", value)

    # Param3
    p3 = params[2].split("=", 1)

    if len(p3) == 2:
        date_str = p3[1]

        if len(date_str) >= 7:
            set_dates.add(date_str[0:2])
            set_mon.add(date_str[2:5])
            set_year.add(date_str[5:])

print("\n--- Result Analysis ---")
print("[*] HTTP Methods observed:", set_methods)
print("[*] Days observed:", set_dates)
print("[*] Months observed:", set_mon)
print("[*] Years observed:", set_year)

num_list.sort()

if num_list:
    print("[*] Minimum Param1:", num_list[0])
    print("[*] Maximum Param1:", num_list[-1])
```

### Why this version is safer

The original educational script assumes every log line has exactly the
expected format.

The improved version:

-   Splits only once when separating the method and URL.
-   Checks that expected fields exist.
-   Handles invalid numeric conversion.
-   Avoids crashing on malformed records.
-   Prints the minimum and maximum `param1` values without dumping the
    entire million-entry list.

For the actual lab, however, the supplied `detect.py` is enough to
understand the intended technique.

------------------------------------------------------------------------

# 21. An Even More Direct Detection Approach

Once you understand the rules, you can search for the known anomaly
patterns directly.

``` bash
grep -E '^HEADER |param3=33JAN2013|param3=20XYZ2019|param1=8119|param2=crachy' logs.txt
```

This should return the five suspicious entries.

This is useful as a **validation step**, but it is better to understand
how the values were discovered first.

------------------------------------------------------------------------

# 22. Recommended Lab Workflow

A clean workflow for this lab is:

``` text
             logs.txt
                │
                ▼
        Inspect sample records
                │
                ▼
       Identify normal pattern
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
      Method   Params    Date
        │       │        │
        │       ├──param1 → numeric range
        │       └──param2 → "brac"
        │
        ▼
     Python analysis
        │
        ▼
   Identify outliers
        │
        ▼
       grep
        │
        ▼
 Complete anomalous entries
```

------------------------------------------------------------------------

# 23. Commands Used in the Lab

Keep this quick-reference section for future revision.

### Inspect logs

``` bash
head logs.txt
head -n 15 logs.txt
less logs.txt
```

### Run Python

``` bash
python3 --version
python3 detect.py
```

### Search anomalies

``` bash
grep '^HEADER ' logs.txt
grep 'param3=33JAN2013' logs.txt
grep 'param3=20XYZ2019' logs.txt
grep 'param1=8119' logs.txt
grep 'param2=crachy' logs.txt
```

### Validate all five

``` bash
grep -E '^HEADER |param3=33JAN2013|param3=20XYZ2019|param1=8119|param2=crachy' logs.txt
```

------------------------------------------------------------------------

# 24. What This Lab Teaches

This small exercise demonstrates several important SOC/DFIR concepts.

## Pattern Recognition

Normal logs establish a baseline.

Anomaly detection then asks:

> "Does this event follow the baseline?"

------------------------------------------------------------------------

## Structured Log Parsing

Instead of treating a log as plain text, break it into fields:

``` text
Method
URL
 ├── param1
 ├── param2
 └── param3
```

This makes analysis much easier.

------------------------------------------------------------------------

## Statistical / Range-Based Thinking

A value such as:

``` text
8119
```

may look like a normal integer by itself.

It becomes suspicious when compared with the distribution of all other
`param1` values.

------------------------------------------------------------------------

## Input Validation

The `param2` rule is a simple example of validation:

``` python
"brac" in value.lower()
```

Anything that violates the expected format deserves investigation.

------------------------------------------------------------------------

## Date Component Analysis

Splitting:

``` text
20APR2013
```

into:

``` text
20
APR
2013
```

allows individual components to be checked.

------------------------------------------------------------------------

## Command-Line Investigation

After Python identifies the suspicious value, `grep` provides a fast way
to recover the complete record.

This is a very practical Linux/SOC workflow:

``` text
Script → suspicious value → grep → complete event
```

------------------------------------------------------------------------

# 25. Final Findings

The five anomalous log entries identified in the supplied lab material
are:

``` text
HEADER http://example.net/access_object.php?param1=2828&param2=brachy&param3=22JUL2018

DELETE http://example.net/access_object.php?param1=2931&param2=brachy&param3=33JAN2013

DELETE http://example.net/access_object.php?param1=2823&param2=brachi&param3=20XYZ2019

CONNECT http://example.net/access_object.php?param1=8119&param2=brachm&param3=23JUL2011

POST http://example.net/access_object.php?param1=3970&param2=crachy&param3=08SEP2013
```

### Anomaly summary

``` text
1. HEADER
   └── Unexpected HTTP method

2. 33JAN2013
   └── Invalid day: 33

3. 20XYZ2019
   └── Invalid month: XYZ

4. param1=8119
   └── Numerical outlier

5. param2=crachy
   └── Does not contain required "brac" pattern
```

------------------------------------------------------------------------

# 26. Key Takeaways

Remember the investigation pattern:

> **Baseline → Parse → Compare → Isolate → Verify**

For this lab:

``` text
Baseline
   ↓
Find the normal log structure
   ↓
Parse the fields
   ↓
Build sets/lists of observed values
   ↓
Find values outside the expected pattern
   ↓
Use grep to recover the full event
```

The most important lesson is not the five answers themselves.

It is the methodology:

**Large logs become manageable when you identify structure and reduce
millions of events into a small set of meaningful attributes.**

------------------------------------------------------------------------

## Source Notes

This walkthrough is based on the provided INE/AttackDefense lab material
and the supplied `detect.py` script. The official PDF describes the lab
as **Log Anomaly Detection Basics**, categorized under **Forensics:
Webserver Log Analysis**, and states that the supplied log contains more
than one million entries with five anomalous records.

The supplied Python script extracts HTTP methods, date/day/month/year
components, checks `param2` for the `brac` pattern, and sorts `param1`
values for outlier inspection.
