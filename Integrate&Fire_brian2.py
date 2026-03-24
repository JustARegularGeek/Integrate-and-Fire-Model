from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

start_scope()
prefs.codegen.target = 'numpy'

tau = 30*ms
v_reset = -65*mV
v_threshold = -50*mV
R = 90*Mohm
I_e = 1*nA
v_start = -67*mV
refractory_period = 2*ms

eqs = '''dv/dt = ( (v_reset - v) + R*I_e ) / tau : volt (unless refractory)'''

def run_simulation():
    G = NeuronGroup(1, eqs, threshold='v > v_threshold', reset='v = v_reset', refractory=refractory_period, method='exact')
    spike_monitor = SpikeMonitor(G)
    G.v = v_start
    state_monitor = StateMonitor(G, 'v', record=False)

    run(1000*ms)

    return spike_monitor, state_monitor

spike_monitor, state_monitor = run_simulation()

spike_times = spike_monitor.t / ms 

if len(spike_times) > 0:
    first_spike = spike_times[0]

    if len(spike_times) > 1:
        isi_values = np.diff(spike_times)
        mean_isi = np.mean(isi_values)
    else:
        mean_isi = 0 

    total_spikes = len(spike_times)

    print(f"--- Results for 1nA (Brian2) ---")
    print(f"1. First Spike: {first_spike:.2f} ms")
    print(f"2. Mean ISI:    {mean_isi:.2f} ms")
    print(f"3. Total Spikes: {total_spikes}")