# -*- coding: utf-8 -*-
"""Mathematically correct Copy of V. PAC therapy in a system with susceptible and antibiotic-resistant bacteria

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Lffknbp4TM_wbJkKVyqkrZxPYGDw2wdF
"""

############################################################
### V. PAC therapy in a system with susceptible and antibiotic-resistant bacteria - Helena Eycken, Margot Debruyne, Vincent Smets ###
############################################################
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define parameters
i = 10**(-6.21)              # Infection rate by phages
d = 0.10                     # Phage decay rate
b = 106                      # Burst size

γ = 0.23                     # Decay rate of antibiotics
Ca = 0                       # Initial antibiotic concentration
ka = 10**(5.4)               # Antibiotic killing constant
e = 1                        # Efficacy of antibiotics

K = 10**(7.94)               # Carrying capacity
rS = 1.85                    # Growth rate of sensitive bacteria
mA = 10**(-6.03)             # Mutation rate from S to A
mS = 10**(-6.03)             # Mutation rate from A to S
rA = 1.63                    # Growth rate of resistant bacteria

# Initial populations
S0 = 0.5*(10**(4.67))                       # Sensitive bacteria
A0 = 0.5*(10**(4.67))              # Resistant bacteria
P0 = 10**(6.27)              # Phage population
y0 = [Ca, S0, A0, P0]

# Antibiotic injection schedule
def antibiotic_input(t):
    """
    Defines the infusion schedule of the antibiotic:
    Every 12 hours, a 1-hour dose of ... is given.
    """
    injection_times = [100]
    dose = 6.61
    infusion_duration = 1

    for t_n in injection_times:
        if t_n <= t < (t_n + infusion_duration):
            return dose
    return 0

# Phage injection function
def phage_input(t):
    injection_times = [0]                # inject phages
    dose = 0                             # phage concentration
    infusion_duration = 1                # hours

    for t_n in injection_times:
        if t_n <= t < (t_n + infusion_duration):
            return dose
    return 0

def alpha(A, S): # variable fraction of antibiotic-resistant cells of total population
    total = A + S
    alpha = A / total
    return alpha if total > 0 else 0

def sigma(A, S): # variable fraction of susceptible cells of total population
    total = A + S
    sigma = S / total
    return sigma if total > 0 else 0

# Define the system of ODEs
def model(t, y, γ, e, ka, rS, K, mA, mS, rA, i, d, b):
    Ca, S, A, P = y  # Unpack variables

    # It is biologically unrealistic to have such low numbers, we set the limit to ... cells/ml (this is still not realistic, but otherwise the model will not work).
    #if S < 1e-10:
    #    S = 0
    #if P < 1e-10:
    #    P = 0
    #if C < 1e-10:
    #    C = 0
    σ = sigma(A, S)
    α = alpha(A, S)

    dCa_dt = -γ * Ca + antibiotic_input(t)  # Antibiotic decay + infusion
    dS_dt = rS * S * (1 - ((S + A) / K)) - (e * Ca * ka) - (i * S * σ * P) - (mA * S) + (mS * A)
    dA_dt = rA * A * (1 - ((S + A) / K)) - (i * A * α * P) + (mA * S) - (mS * A)
    dP_dt = b * i * P * (σ * S + α * A) - (d * P) + phage_input(t)  # Phage replication and decay + infusion

    return [dCa_dt, dS_dt, dA_dt, dP_dt]

# Time settings
t_end = 126
timesteps = 126
t_eval = np.linspace(0, t_end, timesteps)

# Solve the ODE system
# result = odeint(model, y0, t, args=(γ, e, ka, rS, K, mA, mS, rA, i, d, b))
result = solve_ivp(model, [0, timesteps], y0, args=(γ, e, ka, rS, K, mA, mS, rA, i, d, b), method='LSODA', t_eval=t_eval)

# Extract results
# C_concentration, S_population, A_population, P_population = result.T
C_concentration, S_population, A_population, P_population = result.y

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(result.t, C_concentration, label="Antibiotic Concentration (C)", color='green')
plt.plot(result.t, S_population, label="Sensitive Bacteria (S)", color='blue')
plt.plot(result.t, A_population, label="Resistant Bacteria (A)", color='red')
plt.plot(result.t, P_population, label="Phage Population (P)", color='purple')
plt.xlabel("Time (hours)")
plt.ylabel("Population (cells/ml or PFU/ml) or [antibiotic] (µg/ml)")
plt.yscale("log")  # Optional for better scale visibility
plt.legend()
plt.title("V. PAC therapy in a system with susceptible and antibiotic-resistant bacteria")
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.ylim(0, 10**(9))
plt.tight_layout()
plt.show()