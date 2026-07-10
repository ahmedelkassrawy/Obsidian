
----
## 1. Interrupt Handling & Low-Level Input Architecture

- **Hardware Interrupts:** When a physical hardware device registers an input, it triggers a hardware interrupt. The **OS Kernel** immediately captures this low-level signal, traps the CPU's current execution, and packages the raw data into a standardized structure.
    
- **User-Space Routing & Context Switching:** The OS determines which process owns the target context for that data. It then routes the data packet into that specific application's message queue and triggers a context switch, passing execution control back from kernel space to user space.
    
- **Asynchronous Processing vs. Polling:** Rather than wasting CPU cycles by constantly checking the state of a device (polling), the application relies on asynchronous execution. It registers interest in specific event types, leaving its execution thread entirely **idle** to conserve system resources.
    
- **Thread Awakening:** The OS takes over the job of monitoring. It alters the state of the application's sleeping thread, actively waking it up and moving it back to the CPU scheduling queue only when matching data is pushed into its input queue.
    

## 2. Process Memory Management

- **Process Heap Allocation:** When long-lived data structures are initialized, the OS allocates dynamic memory within the application's **Heap Space**.
    
- **Stack vs. Heap Persistence:** Unlike stack memory (which automatically discards data when a specific function finishes executing), the heap allows data to persist across the entire lifecycle of the process, ensuring state data remains accessible across different asynchronous execution blocks.