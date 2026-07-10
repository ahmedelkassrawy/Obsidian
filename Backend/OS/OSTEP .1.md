## Overview

- The **Operating System (OS)** is software responsible for making it easy to run programs.
- Ensures the system operates **correctly** and **efficiently** in an **easy-to-use** manner.

## Key Concept: Virtualization

- The primary technique used by the OS is **Virtualization**.
- The OS takes a **physical resource** (e.g., processor, memory, disk) and transforms it into a more **general, powerful, and easy-to-use virtual form**.
- The OS is sometimes referred to as a **virtual machine**.

## System Calls and APIs

- To allow users to interact with the virtual machine (e.g., run programs, allocate memory, access files), the OS provides **Application Programming Interfaces (APIs)** or **system calls**.
- The OS exports **hundreds of system calls** for tasks like:
    - Running programs
    - Accessing memory and devices
    - Other related actions
- These system calls are often referred to as the OS’s **standard library** for applications.

## Resource Management

- The OS is a **resource manager** because it manages system resources like:
    - **CPU**
    - **Memory**
    - **Disk**
- **Virtualization** enables:
    - Multiple programs to run concurrently
    - Programs to access their own instructions and data (sharing memory)
    - Programs to access devices (sharing disks)

## Virtualizing the CPU

- Even with a single processor, the OS and hardware create the **illusion** of multiple **virtual CPUs**.
- This allows many programs to appear to run **simultaneously**.
- The OS achieves this by **virtualizing the CPU**, effectively turning a single CPU into an **infinite number of CPUs**.

## Memory Virtualization

- **Memory** is an array of bytes:
    - Reading memory requires specifying an **address** to access stored data.
    - Writing/updating memory requires specifying the data and address.
    - Memory is accessed on **each instruction fetch**.
- Each running program has a unique **Process Identifier (PID)**.
- Multiple instances of a program can run concurrently, each accessing memory at the **same virtual address** (e.g., 0x200000), yet updating values **independently**.
- This is because the OS **virtualizes memory**:
    - Each process has its own **private virtual address space**.
    - The OS maps these virtual addresses to the **physical memory** of the machine.
- **Physical memory** is a **shared resource** managed by the OS.

## Concurrency

- **Concurrency** refers to problems that arise when working on multiple tasks simultaneously within a program.
- Concurrency issues first emerged within the **OS itself**, as it juggles multiple processes (e.g., running one process, then another).
- These issues also appear in **modern multithreaded programs**.
- A **thread** is a function running within the **same memory space** as other functions, with multiple threads active simultaneously.

### Concurrency Example

- A program with **two threads** runs a `worker()` routine, where each thread increments a **shared counter** in a loop.
- When the loop count (`loops`) is small (e.g., 1000):
    - Each thread increments the counter 1000 times.
    - Final counter value is **2000** (2 × 1000), as expected.
- When `loops` is large (e.g., 100,000):
    - The final counter value is **inconsistent** (e.g., 143,012 or 137,298 instead of 200,000).
    - Repeated runs produce **varying results**, sometimes even the correct value.
- This **unpredictable behavior** indicates a **concurrency problem**.

### Cause of Concurrency Issue
- Incrementing the shared counter involves **three non-atomic instructions**:
    1. Load the counter’s value from memory.
    2. Increment the value.
    3. Store the new value back to memory.
- These instructions are **not executed as a single, uninterrupted operation**.
- **Concurrent access** by multiple threads can lead to **unpredictable results**, highlighting the concurrency issue.

### Persistence
In system memory, data can be easily lost, as devices such as **DRAM store values in a volatile manner**; when power goes away or the system crashes, **any data in memory is lost.** Thus, we need hardware and software to be able to store data persistently;

The software in the operating system that usually manages the disk is called **the file system** -> responsible for **storing any files the user creates** in a reliable and efficient manner on the disks of the system.
Thus, you can see how files are shared across different processes.

The code example (Figure 2.6) shows how to create a file (`/tmp/file`) containing "hello world" by making three system calls: `open()` to create and open the file, `write()` to write data to it, and `close()` to finish. 
These calls interact with the OS’s file system, which manages the operations and returns error codes if needed. Behind the scenes, the file system must determine where to store the new data and update its structures, requiring complex I/O operations to the storage device. Working directly with devices is intricate, but the **OS simplifies it by offering standard system calls, acting like a standard library for device access.**

### Design Goals
An **OS virtualizes physical resources** (CPU, memory, disk), manages concurrency challenges, and ensures long-term file storage. To design and build an OS, it's crucial to define goals and carefully make trade-offs. One key goal is creating **abstractions** to simplify system use and development. Abstraction is fundamental in computer science, allowing complex systems to be broken into manageable layers, from transistors up to high-level programming. The text emphasizes that understanding OS abstractions is essential and will be discussed throughout.

- One major goal of OS design is to **provide high performance** by **minimizing overheads** (extra time and space usage).
    
- **Virtualization** and **ease of use** are important but must be balanced against performance.
    
- The OS must provide **protection and isolation** between applications and between applications and the OS itself.
    
- **Isolation** ensures that one program's mistakes or malicious behavior don’t harm others or the system.
    
- An OS must be **highly reliable**, because if it crashes, all applications running on it crash too.
    
- Building a **reliable OS** is challenging due to its complexity (often millions of lines of code).
    
- Other important goals include:
    - **Energy efficiency** (important for green computing).
    - **Security** (protecting against malicious apps, especially in networked environments).
    - **Mobility** (adapting OSes for smaller and portable devices).

- The **core principles** of building an OS apply across different kinds of devices, though specific implementations may vary.

