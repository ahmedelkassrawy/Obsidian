# Linux File and Directory Management

## Navigation Commands

### Check Current Directory

- **Command**: `pwd`
    - **Purpose**: Displays the absolute path of the current working directory.
    - **Example**:
        
        ```bash
        pwd
        # Output: /home/user
        ```
        

### List Directory Contents

- **Command**: `ls`
    - **Purpose**: Lists files and directories in the current directory.
    - **Example**:
        
        ```bash
        ls
        # Output: file1.txt file2.txt directory
        ```
        
- **With Directory**:
    - Lists contents of a specific directory.
        
        ```bash
        ls directory
        # Output: ls seasonal
        # Output: spring.csv summer.csv
        ```
        

### Change Directory

- **Command**: `cd directory`
    
    - **Purpose**: Moves to the specified directory.
    - **Example**:
        
        ```bash
        cd seasonal
        # Moves to the seasonal directory
        ```
        
- **Special Navigation**:  
    Symbols**:
    
    - `..`: Refers to the parent directory.
        
        ```bash
        cd ..
        # Moves up one level
        ```
        
    - `.`: Refers to the current directory.
        
        ```bash
        ls .
        # Lists current directory contents
        ```
        
    - `~`: Refers to your home directory.
        
        ```bash
        ls ~
        # Lists contents of home directory
        ```
        

## File and Directory Paths

### Absolute vs. Relative Paths

- **Absolute Path**:
    - A complete path from the root directory (e.g., `/home/user/seasonal`).
    - Consistent regardless of current location.
- **Relative Path**:
    - A path relative to the current directory (e.g., `seasonal/spring.csv`).
    - Changes based on your current location.

## File Operations

### Copy Files

- **Command**: `cp file1 file2`
    - **Purpose**: Creates a copy of `file1` named `file2`. Overwrites `file2` if it exists.
    - **Example**:
        
        ```bash
        cp spring.csv spring_copy.csv
        # Creates a copy of spring.csv
        ```
        
- **Copy to Directory**:
    - Copies files to an existing directory.
    - **Example**:
        
        ```bash
        cp seasonal/spring.csv seasonal/summer.csv backup
        # Copies spring.csv and summer.csv to the backup directory
        ```
        

### Move Files

- **Command**: `mv file1 file2`
    - **Purpose**: Moves `file1` to `file2` or to a directory. Can overwrite existing files.
    - **Example**:
        
        ```bash
        mv autumn.csv winter.csv ..
        # Moves autumn.csv and winter.csv to the parent directory
        ```
        

### Rename Files

- **Command**: `mv file1 file2`
    - **Purpose**: Renames `file1` to `file2`.
    - **Example**:
        
        ```bash
        mv course.txt old-course.txt
        # Renames course.txt to old-course.txt
        ```
        

### Delete Files

- **Command**: `rm file1 file2`
    - **Purpose**: Permanently removes specified files.
    - **Example**:
        
        ```bash
        rm thesis.txt backup/thesis-2017-08.txt
        # Deletes thesis.txt and backup/thesis-2017-08.txt
        ```
        

## Directory Operations

### Create Directory

- **Command**: `mkdir directory_name`
    - **Purpose**: Creates a new directory.
    - **Example**:
        
        ```bash
        mkdir new_folder
        # Creates a directory named new_folder
        ```
        

### Delete Directory

- **Command**: `rmdir directory_name`
    - **Purpose**: Removes an empty directory.
    - **Example**:
        
        ```bash
        rmdir empty_folder
        # Deletes the empty_folder directory
        ```
        

## Key Takeaways

- **Navigation**: Use `pwd`, `ls`, and `cd` to explore and move through directories.
- **Paths**: Understand absolute vs. relative paths for precise file referencing.
- **File Management**: Copy (`cp`), move/rename (`mv`), and delete (`rm`) files efficiently.
- **Directory Management**: Create (`mkdir`) and remove (`rmdir`) directories as needed.
- **Caution**: Commands like `rm` are permanent; double-check before executing.