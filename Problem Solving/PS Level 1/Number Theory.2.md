---
title: Number Theory
tags:
  - problem-solving
  - number-theory
  - competitive-programming
aliases:
  - Number Theory 2
---
# Number Theory

> [!abstract] What's in here
> The modular-arithmetic toolkit you actually reach for in contests: the `%` operator and its identities, divisor preprocessing, binary exponentiation, GCD / extended GCD (Diophantine equations), LCM, and modular inverse.

---

## Modular Arithmetic — the `%` operator

`a % n` returns the **remainder** after dividing `a` by `n`.

$$a \bmod n = a - n \left\lfloor \tfrac{a}{n} \right\rfloor$$

### Clock intuition (wrap-around)

Modulo is how a clock wraps. If the time is `6` now:

```
after 7h  -> (6 + 7)  % 12 = 1
after 19h -> (6 + 19) % 12 = 1     // 7 and 19 land on the same hour
```

Going **backwards** is the tricky part, because in C++ `%` can return a negative value. To force a non-negative result, add `n` and take `%` again:

```
if it's 6 now
before 13h -> (((6 - 13) % 12) + 12) % 12
```

> [!warning] The sign trap in C++
> `%` keeps the sign of the **dividend**, so it can be negative:
> - `A % 3` can be any of `[-2, -1, 0, 1, 2]`
> - `-A % N != A % N`
>
> The canonical fix is the **`((x % n) + n) % n`** idiom whenever `x` might be negative.

### Core identities

| Identity | Meaning |
|---|---|
| `A % N == 0` | `A` is divisible by `N` |
| `A % N == B % N` ⇔ `(A - B) % N == 0` | `A` and `B` are **congruent** mod `N` |
| `(A % N) % N == A % N` | `%` is idempotent |
| `(N^X) % N == 0` | any power of `N` is divisible by `N` |
| `((-A % N) + (A % N)) % N == 0` | a value and its negative cancel |

### Distributes over + and ×

$$(A + B) \bmod N = ((A \bmod N) + (B \bmod N)) \bmod N$$
$$(A \times B) \bmod N = ((A \bmod N) \times (B \bmod N)) \bmod N$$

> [!tip] Why this matters
> These two laws let you take `%` **as you go** instead of at the end — the whole reason overflow-safe modular code is possible. Subtraction works too, but re-normalize the sign: `((A % N - B % N) % N + N) % N`.

---

## Divisor Preprocessing

> **Problem.** Given `q` queries, each a number `X`; for every query print all divisors of `X`.

Instead of factoring each query separately, do a **sieve-style** pass once: every `i` is a divisor of all its multiples `i, 2i, 3i, …`. Push `i` into each of those buckets.

```c++
const int MAX = 1e5;
vector<int> divs[MAXS + 1];
int cnt_of_divs[MAX + 1];

void generate_divs()
{
	for(int i = 1; i <= MAX; i++)
	{
		for(int j = i; j <= MAX; j += i)
		{
			divs[j].push_back(i);
			cnt_of_divs[j]++;
		}
	}
}
```

> [!info] Complexity
> The inner loop runs `MAX/i` times, so the total is $\sum_{i=1}^{MAX} \tfrac{MAX}{i} = O(MAX \log MAX)$ — the harmonic sum. After this, each query is answered in $O(1)$ (just read `divs[X]`).

### Counting divisors of a single number

When you only need the **count** for one number, trial-divide up to $\sqrt{num}$. Every divisor `i < √num` pairs with `num / i`, so each hit contributes 2. A perfect square has an unpaired middle divisor `√num`, counted once.

```c++
int count_divs(int num)
{
	int i,cnt = 0;
	for(int i = 1; i * i < num; i++)
	{
		if(!(num % i))
		{
			cnt += 2;
		}
	}
	
	if((i * i) == num) cnt++;
	return cnt;

}
```

> [!info] Complexity
> $O(\sqrt{num})$ per number — the go-to when you can't afford the $O(MAX \log MAX)$ sieve or `MAX` is huge.

---

## Binary Exponentiation

Goal: compute $base^n$ fast.

### Naive — $O(n)$

Multiply `base` into the result `n` times.

```c++
long long power(int base,int n)
{
	long long res = 1;
	
	for(int i = 1; i <= n; i++)
	{
		res *= base;
	}
	
	return res;
}
```

### Fast — $O(\log n)$

Key idea: **exponentiation by squaring**. Read `n` in binary — square the base each step, and multiply it into the answer only on set bits.

$$base^n = \begin{cases} (base^{2})^{n/2} & n \text{ even} \\ base \cdot base^{\,n-1} & n \text{ odd} \end{cases}$$

```c++
long long power(int base, int n)
{
	long long res = 1;
	
	while(n)
	{
		if(n % 2 != 0)
		{
			res *= base;
			n--;
		}
		else
		{
			base *= base;
			n /= 2;
		}
	}
	
	return res;
}
```

### Fast + modular

Same routine, but reduce mod `mod` after every multiply so nothing overflows. This is the version you use in practice (modular inverse, hashing, combinatorics all depend on it).

```c++
long long power(int base,int n,int mod)
{
	long long res = 1;
	while(n)
	{
		if(n % 2 != 0)
		{
			res = (res * base) % mod;
			n--;
		}
		else
		{
			base = (base * base) % mod;
			n /= 2;
		}
	}
	
	return res;
}
```

> [!warning] Overflow reminder
> Keep `base`, `res`, and `mod` as `long long`. If `mod` is near $10^9$, the product `res * base` can reach $\approx 10^{18}$ — it fits in `long long` but would overflow a 32-bit `int`.

---

## GCD — Greatest Common Divisor

`d` is the GCD of `a` and `b` if it is the **largest** number with `a % d == b % d == 0`.

```c++
int a,b;
cin>>a>>b;

int g = __gcd(a,b);

if(g == 1)
{
	cout<<"NO";
}
else cout<<"YES";
```

> [!note] `__gcd` and coprimality
> `__gcd(a, b)` is built into GCC. `g == 1` means `a` and `b` are **coprime** (share no factor but 1) — exactly the "NO" branch above.

### Handy properties

| Property | |
|---|---|
| `gcd(a, b) = gcd(a - b, b) = gcd(a + b, b)` | shifting by `b` doesn't change the GCD (basis of the subtraction algorithm) |
| `gcd(a, b) = d` ⇒ `gcd(a/d, b/d) = 1` | dividing out the GCD leaves coprime numbers |
| `gcd(a, b, c) = gcd(gcd(a, b), c)` | extends to any count by folding |

---

## Diophantine Equations

A linear Diophantine equation asks for **integer** solutions `(x, y)`:

$$a \cdot y + b \cdot x = c$$

> [!important] Existence condition
> A solution exists **iff `gcd(a, b)` divides `c`**. (Once you have one solution, all others follow by shifting: `x += b/g`, `y -= a/g`.)

### Extended Euclidean algorithm

Standard GCD only returns `d`. The **extended** version also returns the coefficients `x, y` with `a·x + b·y = gcd(a, b)` (Bézout's identity).

```c++
int gcd(int a, int b, int& x , int& y)
{
	if(b == 0)
	{
		x = 1;
		y = 0;
		return a;
	}
	
	int x1,y1;
	int d = gcd(b , a % b, x1 , y1);
	
	x = y1;
	y = x1 - y1 * (a / b);
	return d;
}

bool find_any_solution(int a , int b, int c, int&x0 , int&y0 , int&g)
{
	g = gcd(abs(a), abs(b), x0,y0);
	
	if( c % g)
	{
		return false;
	}
	
	x0 *= c / g;
	y0 *= c / g;
	if( a < 0) x0 = -x0;
	if( b < 0) y0 = -y0;
	return true;
}
```

> [!note] Reading `find_any_solution`
> 1. Solve `a·x0 + b·y0 = g` on the absolute values.
> 2. If `c % g != 0`, no integer solution exists → return `false`.
> 3. Scale the base solution by `c / g` so it satisfies `= c`.
> 4. Flip signs to undo the `abs()` on negative inputs.

---

## LCM — Least Common Multiple

$$\text{lcm}(a, b) = \frac{a \cdot b}{\gcd(a, b)}$$

```c++
int lcm(int a, int b)
{
	return a / ___gcd(a , b) * b;
}
```

> [!tip] Order of operations
> Divide **before** multiplying (`a / gcd * b`, not `a * b / gcd`) so the intermediate value stays small and doesn't overflow.

---

## Modular Inverse

Division doesn't exist in modular arithmetic, so you replace it with multiplication by an **inverse**:

$$\frac{a}{b} \bmod c \;\longrightarrow\; \big(a \cdot b^{-1}\big) \bmod c$$

where $b^{-1}$ is the modular inverse of `b`, i.e. `(b · b⁻¹) % c == 1`.

> [!info] How to compute `b⁻¹`
> - **Fermat's little theorem** (when `c` is prime): $b^{-1} \equiv b^{\,c-2} \pmod c$ — compute it with the modular [`power`](#fast--modular) above.
> - **Extended Euclid** (general, needs `gcd(b, c) = 1`): the `x` from `find_any_solution` for `b·x + c·y = 1`, normalized to `((x % c) + c) % c`.

---

## See also

- [[Number Theory]] — sieve of Eratosthenes, prime factorization, phi function
- [[Binary Exponentiation]]
- [[GCD and LCM]]
