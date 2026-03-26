import numpy as np

# Physical Constants (Constants as defined in the assignment)
T = 30            # Membrane time constant (τm) in ms
V_RESET = -65     # Reset/Resting potential (EL) in mV
V_THRESHOLD = -50 # Firing threshold (Vth) in mV
R = 90            # Membrane resistance (Rm) in MΩ

# Simulation Parameters
TIME_STEP = 0.1       # Integration time step (dt) in ms
TOTAL_TIME = 1000     # Total simulation duration (1000 ms = 1 sec)
T_REFRACTORY = 2.0    # Refractory period in ms
V_START = -67         # Initial membrane voltage

def calculate_voltage(time, voltage_0, current):
    """
    Analytical solution for the Leaky Integrate-and-Fire (LIF) model:
    V(t) = EL + Rm*Ie + (V(0) - EL - Rm*Ie) * exp(-t/τm)
    Units: time (ms), voltage_0 (mV), current (nA)
    """
    exponent = np.exp(-time/T)
    voltage_t = V_RESET + R*current + (voltage_0 - V_RESET - R*current)*exponent

    return voltage_t

def run_simulation(current):

    # Initial State Variables
    t = 0
    spikes = []    # List to store the timestamp (ms) of each spike
    refractory_timer = 0    # Tracks elapsed time within the refractory period

    while t < TOTAL_TIME:

        # 1. Check if the neuron is currently in a refractory state
        if(refractory_timer < T_REFRACTORY):   #if refractory period did not pass, the membrane voltage is the resting membrane voltage
            voltage = V_RESET
            refractory_timer += TIME_STEP

        else:  
            # 2. Determine the time elapsed since the last 'active' state
            if len(spikes) == 0:   
                # Before the first spike, we calculate from t=0 
                voltage = V_START       
                charging_time = t   
            else:  
                # After a spike, we calculate time relative to when the refractory period ended
                voltage = V_RESET   # reset the voltage
                charging_time = t - (spikes[-1] + T_REFRACTORY)    # time since the previous spike

            # 3. Calculate current membrane potential using the analytical formula
            voltage = calculate_voltage(charging_time, voltage, current)  

            # 4. Check for threshold crossing (Spike detection)
            if voltage >= V_THRESHOLD:  # check if voltage has reached threshold
                spikes.append(t)    # Record the spike time
                refractory_timer = 0    # Enter refractory period immediately
                voltage = V_RESET    # Reset voltage for the next step
        
        # Advance simulation time
        t += TIME_STEP

    return spikes

current = 0.5
while(current < 2.5):
    # Run the simulation for 1nA
    test_spikes = run_simulation(current)

    if len(test_spikes) > 0:
        # Time of the first spike event
        first_spike = test_spikes[0]
        
        # Mean Inter-Spike Interval (ISI)
        isi_values = np.diff(test_spikes)
        mean_isi = np.mean(isi_values)
        
        # Total spike count over 1 second
        total_spikes = len(test_spikes)

        print(f"--- Results for {current:.1f}nA ---")
        print(f"1. First Spike: {first_spike:.2f} ms")
        print(f"2. Mean ISI:    {mean_isi:.2f} ms")
        print(f"3. Total Spikes: {total_spikes}")

    current += 0.5    # Increase current by 0.5nA