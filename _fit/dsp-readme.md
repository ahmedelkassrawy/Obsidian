Here is a clean, formatted version specifically designed for an Obsidian vault. I've added Obsidian callouts (`> [!info]`) and YAML frontmatter tags to keep your notes organized.

Markdown

````
# 🔍 Summary Checklist: Bandpass Filter Design with SciPy

> [!info] **Core Concept**
> The following 8 formulas are written explicitly in your code — **memorize them**. Everything else (Butterworth shape, $s \to z$ mapping, partial fractions, difference equation) is handled internally by SciPy — no need to recall the complex math.

### Key Parameters  
*   `btype='bandpass'` → SciPy outputs a bandpass filter.
*   `prototype_order = 2` → Starts with a 2nd‑order lowpass prototype, which naturally doubles into a 4th‑order bandpass filter.
*   `[w_low, w_high]` → Band edges of the target bandpass filter.

---

## 📐 The 8 Formulas to Memorize

### 1. Sampling Period
$$T_s = \frac{1}{f_s}$$
```python
Ts = 1.0 / fs
````

### 2. Analog Radian Frequency

$$\Omega = 2\pi f$$


```
w_low  = 2 * np.pi * f_low
w_high = 2 * np.pi * f_high
```

### 3. BPF Order → Prototype Order

$$N_{\text{prototype}} = \frac{N_{\text{BPF}}}{2}$$



```
prototype_order = total_order // 2
```

### 4. Magnitude in dB

$$|H|_{\text{dB}} = 20 \cdot \log_{10}\bigl(|H(e^{j\omega})|\bigr)$$


```
magnitude_db = 20 * np.log10(np.abs(h) + 1e-12)
```

### 5. Passband Normalization (peak = 0 dB)

$$b = \frac{b}{\max|H|_{\text{passband}}}$$



```
b_digital = b_digital / peak_gain
```

### 6. Stability Check

$$|p_k| < 1 \quad \text{for all poles } p_k$$


```
is_stable = all(np.abs(poles) < 1.0)
```

### 7. Unit Impulse Signal

$$\delta[n] = \begin{cases} 1 & n = 0 \\ 0 & \text{otherwise} \end{cases}$$



```
impulse = np.zeros(N)
impulse[0] = 1.0
```

### 8. Time Axis Conversion to Milliseconds

$$t[n] = n \cdot T_s \times 1000 \quad [\text{ms}]$$

```
time_ms = n * Ts * 1000
```

---

## 🧠 What SciPy Does For You (No Need to Memorize)

> [!abstract] **Black-Boxed Operations**
> 
> You don’t write the math for these steps — SciPy handles them automatically through its built-in functions.

**Internal Math Handled:**

- Butterworth lowpass prototype design.
    
- Impulse invariance $s \to z$ mapping.
    
- Partial fraction expansion.
    
- Difference equation derivation.
    

**Key SciPy Functions:**

- `butter()`
    
- `cont2discrete()`
    
- `tf2zpk()`
    
- `lfilter()`