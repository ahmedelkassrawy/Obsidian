## What is Concurrency?

- **Concurrency** as the name suggests is having **multiple transactions running at the same time**.
- You can have **multiple requests**, say to insert a user in the database, being served **at the same time**, i.e., concurrent requests -> **handle load and increase speed**.
- If you are at a shop one cashier causes queue overload in order to scale this:
    1. **Horizontal Scaling** -> hire a new cashier now we have two rows to serve twice as many customers (current: 2 cashiers).
    2. **Vertical Scaling** -> hiring a superhuman cashier that can serve twice the customers by herself (current: 1 cashier).
- When we have **multiple** things doing the same job, like for the example, 2 cashiers serving customers, we call that **concurrency**.

## Example: Concurrent Transactions

```go
package main

import (
    "log"
    "time"
)

var balance int = 10

func buy(price int, tx string) bool {
    if balance < price {
        log.Printf("%s, refused due to insufficient funds", tx)
        return false
    }
    balance -= price
    log.Printf("%s, succeeded", tx)
    return true
}

func main() {
    go buy(7, "transaction 1")
    go buy(5, "transaction 2")
    time.Sleep(10 * time.Second)
}
```

### Output (Example Run 1):

```plaintext
2022/06/19 23:00:00 transaction 1, succeeded
2022/06/19 23:00:00 transaction 2, refused due to insufficient funds
```

### Output (Example Run 2):

```plaintext
2022/06/19 23:00:00 transaction 2, refused due to insufficient funds
2022/06/19 23:00:00 transaction 1, succeeded
```

This means that the following has likely happened:

1. Transaction 1 checked the balance, allowed the purchase and updated the balance then it got the thread got **suspended** (yeah, this can happen, the OS can suspend threads while they're running and schedule other threads to do some work, then resumes the suspended threads).
2. Transaction 2 checked the balance, found it insufficient and failed the transaction.
3. Transaction 1 got **resumed** and it printed the success message.

## Race Conditions

### Key Points:

1. **Threads can be suspended and resumed**.
2. Each thread is executing the same code section separately.
3. Each line of code can have multiple threads executing it at the same time.
4. This suspension and resumption can lead to **completely different** results.

### Critical Failure:

```plaintext
2022/06/19 23:00:00 transaction 1, succeeded
2022/06/19 23:00:00 transaction 2, succeeded
```

This is **completely wrong**, how could this happen? Let's see:

1. Transaction 1 checks balance, allows the purchase and gets suspended.
2. Transaction 2 checks balance, allows the purchase and gets suspended.
3. Transaction 1 updates the balance and prints succeeded.
4. Transaction 2 updates the balance and prints succeeded.

Now the balance is negative, allowed a transaction that should have never been allowed. This is called a **race condition** which is **when 2 threads race to access a shared resource** (user balance here) -> results in inconsistencies, wrong behaviors.

## Concurrency Control

### Single Threading

The problem we had in the previous code is that we had 2 transactions running **concurrently** on 2 threads. Now let's eliminate threading at all, make it a single threaded:

```go
func main() {
    buy(7, "transaction 1")
    buy(5, "transaction 2")
}
```

Now the code is **single threaded** (everything is executed by the main thread) + **sequential**. The output we want will always be the case here since we declared the queue we want it to execute.

#### Output:

```plaintext
2022/06/19 23:00:00 transaction 1, succeeded
2022/06/19 23:00:00 transaction 2, refused due to insufficient funds
```

**Concurrent but Thread Safe** -> **Single threading** the code of course **solved** our **race conditions** but it **limited our ability to scale**. Now we are stuck with that single cashier forever as the number of our customers grow, it will **infeasible to operate**.

The idea of **sequencing access to the shared resource** (the user's balance) is still a **valid** though, we will try to make it that **only one transaction is accessing** (read and updating) the balance at any given time. The code section that we want to safeguard its access is commonly called a **critical section**.

### Thread-Safe Concurrency with Locking

A common way to **protect critical sections** from concurrent access is called **locking**, the idea of a lock is simple, it's like a **lock and a key**, if you have the key, you can **get inside** the critical section and if you don't you have to **wait** until you get it.

Now let's assume, we have a method called, `mutex.Lock()` to **acquire** that lock to access the critical section and another method called `mutex.Unlock()` to **release** the lock when we are done accessing the critical section and want to allow other waiting transactions to access the critical section since we are done. Our code will look like this:

```go
package main

import (
    "log"
    "sync"
    "time"
)

var balance int = 10

func buy(price int, tx string, mu *sync.Mutex) bool {
    mu.Lock()
    defer mu.Unlock()

    if balance < price {
        log.Printf("%s, refused due to insufficient funds", tx)
        return false
    }
    balance -= price
    log.Printf("%s, succeeded", tx)
    return true
}

func main() {
    var mu sync.Mutex
    go buy(7, "transaction 1", &mu)
    go buy(5, "transaction 2", &mu)
    time.Sleep(10 * time.Second)
}
```

What this did for us, is that now only 1 transaction will be executing at a given time, for example:

1. Transaction 1 acquires the lock and starts executing.
2. Transaction 2 tries to acquire the lock, but fails because it's unavailable so it waits.
3. Transaction 1 completes and succeeds then releases the lock.
4. Transaction 2 can now acquire the lock and start executing then it fails.

How is that different from single threading? As a matter of fact, in this specific example, they are exactly the same, but in so many other cases they will be different.

### Fine-Grained Locking

Now let's assume that our `buy` function is **complicated** and does **more stuff** before or after the section that buys stuff, for example:

```go
func buy(price int, tx string) bool {
    if balance < price {
        log.Printf("%s, refused due to insufficient funds", tx)
        send_insufficient_funds_email()
        return false
    }
    balance -= price
    log.Printf("%s, succeeded", tx)
    generate_sales_report()
    update_inventory()
    return true
}
```

As we can see, it's the same function but it **does extra work** like `send_insufficient_funds_email()` on transaction failures or `generate_sales_report()` and `update_inventory()` on transaction success. **Assuming that those functions are thread safe on their own** (there is no problem in them running concurrently), it **wouldn't make sense to lock the entire function** because now **locks will have to be unavailable for a longer time** (until all other function calls are done which might take time).

**Fine grain our locking to only lock the critical section**:

```go
func buy(price int, tx string, mu *sync.Mutex) bool {
    mu.Lock()
    if balance < price 
    {
        log.Printf("%s, refused due to insufficient funds", tx)
        mu.Unlock()
        
        send_insufficient_funds_email()
        return false
    }
    balance -= price
    log.Printf("%s, succeeded", tx)
    
    mu.Unlock()
    
    generate_sales_report()
    update_inventory()
    
    return true
}
```

We only lock the part that causes race conditions which is checking and updating the balance.

### Common Mistakes

1. **Underlocking**: Sometimes, you want to make your locking as fine grained as possible but you end up underlocking (locking less than you actually need). What if we unlock before we update the price? This might make sense at first because we will be locking the part that checks the balance, so no two transactions will check the balance at the same time. But updating the balance is also part of the critical section because if we unlock before we update the balance, another transaction might check the now old balance which will cause problems. So make sure that you fine grain your locking for better performance, but be wary of underlocking.
2. **Deadlocks**: A deadlock happens in so many ways, but the one way we are interested in here is when a lock is acquired but never released. A common mistake here is to unlock after updating the price but forgetting to unlock when the transaction fails. If you do this, the lock will be acquired and no other transaction will be able to acquire the lock, essentially bringing your system to a halt.

## Concurrency Scope

Concurrency can be on different scopes, for example:

1. An application can be concurrent on the scope of a **single process**, so we have a single process of the application running and it contains multiple threads. This is similar to the examples shown above.
2. An application can be concurrent on the scope of **multiple processes** and those processes can either be on the same machine or on different machines in case we have replica applications running (like the cashier example).

In the previous example where we used locks implemented by the `sync` package in Go, that will **only work for threads within the same process**. But if the same code is running on two **different machines**, we are back to the drawing board.

So we really need to be aware of our concurrency scope in order to handle it correctly.

### Distributed Locking with Redis

Now let's assume that we will run our code on multiple machines, how can we make locking work? Let's just ask ourselves the inverted question, **why didn't lock work when we moved to a multi-machine setup**? It's because **locks were seen only within the same process** so when we run on different machines, the statement `mu.Lock()` **doesn't actually stop the threads on the other machine** from accessing the critical section. So now how can we make the lock **visible** for **both machines**?

We can move our locking logic to a **centralized** place where all machines can access. For example, we can use an in-memory store like **Redis** to do this. If you are not familiar with Redis, it's basically a key-value store like a dictionary, you can set a key to have some value and you can read those keys (_among a ton of other useful features_).

```ruby
def lock(key)
  return false if REDIS.get(key)
  REDIS.set(key, "true")
  true
end

def unlock(key)
  REDIS.del(key)
end
```

The `lock` method checks if the key indicating the lock has a value or not, if it does, then someone else must have locked it, so it returns false. If not, it sets the value of the key to `true` and returns true. In the `unlock` method, it just deletes the key from Redis (so it's unset and can be set later).

This is a very simple lock implemented in Redis and can be seen and accessed by multiple machines connected to the same Redis instance. But wait, doesn't that code have the same race condition we have been talking about? Yes, it does, consider this:

1. Thread 1 checks the value of the key, finds it `nil` and gets suspended.
2. Thread 2 checks the value of the key, finds it `nil` and acquires the lock.
3. Thread 1 is resumed and acquires the lock as well.

Now both threads have acquired the lock, so the lock is useless.

Now let's ask ourselves, what are we missing here? The problem here is that **a thread can get suspended between the two operations of checking the lock value and acquiring the lock**. If we have a way to make sure that the thread will never get interrupted during those two steps, that would be ideal.

Executing **multiple instructions without being interrupted** is called **atomicity**, so we need to make **checking** the lock and **acquiring** the lock **atomic** somehow.

Luckily, there are some hardware instructions for this, Redis introduces an option to the `SET` command called `nx` which sets the value of a key only if it doesn't exist and because **Redis is single threaded**, checking that the **key exists or not and setting is atomic**.

```ruby
def lock(key)
  REDIS.set(key, "true", nx: true)
end

def unlock(key)
  REDIS.del(key)
end
```

`nx` option makes the `SET` command return false if it fails to set the key and true if it succeeds.

This lock now works perfectly. There is one minor caveat however, we should never leave a chance to deadlocks. We need to think of edge cases, like for example, **what if the entire machine crashes after acquiring a lock and before releasing it**? It will be **locked forever**.

A simple way to handle this in a Redis lock is to set a **timeout** for the lock to be held after which it will **expire**, thus being released. Redis has an `ex` option in the `SET` command that implements this expiry functionality, like so:

```ruby
def lock(key)
  REDIS.set(key, "true", nx: true, ex: 1.minute.seconds.to_i)
end

def unlock(key)
  REDIS.del(key)
end
```

This **sets** the key (acquires the lock) for **only 1 minute**, then it **expires**. Be sure to choose an appropriate expiry time based on your use case because you don't want the lock to expire mid-execution and cause race conditions.

## General Tips for Concurrent Programming

1. Whenever you write **concurrent** code, think of **race conditions**, basically think what will happen if two threads are executing the same code at the same time.
2. It helps if you think in terms of **suspension** and **resumption** of threads, like, what if this thread executes this statement, then it gets **suspended** and another thread does something else, then this thread gets **resumed**.
3. Don't look at statements as line. **One line doesn't equal one statement**, for example, a line like `read(val) > 10` is not one instruction, it actually reads the value then compares, so it can get suspended between the two operations.
4. When you're placing locks in your code, make sure to **fine grain** the locking range for better performance, but be sure to not **underlock**.
5. Make sure that any code path that has **a lock has a corresponding unlock**. Make sure to check branching in the code, for example if you lock then get into a `switch ... case`, each code path in the cases should have an unlock in its path to completion, otherwise you will get into **deadlocks**.
6. Think twice about your **concurrency scope** and handle it accordingly as explained.
7. Never declare locks that can be left as locked forever, always add a **safeguard unlock or an expiry**.