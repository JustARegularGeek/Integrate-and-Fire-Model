from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

# Clear any objects from previous runs in the same session
start_scope()
# Use numpy for code generation to avoid C++ assertion errors on this system
prefs.codegen.target = 'numpy'

# Physical Model Parameters
tau = 30*ms               # Membrane time constant (τm)
v_reset = -65*mV          # Reset/Resting potential (EL = Vreset)
v_threshold = -50*mV      # Firing threshold (Vth)
R = 90*Mohm               # Membrane resistance (Rm)
I_e = 1*nA                # External injection current
v_start = -67*mV          # Initial membrane voltage
refractory_period = 2*ms  # Absolute refractory period duration

# Leaky Integrate-and-Fire Differential Equation
# (unless refractory): Forces v to stay at v_reset during the 2ms break
eqs = '''dv/dt = ( (v_reset - v) + R*I_e ) / tau : volt (unless refractory)'''

def run_simulation():
    # Create a group consisting of 1 neuron
    # method='exact': Since the EQ is linear, Brian2 solves it analytically
    G = NeuronGroup(1, eqs, threshold='v > v_threshold', reset='v = v_reset', refractory=refractory_period, method='exact')

    # Initialize voltage
    G.v = v_start

    spike_monitor = SpikeMonitor(G)    # Records timestamps of spikes
    state_monitor = StateMonitor(G, 'v', record=False)    # Records voltage of neuron index 0

    # Run the simulation for 1 second (1000ms)
    run(1000*ms)

    return spike_monitor, state_monitor

spike_monitor, state_monitor = run_simulation()

# Convert Brian2 units (seconds) to simple numpy floats (milliseconds)
spike_times = spike_monitor.t / ms 

if len(spike_times) > 0:
    # Time of the first spike event
    first_spike = spike_times[0]

    # Mean Inter-Spike Interval (ISI)
    if len(spike_times) > 1:
        isi_values = np.diff(spike_times)
        mean_isi = np.mean(isi_values)
    else:
        mean_isi = 0 

    # Total spike count over 1 second
    total_spikes = len(spike_times)

    print(f"--- Results for 1nA (Brian2) ---")
    print(f"1. First Spike: {first_spike:.2f} ms")
    print(f"2. Mean ISI:    {mean_isi:.2f} ms")
    print(f"3. Total Spikes: {total_spikes}")