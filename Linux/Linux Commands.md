## File and Directory Management

### `ls` - List Files and Directories

Lists files and directories in the current directory.

- **Syntax**: `ls [options]`
- **Options**:
    - `-a`: Include hidden files.
    - `-l`: Long format (permissions, owner, size, etc.).
    - `-art`: Long format, sorted by modification time, including hidden files.
- **Example**:
    
    ```bash
    ls
    ls -al
    ls -lart
    ```
    

### `cd` - Change Directory

Changes the current working directory.

- **Syntax**: `cd [directory]`
- **Example**:
    
    ```bash
    cd test
    ```
    

### `mkdir` - Create Directory

Creates a new directory.

- **Syntax**: `mkdir [directory_name]`
- **Example**:
    
    ```bash
    mkdir test
    ```
    

### `rmdir` - Remove Directory

Removes an empty directory.

- **Syntax**: `rmdir [directory_name]`
- **Example**:
    
    ```bash
    rmdir test
    ```
    

### `pwd` - Print Working Directory

Displays the current working directory.

- **Syntax**: `pwd`
- **Example**:
    
    ```bash
    pwd
    ```
    

### `touch` - Create or Update File

Creates an empty file or updates the timestamp of an existing file.

- **Syntax**: `touch [filename]`
- **Example**:
    
    ```bash
    touch bappy.txt
    ```
    

### `cp` - Copy Files or Directories

Copies files or directories to a specified location.

- **Syntax**: `cp [source] [destination]`
- **Example**:
    
    ```bash
    cp example.txt backup/
    ```
    

### `mv` - Move or Rename Files/Directories

Moves or renames files or directories.

- **Syntax**: `mv [source] [destination]`
- **Example**:
    
    ```bash
    mv example.txt backup/
    ```
    

### `rm` - Remove Files or Directories

Deletes files or directories (use `-r` for directories).

- **Syntax**: `rm [options] [file/directory]`
- **Example**:
    
    ```bash
    rm example.txt
    ```
    

### `cat` - Display File Content

Concatenates and displays file content.

- **Syntax**: `cat [filename]`
- **Example**:
    
    ```bash
    cat bappy.txt
    ```
    

### `head` - Display First Lines

Displays the first 10 lines of a file (customizable with `-n`).

- **Syntax**: `head [options] [filename]`
- **Example**:
    
    ```bash
    head file.txt
    ```
    

### `tail` - Display Last Lines

Displays the last 10 lines of a file (customizable with `-n`).

- **Syntax**: `tail [options] [filename]`
- **Example**:
    
    ```bash
    tail file.txt
    ```
    

## File Permissions and Ownership

### `chmod` - Change Permissions

Modifies file or directory permissions.

- **Syntax**: `chmod [permissions] [file]`
- **Permissions**: Three digits (owner, group, others):
    - `0`: No permission
    - `1`: Execute
    - `2`: Write
    - `3`: Write + Execute
    - `4`: Read
    - `5`: Read + Execute
    - `6`: Read + Write
    - `7`: Read + Write + Execute
- **Example**:
    
    ```bash
    chmod 700 file.txt
    ```
    

### `chown` - Change Owner

Changes the owner of a file or directory.

- **Syntax**: `chown [new_owner] [file]`
- **Example**:
    
    ```bash
    chown bappy example.txt
    ```
    

## Package Management

### `sudo apt update` - Update Package Lists

Refreshes the list of available packages.

- **Syntax**: `sudo apt update`
- **Example**:
    
    ```bash
    sudo apt update
    ```
    

### `sudo apt-get upgrade` - Upgrade Packages

Upgrades installed packages to their latest versions.

- **Syntax**: `sudo apt-get upgrade [-y]`
- **Example**:
    
    ```bash
    sudo apt-get update -y
    sudo apt-get upgrade
    ```
    

## Text Editing

### `vim` - Text Editor

Opens Vim for editing files.

- **Syntax**: `vim [filename]`
- **Key Commands**:
    - `i`: Enter Insert mode.
    - `Esc`: Exit Insert mode.
    - `:w`: Save file.
    - `:wq` or `ZZ`: Save and quit.
    - `:q!`: Quit without saving.
- **Example**:
    
    ```bash
    vim happy.txt
    ```
    

## Archiving and Compression

### `tar` - Create/Extract Archives

Creates or extracts tar archives, often with compression.

- **Syntax**: `tar [options] [archive] [files]`
- **Options**:
    - `cf`: Create archive.
    - `xf`: Extract archive.
    - `z`: Use gzip compression.
    - `j`: Use bzip2 compression.
- **Example**:
    
    ```bash
    tar cf archive.tar file1 file2 file3
    ```
    

### `gzip` - Compress Files

Compresses files into `.gz` format.

- **Syntax**: `gzip [file]`
- **Example**:
    
    ```bash
    gzip file.txt
    ```
    

### `gunzip` - Decompress Files

Decompresses `.gz` files.

- **Syntax**: `gunzip [file.gz]`
- **Example**:
    
    ```bash
    gunzip file.txt.gz
    ```
    

## Networking

### `ssh` - Secure Shell

Connects to a remote server securely.

- **Syntax**: `ssh [username]@[server_address]`
- **Example**:
    
    ```bash
    ssh bappy@server_address
    ```
    

### `scp` - Secure Copy

Securely copies files between systems.

- **Syntax**: `scp [source] [destination]`
- **Example**:
    
    ```bash
    scp myfile.txt user@remotehost:/home/user/
    ```
    

### `ping` - Test Network Connectivity

Tests connectivity to a host.

- **Syntax**: `ping [host]`
- **Example**:
    
    ```bash
    ping 8.8.8.8
    ```
    

### `ifconfig` - Network Interface Configuration

Displays or configures network interfaces (use `ip` for modern systems).

- **Syntax**: `ifconfig`
- **Example**:
    
    ```bash
    ifconfig
    ```
    

### `netstat` - Network Connections

Displays network connection information.

- **Syntax**: `netstat`
- **Example**:
    
    ```bash
    netstat
    ```
    

### `route` - Network Routing

Views or configures network routing tables.

- **Syntax**: `route [options]`
- **Example**:
    
    ```bash
    route
    ```
    

## Process and System Monitoring

### `top` - System Resource Usage

Displays real-time system resource usage and processes.

- **Syntax**: `top`
- **Example**:
    
    ```bash
    top
    ```
    

### `htop` - Interactive Process Viewer

An enhanced, interactive process viewer.

- **Syntax**: `htop`
- **Example**:
    
    ```bash
    htop
    ```
    

### `ps` - Process Status

Displays information about running processes.

- **Syntax**: `ps [options]`
- **Example**:
    
    ```bash
    ps aux
    ```
    

### `kill` - Terminate Process

Terminates a process by its PID.

- **Syntax**: `kill [PID]`
- **Example**:
    
    ```bash
    kill 1234
    ```
    

## System Services

### `systemctl` - Manage Services

Controls system services (start, stop, status).

- **Syntax**: `systemctl [action] [service]`
- **Example**:
    
    ```bash
    systemctl start nginx
    systemctl status nginx
    systemctl stop nginx
    ```
    

### `service` - Control Services

Manages system services (alternative to `systemctl`).

- **Syntax**: `service [service] [action]`
- **Example**:
    
    ```bash
    service apache2 start
    ```
    

## User Management

### `useradd` - Add User

Creates a new user.

- **Syntax**: `useradd [username]`
- **Example**:
    
    ```bash
    useradd bappy
    ```
    

### `passwd` - Change Password

Changes a user’s password.

- **Syntax**: `passwd [username]`
- **Example**:
    
    ```bash
    passwd bappy
    ```
    

### `userdel` - Delete User

Deletes a user from the system.

- **Syntax**: `userdel [username]`
- **Example**:
    
    ```bash
    userdel bappy
    ```
    

### `su` - Switch User

Switches to another user account.

- **Syntax**: `su [username]`
- **Example**:
    
    ```bash
    su john
    ```
    

### `sudo` - Execute with Privileges

Runs a command with elevated privileges.

- **Syntax**: `sudo [command]`
- **Example**:
    
    ```bash
    sudo apt update
    ```
    

## System Information

### `uptime` - System Uptime

Displays system uptime and load average.

- **Syntax**: `uptime`
- **Example**:
    
    ```bash
    uptime
    ```
    

### `df` - Disk Space Usage

Displays disk space usage.

- **Syntax**: `df [options]`
- **Example**:
    
    ```bash
    df
    ```
    

### `du` - Directory Disk Usage

Displays disk usage by file or directory.

- **Syntax**: `du [options] [directory]`
- **Example**:
    
    ```bash
    du
    ```
    

### `mount` - Mount Filesystem

Mounts a filesystem to a directory.

- **Syntax**: `mount [device] [mount_point]`
- **Example**:
    
    ```bash
    sudo mount /dev/sdb1 /mnt/usb
    ```
    

### `umount` - Unmount Filesystem

Unmounts a filesystem.

- **Syntax**: `umount [mount_point]`
- **Example**:
    
    ```bash
    sudo umount /mnt/usb
    ```
    

### `date` - System Date and Time

Displays or sets the system date and time.

- **Syntax**: `date`
- **Example**:
    
    ```bash
    date
    ```
    

### `whoami` - Current User

Displays the current user’s username.

- **Syntax**: `whoami`
- **Example**:
    
    ```bash
    whoami
    ```
    

### `uname` - System Information

Displays system information (e.g., kernel version).

- **Syntax**: `uname [options]`
- **Example**:
    
    ```bash
    uname -a
    ```
    

### `finger` - User Information

Displays detailed information about a user.

- **Syntax**: `finger [username]`
- **Example**:
    
    ```bash
    finger bappy
    ```
    

## Miscellaneous

### `man` - Command Manual

Displays the manual for a command.

- **Syntax**: `man [command]`
- **Example**:
    
    ```bash
    man ls
    ```
    

### `history` - Command History

Lists previously executed commands.

- **Syntax**: `history`
- **Example**:
    
    ```bash
    history
    ```
    

### `echo` - Display Text

Displays text or variables to the console.

- **Syntax**: `echo [text]`
- **Example**:
    
    ```bash
    echo 'Hello guys!'
    ```
    

### `tee` - Redirect Output

Redirects output to both a file and the console.

- **Syntax**: `[command] | tee [file]`
- **Example**:
    
    ```bash
    ls | tee file.txt
    ```
    

### `locate` - Find Files

Locates files on the system using a database.

- **Syntax**: `locate [filename]`
- **Example**:
    
    ```bash
    locate file.txt
    ```
    

### `sort` - Sort Lines

Sorts lines of text in a file or input.

- **Syntax**: `sort [file]`
- **Example**:
    
    ```bash
    sort file.txt
    ```
    

### `uniq` - Remove Duplicates

Removes duplicate lines from a file or input.

- **Syntax**: `uniq [file]`
- **Example**:
    
    ```bash
    uniq file.txt
    ```
    

### `which` - Locate Command

Locates a program or command in the system path.

- **Syntax**: `which [command]`
- **Example**:
    
    ```bash
    which ls
    ```