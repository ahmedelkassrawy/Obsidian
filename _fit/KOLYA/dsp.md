### **Design Report: 4th-Order Butterworth Bandpass Digital Filter**

#### **1. Specifications Summary**

- **Filter Type:** Bandpass Filter (BPF)
    
- **Prototype:** Butterworth
    
- **Lower Cut-off Frequency ($f_l$):** 1 kHz
    
- **Upper Cut-off Frequency ($f_h$):** 4 kHz
    
- **Sampling Rate ($f_s$):** 20050 Hz
    
- **Filter Order:** 4th order (requires a 2nd-order analog lowpass prototype)
    
- **Design Technique:** Impulse Invariance Method
    

#### **2. Design Methodology: The Impulse Invariance Method**

Because the Bilinear Transformation (BLT) method was excluded, the **Impulse Invariance Method** serves as the standard alternative for designing Infinite Impulse Response (IIR) digital filters.

This technique ensures that the impulse response of the digital filter is a directly sampled version of the continuous-time analog filter's impulse response:

$$h[n] = T_s h_a(nT_s)$$

where $T_s = \frac{1}{f_s}$ is the sampling period.

**Design Steps:**

1. **Analog Frequencies:** Unlike the Bilinear Transform, there is no frequency warping in the Impulse Invariance method. The analog cutoff frequencies are linearly related to the digital specifications: $\Omega_c = 2\pi f_c$.
    
2. **Analog Prototype Generation:** A 2nd-order continuous-time lowpass Butterworth filter is designed. When transformed into a bandpass filter, the order doubles, yielding the required 4th-order filter.
    
3. **Lowpass-to-Bandpass Transformation:** The analog lowpass filter $H_{LP}(s)$ is converted to an analog bandpass filter $H_{BP}(s)$ using standard s-domain substitutions based on the center frequency and bandwidth.
    
4. **s-to-z Mapping:** Partial fraction expansion is performed on $H_{BP}(s)$. Every pole in the s-domain ($s_k$) is mapped to a pole in the z-domain using the relationship:
    
    $$\frac{1}{s - s_k} \implies \frac{1}{1 - e^{s_k T_s} z^{-1}}$$
    

### **A Note on Aliasing**

The Impulse Invariance method has one main problem called **aliasing**. Here is what that means in simple terms:

When we convert the analog filter into a digital one, the filter's frequency pattern starts repeating itself over and over. Because of this, we have a strict limit called the **Nyquist frequency**, which is exactly half of our sampling rate (10,025 Hz).

If the filter doesn't successfully block out signals above this 10,025 Hz limit, those extra high frequencies will "fold" or leak back into the lower frequencies we actually want to keep. This unwanted leakage is aliasing.

Luckily, our filter stops passing signals at 4 kHz. This leaves a large, safe gap between our 4 kHz cut-off and the 10,025 Hz limit. Because of this big gap, this method works very well for our design. While a tiny bit of aliasing is mathematically impossible to avoid completely, it is so small that it will not cause any problems here.

#### **4. Filter Response Analysis**

**1. Transfer Characteristics: Magnitude Response**

- **Passband:** The magnitude response shows a flat passband between 1 kHz and 4 kHz. This "maximally flat" characteristic is the defining feature of the Butterworth prototype.
    
- **Stopband & Roll-off:** Because it is a 4th-order filter (meaning a 2nd-order analog lowpass was transformed), the roll-off is smooth but relatively moderate. It decays at a rate of roughly -24 dB/octave on the high-frequency side.
    
- **Aliasing Check:** At the Nyquist frequency (10,025 Hz), the magnitude is significantly attenuated (well below -40 dB). Because the Impulse Invariance Method suffers from aliasing, this high attenuation at $f_s/2$ confirms that the method is valid for these specific cut-off frequencies.
    

**2. Transfer Characteristics: Phase Response**

- **Linearity:** The phase response is notably non-linear, smoothly transitioning from positive to negative phase angles near the lower (1 kHz) and upper (4 kHz) cut-off frequencies.
    
- **Group Delay:** This non-linearity implies that different frequency components within the passband will experience slightly different time delays passing through the filter. For audio applications, this is generally acceptable, but for precise data transmission, it might cause phase distortion.
    

**3. Time-Domain Characteristics: Impulse Response ($h[n]$)**

- **Shape:** The impulse response exhibits a damped oscillatory behavior, typical of an Infinite Impulse Response (IIR) bandpass filter.
    
- **Frequency of Oscillation:** The ringing oscillates primarily at the geometric center frequency of the passband ($f_c \approx 2$ kHz).
    
- **Decay:** The envelope of the oscillation decays exponentially toward zero. The speed of this decay is inversely proportional to the filter's bandwidth (3 kHz). Because the bandwidth is relatively wide, the impulse response settles to zero very quickly (within a few milliseconds).

 **4. Pole-Zero Map and Stability**

- **Proof of Stability:** The Pole-Zero map plots the roots of the filter's transfer function in the z-plane. For a digital IIR filter to be strictly stable, all of its poles must be located inside the unit circle (where the magnitude $|z| < 1$). As shown in the generated Pole-Zero plot, all 4 poles (marked with 'x') fall well within the boundary of the unit circle. This confirms that the Impulse Invariance transformation was successful and the resulting digital filter is completely stable.

![[Images/Pasted image 20260518194111.png]]