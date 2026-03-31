from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Clear any objects from previous runs in the same session
start_scope()
# Use numpy for code generation to avoid C++ assertion errors on this system
prefs.codegen.target = 'numpy'

# Physical Constants
TIME_CONSTANT = 30*ms      # Membrane time constant (τm)
RESET_VOLTAGE = -65*mV     # Reset/Resting potential (EL = Vreset)
THRESHOLD_VOLTAGE = -50*mV # Firing threshold (Vth)
RESISTANCE = 90*Mohm       # Membrane resistance (Rm)
REFRACTORY_PERIOD = 2*ms   # Absolute refractory period duration

# Simulation Parameters
TOTAL_TIME = 1000*ms       # Total simulation duration (1000 ms = 1 sec)
START_VOLTAGE = -67*mV     # Initial membrane voltage

def calculate_voltage(current):
    # Leaky Integrate-and-Fire Differential Equation
    # (unless refractory): Forces v to stay at RESET_VOLTAGE during the 2ms break
    voltage = '''dv/dt = ( (RESET_VOLTAGE - v) + RESISTANCE*current ) / TIME_CONSTANT : volt (unless refractory)'''

    return voltage

def run_simulation(current):

    start_scope()

    # Calculate current membrane potential using the analytical formula
    voltage = calculate_voltage(current)

    # Create a group consisting of 1 neuron
    # method='exact': Since the EQ is linear, Brian2 solves it analytically
    G = NeuronGroup(1, voltage, threshold='v > THRESHOLD_VOLTAGE', reset='v = RESET_VOLTAGE', refractory=REFRACTORY_PERIOD, method='exact')

    # Initialize voltage
    G.v = START_VOLTAGE

    spike_monitor = SpikeMonitor(G)    # Records timestamps of spikes
    state_monitor = StateMonitor(G, 'v', record=True)    #

    # Run the simulation for 1 second (1000ms)
    run(TOTAL_TIME)

    return spike_monitor, state_monitor

# Initialize the lists
current_values = []
risi_rates = []

print("=" * 72)
print(f"{'Current (nA)':>12} | {'1st Spike (ms)':>14} | {'Mean ISI (ms)':>13} | {'Rate (Hz)':>10} | {'Total':>6}")
print("=" * 72)

current = 0.5
while current < 2.5:
    
    # Run simulation and get the monitor
    spike_monitor, state_monitor = run_simulation(current*nA)
    
    # Convert to ms
    spike_times_ms = spike_monitor.t / ms
    # Number of total spikes
    total_spikes = len(spike_times_ms)

    if total_spikes > 0:
        # Handle cases with spikes
        first_spike = spike_times_ms[0]
        
        # Calculate risi (Rate)
        if total_spikes > 1:
            mean_isi = np.mean(np.diff(spike_times_ms)) 
            rate = 1000.0 / mean_isi    # Convert ms to Hz
        else:
            rate = 0.0
    
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
    plt.plot(state_monitor.t/ms, state_monitor.v[0]/mV, color='darkslateblue', linewidth=1.5)
    
    # Add visual guides
    plt.axhline(THRESHOLD_VOLTAGE/mV, color='darkred', linestyle='--', alpha=0.6, label='Threshold')
    plt.axhline(RESET_VOLTAGE/mV, color='black', linestyle=':', alpha=0.4, label='Reset')
    
    plt.title(f'Membrane Potential Trace - Current: {current}nA')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.xlim(0, 200)    # Zoom in to see the spikes clearly
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.2)

    # Save the graphical representation as an image
    plt.savefig(os.path.join(SCRIPT_DIR,f'spike_representation_brian2{current:.1f}nA.png'))
    
    plt.show()     
    plt.close()     # Clears memory for the next loop

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
plt.savefig(os.path.join(SCRIPT_DIR,'firing_rate_analysis_brian2.png'))

# Display the result
plt.show()