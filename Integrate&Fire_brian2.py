from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

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

    # Run the simulation for 1 second (1000ms)
    run(TOTAL_TIME)

    return spike_monitor

# Initialize the lists
current_values = []
risi_rates = []

print("-" * 66)
print(f"{'Current (nA)':<15} | {'1st Spike (ms)':<15} | {'Rate (Hz)':<15} | {'Total spikes':<15}")
print("-" * 66)

current = 0.5
while current < 2.5: # Use <= to include the 2.5 nA data point
    
    # Run simulation and get the monitor
    spike_monitor = run_simulation(current*nA)
    
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

        print(f"{current:<15.1f} | {first_spike:<15.2f} | {rate:<15.2f} | {total_spikes}")
    else:
        # Handle cases with no spikes
        current_values.append(current)
        risi_rates.append(0.0)
        print(f"{current:<15.1f} | {'No Spikes':<15} | {0.0:<15.2f} | {0}")

    current += 0.5

# Graphical Representation
plt.figure(figsize=(8, 5))
plt.plot(current_values, risi_rates, 'o-', color='navy', linewidth=2, markersize=8)

plt.title('Firing Rate ($r_{ISI}$) vs. Constant Input Current')
plt.xlabel('Input Current ($I_e$) [nA]')
plt.ylabel('Firing Rate [Hz]')
plt.grid(True, linestyle=':', alpha=0.7)

# Save the graphical representation as an image
plt.savefig('firing_rate_analysis_brian2.png')

# Display the result
plt.show()