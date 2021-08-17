import numpy as np
import h5py
import matplotlib.pyplot as plt
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
plt.rcParams.update(params)
from basic_parameters import get_basic_params

basic_params = get_basic_params()
filepath = basic_params["file_results"]


figfilepath = "./Results/figure_2.png"

fig, axes = plt.subplots(nrows=10, ncols=4, figsize=(20, 15), constrained_layout=True)

t0 = 0
t1 = 1000

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]
    for chan_idx in range(10):
        raw_lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_{}".format(chan_idx+1)][:]

        theta_band = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/theta".format(chan_idx+1)][:]
        slow_gamma_band = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow gamma".format(chan_idx+1)][:]
        middle_gamma_band = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/middle gamma".format(chan_idx+1)][:]
        fast_gamma_band = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/fast gamma".format(chan_idx+1)][:]

        ax = axes[9-chan_idx, :]

        ax[0].plot(t[:raw_lfp.size], raw_lfp)


        ax[1].plot(t[:raw_lfp.size], theta_band)
        ax[1].plot(t[:raw_lfp.size], slow_gamma_band)
        ax[1].set_ylim(-60, 60)


        ax[2].plot(t[:raw_lfp.size], theta_band)
        ax[2].plot(t[:raw_lfp.size], middle_gamma_band)
        ax[2].set_ylim(-60, 60)


        ax[3].plot(t[:raw_lfp.size], theta_band)
        ax[3].plot(t[:raw_lfp.size], fast_gamma_band)
        ax[3].set_ylim(-60, 60)



        if chan_idx == 9:
            ax[0].set_title("Raw LFP")
            ax[1].set_title("Slow gamma")
            ax[2].set_title("Middle gamma")
            ax[3].set_title("Fast gamma")


        for a in ax:
            a.set_xlim(t0, t1)
            a.set_ylabel("LFP, mV")

            if chan_idx > 0:
                a.set_xticks([])
            else:
                a.set_xlabel("time, ms")

fig.savefig(figfilepath)
plt.show()