import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import sys
from copy import deepcopy

sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import basic_params
from time import time



###### parameters block ############
dur = 5000
Ngens = 500
Rtheta = 0.4
Rgamma = 0.6
#####################################

RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")


generators = []
firings = []
spike_times_vecs = []
places = np.flip( np.linspace(0, dur, Ngens) )

for idx in range(Ngens):
	theta_kappa, theta_i0 = prelib.r2kappa(Rtheta)
	gamma_kappa, gamma_i0 = prelib.r2kappa(Rgamma)

	gen = h.ArtificialRhytmicPlaceCell()
	gen.delta_t = 0.5

	gen.spike_rate = 100000
	gen.place_center_t = places[idx]
	gen.place_t_radius = 1000
	gen.latency = 10

	gen.low_kappa = theta_kappa
	gen.low_I0 = theta_i0
	gen.high_kappa = gamma_kappa
	gen.high_I0 = gamma_i0




	firing = h.NetCon(gen, None)
	fring_vector = h.Vector()
	
	firing.record(fring_vector)
	
	
	generators.append(gen)
	firings.append(firing)
	spike_times_vecs.append(fring_vector)

h.tstop = dur
h.run()

fig, ax = plt.subplots()
for idx in range(Ngens):
	
	t = np.asarray( spike_times_vecs[idx] )

	print(t.size)

	fir = np.zeros_like(t) + idx + 1
	ax.scatter(t, fir, color="blue", s=0.5)

plt.show()















