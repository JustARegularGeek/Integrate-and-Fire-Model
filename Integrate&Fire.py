import numpy as np

T = 30    # τm = 30 ms
V_RESET = -65    # EL = Vreset = −65 mV
V_THRESHOLD = -50     # Vth = −50 mV
R = 90    # Rm = 90 MΩ

# Simulation parameters
TIME_STEP = 0.1    # Time step (ms)
TOTAL_TIME = 1000    # 1 sec = 1000 ms
T_REFRACTORY = 2.0    # Refractory period (2ms)

def calculate_voltage(time, voltage_0, current):
    """
    Calculates the membrane potential V(t) at time t.
    Units: time (ms), voltage_0 (mV), current (nA)
    V(t) = EL + Rm*Ie + (V(0) − EL − Rm*Ie)*exp(−t/τm)
    """

    exponent = np.exp(-time/T)
    voltage_t = V_RESET + R*current + (voltage_0 - V_RESET - R*current)*exponent

    return voltage_t

def run_simulation():

    # Initial state
    t = 0
    spikes = []    #store the time of each spike
    refractory_timer = 0    # how much time has passed since the previous spike
    current = 1    # Initian current (nA)

    while t < TOTAL_TIME:

        if(refractory_timer < T_REFRACTORY):   #if refractory period did not pass, the membrane voltage is the resting membrane voltage
            voltage = V_RESET
            refractory_timer += TIME_STEP

        else:   # if refractory period has passed, reset the timer and find the new membrane voltage
            if len(spikes) == 0:    # no spike was initiated yet
                voltage = -67   # initial voltage is set to -67mv
                charging_time = t   
            else:  
                voltage = V_RESET   # reset the voltage
                charging_time = t - (spikes[-1] + T_REFRACTORY)    # time since the previous spike

            voltage = calculate_voltage(charging_time, voltage, current)  

            if voltage >= V_THRESHOLD:  # check if voltage has reached threshold
                spikes.append(t)    # add the time of the current spike to spikes list
                refractory_timer = 0    # reset the refractory timer
                voltage = V_RESET   # reset the voltage
        
        t += TIME_STEP

    return spikes


# Run the simulation for 1nA
test_spikes = run_simulation()

if len(test_spikes) > 0:
    # Question 1: First spike time
    first_spike = test_spikes[0]
    
    # Question 2: Mean ISI
    # We calculate the difference between each spike time
    isi_values = np.diff(test_spikes)
    mean_isi = np.mean(isi_values)
    
    # Question 3: Total spikes
    total_spikes = len(test_spikes)

    print(f"--- Results for 1nA ---")
    print(f"1. First Spike: {first_spike:.2f} ms")
    print(f"2. Mean ISI:    {mean_isi:.2f} ms")
    print(f"3. Total Spikes: {total_spikes}")