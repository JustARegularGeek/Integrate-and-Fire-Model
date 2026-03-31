# Leaky Integrate-and-Fire (LIF) Neuron Model

This repository contains two implementations of the **Leaky Integrate-and-Fire (LIF)** neuron model, one of the most widely used models in computational neuroscience to study the relationship between input current and neuronal firing rates.

## What is this about?
The LIF model simulates the membrane potential ($V_m$) of a neuron. The neuron acts like a capacitor that "leaks" charge over time. When an input current ($I_e$) is applied, the voltage rises. If it hits a specific **Threshold**, the neuron "fires" a spike, resets to a lower voltage, and enters a brief **Refractory Period** where it cannot fire again.

### Physical Constants Used:
* **Membrane Time Constant ($\tau_m$):** 30 ms
* **Resting/Reset Potential ($E_L$):** -65 mV
* **Threshold Potential ($V_{th}$):** -50 mV
* **Membrane Resistance ($R_m$):** 90 MΩ
* **Refractory Period:** 2.0 ms

---

## Files in this Repository

### 1. `Integrate&Fire.py` (Manual Implementation)
This script uses the **analytical solution** of the LIF differential equation to calculate the voltage trace manually using NumPy.
* **How it works:** It uses the formula:
    $$V(t) = E_L + R_m I_e + (V(0) - E_L - R_m I_e) e^{-t/\tau_m}$$
* **Best for:** Understanding the raw math behind the physics without external simulators.

### 2. `Integrate&Fire_brian2.py` (Brian2 Implementation)
This script uses the **Brian2 simulator**, a industry-standard library for spiking neural networks.
* **How it works:** It defines the neuron using differential equations and uses Brian2’s `StateMonitor` and `SpikeMonitor` to track the simulation.
* **Best for:** Scalable simulations and verified numerical accuracy.

---

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install numpy matplotlib brian2
    ```
2.  **Run the simulations:**
    ```bash
    python Integrate\&Fire.py
    python Integrate\&Fire_brian2.py
    ```

---

## Results

### Membrane Potential Traces
The scripts generate voltage traces for various input currents (0.5nA to 2.0nA). You can observe the characteristic exponential rise of the membrane potential toward the threshold, followed by an instantaneous reset to the resting potential and a brief flat segment representing the absolute refractory period during which the neuron cannot fire again.

### Firing Rate (F-I Curve)
The simulation concludes by plotting the **Firing Rate (Hz) vs. Input Current (nA)**.
* **Rheobase:** Notice that at low currents (e.g., 0.5nA), the neuron may not fire at all because the "leak" is stronger than the input.
* **Frequency Coding:** As current increases, the Inter-Spike Interval (ISI) decreases, resulting in a higher firing frequency.