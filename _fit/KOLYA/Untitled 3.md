## Question (1): Multiple Choice Questions

**1) Reactive architecture agents are characterized by:**
- **Answer:** Acting directly on sensor input with minimal internal state.
    

**2) A major limitation of reactive architectures is:**
- **Answer:** Lack of long-term planning and reasoning.
    

**3) Deliberative architecture agents rely on:**
- **Answer:** Planning and symbolic reasoning with explicit world models.
    

**4) Which of the following best describes a hybrid (reactive + deliberative) approach?**
- **Answer:** Combining fast reflexes with higher-level planning.
    

**5) Blackboard architecture is inspired by:**
- **Answer:** Centralized shared memory where agents post and read information.
    

**6) In blackboard systems, the "blackboard" acts as:**
- **Answer:** A shared knowledge repository accessible by multiple agents.
    

**7) Cooperation among agents means:**
- **Answer:** Agents work together to achieve a shared objective.

**8) Competition among agents typically involves:**
- **Answer:** Agents trying to outperform each other.

**9) Negotiation in multi-agent systems involves:**
- **Answer:** Agents bargaining to resolve conflicts between goals.

**10) In the Contract Net Protocol (CNP):**
- **Answer:** A manager announces a task, agents bid, and the best candidate is assigned.

**11) In the BDI model, "Desires" represent:**
- **Answer:** Objectives or goals the agent wants to achieve.

**12) An agent's "Intentions" in the BDI architecture refer to:**
- **Answer:** The subset of desires the agent commits to with specific plans.

**13) Which of the following best describes "Beliefs" in the BDI model?*
- **Answer:** The agent's assumptions, facts, and knowledge about the world.

**14) A mobile agent architecture is characterized by:**
- **Answer:** Its ability to migrate across different machines/networks with its code and state.

**15) Which is an example of a mobile agent in e-commerce?**
- **Answer:** A shopping bot that compares prices across multiple sites by moving between servers.

**16) In agent communication, the "Performative" field specifies:**
- **Answer:** The speech act type such as inform, request, propose.

**17) Which of the following is NOT a common coordination strategy in multi-agent systems?**
- **Answer:** Randomization.

**18) Which of the following message types is part of the FIPA Agent Communication Language (ACL)?**
- **Answer:** Request.

**19) Which communication standard is widely used for ensuring heterogeneous agents can understand each other?**
- **Answer:** FIPA ACL.

**20) The primary goal of KQML (Knowledge Query and Manipulation Language) in Multi-Agent Systems is:**
- **Answer:** To enable agents to communicate knowledge and intentions using standardized performatives.

**21) An agent is defined as:**
- **Answer:** Anything that perceives its environment and acts upon it.
    

**22) In the PEAS framework, the "Sensors" of an automated taxi driver include:**
- **Answer:** Cameras, sonar, GPS, odometer, speedometer.


**23) A rational agent chooses actions based on:**
- **Answer:** Maximizing expected performance measure given percept history and knowledge.

**24) In the PEAS framework, the "Actuators" of an automated taxi driver include:**
- **Answer:** Steering wheel, accelerator, brake, signal, horn.

**25) The autonomy of an agent refers to:**
- **Answer:** The extent to which its behavior depends on its own experience.

**26) Which of the following environments is fully observable?**
- **Answer:** A security system with cameras in every corner of a building.

**27) A vending machine that always provides the correct item after inserting the required coins is an example of:**
- **Answer:** Deterministic environment.

**28) In a sequential environment:**
- **Answer:** Current actions affect future states and decisions.

**29) A goal-based agent differs from a reflex agent because:**
- **Answer:** It uses knowledge of the environment and goals to plan actions.

**30) In a utility-based agent, the utility function is used to:**
- **Answer:** Map states to numerical values representing success or happiness.

**31) Swarm intelligence is defined as:**
- **Answer:** Collective behavior of decentralized, self-organized systems.

**32) The main communication mechanism among ants in ACO is:**
- **Answer:** Stigmergy through pheromone trails.

**33) Why do ants eventually select the shortest path in nature?**
- **Answer:** Shorter paths accumulate pheromone faster due to more frequent traversal.

**34) Which of the following best describes pheromone trails in ACO?**
- **Answer:** A reinforcement signal that guides ants toward better solutions.

**35) Which type of problems is ACO best suited for?**
- **Answer:** Combinatorial optimization problems.

**36) In the probabilistic transition function of ACO, $\eta_{ij}=1/d_{ij}$ represents:**
- **Answer:** Visibility or inverse of distance between nodes.

**37) What role does pheromone evaporation ($\rho$) play in ACO?**
- **Answer:** Prevents unlimited accumulation of pheromone and encourages exploration.

**38) In Ant Colony Optimization, the parameter $\alpha$ (alpha) in the transition probability function controls:**
- **Answer:** The influence of pheromone trails on the decision-making process.

**39) Which of the following is a real-world application of ACO?**
- **Answer:** Network routing and logistics optimization.

**40) A major advantage of ACO over other optimization techniques is:**
- **Answer:** It adapts well to dynamic environments.

---

## Question (2): Genetic Algorithm (10 Marks)

**Task:** Consider a binary string optimization problem to maximize the number of ones in a string of length 8. Population size 4, roulette wheel selection.

1. **Calculate fitness:** Fitness is the count of '1's in each 8-bit string.
    
2. **Roulette Wheel Selection:** Calculate selection probability $P_i = \text{Fitness}_i / \sum \text{Fitness}$. Create a cumulative probability range to select parents based on a random number.
    
3. **Rank-based vs. Roulette Wheel Selection:**
    
    - **Roulette Wheel:** Selection probability is directly proportional to fitness. High-fitness individuals can dominate too quickly (premature convergence).
        
    - **Rank-based:** Individuals are ranked by fitness. Selection is based on rank rather than raw score, which maintains more genetic diversity.
        

---

## Question (3): Particle Swarm Optimization (10 Marks)

**Task:** Maximize $f(x) = \frac{(x-3)^2}{2} + 1$ with 3 particles.

- **Initial Positions ($x_i$):** $P_1: -5.0, P_2: 2.0, P_3: 7.0$.
    
- **Initial Velocities ($v_i$):** $P_1: 0.5, P_2: -0.3, P_3: 0.2$.
    
- **Constants:** $w=1, c_1=1, c_2=1, r_1=0.2, r_2=0.3$.
    

**Calculation Steps:**

1. **Evaluate $f(x)$** for each $x_i$ to find individual bests ($P_{best}$) and global best ($G_{best}$).
    
2. **Update Velocity:** $v_i^{t+1} = v_i^t + (1)(0.2)[P_{best,i} - x_i^t] + (1)(0.3)[G_{best} - x_i^t]$.
    
3. **Update Position:** $x_i^{t+1} = x_i^t + v_i^{t+1}$.

----
## Swarm Intelligence Quiz (15 Questions)

**1) What does the inertia weight in PSO control?**

- **Answer:** Trade-off between exploration and exploitation.
    

**2) In ACO, what is used by ants to communicate paths to food?**

- **Answer:** Pheromones.
    

**3) What happens when ants find a good path to food?**

- **Answer:** Ants reinforce the path with pheromones, leading more ants to the food.
    

**4) How is a particle's velocity updated?**

- **Answer:** Using current velocity, cognitive and social components.
    

**5) How do particles find the best solution?**

- **Answer:** Particles find the best solution by exploring and exploiting the solution space through collaboration and adjustment.
    

**6) How do ants communicate with each other?**

- **Answer:** Ants communicate using pheromones, tactile signals, and sounds.
    

**7) What happens when pheromone evaporation is too low in ACO?**

- **Answer:** Premature convergence to suboptimal paths.
    

**8) What is a common use for swarm optimization?**

- **Answer:** Finding optimal solutions in complex optimization problems.
    

**9) What does the parameter rho ($\rho$) represent in ACO?**

- **Answer:** Evaporation rate.
    

**10) How do ants probabilistically choose the next node?**

- **Answer:** Based on pheromone level and heuristic information.
    

**11) Which parameter in ACO controls the influence of pheromone trails?**

- **Answer:** Alpha ($\alpha$).
    

**12) In PSO, what does a "particle" represent?**

- **Answer:** A solution.
    

**13) Which parameters in PSO influence the cognitive and social behaviors?**

- **Answer:** $c_1$ and $c_2$.
    

**14) What happens if inertia weight is too high in PSO?**

- **Answer:** The swarm may overshoot good solutions.
    

**15) What two main best positions are tracked in PSO?**

- **Answer:** Personal best and global best.
---
## Swarm Intelligence and Ant Colony Optimization Quiz

* **What is the main focus of Swarm Intelligence?**
* Collective behavior.

* **What do ants use to communicate with each other?**
* Pheromones

* **What is the Traveling Salesman Problem (TSP)?**
* Finding the shortest path.

* **What do ants rely on for survival?**
* Swarm intelligence.

* **What is stigmergy?**
* Indirect interaction through the environment.

* **What happens to a pheromone trail when more ants follow it?**
* It becomes more attractive.

* **What is one characteristic of swarms?**
* Local interaction based on simple rules.

* **What is the goal of Ant Colony Optimization?**
* To find the shortest path.

* **What happens to a trail when fewer ants use it?**
* It evaporates.

* **What is the first step in the Ant System algorithm?**
* Randomly place ants.

* **What do ants do after completing a tour?**
* Lay pheromone.

* **What is the role of pheromone in Ant Colony Optimization?**
* To mark paths.

* **What is one advantage of Ant Colony Optimization algorithms?**
* They adapt to dynamic environments.

* **What do ants do when they find a shorter route?**
* Follow it more.

* **What is the purpose of the transition probability in the Ant System?**
* To choose the next path.

* **What does the term 'visibility' refer to in Ant Colony Optimization?**
* Distance to the next town.

* **What is the main behavior of ants when foraging for food?**
* They follow simple rules.

* **What is the main feature of swarm intelligence?**
* Decentralized behavior.

* **What happens to the pheromone trail over time?**
* It evaporates.

* **What do ants do to mark the paths they have taken?**
* Leave pheromones.
---
## Genetic Algorithms (GA) Quiz

- **What does GA stand for?**
    - Genetic Algorithms.
        
- **What is a chromosome made of?**
    - Genes.
        
- **What is the process of creating offspring called?**
    - Reproduction.
        
- **What does 'survival of the fittest' mean?**
    - Only the strongest survive.
        
- **What is the fitness value?**
    - How much an organism can reproduce.
        
- **What is the first step in simulating natural selection?**
    - Encoding.
        
- **What is mutation in Genetic Algorithms?**
    - Random changes in genes.
        
- **What is crossover in Genetic Algorithms?**
    - Combining features from parents.
        
- **What is the purpose of the fitness function?**
    - To measure the quality of a chromosome.
        
- **What is the role of the population in Genetic Algorithms?**
    - To represent solutions.
        
- **What does the term 'termination' refer to?**
    - Ending the process.
        
- **What is binary encoding?**
    - Using bits to represent solutions.
        
- **What is the purpose of the roulette wheel selection?**
    - To randomly select chromosomes.
        
- **What happens during the mutation process?**
    - Genes are randomly changed.
        
- **What is the goal of Genetic Algorithms?**
    - To find the best solution.
        
- **What is the significance of crossover?**
    - To create new chromosomes.
        
- **What is the expected number of changes during mutation?**
    - $L \cdot p$ (where $L$ is length and $p$ is probability).
        
- **What does convergence mean in Genetic Algorithms?**
    - All genes have the same value.
---
Based on the provided exam materials and subject matter, here are the questions with their correct answers:

**1) In a Multi-Agent System, agents communicate mainly to:**

- **Answer:** B) Share knowledge, request services, and coordinate actions.
    

**2) A communication message in agent systems usually includes:**

- **Answer:** A) Sender, receiver, performative, and content.
    

**3) Coordination in multi-agent systems means:**

- **Answer:** A) How agents manage dependencies and avoid conflicts.
    

**4) Which coordination strategy involves agents bargaining to resolve conflicts?**

- **Answer:** C) Negotiation.
    

**5) In the Contract Net Protocol (CNP):**

- **Answer:** B) A manager announces a task, agents bid, and the best one is chosen.
    

**6) Which message type is used for sending information?**

- **Answer:** B) Inform.
    

**7) Which message type best fits the sentence: “What is your battery level?”**

- **Answer:** B) Query.
    

**8) What does KQML stand for?**

- **Answer:** B) Knowledge Query and Manipulation Language.
    

**9) FIPA ACL (Foundation for Intelligent Physical Agents – Agent Communication Language) is important because it:**

- **Answer:** A) Ensures heterogeneous agents can understand and interact with each other.
    

**10) An agent is defined as anything that:**

- **Answer:** A) Perceives its environment through sensors and acts upon it through actuators.
    

**11) In a human agent, which of the following are considered sensors?**

- **Answer:** C) Eyes and ears.
    

**12) The agent function maps:**

- **Answer:** B) Percept histories to actions.
    

**13) An agent is equal to:**

- **Answer:** B) Architecture + program.
    

**14) A rational agent selects an action that is expected to:**

- **Answer:** C) Maximize its performance measure.
    

**15) Which of the following is one factor that affects rationality?**

- **Answer:** B) The agent’s prior knowledge of the environment.
    

**16) Rationality is different from perfection because rationality:**

- **Answer:** C) Maximizes expected outcome.
    

**17) The autonomy of an agent is the extent to which its behavior is determined by:**

- **Answer:** C) Its own experience.
    

**18) What does PEAS stand for?**

- **Answer:** B) Performance measure, Environment, Actuators, Sensors.
    

**19) Genetic Algorithms are a particular class of:**

- **Answer:** B) Evolutionary algorithms.
    

**20) A chromosome in Genetic Algorithms is:**

- **Answer:** C) A string of genes that represents a solution.
    

**21) A gene is defined as:**

- **Answer:** A) One component of the solution pattern.
    

**22) Higher fitness value in a Genetic Algorithm means:**

- **Answer:** C) Better solution.
    

**23) In Particle Swarm Optimization, each particle is characterized mainly by:**

- **Answer:** B) Position and velocity.
    

**24) The best position found by a particle itself is called:**

- **Answer:** C) Personal best.
    

**25) The best position found by any particle in the swarm is called:**

- **Answer:** B) Global best.
    

**26) Which of the following is NOT one of the simple factors of swarm behavior?**

- **Answer:** D) Mutation.
    

**27) In Particle Swarm Optimization, particles adjust their movement according to:**

- **Answer:** C) Their own experience and the experience of other particles.
    

**28) What does the inertia component in Particle Swarm Optimization do?**

- **Answer:** B) Makes the particle move in the same direction with the same velocity.
    

**29) The stopping criterion in Particle Swarm Optimization determines when the algorithm:**

- **Answer:** C) Ends the iterations.
    

**30) Particle Swarm Optimization combines:**

- **Answer:** B) Self-experiences with social experiences.