import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

animal_velocity = 20 # cm / sec
track_len = 200 # cm

duration = track_len / animal_velocity
dt = 0.1
t = np.arange(0, duration, 0.001*dt)
place_ca3 = 105 / animal_velocity
place_mec = 100 / animal_velocity
w = 5

# print(duration)
# print(place_ca3)
# print(place_mec)



fi_ca3 = np.deg2rad(260)
fi_mec = np.deg2rad(100)
sigma = 21.2 / animal_velocity
sigma_inv = -0.5 / sigma**2
ca3_weight = 1.0
mec_weight = 1.0

theta_phases = 2*np.pi*t*w
theta_phases = theta_phases % (2*np.pi)
theta_phases[theta_phases >= np.pi] -= 2*np.pi




after_place_mec = np.ones_like(t)
after_place_ca3 = np.ones_like(t)
# after_place_ca3[t > place_ca3] = np.exp( 5.0 * (place_ca3-t[t > place_ca3]) )
# after_place_mec[t > place_mec] = np.exp( 5.0 * (place_mec-t[t > place_mec]) )

ca3 = np.exp( sigma_inv*(t - place_ca3)**2 ) * (np.cos(2*np.pi*t*(w+0.0) + fi_ca3) + 1)*after_place_ca3
mec = np.exp( sigma_inv*(t - place_mec)**2 ) * (np.cos(2*np.pi*t*(w+0.0) + fi_mec) + 1)*after_place_mec

tot_input = (ca3_weight * ca3 + mec_weight * mec)
tot_input = 15 * tot_input / np.max(tot_input) # np.zeros_like(tot_input) + 11 #



N = 1000

V = np.zeros(N, dtype=np.float)
tau = 50
th = np.zeros(N, dtype=np.float) + 20

neurons_indexes = np.arange(1, N+1)

firing_times = np.empty(0, dtype=np.float)
firing_index = np.empty(0, dtype=np.float)

Vhist = []
firing_phases = np.empty(0 , dtype=np.float)
for t_idx in range(t.size):
    
    V += dt * (-V + tot_input[t_idx] ) / tau + np.random.normal(0, 0.2, N)
    th += dt * (-th + 20) / tau 
    
    fired = V > th
    n_fired = np.sum(fired)
    if n_fired > 0:
        V[fired] = -10
        th[fired] += 10

        firing_times = np.append(firing_times, np.zeros(n_fired) + t[t_idx] )
        firing_index = np.append(firing_index, neurons_indexes[fired] )
        firing_phases = np.append(firing_phases, np.zeros(n_fired) + theta_phases[t_idx] )
    
    Vhist.append(V[0])
    
Vhist = np.asarray(Vhist)



fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

axes[0].plot(t, tot_input)
axes[1].scatter(firing_times, firing_index, s=0.5, color="red")
axes[1].plot(t, N*0.5*(np.cos(theta_phases)+1), color="blue")
axes[2].plot(t, Vhist, color="green")


fig, axes = plt.subplots(nrows=1, ncols=1)
position = firing_times * animal_velocity
for idx in neurons_indexes[:100]:

    neur = firing_index == idx

    axes.scatter(position[neur], firing_phases[neur], s=0.5)

# axes.plot( (np.cos(theta_phases)+1)*100, theta_phases)


axes.set_xlim(0, 200)
axes.set_ylim(-np.pi, np.pi)



plt.show()


