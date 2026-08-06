# Bits, Bitwise & Bitmasks

> A gentle, explain-it-like-I'm-6 walkthrough — with all my code snippets kept.

---

## 1. What is a bit? 🧱

Imagine every number is made of tiny **light switches** in a row.
Each switch can only be **ON (1)** or **OFF (0)**. That's a **bit**.

The computer doesn't count with 10 fingers like us. It counts with these switches — that's called **binary** (base 2).

- `5` is really `101` → 💡⬛💡 (on, off, on)
- `7` is really `111` → 💡💡💡 (all on)
- `3` is really `011` → ⬛💡💡 (off, on, on)

The switches are numbered from the **right side**, starting at **0**:

```
bit number:  ... 3   2   1   0
number 5  =        1   0   1
                (bit2) (bit1) (bit0)
```

### Turning any number into its switches (binary)

This little helper walks a number and writes down each switch:

```c++
vector<int> getbinary(long long n,long long base)
{
	vector<int> v;
	
	while(n)
	{
		v.push_back(n % base);   // grab the last switch
		n /= base;               // throw it away, look at the next
	}
	
	reverse(v.begin(),v.end());  // we collected them backwards, so flip
	return v;
}
```

**Why it works:** `n % 2` tells you if the last switch is on or off. `n / 2` slides everything one switch to the right so you can look at the next one. You keep going until nothing is left.

---

## 2. The magic buttons (bitwise operators) 🎛️

These are special buttons that work on **all the switches at once**.

| Button | Name        | What it does (for a 6-year-old)            |
| ------ | ----------- | ------------------------------------------ |
| `&`    | AND         | Keeps a switch ON only if **both** were ON |
| ` \| ` | OR          | Turns a switch ON if **either** was ON     |
| `^`    | XOR         | ON only if the two are **different**       |
| `~`    | NOT         | Flips **every** switch (on↔off)            |
| `<<`   | Left shift  | Push all switches to the **left**          |
| `>>`   | Right shift | Push all switches to the **right**         |

> ⚠️ Careful: `&&` and `||` (doubles) are the "yes/no" logic buttons — **not** the switch buttons. Use single `&` and `|` for bits.

### The shifting trick 🚂

- **Shift left** `x << 1` = add a `0` at the end = **multiply by 2**
- **Shift right** `x >> 1` = remove the last switch = **divide by 2**

So `1 << k` means "put a single ON switch at position `k`" — that's exactly the number **2 to the power k**.

### Big-number safety belt 🦺

If you shift a lot (like 60 switches), a normal number is too small and it **breaks (overflow)**. Use the long-long `1` so the box is big enough:

```c++
1LL << 60   // safe for big shifts
```

And a tiny gotcha with brackets — the computer does `-1` before `<<` if you're not careful:

```c++
// WRONG: (1 << k - 1)
// RIGHT: (1 << k) - 1   ← always add the brackets!
```

---

## 3. Silly-but-true switch facts 🪄

These are always true, like "1 + 0 = 1". Handy shortcuts:

```
A & 1 = A         (AND with a lone 1 keeps A's last switch)
A | 0 = A         (OR with 0 changes nothing)
A ^ 0 = A         (XOR with 0 changes nothing)
A ^ 1 = 1 - A     (XOR with 1 flips it)
A ^ A = 0         (anything XOR itself cancels out to zero)
```

That last one (`A ^ A = 0`) is super famous — it's how you find the "odd one out" in puzzles.

---

## 4. Playing with a single switch 🔦

### Is the number odd or even?

The **last switch (bit 0)** tells you everything:
- last switch ON → odd
- last switch OFF → even

```c++
void checkparity(long long n)
{
	cout << ((n & 1) ? "odd" : "even");
}
```

**Why:** `n & 1` only looks at the very last switch. If it's a 1, the number is odd.

### Is switch number `i` ON? (check a bit)

Slide the switch you care about down to the last spot, then peek:

```c++
bool checkbit(long long n,long long i)
{
	return (n >> i) & 1;
}
```

### Flip switch number `bit` (toggle)

XOR with a single ON switch flips it — on becomes off, off becomes on:

```c++
long long togglebit(long long n,long long bit)
{
	return (n ^ (1ll << bit));
}
```

### Turn switch `bit` ON (set)

OR with a single ON switch — if it was already on, it stays on:

```c++
long long setbit(long long n, long long bit)
{
	return (n | (1ll << bit));
}
```

### Turn switch `bit` OFF (clear)

Make a mask that is "all ON **except** the one switch" (`~(1 << bit)`), then AND. Everything survives except the switch we zapped:

```c++
long long clearbit(long long n,long long bit)
{
	return (n & (~(1ll << bit)));
}
```

---

## 5. Is a number a power of 2? 🎯

A power of 2 (like 1, 2, 4, 8, 16...) has **exactly one switch ON**.
`__builtin_popcountll` is a magic helper that **counts the ON switches**. If the count is 1 → it's a power of 2.

```c++
long long pow2(long long n)
{
    return ((__builtin_popcountll(n)) == 1); // only one bit is 1 → power of 2
}
```

---

## 6. Looking at one column of switches across many numbers 🧮

Sometimes you have a whole list of numbers and you ask:
*"For switch position `bit`, how many numbers have it ON?"*

You just walk the list and check that one switch each time:

```C++
for (int bit = 30; bit >= 0; bit--)
{
	 int cost = 0;
	 
	 for (int i = 0; i < n; i++)
	 {
		if ((arr[i] & (1 << bit)) == 0) cost++;   // this one is OFF here
	 }
}
```

---

## 7. Prefix bits: counting ON switches super fast ⚡

Idea: for **each switch column**, keep a running total ("how many ON switches so far") so you can answer *any* range question instantly.

Think of it like a scoreboard that only ever adds up.

```C++
#include <iostream>
#include <vector>
using namespace std;
 
int main() 
{
    int n;
    cin >> n;

    vector<long long> v(n + 1);
    vector<vector<long long>> prefixBits(64, vector<long long>(n + 1));

    for (int i = 1; i <= n; i++) 
    {
        cin >> v[i];
    }

    // Build the scoreboard: for every switch (0..63), add up ON switches as we go
    for (int bit = 0; bit < 64; bit++) 
    {
        for (int i = 1; i <= n; i++) 
        {
            prefixBits[bit][i] = prefixBits[bit][i - 1] + ((v[i] >> bit) & 1);
        }
    }

    int q;
    cin >> q;

    while (q--) 
    {
        int l, r;
        cin >> l >> r; //1 indexed

        // OR of the range: a switch is ON if AT LEAST ONE number has it ON
        long long OR = 0;
        for (int bit = 0; bit < 64; bit++) 
        {
            int cnt = prefixBits[bit][r] - prefixBits[bit][l - 1];
            
            if (cnt)
            {
                OR += (1LL << bit);
            }
        }
        cout << OR << endl;

        // AND of the range: a switch is ON only if EVERY number has it ON
        long long AND = 0;
        for (int bit = 0; bit < 64; bit++)
        {
            int cnt = prefixBits[bit][r] - prefixBits[bit][l - 1];

            if (cnt == r - l + 1)   // all of them had it ON
            {
                AND += (1LL << bit);
            }
        }
        cout << AND << endl;
    }

    return 0;
}
```

### Why this works — a picture 🖼️

```
// arr = [0 , 5 , 7 , 3]   // arr 1-indexed
//
// 5 --> 101
// 7 --> 111
// 3 --> 011
//
// (2)power of 0 --> [0 , 1 , 2 , 3]
//   why? every number had a 1 in the last spot,
//   so the running total climbs 0,1,2,3
//
// 2 power of 1 --> [0, 0 , 1 , 2]
//   why? the 5 does NOT have a 1 in the 2nd spot,
//   so the total doesn't grow there
```

- **OR over a range** = "was this switch ON in *anyone*?" → count > 0.
- **AND over a range** = "was this switch ON in *everyone*?" → count equals how many numbers are in the range (`r - l + 1`).

---

## 8. A neat XOR trick from 0 to n ➕

XOR from `0` up to `n` has a repeating pattern every 4 numbers (because `A ^ A = 0` keeps cancelling pairs). This little loop backs up until it hits a clean stopping point:

```c++
long long XOR(long long n)
{
    long long ans = 0;

    for (long long i = n;; i--)
    {
        if (i % 4 == 3) break;   // clean stopping point
        ans = ans ^ i;
    }

    return ans;
}
```

---

## 9. Bitmask: using switches to pick a team 👥

Here's the big idea the whole page is named after.

A **bitmask** is just a number whose switches mean *"is this thing chosen or not?"*
- switch `i` ON → item `i` is **on the team**
- switch `i` OFF → item `i` is **left out**

If you have `n` items, the numbers from `0` to `2^n - 1` list **every possible team** — no team is ever missed!

```C++
for(int mask = 0; mask < (1 << n); mask++)
{
    int mn = 2e9, mx = 0, cnt = 0, sum = 0;
    for(int i = 0; i < n; i++)
    {
        if(mask & (1 << i))          // is item i on THIS team?
        {
            cnt++;                    // count the team members
            sum += arr[i];            // add up their values
            mn = min(mn, arr[i]);     // smallest on the team
            mx = max(mx, arr[i]);     // biggest on the team
        }
    }
    // ...now do something with this team (cnt, sum, mn, mx)
}
```

**How to read it like a story:**
1. The outer loop `mask` counts through **every possible team** (0 up to 2ⁿ−1).
2. The inner loop asks each item: *"switch `i` — are you ON in this mask?"* using `mask & (1 << i)`.
3. If yes, that item joins the team and we tally it up.

That's the superpower of bitmasks: **one number holds a whole yes/no team**, and counting from `0` upward tries every combination for free. 🎉

---

### 🧠 Cheat-sheet (stick this on the wall)

| I want to… | Spell |
|---|---|
| Check bit `i` | `(n >> i) & 1` |
| Set bit `i` ON | `n \| (1LL << i)` |
| Clear bit `i` OFF | `n & ~(1LL << i)` |
| Flip bit `i` | `n ^ (1LL << i)` |
| Is odd? | `n & 1` |
| Multiply by 2 | `n << 1` |
| Divide by 2 | `n >> 1` |
| Count ON switches | `__builtin_popcountll(n)` |
| Loop all teams of n items | `for (mask = 0; mask < (1 << n); mask++)` |
| Big-shift safety | use `1LL << k` |
