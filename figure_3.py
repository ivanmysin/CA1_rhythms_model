import numpy as np
import matplotlib.pyplot as plt
import h5py
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
plt.rcParams.update(params)


from plot_result import plotting_param
from basic_parameters import get_basic_params

basic_params = get_basic_params()
filepath = basic_params["file_results"]
figfilepath = "./Results/figure_3.png"

gridspec_kw = {
    "width_ratios": [1, 0.2],
}
fig, axes = plt.subplots(nrows=10, ncols=2, gridspec_kw=gridspec_kw, constrained_layout=True, figsize=(20, 15))

for ax in axes[:, 1]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

tmin = 0
tmax = 3000

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]

    raw_lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_{}".format(plotting_param["number_pyr_layer"])][
              :]

    axes[0, 0].plot(t[:raw_lfp.size], raw_lfp, label="raw lfp")
    axes[0, 0].set_ylabel("mV")
    axes[0, 1].text(0, 0.5, "Raw LFP", fontsize="xx-large")


    intracellular_group = h5file["intracellular/origin_data"]

    axes_idx = 1
    for celltype_idx, celltype in enumerate(plotting_param["neuron_order"]):
        for neuron_number in intracellular_group.keys():
            if celltype == intracellular_group[neuron_number].attrs["celltype"]:
                Vm = intracellular_group[neuron_number][:]
                if np.sum(Vm[0:120000] > 0) == 0:
                    continue

                axes[axes_idx, 0].plot(t, Vm, label=celltype, color=plotting_param["neuron_colors"][celltype])
                axes[axes_idx, 1].text(0, 0.5, celltype, fontsize="xx-large")

                axes[axes_idx, 0].set_ylabel("mV")

                axes[axes_idx, 0].set_ylim(Vm.min()*1.2, 1.2*Vm.max())

                axes_idx += 1
                break

for ax in axes[:, 0]:
    ax.set_xlim(tmin, tmax)

axes[-1, 0].set_xlabel("time, ms", fontsize=16)

fig.savefig(figfilepath)
plt.show()