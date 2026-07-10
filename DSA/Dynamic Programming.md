Faker [[Knapsack]] , ROO7 efta7 ktab ch. 34an rsoomat kteer werg3ly hena

- So now it’s not all or nothing—you can take a fraction of an item. How do you handle this using dynamic programming? Answer: You can’t. With the dynamic-programming solution, you either take the item or not. There’s no way for it to figure out that you should take half an item.
- Dynamic programming is useful when you’re trying to optimize something given a constraint. In the knapsack problem, you had to maximize the value of the goods you stole, constrained by the size of the knapsack. 
- You can use dynamic programming when the problem can be broken into discrete subproblems, <span style="background:#ff4d4f">==and they don’t depend on each other.==</span>

General Tips:
1. Every dynamic-programming solution involves a grid. 
2. The values in the cells are usually what you’re trying to optimize. For the knapsack problem, the values were the value of the goods. 
3. Each cell is a subproblem, so think about how you can divide your problem into subproblems. That will help you figure out what the axes are.
4. In dynamic programming, you’re trying to maximize something

