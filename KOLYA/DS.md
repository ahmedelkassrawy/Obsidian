Drawback of Centralization -> Overlaod , dealy and inefficeiency
Biological systems -> Distribution and divide work
Plants demonstart a distributed sytem -> work is distributed
two common software resources in distributed system -> Apps and DB
distributed system -> divide complex task across multiple machines for parrallel processing
distibuted system -> collection of indepenedent computers that appear as a single system
computer or autonomous devices in distributed systems -> nodes
middleware -> software that sits between the os and application to enable the cordination of hetorgenity components to work and give actions
Enslow -> Distbuted Hardware and control and data
concurrency -> overlapping or prcoess and multiple actions simultaneously
distributed systems -> Lack of global clock , no single point of failure, concurrency
Openess -> Interopability , portabilty , standard interface protocol , extensibilty
Interopability -> allow diff system to exchange data and communicate without errors
portability -> allow apps to execute different harware platform types
Vertical scalabilty -> UP -> inc more power and rams and cpu
Horizontal Scalabilty -> OUT -> adding more computers and machines
fail tolerance -> sys continues even if nodes fail unexpectedly
hetorgnouity -> diff hardware components that work together
move somehting -> migration transparency
prevent two concurrent database queries -> concurrency transparency
used in heterogenity -> middleware

Lec 2
Flynn Taxonomy -> classify the computer arch based on data streams and instructions streams
SISD -> Van Neuman 
Speed limit -> CPU speed and bus speed
Bus -> communication between the memory and cpu 
SISD -> O(N) , sequential 
to overcome speed in SISD -> concurrency
concurrency in SISD -> multiprogramming,prallel functional unit , I/O concurrecny , pipeline
pipeline -> Fetch,decode,operand fetch,ALU execution, Write back
SIMD -> synchornizations -> global clock
SIMD have proccessign elements used by Control Unit (CU)
SIMD -> vector and matrix programming , graphical
parallel programming -> Thinking machines
Vector array -> IBM 9000
SIMD -> processor arrays and vector pipelines
SIMD -> GPUS
matrix addition A + B = C order on SIMD with 4 processors -> Takes 1 step only
SIMD handle conditional statements where only specific data elements ***must be operated on -> active and passive processors , encoding status mask bits to instrcutions

SIMD and MIMD mecahnisms for inter prcoess communtication -> shared memory and interconnection
MISD -> Pipeline
MISD -> buffers between the stages of the pipeline -> act as cache for the data temporary until next stage and avoid conflicts
MIMD -> Multi computers and multi processors
MIMD -> async
shared memory -> tightly coupled -> multi procossor -> example ENCORE
interconnection -> loosely coupled -> multi computer 
multicomputer is defined as -> distributed systems
tightly coupled -> latency low , data transfer high
loosely coupled -> latency high , data transfer low

tightly coupled is best for -> single centralized OS
loosley coupled communication done at-> I/O level

loosely coupled -> examples grid and hypercube multiprocessors
physically loosely coupled as logically tightly coupled -> use middleware
tightly coupled -> crossbar and omega switching

shared memory examples -> ENCORE,balance
interconnection - >Cluster , grid , cloud

tightly coupled are used to solve -> parrallel systems
loosely coupled -> distbiuted systems

Lec 3
parallel computing -> simulataneosuly to solve one problem
Parallel computing examples -> bits and instructions level
parallel computing execution -> its broken down into subtasks processed ndependently and combined at result
what stopped single prcoess clock frequency scaling and shift towardds multicore parallel -> power consumption and heat generation
Concurrent computing -> overlapping time periods 
Concurrent computing examples -> OS and DBMS
Parallel computing -> multi cores
concurrent systems DBMS and OS requirements are- >resource sharing
parallelism without concurrency -> bits level
concurrency without parralelism -> multi tasking (time sharing on a single cpu)
