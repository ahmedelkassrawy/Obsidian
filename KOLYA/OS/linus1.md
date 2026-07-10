## Linux Component
* **User interacting with Terminal:** The user types into the terminal (`bash$`).
* **Application Layer:** Shell and applications interact with the Kernel via APIs and libs.
* **Kernel:** Contains modules that communicate directly with the Hardware.
* **Hardware:** Includes IDE, SATA, USB, etc..
* **Command Structure:** `command [-option] [-option] [--option(word)] [argument]`.
### Basic Commands
* `ls` 
* `cat` 
* `uname` 
* `cal 10 2023` 
* `date` 
* `man` 
* `tree` 
* `apt` 
## User Accounts
**What is a user account?** A user account is a systematic approach to track and monitor the usage of system resources. Each user account contains two unique identifiers; username and UID.

Components of a user account include:
* UID (User ID) 
* GID (Group ID) 
* Home directory 
* Default shell, and password 

* Example output: `$john:x:1002:1002:,,:/home/john:/bin/bash$` 
### Users Type
1. The root user account 
	* This is the main user account in Linux system.
	* It is automatically created during the installation.
	* It has the highest privilege in system.
	* It can do any administrative work and can access any service.

* ID: `0`.

2. The regular user account 
	* This is the normal user account. During the installation, one regular user account is created automatically.
	* After the installation, we can create as many regular user accounts as we need.
	* It can perform only the tasks for which it is allowed and can access only those files and services for which it is authorized.

* ID: `>= 1000`.

3. The service account 
	* Service accounts are created by installation packages when they are installed.
	* Dummy user doesn't have home directory.

* ID: `0 < id < 1000`.

### User Management Practice
**Viewing User Info:**
* Display user id: `id user_name` 
* Get information about users in system: `tail /etc/passwd` 
* Get users' password: `tail /etc/shadow` 

**Switching and Creating Users:**
* Switch to root user: `sudo su -` or `su` 
* Switch to username: `username` (Note: command is usually `su username`) 
* Add new user: `useradd -u user_id -d home_directory -s default_shell_used` 
* Add password for user: `passwd user` 
* Another way to add user: `adduser user_name` 
* Delete user and home directory: `userdel -r username` 
## The File System
Think of the file system as a building, a directory is a room, and a file is a desk.
**Windows vs Linux Paths:** 
* 
**Windows:** `C:\`, `Program Files`, `Windows`, `temp`, `Common Files`, `system32`, `Microsoft Office`, `Microsoft.NET`, `assembly`, `Web` .
* 
**Linux:** `bin`, `dev`, `etc`, `home`, `lib`, `mnt`, `proc`, `root`, `sbin`, `tmp`, `usr` .

### Linux File System Structure

The root of the file system is `/`. Subdirectories include: `/bin/`, `/boot/`, `/dev/`, `/etc/`, `/home/`, `/lib/`, `/media/`, `/mnt/`, `/opt/`, `/root/`, `/sbin/`, `/srv/`, `/tmp/`, `/usr/`, `/var/` .

* `/etc` ==> It holds the configuration files of the system (passwd, shadows and group).
* `/var` ==> Variable data of the system, these files are dynamically changed (database files, mail directory, log files, printer and website content).
* `/bin` ==> User commands (binaries) ==> ls command.
* `/sbin` ==> System administration command.
* `/lib` ==> Contains kernel modules and those shared library images (the C programming code library) needed to boot the system and run the commands in the root filesystem.
* `/home/` ==> Standard user home (ali, ahmed, sami). ex. `/home/ali`, `/home/sami`, `/home/ahmed`
* `/root` ==> Super user home.
* `/tmp` ==> Temp files that is deleted after 10 days.
* `/dev` ==> System devices (hard disks).
* `/boot` ==> To boot the operating system (grub).
* `/usr` ==> Shared files between users.
### Navigating the File System
* `pwd`: Print work directory.
* `cd path`: Change directory.
* `cd -`: Last working directory.
* `cd` or `cd ~`: Go to home directory.
* `cd ~user_name`: Go to username home directory.
* `.`: Current working directory.
* `..`: Parent directory.

### How to Get Path
**1- Absolute path:** Is defined as the specifying the location of a file or directory from the root directory (`/`).
**2- Relative path:** Is defined as the path related to the present working directly (`pwd`). It starts at your current directory and never starts with a `/`.

**Examples:**
* Current Directory: `work` (inside `jono`). Destination: `cory`. 
* Absolute path: `/home/cory`.
* Relative path: `./../../cory`.

* Current Directory: `work`. Destination: `photos`. 
* Absolute path: `/home/jono/photos`.
* Relative path: `./photos`.

* Current Directory: `work`. Destination: `lib` (under `/usr`). 
* Absolute path: `/usr/lib`.
* Relative path: `./../../../usr/lib`.

### File and Directory Operations
| **Operation** | **Files**                           | **Directories**                                                                            |
| ------------- | ----------------------------------- | ------------------------------------------------------------------------------------------ |
| **Create**    | `touch file_name1 file_name2 .....` | `mkdir dir_name1 dir_name2 dir_name3....`                                                  |
| **Copy**      | `cp source_file destination_file`   | `cp source_directory directory` (copy dir if empty). Put `-r` (recursive) if has contents. |
| **Delete**    | `rm file_name1 file_name2 .....`    | `rmdir dir_name1 dir_name2 dir_name3....` (delete directories if empty).                   |
 
* `rm -r dir_name` delete dir if not empty in this case terminal ask before delete any of dir contents.
* `rm -rf dir` remove with out ask.

**Moving and Renaming:**
* `mv options source(s) target`.
* `-i` Prevents you from accidentally overwriting existing files or directories.
### Viewing and Editing File Content
* `cat fname` 
* `more fname` 
* Spacebar: moves forward on screen 
* b: move back one screen 
* /string: search forward for pattern 
* q: quit and return to the shell prompt 

* `head -n fname`: show first n lines 
* `tail -n fname`: show last n lines 

**Editors:**
* **gedit:** The gedit text editor is a graphical tool for editing text files. Command: `gedit new_filename`

* **nano:** Nano is a user-friendly, simple text editor. Unlike vim editor or any other command-line editor, it doesn't have any mode. It has an easy GUI (Graphical User Interface) which allows users to interact directly with the text in spite of switching between the modes as in vim editor. Command: `nano new_filename`.
---

# Solutions to Presentation Tasks

### Task 1: Create a User Account (Page 10)

**Requirements:** Create a user account `sara`, full name `sara mohamed`, password `1234`, and show details.

```bash
# Create the user and add the full name comment
sudo useradd -c "sara mohamed" sara

# Set the password (you will be prompted to type 1234)
sudo passwd sara

# Show user details
id sara

```

### Task 2: Relative and Absolute Paths (Page 21/22)

**Requirements:** Find the paths from the current directory `work` (`/home/jono/work`) to the destination `lib` (`/usr/lib`).

* **Absolute path:** `/usr/lib`
* **Relative path:** `../../../usr/lib` *(Note: The presentation slide uses `./../../../usr/lib` which works, but strictly speaking, `../../../usr/lib` is the standard notation).*

### Task 3: Create and Remove Hierarchy (Page 25)

**Requirements:** Create `dir1` containing `dir11` and `dir12`, and `dir11` containing `file1` under your home directory. Then remove `dir11` in one step.

```bash
# Create the directory structure (-p creates parent directories as needed)
mkdir -p ~/dir1/dir11 ~/dir1/dir12

# Create the file inside dir11
touch ~/dir1/dir11/file1

# Remove dir11 and its contents in one step
rm -r ~/dir1/dir11

```

### Task 4: Copy and Rename File (Page 26)

**Requirements:** Copy `/etc/passwd` to your home directory as `mypasswd`. Rename it to `oldpasswd`.

```bash
# Copy the file to the home directory with the new name
cp /etc/passwd ~/mypasswd

# Rename the file using the move (mv) command
mv ~/mypasswd ~/oldpasswd

```

### Task 5: View and Edit Files (Page 30)

**Requirements:** Create `hello.text` using an editor and cat contents. Display first 4 lines of `/etc/passwd` and last 7 lines.

```bash
# Open nano to create the text file, type your content, and save (Ctrl+O, Enter, Ctrl+X)
nano hello.text

# View the contents
cat hello.text

# Display the first 4 lines
head -n 4 /etc/passwd

# Display the last 7 lines
tail -n 7 /etc/passwd

```

