# Number Theory — PS Level 1

Core building blocks: finding divisors, prime factorization (three flavors), and the sieve used to preprocess primes so queries become **O(1)**.

---

## 1. All divisors of `n`

Trick: divisors come in **pairs**. If `i` divides `n`, then `n / i` divides it too — so we only loop up to `√n` and grab both sides of each pair.

```C++
vector<int> prime(int n) 
{
    vector<int> ret;

    // Step 1: Check every number up to the square root of n
    for (int i = 2; i * i <= n; i++) 
    {
        // Step 2: Keep dividing n by i as long as it's a factor
        while (n % i == 0) 
        {
            ret.push_back(i);
            n /= i;
        }
    }

    // Step 3: If n is still greater than 1, the leftover is a prime itself
    if (n > 1) 
    {
        ret.push_back(n);
    }

    return ret;
}
```

---

## 2. Prime factorization — three versions

### v1 — trial division, one prime at a time

Walk `i` from 2 up to `√n`. The first `i` that divides `n` is guaranteed prime (smaller factors were already stripped). Divide it out and restart. Whatever survives above `√n` is itself prime.

```C++
vector<int> prime_factorization(int n)
{
    vector<int> ret;
    while (n != 1)
    {
        bool divided = false;
        for (int i = 2; i * i <= n; i++)
        // only up to i*i: past sqrt(n) the leftover can only be one prime
        {
            if (n % i == 0)
            {
                ret.push_back(i);
                n /= i;
                divided = true;
                break;
            }
        }

        if (!divided) // e2fesh prime: nothing <= sqrt divided n
        {
            ret.push_back(n); // n itself is the last prime factor
            n = 1;            // so we break the while loop
        }
    }
    return ret;
}
```

### v2 — strip each prime fully before moving on

Same idea, but the inner `while` peels **all** copies of `i` at once (so `8 -> 2,2,2`). Cleaner and slightly faster.

```C++
vector<int> prime_factorization2(int n)
// 3ayz ageeb as8r 3dd mn el arkam ely lw etdrbt fy b3d tdeeny n
{
    vector<int> ret;
    for (int i = 2; i * i <= n; i++)
    {
        while (n % i == 0) // keep dividing while i fits
        {
            ret.push_back(i);
            n /= i; // shrink n each time, zy ma bn3ml fl loop
        }
    }

    if (n != 1) // leftover > sqrt is prime -> it never entered the loop
    {
        ret.push_back(n);
        n = 1;
    }

    return ret;
}
```

---

## 3. The sieve (preprocessing)

Sieve of Eratosthenes. Two outputs in one pass:
- `is_prime[x]` — answer any "is x prime?" query in **O(1)**.
- `divide[x]` — the **smallest prime factor** of `x`, which powers the fast factorization in v3.

Any prime marks all of its multiples as non-prime; the first prime to touch a number records itself as that number's smallest prime factor.

```C++
// fills is_prime[] and divide[] (smallest prime factor) up to n
void sieve(int n, vector<bool> &is_prime, vector<int> &divide)
{
    is_prime.assign(n + 1, true);
    divide.assign(n + 1, 0);

    // 0 and 1 are not prime -> set manually
    is_prime[0] = is_prime[1] = false;

    for (int i = 2; i <= n; i++) // 0 and 1 already handled
    {
        if (is_prime[i]) // still true => i is prime
        {
            divide[i] = i; // a prime's smallest prime factor is itself

            for (int j = 2 * i; j <= n; j += i) // the multiples of i
            {
                is_prime[j] = false;
                if (divide[j] == 0)   // first prime to reach j
                    divide[j] = i;    // record smallest prime factor
            }
        }
    }
}
```

### v3 — factorize using the sieve's `divide[]` table

Once `divide[]` is built, factorizing is just repeatedly jumping to the smallest prime factor — no trial division at all.

```C++
vector<int> prime_factorization3(int n, vector<int> &divide)
{
    vector<int> ret;
    while (n != 1)
    {
        int p = divide[n]; // smallest prime factor, O(1)
        ret.push_back(p);
        n /= p;
    }
    return ret;
}
```

---

## 4. Single primality check

When you only need to test **one** number (no preprocessing worth it), trial-divide up to `√n`.

```C++
bool is_prime(long long n)
{
    if (n <= 1) return false;
    for (long long i = 2; i * i <= n; i++)
    {
        if (n % i == 0) return false;
    }
    return true;
}
```

---

## When to use what

| Need | Use | Cost |
|------|-----|------|
| Divisors of one `n` | `divisors` | O(√n) |
| Factorize one `n` | `prime_factorization2` | O(√n) |
| Test one `n` for prime | `is_prime` | O(√n) |
| Many prime queries / factorize many | `sieve` then `is_prime[]` / `prime_factorization3` | O(n log log n) build, O(1) / O(log n) query |

---

[Math/Level 1 at main · UwUkareem/Math · GitHub](https://github.com/UwUkareem/Math/tree/main/Level%201)
