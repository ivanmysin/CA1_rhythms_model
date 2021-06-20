
import numpy as np
import matplotlib.pyplot as plt
from presimulation_lib import r2kappa
x_pyr = 5000
ca3_x = np.arange(0, 10000, 3)
mec_x = np.arange(0, 10000, 3)
pvbas_x = np.arange(0, 10000, 50)
var_conns_on_pyr = 9000


# print(ca3_x)

ca32pyr = np.exp(-0.5*(x_pyr - ca3_x)**2 / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))
pvbas2pyr = np.exp(-0.5* ((x_pyr - pvbas_x + 0.000001)**-2) / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))


kappa , i0 = r2kappa(0.9)
mec2pyr = np.exp(kappa * np.cos(2*np.pi*0.1*0.001*(x_pyr-mec_x-500) )  )



mec2pyr = 0.5 * mec2pyr  / np.max(mec2pyr)
ca32pyr = ca32pyr  / np.max(ca32pyr)
pvbas2pyr = 0.1 * pvbas2pyr  / np.max(pvbas2pyr)

fig, axes = plt.subplots(nrows=2, ncols=1)

axes[0].plot(ca3_x, ca32pyr, color="orange", label="ca3")
axes[0].plot(mec_x, mec2pyr, color="red", label="mec")
axes[0].plot(pvbas_x, pvbas2pyr, color="blue", label="pvbas")
axes[0].set_xlim(0, 10000)
axes[0].set_ylim(0, 1)
axes[0].set_ylabel("Relative weight of connections")
axes[0].set_xlabel("Time of pyramidal neuron, ms")
axes[0].legend()
plt.show()



