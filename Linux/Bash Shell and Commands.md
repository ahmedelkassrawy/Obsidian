## 1. Listing Files with `ls`

### Overview

The `ls` command lists files and directories in the current directory.

### Code

```bash
ls -l
```

### Explanation

- **Command**: `ls`
    - Lists files and directories in the current working directory.
- **Flag**: `-l`
    - Enables long listing format, showing additional details like permissions, owner, size, and modification date.
- **Use Case**: Useful for inspecting file metadata in a directory.

## 2. Finding Executable Locations with `which`

### Overview

The `which` command locates the executable file for a given command.

### Code

```bash
which ls
```

### Explanation

- **Command**: `which`
    - Searches the system's `PATH` environment variable to find the full path of the specified command's executable.
- **Example**: `which ls` might return `/bin/ls` or `/usr/bin/ls`, depending on the system.
- **Use Case**: Helps identify where a command is installed, useful for debugging or verifying command versions.

## 3. Displaying Current Directory with `pwd`

### Overview

The `pwd` command prints the full path of the current working directory.

### Code

```bash
pwd
# Output: /Users/noahgift
```

### Explanation

- **Command**: `pwd` (Print Working Directory)
    - Displays the absolute path of the current directory.
- **Output**: `/Users/noahgift` (example path, varies by system and user).
- **Use Case**: Confirms your current location in the file system, especially when navigating directories.

## 4. Changing Directories with `cd`

### Overview

The `cd` command changes the current working directory.

### Code

```bash
cd /tmp
```

### Explanation

- **Command**: `cd`
    - Changes the current directory to the specified path.
- **Path**: `/tmp`
    - A common temporary directory in Unix-like systems for storing temporary files.
- **Use Case**: Used to navigate to different directories for file operations or script execution.

## 5. Input/Output Operations

### Overview

This section demonstrates creating a file with `echo`, redirecting output, and counting bytes and words with `wc`.

### Code

```bash
cd /tmp
echo "foo bar baz" > out.txt
cat out.txt | wc -c
# Output: 12
cat out.txt | wc -w
# Output: 3
```

### Explanation

- **Step 1: `cd /tmp`**
    - Changes the current directory to `/tmp`.
- **Step 2: `echo "foo bar baz" > out.txt`**
    - `echo`: Outputs the string `"foo bar baz"` to standard output.
    - `>`: Redirects the output to `out.txt`, overwriting it if it exists or creating it if it doesn't.
    - **Result**: Creates `out.txt` with the content `foo bar baz` plus a newline (added by `echo`).
- **Step 3: `cat out.txt | wc -c`**
    - `cat out.txt`: Reads and outputs the content of `out.txt`.
    - `|`: Pipes the output to the next command.
    - `wc -c`: Counts the number of bytes in the input.
    - **Content Analysis**: The string `foo bar baz` has 11 characters (3 for `foo`, 1 space, 3 for `bar`, 1 space, 3 for `baz`), plus 1 newline character, totaling 12 bytes.
    - **Output**: `12`.
- **Step 4: `cat out.txt | wc -w`**
    - `cat out.txt`: Outputs the content of `out.txt`.
    - `|`: Pipes the output to the next command.
    - `wc -w`: Counts the number of words (sequences of characters separated by whitespace).
    - **Content Analysis**: `foo bar baz` contains 3 words (`foo`, `bar`, `baz`).
    - **Output**: `3`.
- **Use Case**: Demonstrates file creation, output redirection, and text analysis with pipes.

## 6. Creating and Running a Bash Script

### Overview

This section shows how to create a simple Bash script, make it executable, and run it.

### Code

```bash
#!/usr/bin/env bash

echo "hello world"
```

```bash
chmod +x hello.sh
./hello.sh
# Output: hello world
```

### Explanation

- **Script Creation**:
    - **Shebang**: `#!/usr/bin/env bash`
        - Specifies that the script should be executed using the Bash interpreter, located via the `env` command for portability.
    - **Command**: `echo "hello world"`
        - Outputs the string `"hello world"` to standard output.
- **Making Executable**:
    - `chmod +x hello.sh`
        - Adds the executable permission to `hello.sh`, allowing it to be run as a program.
- **Running the Script**:
    - `./hello.sh`
        - Executes the script in the current directory (`.`).
        - **Output**: `hello world` (case preserved as in the script).
- **Use Case**: Introduces basic Bash scripting for automating tasks.

