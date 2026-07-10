**8) Which of the following components should be connected to the Microprocessor to be able to connect its output pin to more than 10 loads?**

a. Latch
b. Multiplexer
c. Buffer
d. Decoder

> **Correct Answer: c. Buffer**
> 
> _Explanation:_ Microprocessor output pins have a limited fan-out (current driving capability). A buffer is used to amplify this current, allowing the single output pin to drive a larger number of external loads without degrading the signal.

---

**9) Intel 8086 microprocessor, READY signal used**

a. To indicate to user that the microprocessor is working and is ready for use.

b. To slow down a fast peripheral device so as to communicate at the microprocessor's device.

c. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.

d. None of the above.

> **Correct Answer: c. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.**
> 
> _Explanation:_ The READY input pin allows slower memory or I/O devices to tell the CPU that they need more time to complete a data transfer. If READY is low, the CPU inserts WAIT states into the bus cycle until READY goes high again.

---

**10) In Intel 8086 microprocessor ALE signal is made high to**

a. To latch address from data\address bus.
b. To latch data D0-D7 from data\address bus.
c. To add WAIT state.
d. To achieve all the functions listed above.

> **Correct Answer: a. To latch address from data\address bus.**
> 
> _Explanation:_ ALE (Address Latch Enable) is pulsed high during the first clock cycle (T1) to signal that a valid address is currently on the multiplexed address/data bus (AD0-AD15). External latches use this signal to capture and hold the address before the bus switches to transferring data.

---

**11) In protected mode, the descriptor is ________ in length.**

a. 1 MB
b. 1 KB
c. 8 Byte
d. 8 MB

> **Correct Answer: c. 8 Byte**
> 
> _Explanation:_ In x86 protected mode, a segment descriptor (which contains the segment's base address, limit, and access rights) is exactly 8 bytes (64 bits) long.

---

**12) During the execution of an interrupt, which of the following registers are pushed into the stack**

1. IP
2. Flag Register
3. DS
4. CS
5. SP

a. 1 & 2
b. 1 & 2 & 3
c. 1 & 2 & 3 & 4
d. 1 & 2 & 4
e. 1 & 2 & 4 & 5

> **Correct Answer: d. 1 & 2 & 4**
> 
> _Explanation:_ When a hardware or software interrupt occurs in the 8086 architecture, the CPU must save its current state to return later. It automatically pushes the **Flag Register** first, then the **CS (Code Segment)** register, and finally the **IP (Instruction Pointer)** onto the stack before jumping to the Interrupt Service Routine (ISR).

---

**1. Which of the following instruction is not valid?**

a. `MOV AX, BX`

b. `MOV ES, 5000H`

c. `MOV AX, 5000H`

d. `PUSH AX`

> **Correct Answer: b. `MOV ES, 5000H`**
> 
> _Explanation:_ In the 8086 instruction set, you cannot move an immediate value directly into a segment register (like ES, DS, SS, or CS). You must first move the immediate value into a general-purpose register (e.g., `MOV AX, 5000H`) and then move it from that register to the segment register (e.g., `MOV ES, AX`). All other instructions listed are valid.

---

**2. The 1 MB byte of memory can be divided into segments of ___________**

a. 1 Kbyte

b. 64 Kbyte

c. 32 Kbyte

d. 34 Kbyte

> **Correct Answer: b. 64 Kbyte**
> 
> _Explanation:_ The Intel 8086 uses a 16-bit segment register to offset memory addresses. The maximum size that can be addressed by a 16-bit register is $2^{16}$ bytes, which equals 65,536 bytes, or 64 Kbytes.

---

**3. Which of the following instructions modifies the contents of the sign, zero, carry, auxiliary carry, parity, and overflow flags?**

a. `MOV`

b. `JMP`

c. `ADD`

d. `INS`

> **Correct Answer: c. `ADD`**
> 
> _Explanation:_ The `ADD` instruction performs arithmetic and updates all six standard status flags in the Flags Register based on the result of the operation. Data transfer instructions like `MOV` and control flow instructions like `JMP` do not affect these flags.

---

**4. Which of the following instructions is used to transfers a byte, word, or doubleword of data from an I/O device into the extra segment memory location?**

a. `INS`

b. `OUTS`

c. `STOS`

d. `LODS`

> **Correct Answer: a. `INS`**
> 
> _Explanation:_ `INS` (Input String) is specifically designed to read data from an I/O port (specified by the DX register) and store it directly into memory at the location pointed to by ES:DI (Extra Segment:Destination Index). `STOS` only stores data from the accumulator (AL/AX) to memory, not from an I/O device.

---

**5. How can we sum the following two 32-bit numbers using Intel 8086 Microprocessor? (9EF2 A13F) + (7B92 853E)**

a. Use single ADD instruction

b. Use two sequential ADD instructions

c. Use ADD instruction followed by ADC instruction

d. Use ADC instruction followed by ADD instruction

e. Use XADD instruction

> **Correct Answer: c. Use ADD instruction followed by ADC instruction**
> 
> _Explanation:_ Because the standard 8086 is a 16-bit microprocessor, it cannot add 32-bit numbers in a single operation. To sum them, you must first add the lower 16 bits together using the `ADD` instruction. If this generates a carry, the Carry Flag (CF) is set. Next, you add the upper 16 bits together using the `ADC` (Add with Carry) instruction, which automatically includes any carry generated from the lower 16-bit addition.

---

**6. The 8086 fetches instructions one after another from the ________ segment of memory.**

a. CS

b. ES

c. SS

d. IP

> **Correct Answer: a. CS**
> 
> _Explanation:_ The 8086 microprocessor divides memory into logical segments. The Code Segment (CS) is specifically designated to store the executable instructions of a program. The CPU fetches instructions from the memory locations pointed to by the CS register combined with the Instruction Pointer (IP) offset.

---

**7. What is the function of the instruction pointer (IP) in the 8086 microprocessor?**

a. It points to the data segment.

b. It is used for interrupt handling.

c. It stores the address of the next instruction to be executed.

d. It holds the stack pointer.

> **Correct Answer: c. It stores the address of the next instruction to be executed.**
> 
> _Explanation:_ The Instruction Pointer (IP) is a 16-bit register that contains the offset address of the _next_ instruction that the CPU needs to fetch from the Code Segment (CS) for execution.

---

**8. A 21-bit address bus can locate ________**

a. 1,048,576 locations

b. 2,097,152 locations

c. 4,194,304 locations

d. 8,388,608 locations

> **Correct Answer: b. 2,097,152 locations**
> 
> _Explanation:_ The total number of addressable memory locations is determined by the formula $2^n$, where $n$ is the number of bits in the address bus. For a 21-bit address bus, the calculation is $2^{21}$, which equals 2,097,152 distinct locations.

---

**9. Which of the following instructions does not change the destination register?**

a. ADD

b. SUB

c. CMP

d. XADD

> **Correct Answer: c. CMP**
> 
> _Explanation:_ The `CMP` (Compare) instruction effectively subtracts the source operand from the destination operand to update the status flags (like Zero, Sign, Carry, etc.), but it discards the result. The original value in the destination register remains unchanged. `ADD`, `SUB`, and `XADD` all modify their destination operands.

---

**10. Number of the times the instruction sequence below will loop before coming out of loop is**

Code snippet

```
      MOV CL, FFh
Again: INC CL
      JNZ Again
```

a. 0

b. 1

c. 2

d. 254

e. 255

> **Correct Answer: b. 1**
> 
> _Explanation:_ Let's trace the execution:
> 
> 1. `MOV CL, FFh`: The 8-bit `CL` register is loaded with the hexadecimal value `FF` (which is 255 in decimal, or the maximum unsigned 8-bit value).
>     
> 2. `INC CL`: The value in `CL` is incremented by 1. Because `CL` is an 8-bit register, adding 1 to `FFh` causes it to roll over to `00h`. Because the result of the operation is exactly zero, the Zero Flag (ZF) is set to 1.
>     
> 3. `JNZ Again`: This means "Jump if Not Zero". Since the previous `INC` instruction resulted in zero (ZF=1), the condition is false. The loop does not jump back to "Again"; it immediately falls through and exits. Therefore, the instructions inside the loop execute only 1 time.

---
Based on the file **image_8f4b7d.png**, here are the transcribed questions along with their independently verified correct answers and explanations:

**1. Intel 8086/8088 microprocessor is a ________ microprocessor.**

a. 4-bit

b. 8-bit

c. 16-bit

d. 32-bit

> **Correct Answer: c. 16-bit**
> 
> _Explanation:_ Both the 8086 and 8088 are internally 16-bit microprocessors, meaning their Arithmetic Logic Unit (ALU) and internal registers are 16 bits wide, even though the 8088 has an 8-bit external data bus.

---

**3. ___________ are the registers that are not addressable directly during application programming.**

a. Program visible registers.

b. Program invisible registers.

c. Segment registers.

d. None of the above.

> **Correct Answer: b. Program invisible registers.**
> 
> _Explanation:_ Program invisible registers (such as the hidden cache portions of segment registers in protected mode) manage system-level operations and memory mapping. They cannot be directly read or modified by a standard application programmer.

---

**4. If the clock of 8086/8088 is operated at 10 MHz, how long is one bus cycle?**

a. 800 ns

b. 1600 ns

c. 400 ns

d. 200 ns

> **Correct Answer: c. 400 ns**
> 
> _Explanation:_ The clock period (T-state) is the inverse of the frequency: $1 / 10 \text{ MHz} = 100 \text{ ns}$. A standard basic bus cycle in the 8086 architecture consists of four T-states (T1, T2, T3, T4). Therefore, one bus cycle is $4 \times 100 \text{ ns} = 400 \text{ ns}$.

---

**5. Which of the following instructions does not change the FLAG register?**

a. ADD

b. SUB

c. MOV

d. RCL

> **Correct Answer: c. MOV**
> 
> _Explanation:_ Data transfer instructions like `MOV` simply copy data from a source to a destination without performing arithmetic or logical operations, so they do not affect the status flags. `ADD`, `SUB`, and `RCL` all modify the flags based on their execution results.

---

**6. Number of the times the instruction sequence below will loop before coming out of loop is:**

Code snippet

```
      MOV CL, 01h
Again: INC CL
      JNZ Again
```

a. 0

b. 1

c. 255

d. 256

e. 254

> **Correct Answer: c. 255**
> 
> _Explanation:_ The `CL` register starts at `01h`. The loop increments `CL` and jumps back if the result is Not Zero (`JNZ`). It will increment through `02h`, `03h`, all the way to `FFh` (255 in decimal). On the 255th increment, `CL` goes from `FFh` to `00h` (rolling over its 8-bit capacity). This sets the Zero Flag to 1, causing the `JNZ` condition to fail and the loop to terminate. Thus, it loops 255 times.

---

**7. In 8086 microprocessor one of the following statements is not true.**

a. Coprocessor is interfaced in MAX mode.

b. Coprocessor is interfaced in MIN mode.

c. I/O can be interfaced in MAX/MIN mode.

d. Memory can be interfaced in MAX/MIN mode.

> **Correct Answer: b. Coprocessor is interfaced in MIN mode.**
> 
> _Explanation:_ This statement is false. To use a math coprocessor like the 8087, the 8086 must be operated in Maximum Mode (by grounding the MN/MX pin). This mode provides the necessary bus arbitration signals (RQ/GT) for the CPU and coprocessor to share the system bus.

---

**8. Which of the following components should be connected to the Microprocessor to be able to connect its output pin to more than 10 loads?**

a. Latch

b. Multiplexer

c. Buffer

d. Decoder

> **Correct Answer: c. Buffer**
> 
> _Explanation:_ A single microprocessor output pin has limited current driving capability (fan-out). If you need to connect it to many loads (typically more than 10 TTL loads), a buffer is used to amplify the current drive without altering the logical state of the signal.


**9. 8086 can access up to?**

a. 512 KB

b. 1 MB

c. 2 MB

d. 8 MB

> **Correct Answer: b. 1 MB**
> 
> _Explanation:_ The 8086 microprocessor has a 20-bit address bus. The maximum memory it can address is calculated as $2^{20}$ bytes, which equals 1,048,576 bytes, or exactly 1 MB.

---

**10. How can we sum the following two 32-bit numbers using Intel 8086 Microprocessor: (1BF7 235A) + (01F0 9E14)**

a. Use single ADD instruction

b. Use ADD instruction followed by ADC instruction

c. Use two sequential ADD instructions

d. Use ADC instruction followed by ADD instruction

e. Use XADD instruction

> **Correct Answer: b. Use ADD instruction followed by ADC instruction**
> 
> _Explanation:_ Since the 8086 is a 16-bit processor, it processes 32-bit addition in two steps. First, the lower 16 bits are added using the `ADD` instruction (which may generate a carry). Then, the upper 16 bits are added using the `ADC` (Add with Carry) instruction to ensure any carry from the first addition is included in the final result.

---

**11. In Intel 8086 microprocessor, READY signal used**

a. To indicate to user that the microprocessor is working and is ready for use.

b. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.

c. To slow down a fast peripheral device so as to communicate at the microprocessor's device.

d. None of the above.

> **Correct Answer: b. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.**
> 
> _Explanation:_ The READY input pin allows slower external memory or I/O devices to synchronize with the faster microprocessor. If the device isn't ready to transfer data, it pulls the READY signal low, forcing the CPU to insert WAIT states until it goes high again.

---

**12. The short and near Jumps are often called**

a. Intrasegment Jumps

b. Intersegment Jumps

c. Conditional Jumps

d. None of the above

> **Correct Answer: a. Intrasegment Jumps**
> 
> _Explanation:_ Short and near jumps only modify the Instruction Pointer (IP) and remain within the current 64 KB Code Segment (CS). Because they do not change the segment register, they are referred to as intrasegment (within the same segment) jumps. Far jumps modify both CS and IP and are called intersegment jumps.

---

**13. Consider the following statements: In 8086 microprocessor, data-bus and address bus are multiplexed in order to**

I) Increase the speed of microprocessor.

II) Reduce the number of pins.

III) Connect more peripheral chips.

**Which of these statements is/are correct?**

a. (I) only

b. (II) only

c. (II) & (III)

d. (I), (II) & (III)

> **Correct Answer: b. (II) only**
> 
> _Explanation:_ The 8086 multiplexes its lower 16 address lines with the 16 data lines (AD0-AD15). The primary engineering reason for this is to reduce the physical pin count on the IC package, allowing it to fit into a standard 40-pin DIP (Dual In-line Package). It does not increase speed; in fact, demultiplexing requires external latches.

---

**1) Which register is used with the Destination Index (DI) in string operations?**

a) ES

b) DS

c) SS

d) CS

> **Correct Answer: a) ES**
> 
> _Explanation:_ In 8086 string operations (like `MOVSB` or `STOSB`), the destination operand is always pointed to by the `DI` register, and it is strictly tied to the Extra Segment (`ES`). The physical address is calculated as `ES:DI`.

---

**2) What is the purpose of the Direction Flag (D) in the 8086?**

a) Controls the sign of arithmetic operations

b) Enables or disables interrupts

c) Determines the direction of string operations

d) Indicates carry in arithmetic operations

> **Correct Answer: c) Determines the direction of string operations**
> 
> _Explanation:_ The Direction Flag (DF) tells the processor whether to auto-increment or auto-decrement the index registers (`SI` and `DI`) during string instructions. If DF=0, it processes strings forward (increments); if DF=1, it processes strings backward (decrements).

---

**3) What is the effect of the LOOP instruction in the 8086?**

a) Increments CX and jumps to a label if CX $\neq$ 0

b) Decrements CX and jumps to a label if CX $\neq$ 0

c) Increments CX and jumps to a label if ZF = 1

d) Decrements CX and jumps to a label if ZF = 1

> **Correct Answer: b) Decrements CX and jumps to a label if CX $\neq$ 0**
> 
> _Explanation:_ The `LOOP` instruction is designed for iteration. It automatically subtracts 1 from the `CX` (Count) register. If the new value of `CX` is not zero, the instruction transfers control (jumps) to the specified target label.

---

**4) What is the purpose of the TEST instruction in the 8086?**

a) Performs a bitwise AND and sets flags without storing the result

b) Tests the carry flag and jumps if set

c) Compares two operands and stores the result

d) Performs a logical OR and sets flags

> **Correct Answer: a) Performs a bitwise AND and sets flags without storing the result**
> 
> _Explanation:_ The `TEST` instruction performs a logical bitwise AND operation between two operands to update the status flags (like Zero, Sign, and Parity). Unlike the standard `AND` instruction, it discards the computed result, leaving the destination operand unmodified.

---

**5) What is the size of the Instruction Pointer (IP) in the 8086?**

a) 8 bits

b) 16 bits

c) 20 bits

d) 32 bits

> **Correct Answer: b) 16 bits**
> 
> _Explanation:_ The 8086 is a 16-bit processor internally. The Instruction Pointer (IP) is a 16-bit register that holds the offset address of the next instruction to be fetched within the current 64 KB Code Segment (CS).

---

**6) How can we sum the following two 16-bit numbers using Intel 8086 Microprocessor: (2FB1) + (A23E)**

a) Use single ADD instruction

b) Use ADD instruction followed by ADC instruction

c) Use two sequential ADD instructions

d) Use ADC instruction followed by ADD instruction

e) Use XADD instruction

> **Correct Answer: a) Use single ADD instruction**
> 
> _Explanation:_ Because both numbers are 16-bit values and the 8086 possesses 16-bit general-purpose registers (like `AX`, `BX`) along with a 16-bit Arithmetic Logic Unit (ALU), it can add these two numbers entirely in a single `ADD` operation.

---

**7) Which addressing mode is used in "MOV AX, [1000H]"?**

a) Immediate addressing

b) Direct addressing

c) Register addressing

d) Indirect addressing

> **Correct Answer: b) Direct addressing**
> 
> _Explanation:_ Direct addressing occurs when the effective offset address of the memory operand is explicitly provided as a constant value enclosed in brackets. Here, `[1000H]` directly tells the processor to fetch data from offset 1000H in the Data Segment.

---

**8) What does the STI instruction do in the 8086?**

a) Clears the Carry Flag

b) Enables interrupts

c) Halts the processor

d) Resets the stack

> **Correct Answer: b) Enables interrupts**
> 
> _Explanation:_ `STI` stands for Set Interrupt Flag. It sets the Interrupt Flag (IF) in the flags register to 1, which allows the microprocessor to recognize and respond to external maskable hardware interrupts.

---

**9) If the clock of 8086/8088 is operated at 5 MHz, how long is one bus cycle if we added two more $T_w$?**

a) 800 ns

b) 1200 ns

c) 1600 ns

d) 200 ns

> **Correct Answer: b) 1200 ns**
> 
> _Explanation:_
> 
> 1. First, find the duration of one clock state (T-state). The period is $1 / \text{Frequency}$.
>     
>     $1 / 5 \text{ MHz} = 200 \text{ ns per T-state}$.
>     
> 2. A standard 8086 bus cycle requires 4 T-states ($T_1, T_2, T_3, T_4$).
>     
> 3. The problem states we are adding two wait states ($T_w$).
>     
> 4. Total T-states = $4 + 2 = 6 \text{ T-states}$.
>     
> 5. Total time = $6 \text{ T-states} \times 200 \text{ ns} = 1200 \text{ ns}$.


![[Pasted image 20260512224147.png]]

### Setup Data

To solve these real-mode memory addressing problems, we extract the initial register values provided in the table:

- **Segment Registers:**
    
    - `CS = 0100H`
        
    - `DS = 0200H`
        
    - `SS = 0300H`
        
    - `EX` (ES) = `0400H`
        
- **General/Index Registers (Lower 16 bits):**
    
    - `AX = 1010H`
        
    - `BX = 2040H`
        
    - `SI = 0020H`
        
    - `DI = 0030H`
        
    - `SP = 0010H`
        
- **Constants:**
    
    - `ARRAY = 2000H`
        

In real-mode addressing, the 20-bit Physical Address (PA) is calculated using the formula:

$\text{Physical Address} = (\text{Segment Register} \times 10\text{H}) + \text{Offset}$

---

**12) `MOV AX, ARRAY[DI]`**

a) 5000 H, 5001 H

b) 5030 H, 5031 H

c) 4030 H, 4031 H

d) 5030 H

> **Correct Answer: c) 4030 H, 4031 H**
> 
> _Explanation:_
> 
> 1. By default, `ARRAY[DI]` uses the Data Segment (`DS`) register.
>     
> 2. The Effective Address (Offset) is `ARRAY` + `DI`.
>     
>     $\text{Offset} = 2000\text{H} + 0030\text{H} = 2030\text{H}$.
>     
> 3. Calculate the Physical Address:
>     
>     $\text{PA} = (0200\text{H} \times 10\text{H}) + 2030\text{H} = 2000\text{H} + 2030\text{H} = 4030\text{H}$.
>     
> 4. Because the destination is `AX` (a 16-bit / 2-byte register), the operation accesses two consecutive memory byte locations: the starting address `4030H` and the next address `4031H`.
>     

---

**13) `PUSH AX`**

a) 2010 H

b) 1010 H

c) 3010 H

d) 3010 H, 3011 H

e) 300F H, 300E H

> **Correct Answer: e) 300F H, 300E H**
> 
> _Explanation:_
> 
> 1. The `PUSH` instruction inherently uses the Stack Segment (`SS`) and Stack Pointer (`SP`).
>     
> 2. When a 16-bit register (`AX`) is pushed, the `SP` is first decremented by 2.
>     
>     $\text{New SP} = 0010\text{H} - 2 = 000\text{EH}$.
>     
> 3. Calculate the Physical Address where the data is stored:
>     
>     $\text{PA} = (0300\text{H} \times 10\text{H}) + 000\text{EH} = 3000\text{H} + 000\text{EH} = 300\text{EH}$.
>     
> 4. The 8086 processor is little-endian. It stores the lower byte at the lower address (`300EH`) and the higher byte at the higher address (`300FH`). Therefore, the accessed addresses are `300FH` and `300EH`.
>     

---

**14) `MOV EAX, [BX + SI + 300H]`**

a) 4240 H, 4241 H

b) 4240 H, 4241 H, 4242 H, 4243 H

c) 4360 H, 4361 H, 4362 H, 4363 H

d) 4360 H, 4361 H

> **Correct Answer: c) 4360 H, 4361 H, 4362 H, 4363 H**
> 
> _Explanation:_
> 
> 1. Because `BX` is used as the base register, the default segment is the Data Segment (`DS`).
>     
> 2. Calculate the Effective Address (Offset):
>     
>     $\text{Offset} = \text{BX} + \text{SI} + 300\text{H} = 2040\text{H} + 0020\text{H} + 0300\text{H} = 2360\text{H}$.
>     
> 3. Calculate the Physical Address:
>     
>     $\text{PA} = (0200\text{H} \times 10\text{H}) + 2360\text{H} = 2000\text{H} + 2360\text{H} = 4360\text{H}$.
>     
> 4. Because the destination is `EAX` (a 32-bit / 4-byte extended register), the microprocessor must read four consecutive bytes of memory starting at the base physical address. These locations are `4360H`, `4361H`, `4362H`, and `4363H`.

![[Pasted image 20260512224310.png]]



### Setup Data

To solve these real-mode memory addressing problems, we extract the initial register values provided in the table. The 32-bit extended registers are displayed with their lower 16 bits split into high and low bytes.

- **Segment Registers:**
    
    - `CS = 0400H`
        
    - `DS = 0500H`
        
    - `SS = 0700H`
        
    - `ES = 0800H`
        
- **General/Index/Pointer Registers:**
    
    - `EAX = ---- 0500H` $\rightarrow$ `AX = 0500H`
        
    - `EBX = ---- 0600H` $\rightarrow$ `BX = 0600H`, `BH = 06H`, `BL = 00H`
        
    - `ESI = ---- 0050H` $\rightarrow$ `SI = 0050H`
        
    - `EDI = ---- 0030H` $\rightarrow$ `DI = 0030H`
        
    - `ESP = ---- 0080H` $\rightarrow$ `SP = 0080H`
        

In real-mode, the 20-bit Physical Address (PA) is calculated as:

$\text{Physical Address} = (\text{Segment Register} \times 10\text{H}) + \text{Offset}$

---

**6. MOV AL, [BX]**

a. 600H

b. 1100H and 1101H

c. 5600H and 5601H

d. 5600H

e. 1100H

> **Correct Answer: d. 5600H**
> 
> _Explanation:_
> 
> 1. The default segment register for `[BX]` is the Data Segment (`DS`).
>     
> 2. The Effective Address (Offset) is `BX = 0600H`.
>     
> 3. Calculate the Physical Address:
>     
>     $\text{PA} = (0500\text{H} \times 10\text{H}) + 0600\text{H} = 5000\text{H} + 0600\text{H} = 5600\text{H}$.
>     
> 4. Because the destination is `AL` (an 8-bit / 1-byte register), only a single memory location is accessed at `5600H`.
>     

---

**7. MOV AX, [BH+SI+0200H]**

a. 5250H

b. 5256H

c. 5256H and 5257H

d. 5250H and 5251H

e. 256H

> **Correct Answer: c. 5256H and 5257H**
> 
> _Explanation:_
> 
> 1. The default segment register is the Data Segment (`DS`).
>     
> 2. Calculate the Effective Address (Offset) using the given values (`BH = 06H`):
>     
>     $\text{Offset} = 06\text{H} + 0050\text{H} + 0200\text{H} = 0256\text{H}$.
>     
> 3. Calculate the Physical Address:
>     
>     $\text{PA} = (0500\text{H} \times 10\text{H}) + 0256\text{H} = 5000\text{H} + 0256\text{H} = 5256\text{H}$.
>     
> 4. Because the destination is `AX` (a 16-bit / 2-byte register), the instruction must access two consecutive memory bytes: `5256H` and `5257H`.
>     

---

**9. PUSHF**

a. 7079H and 7080H

b. 5079H and 5080H

c. 5049H and 5050H

d. 707EH and 707FH _(Note: Typographical smudging in the original print makes E/F resemble 8/9)_

e. 7080H

> **Correct Answer: d. 707EH and 707FH**
> 
> _Explanation:_
> 
> 1. `PUSHF` pushes the 16-bit Flags register onto the stack. Stack operations use the Stack Segment (`SS`) and Stack Pointer (`SP`).
>     
> 2. When a 16-bit value is pushed, the `SP` is first decremented by 2:
>     
>     $\text{New SP} = 0080\text{H} - 2 = 007\text{EH}$.
>     
> 3. Calculate the Physical Address where the data will be stored:
>     
>     $\text{PA} = (0700\text{H} \times 10\text{H}) + 007\text{EH} = 7000\text{H} + 007\text{EH} = 707\text{EH}$.
>     
> 4. Because it pushes a 16-bit (2-byte) value, it occupies the calculated address and the next sequential byte. Thus, the accessed memory locations are `707EH` and `707FH`.


![[Pasted image 20260512224519.png]]

### Setup Data

From the provided tables and notes, we can extract the following initial register values (in hexadecimal):

- **Segment Registers:**
    
    - `CS = 0100H`
        
    - `DS = 0200H`
        
    - `SS = 0300H`
        
    - `EX` (ES) = `0400H`
        
- **General/Index Registers (Lower 16 bits):**
    
    - `EAX = ---- 1010` $\rightarrow$ `AX = 1010H`
        
    - `EBX = ---- 2020` $\rightarrow$ `BX = 2020H`
        
    - `ESI = ---- 0020` $\rightarrow$ `SI = 0020H`
        
    - `EDI = ---- 0030` $\rightarrow$ `DI = 0030H`
        
- **Constants:**
    
    - `ARRAY = 3000H`
        
        _(Note: There is a handwritten note "Ip = 50", but it is not required to solve these specific instructions)._
        

In real-mode addressing, the 20-bit Physical Address (PA) is calculated as:

$\text{Physical Address} = (\text{Segment} \times 10\text{H}) + \text{Offset}$

---

### Questions & Answers

**I. MOV AX, ARRAY[DI]**

> **Answer: 5030H and 5031H**
> 
> _Explanation:_
> 
> 1. The default segment for standard array indexing with `DI` is the Data Segment (`DS`).
>     
> 2. The Effective Address (Offset) is calculated as: `ARRAY` + `DI` = $3000\text{H} + 0030\text{H} = 3030\text{H}$.
>     
> 3. Calculate the Physical Address: $\text{PA} = (0200\text{H} \times 10\text{H}) + 3030\text{H} = 2000\text{H} + 3030\text{H} = 5030\text{H}$.
>     
> 4. Since the destination is `AX` (a 16-bit/2-byte register), it reads from two consecutive bytes: `5030H` and `5031H`.
>     

**II. MOV AX, [BX]**

> **Answer: 4020H and 4021H**
> 
> _Explanation:_
> 
> 1. The default segment register when using `[BX]` as a base pointer is the Data Segment (`DS`).
>     
> 2. The Effective Address (Offset) is simply the value in `BX`: $2020\text{H}$.
>     
> 3. Calculate the Physical Address: $\text{PA} = (0200\text{H} \times 10\text{H}) + 2020\text{H} = 2000\text{H} + 2020\text{H} = 4020\text{H}$.
>     
> 4. Since the destination is `AX` (a 16-bit register), it reads from two consecutive bytes: `4020H` and `4021H`.
>     

**III. JMP AX**

> **Answer: Jumps to Instruction Pointer (IP) 1010H. The next instruction is fetched from physical address 2010H.**
> 
> _Explanation:_
> 
> 1. This is a register-indirect jump. It does not read data from memory into a register like a `MOV`; instead, it changes the flow of execution.
>     
> 2. It takes the value inside `AX` ($1010\text{H}$) and loads it directly into the Instruction Pointer (`IP`).
>     
> 3. The CPU will fetch its next instruction using the Code Segment (`CS`).
>     
> 4. The physical address for the next instruction fetch is: $\text{PA} = (0100\text{H} \times 10\text{H}) + 1010\text{H} = 1000\text{H} + 1010\text{H} = 2010\text{H}$.
>     

**IV. MOV EAX, [BX + SI + 200H]**

> **Answer: 4240H, 4241H, 4242H, and 4243H**
> 
> _Explanation:_
> 
> 1. The default segment register for base `[BX]` is the Data Segment (`DS`).
>     
> 2. The Effective Address (Offset) is calculated as: `BX` + `SI` + `200H` = $2020\text{H} + 0020\text{H} + 0200\text{H} = 2240\text{H}$.
>     
> 3. Calculate the Physical Address: $\text{PA} = (0200\text{H} \times 10\text{H}) + 2240\text{H} = 2000\text{H} + 2240\text{H} = 4240\text{H}$.
>     
> 4. Since the destination is `EAX` (a 32-bit/4-byte extended register), it must read four consecutive bytes of memory starting at the base address: `4240H`, `4241H`, `4242H`, and `4243H`.


![[Pasted image 20260512224603.png]]

### Question

**A. Consider the two registers EAX and EBX which contain initial values 14EA 7CA5H, and 051B 782DH respectively. Write the value of EBX register after executing each of the following operations separately: (5 Marks)**

I. `MOV BL, AL`

II. `MOV BH, AH`

III. `MOV BX, AX`

IV. `MOV EBX, EAX`

V. `ADD BX, AX`

---

### Setup & Register Breakdown

Before solving, let's break down the 32-bit registers into their 16-bit and 8-bit components based on the given initial values:

- **EAX = 14EA 7CA5H**
    
    - Upper 16 bits = `14EAH`
        
    - **AX** (Lower 16 bits) = `7CA5H`
        
    - **AH** (Upper 8 bits of AX) = `7CH`
        
    - **AL** (Lower 8 bits of AX) = `A5H`
        
- **EBX = 051B 782DH**
    
    - Upper 16 bits = `051BH`
        
    - **BX** (Lower 16 bits) = `782DH`
        
    - **BH** (Upper 8 bits of BX) = `78H`
        
    - **BL** (Lower 8 bits of BX) = `2DH`
        

_(Note: The prompt specifies that each operation is executed **separately**, meaning we must start with the original initial values for every step)._

### Answers

**I. MOV BL, AL**

- **Action:** Copies the value of `AL` (`A5H`) into `BL`. The rest of `EBX` remains unchanged.
    
- **Result:** **EBX = 051B 78A5H**
    

**II. MOV BH, AH**

- **Action:** Copies the value of `AH` (`7CH`) into `BH`. The rest of `EBX` remains unchanged.
    
- **Result:** **EBX = 051B 7C2DH**
    

**III. MOV BX, AX**

- **Action:** Copies the entire 16-bit value of `AX` (`7CA5H`) into `BX`. The upper 16 bits of `EBX` remain unchanged.
    
- **Result:** **EBX = 051B 7CA5H**
    

**IV. MOV EBX, EAX**

- **Action:** Copies the entire 32-bit value of `EAX` directly into `EBX`, overwriting it completely.
    
- **Result:** **EBX = 14EA 7CA5H**
    

**V. ADD BX, AX**

- **Action:** Adds the 16-bit value of `AX` (`7CA5H`) to the 16-bit value of `BX` (`782DH`) and stores the result in `BX`. The upper 16 bits of `EBX` are not affected by this 16-bit addition.
    
- **Math:** `782DH + 7CA5H = F4D2H`
    
- **Result:** **EBX = 051B F4D2H**
---

**1) Which of the following instructions is used to transfers a byte, word, or doubleword of data from an I/O device into the extra segment memory location?**

- **Answer:** **a. INS**
    
- _Explanation:_ The `INS` (Input String) instruction transfers data from the I/O port specified by the DX register into the memory location pointed to by ES:DI (Extra Segment : Destination Index).
    

**2) The 1 MB byte of memory can be divided into segment**

- **Answer:** **b. 64 Kbyte**
    
- _Explanation:_ In the 8086 architecture, memory is divided into logical segments, and each segment has a maximum size of 64 Kilobytes (64 KB).
    

**3) The 8086 fetches instructions one after another from the _____ segment of memory.**

- **Answer:** **a. CS**
    
- _Explanation:_ The Code Segment (CS) register points to the segment in memory where the executable instructions of a program are stored.
    

**4) _______ are the registers that can be addressed directly by a program.**

- **Answer:** **a. Program visible registers**
    
- _Explanation:_ Registers that a programmer can access and modify directly using instructions (like AX, BX, CS, etc.) are called program-visible registers.
    

**5) In Intel 8086 microprocessor ALE signal is made high to**

- **Answer:** _Note: The provided options in the image are poorly phrased, but it is conceptually tied to capturing the address from the multiplexed bus._ The true function of ALE (Address Latch Enable) is to latch the lower-order address (A0-A15) from the multiplexed address/data bus (AD0-AD15) during the first clock cycle.
    

**6) Intel 8086/8088 microprocessor address bus can locate**

- **Answer:** **c. 1,048,576 locations**
    
- _Explanation:_ The 8086 has a 20-bit address bus. $2^{20}$ equals 1,048,576 distinct memory locations (which is 1 Megabyte).
    

**7) In max mode, control bus signal So, S1 and S2 are sent out in ............. form.**

- **Answer:** **a. encoded**
    
- _Explanation:_ In Maximum Mode, the 8086 outputs status signals ($\overline{S_0}$, $\overline{S_1}$, $\overline{S_2}$) in an encoded form to an external bus controller (like the 8288), which decodes them to generate the actual memory and I/O control signals.
    

**8) In 8086 microprocessor one of the following statements is not true.**

- **Answer:** **c. Coprocessor is interfaced in MIN mode.**
    
- _Explanation:_ A coprocessor (like the 8087 math coprocessor) requires the 8086 to be in Maximum Mode to function properly, as it relies on the request/grant ($\overline{RQ}/\overline{GT}$) pins and external bus control that are only available in MAX mode. Therefore, statement "c" is false.
    

**9) Which of the following instructions modifies the contents of the sign, zero, carry, auxiliary carry, parity, and overflow flags?**

- **Answer:** **c. ADD**
    
- _Explanation:_ Arithmetic instructions like `ADD` evaluate the result of the operation and update all the status flags accordingly. (`MOV` and `JMP` do not affect flags).

Based on the file `image_8ec73c.png`, here are the transcribed questions along with their correct answers and explanations:

**10) Which of the following components should be connected to the Microprocessor to be able to connect its output pin to more than 10 loads?**

- **Answer:** **c. Buffer**
    
- _Explanation:_ A buffer is used to increase the driving capability (fan-out) of a microprocessor's output pin, allowing it to provide enough current to drive multiple loads reliably.
    

**11) If the clock of 8086/8088 is operated at 8 MHz, how long is one bus cycle?**

- **Answer:** **a. 500 ns**
    
- _Explanation:_ The clock period ($T$) is the inverse of the frequency ($f$):
    
    $T = \frac{1}{8 \text{ MHz}} = 0.125 \text{ \mu s} = 125 \text{ ns}$
    
    A standard 8086 bus cycle consists of 4 clock cycles ($T_1, T_2, T_3, T_4$). Therefore, one bus cycle takes $4 \times 125 \text{ ns} = 500 \text{ ns}$.
    

**12) Number of the times the instruction sequence below will loop before coming out of loop is:**

Code snippet

```
    MOV CL, 02h
Again: INC CL
    JNZ Again
```

- **Answer:** **e. 254**
    
- _Explanation:_ The `CL` register is an 8-bit register. It starts at `02h` and increments by 1 in each loop iteration. The `JNZ` (Jump if Not Zero) instruction keeps the loop going until `CL` overflows from `FFh` (255) to `00h`, which sets the Zero Flag. To get from 2 to 0 in an 8-bit space requires 254 increments ($256 - 2 = 254$).
    

**13) Which of the following instruction is not valid?**

- **Answer:** **c. MOV DS, 2000H**
    
- _Explanation:_ In the 8086 microprocessor architecture, you cannot move an immediate value (like `2000H`) directly into a segment register (like `DS`). You must first move the immediate value into a general-purpose register (e.g., `AX`), and then move the contents of that register into the segment register.
    

---

**Determine the address of the memory locations accessed by the following instructions (Questions 14, 15, 16, and 17), assume real-mode memory addressing.**

_(Reference Table Values from Image)_

- `EBX` contains `BX = 3040H`
    
- `EDI` contains `DI = 0030H`
    
- `ESP` contains `SP = 0010H`
    
- `DS = 0200H`
    
- `SS = 0300H`
    
- `ARRAY = 3000H`
    

**14) MOV AX, [BX]**

- **Answer:** **e. 5040 H, 5041 H**
    
- _Explanation:_ The default segment for `BX` is the Data Segment (`DS`).
    
    The Physical Address (PA) calculation is: $\text{PA} = (\text{DS} \times 10\text{H}) + \text{BX}$
    
    $\text{PA} = (0200\text{H} \times 10\text{H}) + 3040\text{H} = 02000\text{H} + 3040\text{H} = 5040\text{H}$.
    
    Because data is being moved into `AX` (a 16-bit register), the microprocessor must access a word (two bytes), meaning it accesses the memory locations at `5040H` and the subsequent byte at `5041H`.
    

**15) MOV AX, ARRAY[DI]**

- **Answer:** **b. 5030 H, 5031 H**
    
- _Explanation:_ The default segment for `DI` is `DS`.
    
    The Effective Address (EA) is $\text{ARRAY} + \text{DI} = 3000\text{H} + 0030\text{H} = 3030\text{H}$.
    
    The Physical Address (PA) is: $(\text{DS} \times 10\text{H}) + \text{EA}$
    
    $\text{PA} = 02000\text{H} + 3030\text{H} = 5030\text{H}$.
    
    Again, because `AX` is a 16-bit register, two consecutive bytes are accessed: `5030H` and `5031H`.
    

**16) PUSH AL**

- **Answer:** **c. 300F H**
    
- _Explanation:_ _Note: Pushing an 8-bit register like `AL` is technically an invalid instruction in standard x86 architecture (pushes must be 16-bit or 32-bit)._ However, assuming this is a theoretical question asking you to apply standard stack logic to an 8-bit value:
    
    The stack operates in the Stack Segment (`SS`). Pushing a value pre-decrements the Stack Pointer (`SP`).
    
    If `SP` is decremented by 1 byte for `AL`: $\text{SP}_{new} = 0010\text{H} - 1 = 000\text{FH}$.
    
    The Physical Address (PA) calculation is: $\text{PA} = (\text{SS} \times 10\text{H}) + \text{SP}_{new}$
    
    $\text{PA} = (0300\text{H} \times 10\text{H}) + 000\text{FH} = 03000\text{H} + 000\text{FH} = 300\text{FH}$.

**17) MOV EAX, [BX + SI + 300H]**

- **Answer:** **b. 53A0 H, 53A1 H, 53A2 H, 53A3 H**
    
- _Explanation:_ Using the register values from the previously provided table: `DS = 0200H`, `BX = 3040H`, and `SI = 0060H`.
    
    The Effective Address (EA) is calculated as: `BX + SI + 300H`
    
    $\text{EA} = 3040\text{H} + 0060\text{H} + 0300\text{H} = 33A0\text{H}$
    
    The Physical Address (PA) is calculated using the Data Segment (DS):
    
    $\text{PA} = (\text{DS} \times 10\text{H}) + \text{EA}$
    
    $\text{PA} = (0200\text{H} \times 10\text{H}) + 33A0\text{H} = 2000\text{H} + 33A0\text{H} = 53A0\text{H}$
    
    Because the destination register `EAX` is a 32-bit (4-byte) register, the microprocessor accesses four consecutive memory bytes starting at the physical address: `53A0H`, `53A1H`, `53A2H`, and `53A3H`.
    

**18) During ........., the processors issue the RD or WR signal.**

- **Answer:** **b. T2**
    
- _Explanation:_ In an 8086 basic bus cycle, the address is placed on the bus during the first clock cycle (T1). During the second clock cycle (T2), the bus direction is established, and the control signals for read ($\overline{RD}$) or write ($\overline{WR}$) are issued to memory or I/O.
    

**19) Intel 8086 microprocessor, READY signal used**

- **Answer:** **b. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.**
    
- _Explanation:_ The READY pin is an input to the processor. Slow memory or I/O devices use this signal to force the processor to insert WAIT states ($T_w$) between T3 and T4 of the bus cycle, giving the slow device more time to complete the data transfer.
    

**20) Which of the following is a special software interrupt designed to function as a breakpoint?**

- **Answer:** **b. INT 3**
    
- _Explanation:_ `INT 3` (which translates to the single-byte machine code `CC`) is a dedicated breakpoint instruction in the x86 architecture. Debuggers use it to temporarily replace an instruction in a program to halt execution and examine the processor's state.
---

**1) _________ are the registers that cannot be addressed directly by a program.**

- **Answer:** **b. Program invisible registers.**
    
- _Explanation:_ These are internal registers (like cache descriptors or internal temporary registers) used by the microprocessor hardware during execution but are not accessible to the programmer via standard instruction sets.
    

**2) Intel 8086/8088 microprocessor address bus can locate**

- **Answer:** **c. 1,048,576 locations**
    
- _Explanation:_ The 8086 has a 20-bit address bus. The number of addressable locations is $2^{20}$, which equals 1,048,576 bytes (1 Megabyte).
    

**3) Which of the following instructions is used to transfer a byte, word, or doubleword of data from data segment memory location to an I/O device?**

- **Answer:** **b. OUTS**
    
- _Explanation:_ The `OUTS` (Output String) instruction transfers data from a memory location pointed to by DS:SI to an I/O port specified in the DX register. (`INS` does the reverse).
    

**4) The 1 MB byte of memory can be divided into segment**

- **Answer:** **b. 64 Kbyte**
    
- _Explanation:_ In the 8086 architecture, the maximum size of any logical memory segment is 64 KB (65,536 bytes) because the segment offset registers are 16-bit.
    

**5) If the clock of 8086/8088 is operated at 10 MHz, how long is one bus cycle?**

- **Answer:** **c. 400 ns**
    
- _Explanation:_ The clock period ($T$) is the inverse of the frequency: $T = 1 / 10 \text{ MHz} = 100 \text{ ns}$. A standard 8086 bus cycle consists of 4 clock cycles ($T_1, T_2, T_3, T_4$). Therefore, $4 \times 100 \text{ ns} = 400 \text{ ns}$.
    

**6) In max mode, control bus signal So, S1 and S2 are sent out in ............. form.**

- **Answer:** **b. encoded**
    
- _Explanation:_ In Maximum Mode, the 8086 outputs status signals ($\overline{S_0}$, $\overline{S_1}$, $\overline{S_2}$) in an encoded format. These must be decoded by an external bus controller (like the 8288) to generate the actual memory and I/O read/write control signals.
    

**7) Access time is faster for .............**

- **Answer:** **b. SRAM**
    
- _Explanation:_ Static RAM (SRAM) is significantly faster than Dynamic RAM (DRAM) and non-volatile memory like ROM or EEPROM. It is typically used for CPU cache due to its speed.
    

**8) Which of the following is not an arithmetic instruction?**

- **Answer:** **d. ROL**
    
- _Explanation:_ `ROL` (Rotate Left) is a bitwise shift/logical instruction, not an arithmetic one. `INC` (Increment), `CMP` (Compare - which performs a subtraction), and `DEC` (Decrement) are arithmetic.
    

**9) Number of the times the instruction sequence below will loop before coming out of loop is:**

Code snippet

```
    MOV CL, 00h
Again: INC CL
    JNZ Again
```

- **Answer:** **d. 256**
    
- _Explanation:_ `CL` is an 8-bit register starting at `00h`. The `INC CL` instruction adds 1. The `JNZ` (Jump if Not Zero) jumps back as long as `CL` is not zero. `CL` will count up to `FFh` (255), and on the 256th increment, it will overflow back to `00h`, triggering the zero flag and exiting the loop.
    

---

**10) In 8086 microprocessor one of the following statements is not true.**

- **Answer:** **b. Coprocessor is interfaced in MIN mode.**
    
- _Explanation:_ The 8086 must be operated in Maximum (MAX) mode to interface with a coprocessor (like the 8087). MAX mode provides the necessary $\overline{RQ}/\overline{GT}$ (Request/Grant) bus control signals needed for the coprocessor to take control of the system bus.
    

**11) Which of the following components should be connected to the Microprocessor to be able to connect its output pin to more than 10 loads?**

- **Answer:** **c. Buffer**
    
- _Explanation:_ A buffer is used to increase the fan-out (current driving capability) of a signal, allowing one output pin to reliably drive multiple external loads without voltage degradation.
    

**12) How can we sum the following two 16-bit numbers using Intel 8086 Microprocessor: (2FB1) + (A23E)**

- **Answer:** **a. Use single ADD instruction**
    
- _Explanation:_ The 8086 is a 16-bit microprocessor with a 16-bit ALU. It can add two 16-bit numbers directly using a single `ADD` instruction (e.g., `ADD AX, BX`).
    

**13) Which of the following instruction is not valid?**

- **Answer:** **b. MOV ES, 5000H**
    
- _Explanation:_ The x86 instruction set does not allow moving an immediate numerical value directly into a segment register (like `ES`, `DS`, `CS`, `SS`). You must first move the value into a general-purpose register and then move it to the segment register.
    

---

**Determine the address of the memory locations accessed by the following instructions (Questions 14, 15, 16, and 17), assume real-mode memory addressing.**

_(Reference Table Values for 14-17)_

- `EAX`: 10 10 -> `AX` = 1010H
    
- `EBX`: 20 40 -> `BX` = 2040H
    
- `ESI`: 00 20 -> `SI` = 0020H
    
- `EDI`: 00 30 -> `DI` = 0030H
    
- `CS`: 0100H, `DS`: 0200H, `SS`: 0300H
    
- `ARRAY = 2000H`
    

**14) MOV AX, ARRAY[DI]**

- **Answer:** **c. 4030 H, 4031 H**
    
- _Explanation:_
    
    Effective Address (EA) = `ARRAY` + `DI` = `2000H` + `0030H` = `2030H`.
    
    The default segment is `DS`.
    
    Physical Address (PA) = (`DS` $\times$ 10H) + EA = `02000H` + `2030H` = `4030H`.
    
    Since `AX` is a 16-bit register, two consecutive bytes are accessed: `4030H` and `4031H`.
    

**15) MOV AX, [BX]**

- **Answer:** **c. 4040 H, 4041 H**
    
- _Explanation:_
    
    Effective Address (EA) = `BX` = `2040H`.
    
    The default segment is `DS`.
    
    Physical Address (PA) = (`DS` $\times$ 10H) + EA = `02000H` + `2040H` = `4040H`.
    
    Since `AX` is a 16-bit register, two consecutive bytes are accessed: `4040H` and `4041H`.
    

---

**16) JMP AX**

- **Answer:** **a. 2010 H**
    
- _Explanation:_ This is an indirect jump where the target offset is stored in `AX` (`1010H`). The jump changes the Instruction Pointer (IP) to this new offset within the current Code Segment (`CS`).
    
    Target Physical Address = (`CS` $\times$ 10H) + `AX` = (`0100H` $\times$ 10H) + `1010H` = `01000H` + `1010H` = `2010H`.
    

**17) MOV EAX, [BX + SI + 300H]**

- **Answer:** **c. 4360 H, 4361 H, 4362 H, 4363 H**
    
- _Explanation:_
    
    Effective Address (EA) = `BX` + `SI` + `300H` = `2040H` + `0020H` + `0300H` = `2360H`.
    
    The default segment is `DS`.
    
    Physical Address (PA) = (`DS` $\times$ 10H) + EA = `02000H` + `2360H` = `4360H`.
    
    Because `EAX` is a 32-bit register (4 bytes), it accesses four consecutive memory locations starting at `4360H`.
    

**18) During the execution of an interrupt, which of the following registers are pushed into the stack:**

`1) IP 2) Flag Register 3) DS 4) CS 5) SP`

- **Answer:** **d. 1 & 2 & 4**
    
- _Explanation:_ When an interrupt occurs, the CPU must save its current state to return later. It automatically pushes the Flags register, the Code Segment (`CS`), and the Instruction Pointer (`IP`) onto the stack.
    

**19) Intel 8086 microprocessor, READY signal used**

- **Answer:** **c. To provide proper WAIT states when the microprocessor is communicating with a slow peripheral device.**
    
- _Explanation:_ The `READY` pin allows slower memory or I/O devices to tell the CPU to pause and insert wait states into the bus cycle until the device is ready to complete the data transfer.
    

**20) Consider the following statements: In 8086 microprocessor, data-bus and address bus are multiplexed in order to**

`I) Increase the speed of microprocessor.`

`II) Reduce the number of pins.`

`III) Connect more peripheral chips.`

`Which of these statements is/are correct?`

- **Answer:** **b. (II) only**
    
- _Explanation:_ Multiplexing AD0-AD15 allows the same physical pins to serve as the address bus during the first clock cycle and the data bus during subsequent cycles. This design choice strictly reduces the physical pin count on the IC package (keeping it at 40 pins). It actually slightly _decreases_ speed compared to separate buses and does not natively connect more chips.

---
### **Question (1) Choose the correct answer**

**1. Which of the following instructions does not change the FLAG register?**

- **Answer:** **c. MOV**
    
- _Explanation:_ The `MOV` instruction is a data transfer instruction and does not affect the status flags. Arithmetic instructions like `ADD`, `SUB`, and `ADC` evaluate the result and update the flags accordingly.
    

**2. Which of the following instructions is used to transfers a byte, word, or doubleword of data from an I/O device to an extra segment memory location?**

- **Answer:** **a. INS**
    
- _Explanation:_ The `INS` (Input String) instruction reads data from the I/O port specified by the DX register into the memory location pointed to by ES:DI (Extra Segment : Destination Index).
    

**3. Which of the following instructions does not change the destination register?**

- **Answer:** **c. CMP**
    
- _Explanation:_ The `CMP` (Compare) instruction internally performs a subtraction between the destination and source operands to update the FLAG register, but it does not store the result, leaving the destination register unchanged.
    

**4. The first 1M byte of memory in a DOS-based computer system contains a(n) _________ and a _________ area.**

- **Answer:** **c. TPA, System**
    
- _Explanation:_ In DOS architecture, the 1MB of real-mode memory is divided into the Transient Program Area (TPA), which takes up the lower 640KB for user programs, and the System Area, which takes up the upper 384KB for BIOS and video memory.
    

**5. Which of the following instruction is not valid?**

- **Answer:** **d. MOV DS, 0FA0H** _(Note: Transcribed from OFAO in the document)_
    
- _Explanation:_ In x86 assembly, you cannot move an immediate constant value directly into a segment register (like DS). You must first load the value into a general-purpose register (like AX) and then move it from that register into the segment register.
    

**6. _________ are the registers that are not addressable directly during application programming.**

- **Answer:** **b. Program invisible registers**
    
- _Explanation:_ Program invisible registers (such as cache descriptors or certain control registers) are used by the microprocessor hardware during execution but cannot be directly manipulated by the programmer using standard instructions.
    

**7. A 22-bit address bus can locate**

- **Answer:** **c. 4,194,304 locations**
    
- _Explanation:_ The number of addressable locations is $2^n$ where $n$ is the bus width. 2 to the power of 22 is 4,194,304 locations (or 4 Megabytes).
    

**8. The 8086 microprocessor is based on which architecture?**

- **Answer:** **b. CISC**
    
- _Explanation:_ The Intel 8086 is a classic example of a Complex Instruction Set Computer (CISC) architecture, which features a wide variety of instructions with varying lengths and execution times.
    

**9. The base address of the local descriptor table is stored in**

- **Answer:** **b. LDTR (Local Descriptor Table Register)**
    
- _Explanation:_ In protected mode, the LDTR holds the segment selector and base address for the Local Descriptor Table.
    

**10. The 8086 fetches instructions one after another from _________ of memory.**

- **Answer:** **a. CS**
    
- _Explanation:_ The Code Segment (CS) register points to the segment in memory where the program's executable instructions are stored.
    

---

### **Determine the address of the memory locations accessed by the following instructions (Question 11, 12, 13, 14 and 15):**

**Reference Values:**

- **EAX:** 01 00 $\rightarrow$ `AX` = 0100H
    
- **EBX:** 02 00 $\rightarrow$ `BX` = 0200H
    
- **ESI:** 00 10 $\rightarrow$ `SI` = 0010H
    
- **EDI:** 00 20 $\rightarrow$ `DI` = 0020H
    
- **ESP:** 00 30 $\rightarrow$ `SP` = 0030H
    
- **CS:** 0300H | **DS:** 0400H | **SS:** 0500H | **ES:** 0600H
    

**11. MOV AX, [SI + 0100H]** _(Note: Corrected from presumed OCR typo 'BL+SI')_

- **Answer:** **d. 4110H and 4111H**
    
- _Explanation:_ The Effective Address (EA) is `SI` + 0100H = 0010H + 0100H = 0110H. The default segment is DS. The Physical Address (PA) = (DS $\times$ 10H) + EA = 04000H + 0110H = 4110H. Since AX is a 16-bit register, it accesses two bytes at 4110H and 4111H.
    

**12. MOV AL, [BX]**

- **Answer:** **a. 4200H**
    
- _Explanation:_ EA = `BX` = 0200H. Default segment is DS. PA = (DS $\times$ 10H) + EA = 04000H + 0200H = 4200H. Since AL is an 8-bit register, it only accesses a single byte at 4200H.
    

**13. STOS (Assume D = 0)**

- **Answer:** **b. 6020H and 6021H**
    
- _Explanation:_ `STOS` (Store String) uses the Extra Segment (ES) and Destination Index (DI). PA = (ES $\times$ 10H) + DI = 06000H + 0020H = 6020H. Based on the options provided, the operation assumes a 16-bit word (`STOSW`), so it accesses 6020H and 6021H.
    

**14. PUSH BX**

- **Answer:** **d. 502FH and 502EH**
    
- _Explanation:_ Pushing a value onto the stack decrements the Stack Pointer (`SP`) by 2 before writing. New `SP` = 0030H - 2 = 002EH. The Physical Address = (SS $\times$ 10H) + `SP` = 05000H + 002EH = 502EH. Because it's a 16-bit push, it writes to the addresses 502EH and 502FH. (Note: x86 is little-endian, so it's common to see it written as 502FH and 502EH depending on byte-order convention).
    

**15. JMP AX**

- **Answer:** **a. 3100 H**
    
- _Explanation:_ This is an indirect jump that replaces the Instruction Pointer (`IP`) with the value in `AX` (0100H). The CPU calculates the next physical address using the Code Segment (CS). PA = (CS $\times$ 10H) + AX = 03000H + 0100H = 3100H.

Based on the provided exam document, here are the transcribed questions along with their correct answers and explanations:

### **Question (1)**

1. Intel 8086 microprocessor is a 

* **Answer:** c. 16-bit 

* *Explanation:* The Intel 8086 is a 16-bit microprocessor because its internal registers, internal data bus, and ALU are all 16-bit wide, allowing it to process 16 bits of data at a time.

2. Which bus is bidirectional? 

* **Answer:** c. Data bus 

* *Explanation:* The data bus is bidirectional because the microprocessor needs to both read data from memory/peripherals and write data to them. The address bus is unidirectional (CPU to memory), and the control bus consists of individual unidirectional lines.

3. The first 1M byte of memory in a DOS-based computer system contains a(n) _________ and a(n) _________ area. 

* **Answer:** d. TPA, System 

* *Explanation:* The 1MB of real-mode memory in DOS systems is logically partitioned into the Transient Program Area (TPA) for user applications (lower 640KB) and the System Area for BIOS and video memory (upper 384KB).

4. The _________ contains an offset instead of actual address. 

* **Answer:** a. IP 

* *Explanation:* The Instruction Pointer (IP) holds the 16-bit offset address of the next instruction to be executed within the current Code Segment (CS). It does not hold the physical (actual) address.

5. The instruction that is used to transfer the data from source operand to destination operand is 

* **Answer:** **d. data copy/transfer instruction** 

* *Explanation:* Instructions like `MOV`, `PUSH`, `POP`, and `XCHG` belong to the data transfer instruction category, designed to move data between registers, memory, and I/O without modifying the data itself.

---

**Determine the address of the memory locations accessed by the following instructions (Question 6, 7, 8, and 9):** 

**Reference Values:** 

* **EAX:** 05 00 $\rightarrow$ `AX` = 0500H
* **EBX:** 06 00 $\rightarrow$ `BX` = 0600H (Therefore, `BH` = 06H, `BL` = 00H)
* **ESI:** 00 50 $\rightarrow$ `SI` = 0050H
* **EDI:** 00 30 $\rightarrow$ `DI` = 0030H
* **ESP:** 00 80 $\rightarrow$ `SP` = 0080H
* **CS:** 0400H | **DS:** 0500H | **SS:** 0700H | **ES:** 0800H

6. MOV AL, [BX] 

* **Answer:** d. 5600H 

* *Explanation:* The Effective Address (EA) is `BX` = 0600H. The default segment is the Data Segment (`DS` = 0500H). The Physical Address (PA) = (`DS` $\times$ 10H) + EA = 05000H + 0600H = 5600H. Because the destination register `AL` is 8-bit, only a single byte at 5600H is accessed.

7. MOV AX, [BH+SI+0200H] *(Note: Interpreting based on the transcribed text, though using BH as a base is technically invalid in standard x86 real-mode assembly. Calculating based on the provided values regardless)* 

* **Answer:** c. 5256H and 5257H 

* *Explanation:* Using the register values: `BH` = 06H, `SI` = 0050H.
EA = 06H + 0050H + 0200H = 0256H.
The default segment is `DS` (0500H). PA = (`DS` $\times$ 10H) + EA = 05000H + 0256H = 5256H.
Because `AX` is a 16-bit register, it accesses two consecutive bytes: 5256H and 5257H.

8. STOSW (Assume D=0) 

* **Answer:** d. 8030H and 8031H 

* *Explanation:* The `STOSW` (Store String Word) instruction always uses the Extra Segment (`ES`) and the Destination Index (`DI`).
PA = (`ES` $\times$ 10H) + `DI` = 08000H + 0030H = 8030H.
Since it's a word operation ("W"), it writes 2 bytes to memory at addresses 8030H and 8031H.

9. PUSHF 

* **Answer:** **707EH and 707FH** *(Note: The options provided in the document appear to have typographical errors, likely meaning 707EH/F instead of 7078/9)*

* *Explanation:* `PUSHF` pushes the 16-bit Flag register onto the stack. The CPU pre-decrements the Stack Pointer (`SP`) by 2.
New `SP` = 0080H - 2 = 007EH.
The stack operates in the Stack Segment (`SS` = 0700H). PA = (`SS` $\times$ 10H) + New `SP` = 07000H + 007EH = 707EH.
As a 16-bit push, it writes to 707EH and 707FH.

---

10. Number of the times the instruction sequence below will loop before coming out of loop is: 

```assembly
    MOV AL, 00h
Again: INC AL
    JNZ Again

```

* **Answer:** b. 256 

* *Explanation:* `AL` is an 8-bit register starting at `00h`. The loop increments `AL` by 1 each iteration. The `JNZ` (Jump if Not Zero) instruction will keep looping until `AL` equals `00h` again. `AL` will count from 0 up to 255 (`FFh`), and on the 256th increment, it will overflow back to `00h`, setting the zero flag and exiting the loop.

11. What will be the contents of register AL after the following has been executed 

```assembly
    MOV BL, 8B
    MOV AL, 9F
    ADD AL, BL

```

* **Answer:** b. 2A and carry flag is set 

* *Explanation:* You are adding 9FH (159 in decimal) and 8BH (139 in decimal).
`9FH + 8BH = 12AH`.
Because `AL` is an 8-bit register, it can only hold the lower two hex digits (`2A`). The overflow beyond 8 bits (the `1`) is caught by setting the Carry Flag (CF = 1).

12. The base address of the local descriptor table is stored in 

* **Answer:** b. LDTR (Local Descriptor Table Register) 

* *Explanation:* In x86 protected mode, the LDTR contains the selector and base address pointing to the Local Descriptor Table in memory.

13. How can we sum the following two 32-bit numbers using Intel 8086 Microprocessor: (0BF0 23A2) + (01B0 0216) 

* **Answer:** e. Use ADD instruction followed by ADC instruction 

* *Explanation:* Because the 8086 is a 16-bit processor, it cannot add 32 bits at once. You must first add the lower 16 bits (`23A2` + `0216`) using the `ADD` instruction. Then, you add the upper 16 bits (`0BF0` + `01B0`) using the `ADC` (Add with Carry) instruction, which automatically includes any carry-over generated from the first addition.

14. JMP EAX is considered 

* **Answer:** c. Near Jump 

* *Explanation:* `JMP EAX` is an indirect jump where the target offset is stored in a register. Because it only changes the instruction pointer (offset) and does not change the Code Segment (CS), it is classified as a Near Jump.

15. During the execution of an interrupt, which of the following registers are pushed into the stack: `1) IP   2) CS   3) DS   4) Flag Register   5) SP` 

* **Answer:** b. 1 & 2 & 4 

* *Explanation:* When a hardware or software interrupt occurs, the microprocessor must save its current execution state. It automatically pushes the Flags register, the Code Segment (`CS`), and the Instruction Pointer (`IP`) onto the stack before jumping to the interrupt service routine.
---
### **Question (1) Choose the correct answer**

**1. The first 1M byte of memory in a DOS-based computer system contains a(n) _________ and a(n) _________ area.**

- **Answer:** **d. TPA, System**
    
- _Explanation:_ The 1MB of real-mode memory in DOS systems is partitioned into the Transient Program Area (TPA) for user programs (the lower 640KB) and the System Area for BIOS and video memory (the upper 384KB).
    

**2. Intel 8086/8088 microprocessor is a _________ microprocessor.**

- **Answer:** **c. 16-bit**
    
- _Explanation:_ Both the 8086 and 8088 are considered 16-bit microprocessors because their internal architecture, including registers and the Arithmetic Logic Unit (ALU), operates on 16 bits of data at a time. (The 8088 simply has an 8-bit external data bus).
    

**3. 8086/8088 can access up to?**

- **Answer:** **b. 1 MB**
    
- _Explanation:_ The 8086 has a 20-bit address bus. The total number of addressable memory locations is $2^{20}$, which equals 1,048,576 bytes, or 1 Megabyte (1 MB).
    

**4. How can we sum the following two 32-bit numbers using Intel 8086 Microprocessor? (3EF2 A132) + (7B92 453E)**

- **Answer:** **c. Use ADD instruction followed by ADC instruction**
    
- _Explanation:_ Because the 8086 is a 16-bit processor, it processes 32-bit additions in two steps. First, the lower 16 bits are added using the `ADD` instruction. Then, the upper 16 bits are added using the `ADC` (Add with Carry) instruction, which accounts for any carry generated by the first step.
    

**5. Which of the following instructions is used to transfers a byte, word, or doubleword of data from a data segment memory location to an I/O device?**

- **Answer:** **b. OUTS**
    
- _Explanation:_ The `OUTS` (Output String) instruction specifically transfers data from a memory location (pointed to by DS:SI) to an I/O port (specified in the DX register).
    

**6. _________ are the registers that are addressable directly during application programming.**

- **Answer:** **a. Program visible registers.**
    
- _Explanation:_ Registers that a programmer can access and modify directly (like AX, BX, CX, DX) are known as program-visible registers.
    

**7. Which of the following instructions does not change the destination register?**

- **Answer:** **c. CMP**
    
- _Explanation:_ The `CMP` (Compare) instruction performs a subtraction internally to evaluate the relationship between two operands and updates the flags accordingly. However, it discards the result and leaves the destination register unchanged.
    

**8. Which of the following instructions is not valid?**

- **Answer:** **b. MOV DS, 0FA5H** _(Note: Transcribed from OFA5H based on context)_
    
- _Explanation:_ In the x86 instruction set, you cannot move an immediate hex value directly into a segment register (like DS). You must first load the value into a general-purpose register (e.g., AX) and then move it into the segment register.
    

**9. During the execution of an interrupt, which of the following registers are pushed into the stack:**

`1) IP 2) CS 3) Flag Register 4) DS 5) SP`

- **Answer:** **b. 1 & 2 & 3**
    
- _Explanation:_ When an interrupt is serviced, the CPU automatically saves its current state to resume later. It pushes the Flag Register, the Code Segment (`CS`), and the Instruction Pointer (`IP`) onto the stack.
    

**10. Number of the times the instruction sequence below will loop before coming out of loop is:**

Code snippet

```
    MOV CL, 00h
Again: INC CL
    JNZ Again
```

- **Answer:** **d. 256**
    
- _Explanation:_ The `CL` register is 8 bits wide and starts at `00h`. The `INC` instruction adds 1 each iteration, and `JNZ` loops back as long as the zero flag is not set. `CL` will count up to 255 (`FFh`), and on the 256th increment, it will roll over to `00h`, setting the zero flag and exiting the loop.
    

**11. The FAR jumps are often called**

- **Answer:** **b. Intersegment Jumps**
    
- _Explanation:_ A FAR jump changes both the Instruction Pointer (IP) and the Code Segment (CS), meaning it jumps to a different, independent segment of memory (intersegment).
    

---

**Determine the address of the memory locations accessed by the following instructions (Question 12, 13, 14, and 15):**

**Reference Values:**

- **EAX:** 01 00 $\rightarrow$ `AX` = 0100H
    
- **EBX:** 02 00 $\rightarrow$ `BX` = 0200H (and `BH` = 02H)
    
- **ESI:** 00 40 $\rightarrow$ `SI` = 0040H
    
- **EDI:** 00 20 $\rightarrow$ `DI` = 0020H
    
- **ESP:** 00 10 $\rightarrow$ `SP` = 0010H
    
- **CS:** 0300H | **DS:** 0400H | **SS:** 0500H | **ES:** 0600H
    

**12. MOV AL, [BX]**

- **Answer:** **d. 4200H**
    
- _Explanation:_ Effective Address (EA) = `BX` = 0200H.
    
    Default segment is Data Segment (`DS` = 0400H).
    
    Physical Address (PA) = (`DS` $\times$ 10H) + EA = 04000H + 0200H = 4200H.
    
    Because `AL` is an 8-bit register, only a single byte at 4200H is accessed.
    

**13. MOV AX, [BH+SI+0100H]**

- **Answer:** **d. 4142H and 4143H**
    
- _Explanation:_ EA = `BH` + `SI` + 0100H = 02H + 0040H + 0100H = 0142H.
    
    Default segment is `DS` (0400H).
    
    PA = (`DS` $\times$ 10H) + EA = 04000H + 0142H = 4142H.
    
    Because `AX` is a 16-bit register, it accesses two consecutive bytes at 4142H and 4143H.
    

**14. STOSW (Assume D=0)**

- **Answer:** **d. 6020H and 6021H**
    
- _Explanation:_ `STOSW` uses the Extra Segment (`ES` = 0600H) and Destination Index (`DI` = 0020H).
    
    PA = (`ES` $\times$ 10H) + `DI` = 06000H + 0020H = 6020H.
    
    Because it's a word operation, it accesses two bytes at 6020H and 6021H.
    

**15. PUSHF**

- **Answer:** _(Note: Based on standard 8086 architecture, the exact addresses should be 500EH and 500FH. None of the listed options in the document correctly reflect this standard calculation. The closest intended option might have been mistyped in the original exam)._
    
- _Explanation:_ `PUSHF` pushes the 16-bit Flag register. It pre-decrements the Stack Pointer (`SP` = 0010H) by 2.
    
    New `SP` = 0010H - 2 = 000EH.
    
    The Stack Segment is `SS` (0500H).
    
    PA = (`SS` $\times$ 10H) + New `SP` = 05000H + 000EH = 500EH.
    
    It writes to addresses 500EH and 500FH.