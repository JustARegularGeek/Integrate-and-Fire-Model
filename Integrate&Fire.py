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
    voltage_history = []
    time_history = []
    refractory_timer = REFRACTORY_PERIOD

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

        voltage_history.append(voltage)
        time_history.append(t)
        
        # Advance simulation time
        t += TIME_STEP

    return spikes, voltage_history, time_history

# Initialize the lists
current_values = []
risi_rates = []

print("=" * 72)
print(f"{'Current (nA)':>12} | {'1st Spike (ms)':>14} | {'Mean ISI (ms)':>13} | {'Rate (Hz)':>10} | {'Total':>6}")
print("=" * 72)

current = 0.5
while current < 2.5:
    
    spikes, voltage_history, time_history = run_simulation(current)
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
            mean_isi = 0.0
        
        # Store data for the graph
        current_values.append(current)
        risi_rates.append(rate)

        # Print clean table row
        print(f"{current:>12.1f} | {first_spike:>14.2f} | {mean_isi:>13.2f} | {rate:>10.2f} | {total_spikes:>6}")
    else:
        # Handle cases with no spikes
        current_values.append(current)
        risi_rates.append(0.0)
        print(f"{current:>12.1f} | {'No Spikes':>14} | {'---':>13} | {'---':>10} | {'0':>6}")

    plt.figure(figsize=(10, 4))
    plt.plot(time_history, voltage_history, color='darkslateblue', linewidth=1.5)
    
    # Add visual guides
    plt.axhline(THRESHOLD_VOLTAGE, color='darkred', linestyle='--', alpha=0.6, label='Threshold')
    plt.axhline(RESET_VOLTAGE, color='black', linestyle=':', alpha=0.4, label='Reset')
    
    plt.title(f'Membrane Potential Trace - Current: {current}nA')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(0, 200)    # Zoom in to see the spikes clearly
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)

    # Save the graphical representation as an image
    plt.savefig(f'spike_representation{current:.1f}nA.png')
    
    plt.show()    
    plt.close()    # Clears memory for the next loop

    current += 0.5

print("=" * 72)  # bottom border

# Graphical Representation
plt.figure(figsize=(8, 5))
plt.plot(current_values, risi_rates, 'o-', color='darkslateblue', linewidth=2, markersize=8)

plt.title('Firing Rate ($r_{ISI}$) vs. Constant Input Current')
plt.xlabel('Input Current ($I_e$) [nA]')
plt.ylabel('Firing Rate [Hz]')
plt.grid(True, linestyle=':', alpha=0.7)

# Save the graphical representation as an image
plt.savefig('firing_rate_analysis.png')

# Display the result
plt.show()