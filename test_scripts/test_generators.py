import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt

h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")


gen = h.ArtificialRhytmicCell()
gen.mu = np.pi
gen.latency = 1
gen.freqs = 5



firing = h.NetCon(gen, None)
fring_vector = h.Vector()
firing.record(fring_vector)

h.tstop = 1500

h.run()

fring_vector = np.asarray(fring_vector)
y = -np.ones_like(fring_vector)

t = np.linspace(0, 1500, 1000)
sine = np.cos(2 * np.pi * t * 0.005)



plt.scatter(fring_vector, y, s=1.5, color="red")
plt.plot(t, sine)
plt.show()






