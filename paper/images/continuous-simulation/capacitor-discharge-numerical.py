import matplotlib.pyplot as plt
import numpy as np


def capacitor_discharge_analytical(V0, t, R, C):
    V = V0 * np.exp(-t / (R * C))
    return V


def capacitor_discharge_euler(V0, R, C, dt, t_end):
    num_steps = int(t_end / dt)
    t = np.linspace(0, t_end, num_steps + 1)
    V = np.zeros(num_steps + 1)
    V[0] = V0

    for i in range(num_steps):
        V[i + 1] = V[i] - (V[i] / (R * C)) * dt

    return t, V


V0 = 5
R = 1
C = 1
dt = 0.2
t_end = 1

t_euler, V_euler = capacitor_discharge_euler(V0, R, C, dt, t_end)

t_analytical = np.linspace(0, t_end, 100)
V_analytical = capacitor_discharge_analytical(V0, t_analytical, R, C)

plt.plot(t_analytical, V_analytical, label='Analytical')

plt.plot(t_euler[t_euler <= 0.61], V_euler[t_euler <= 0.61], 'o-', color='orange', label='Numerical (Euler)')
plt.plot(t_euler[t_euler >= 0.6], V_euler[t_euler >= 0.6], 'o:', color='orange')

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Capacitor Discharge')
plt.grid(True)
plt.legend()

plt.savefig('capacitor_discharge_plot.svg', format='svg')
