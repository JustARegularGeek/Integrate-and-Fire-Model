import numpy as np
import matplotlib.pyplot as plt

# Physical Constants
TIME_CONSTANT = 30      # Membrane time constant (τm) in ms
RESET_VOLTAGE = -65     # Reset/Resting potential (EL) in mV
THRESHOLD_VOLTAGE = -50 # Firing threshold (Vth) in mV
RESISTANCE = 90         # Membrane resistance (Rm) in MΩ
REFRACTORY_PERIOD = 2.0 # Refractory period in ms

# Simulation Parameters
TIME_STEP = 0.1         # Integration time step (dt) in ms
TOTAL_TIME = 1000       # Total simulation duration (1000 ms = 1 sec)
START_VOLTAGE = -67     # Initial membrane voltage

def calculate_voltage(time, voltage_0, current):
    """
    Analytical solution for the Leaky Integrate-and-Fire (LIF) model:
    V(t) = EL + Rm*Ie + (V(0) - EL - Rm*Ie) * exp(-t/τm)
    Units: time (ms), voltage_0 (mV), current (nA)
    """
    exponent = np.exp(-time/TIME_CONSTANT)
    voltage_t = RESET_VOLTAGE + RESISTANCE*current + (voltage_0 - RESET_VOLTAGE - RESISTANCE*current)*exponent

    return voltage_t

def run_simulation(current):

    # Initial State Variables
    t = 0
    spikes = []    # List to store the timestamp (ms) of each spike
    refractory_timer = 0    # Tracks elapsed time within the refractory period

    while t < TOTAL_TIME:

        # 1. Check if the neuron is currently in a refractory state
        if(refractory_timer < REFRACTORY_PERIOD):   #if refractory period did not pass, the membrane voltage is the resting membrane voltage
            voltage = RESET_VOLTAGE
            refractory_timer += TIME_STEP

        else:  
            # 2. Determine the time elapsed since the last 'active' state
            if len(spikes) == 0:   
                # Before the first spike, we calculate from t=0 
                voltage = START_VOLTAGE       
                charging_time = t   
            else:  
                # After a spike, we calculate time relative to when the refractory period ended
                voltage = RESET_VOLTAGE   # reset the voltage
                charging_time = t - (spikes[-1] + REFRACTORY_PERIOD)    # time since the previous spike

            # 3. Calculate current membrane potential using the analytical formula
            voltage = calculate_voltage(charging_time, voltage, current)  

            # 4. Check for threshold crossing (Spike detection)
            if voltage >= THRESHOLD_VOLTAGE:  # check if voltage has reached threshold
                spikes.append(t)    # Record the spike time
                refractory_timer = 0    # Enter refractory period immediately
                voltage = RESET_VOLTAGE    # Reset voltage for the next step
        
        # Advance simulation time
        t += TIME_STEP

    return spikes

# Initialize the lists
current_values = []
risi_rates = []

print("-" * 66)
print(f"{'Current (nA)':<15} | {'1st Spike (ms)':<15} | {'Rate (Hz)':<15} | {'Total spikes':<15}")
print("-" * 66)

current = 0.5
while current < 2.5:
    
    spikes = run_simulation(current)
     # Number of total spikes
    total_spikes = len(spikes)

    if total_spikes > 0:
        # Handle cases with spikes
        first_spike = spikes[0]
        
        # Calculate risi (Rate)
        if total_spikes > 1:
            mean_isi = np.mean(np.diff(spikes))
            rate = 1000.0 / mean_isi  # Convert ms to Hz
        else:
            rate = 0.0
        
        # Store data for the graph
        current_values.append(current)
        risi_rates.append(rate)

        # Print clean table row
        print(f"{current:<15.1f} | {first_spike:<15.2f} | {rate:<15.2f} | {total_spikes}")
    else:
        # Handle cases with no spikes
        current_values.append(current)
        risi_rates.append(0.0)
        print(f"{current:<15.1f} | {'No Spikes':<15} | {0.0:<15.2f} | {0}")

    current += 0.5

print("-" * 66)

# Graphical Representation
plt.figure(figsize=(8, 5))
plt.plot(current_values, risi_rates, 'o-', color='navy', linewidth=2, markersize=8)

plt.title('Firing Rate ($r_{ISI}$) vs. Constant Input Current')
plt.xlabel('Input Current ($I_e$) [nA]')
plt.ylabel('Firing Rate [Hz]')
plt.grid(True, linestyle=':', alpha=0.7)

# Save the graphical representation as an image
plt.savefig('firing_rate_analysis.png')

# Display the result
plt.show()