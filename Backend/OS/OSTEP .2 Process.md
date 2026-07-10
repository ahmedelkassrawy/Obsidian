- **CPU Virtualization**  
    ➔ The OS creates the illusion of many CPUs by rapidly switching between processes.
    
- **Time Sharing**  
    ➔ The technique where the CPU runs one process for a while, then switches to another, creating concurrency.
    
- **Illusion of Concurrent Processes**  
    ➔ Even with one or few physical CPUs, many processes can seem to run "at the same time."
    
- **Performance Tradeoff**  
    ➔ Sharing the CPU among many processes can make each individual process slower.
    
- **Mechanisms vs. Policies** (terms introduced indirectly)  
    ➔ **Mechanisms**: Low-level methods or protocols (e.g., _context switching_ to switch between processes).
    
- **Context Switching**  
    ➔ A mechanism where the OS saves the state of one process and loads the state of another to switch CPU execution.