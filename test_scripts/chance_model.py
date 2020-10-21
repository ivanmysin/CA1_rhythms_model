import numpy as np
import matplotlib.pyplot as plt


animal_velocity = 20 # cm / sec
track_len = 200 # cm

duration = track_len / animal_velocity
dt = 0.1
t = np.arange(0, duration, 0.001*dt)
place_ca3 = 90 / animal_velocity
place_mec = 110 / animal_velocity
w = 5

print(duration)
print(place_ca3)
print(place_mec)


"""
fi_ca3 = np.deg2rad(260)
fi_mec = np.deg2rad(100)
sigma = 21.2 / animal_velocity
sigma_inv = -0.5 / sigma**2
ca3_weight = 1.0
mec_weight = 1.0

theta_phases = 2*np.pi*t*w
theta_phases = theta_phases % (2*np.pi)
theta_phases[theta_phases > np.pi] = theta_phases[theta_phases > np.pi] - 2*np.pi


after_place = np.ones_like(t)
# after_place[t > place_ca3] = np.exp( 5*(place_ca3-t[t > place_ca3]) )

ca3 = np.exp( sigma_inv*(t - place_ca3)**2 ) * (np.cos(2*np.pi*t*w + fi_ca3) + 1)*after_place
mec = np.exp( sigma_inv*(t - place_mec)**2 ) * (np.cos(2*np.pi*t*w + fi_mec) + 1)*after_place

tot_input = (ca3_weight * ca3 + mec_weight * mec)
tot_input = 70 * tot_input / np.max(tot_input)

# plt.plot(t, tot_input)
# plt.show()


N = 100

V = np.zeros(N, dtype=np.float)
tau = 50
th = np.zeros(N, dtype=np.float) + 20


firing = np.empty(0 , dtype=np.float)
Vhist = []
firing_phases = np.empty(0 , dtype=np.float)
for t_idx in range(t.size):
    
    V += dt * (-V + tot_input[t_idx] + np.random.normal(0, 5, N)) / tau 
    th += dt * (-th + 20) / tau 
    
    fired = V > th
    V[fired] = -10
    th[fired] += 5
    
    firing = np.append(firing, np.zeros(np.sum(fired)) + t[t_idx] )
    firing_phases = np.append(firing_phases, np.zeros(np.sum(fired)) + theta_phases[t_idx] )
    
    Vhist.append(V[0])
    
Vhist = np.asarray(Vhist)
firing = np.asarray(firing)
firing_phases = np.asarray(firing_phases)


fig, axes = plt.subplots(nrows=3, ncols=1)

axes[0].plot(t, tot_input)

axes[1].scatter(firing, np.zeros_like(firing), s=2, color="red")
axes[1].plot(t, np.cos(2*np.pi*w*t), color="blue")

axes[2].plot(t, Vhist, color="green")

fig, axes = plt.subplots(nrows=1, ncols=1)

position = firing * animal_velocity
axes.scatter(position, firing_phases, s=1)
axes.set_xlim(0, 200)



plt.show()

"""
