import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
from matplotlib import gridspec
import h5py
from plot_result import plotting_param
filepath = "/home/ivan/Data/CA1_simulation/theta_nice.hdf5"
figfilepath = "/home/ivan/Data/CA1_simulation/figure_4.png"

firing4plot = ["pyr", "pvbas", "ca3_spatial", "mec"]
simtime = 600
npyr4preces = 6

gridspec_kw = {
    "width_ratios" : [0.1, 0.5, 0.5, 0.5, 0.5, 1],
}
# fig, axes = plt.subplots(nrows=14, ncols=6, gridspec_kw=gridspec_kw, constrained_layout=True)

fig = plt.figure(constrained_layout=True, figsize=(10, 10))

indicesofpyr = []
pyrfirsize = []

with h5py.File(filepath, 'r') as h5file:
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
    intracellular_group = h5file["intracellular/origin_data"]
    theta_signal = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/theta".format(plotting_param["number_pyr_layer"])][:]
    theta_phases = np.angle(hilbert(theta_signal))
    theta_phases[theta_phases < 0] += 2 * np.pi
    sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]


    gs1 = fig.add_gridspec(nrows=6, ncols=npyr4preces+1)  # , left=0.05, right=0.48, wspace=0.05

    for fir_idx, celltype in enumerate(firing4plot):
        if celltype.find("ca3") != -1:
            celltype_firings = raster_group["ca3"]
        else:
            celltype_firings = raster_group[celltype]

        firings_x = np.empty(0, dtype=np.float)
        firings_y = np.empty(0, dtype=np.float)

        for cell_idx, cell_number in enumerate(sorted(celltype_firings.keys(), key=lambda x: int(x.split("_")[-1]))):
            firings_x = np.append(firings_x, celltype_firings[cell_number][:])
            firings_y = np.append(firings_y, np.zeros(celltype_firings[cell_number].size) + cell_idx)

            pyrfirsize.append(celltype_firings[cell_number].size)
            indicesofpyr.append(cell_number)

        ax0 = fig.add_subplot(gs1[fir_idx, 0])
        ax0.set_xlim(0, 1)
        ax0.set_ylim(0, 1)
        ax0.axis('off')

        ax1 = fig.add_subplot(gs1[fir_idx, 1:])
        ax1.scatter(firings_x, firings_y, s=2, color=plotting_param["neuron_colors"][celltype])
        ax1.set_xlim(0, simtime)
        ax1.set_ylim(0, cell_idx+1)

        ax0.text(0, 0.5, celltype)

        if fir_idx == 0:
            ax1.set_title("Raster of spikes")
        if fir_idx == len(firing4plot)-1:
            ax1.set_xlabel("time, ms")

    pyrfirsort = np.argsort(pyrfirsize)
    indicesofpyr.append(cell_number)

    for pyr_idx in range(npyr4preces):
        ax1 = fig.add_subplot(gs1[len(firing4plot), pyr_idx+1])

        fir = raster_group["pyr"][ indicesofpyr[ pyrfirsort[pyr_idx] ] ][:]

        fir_phases = theta_phases[np.floor(fir*0.001*sampling_rate).astype(np.int)]
        ax1.scatter(fir, fir_phases)

        ax1.set_xlim(-1000, 1000)
        ax1.set_ylim(0, 2*np.pi)
        ax1.set_ylabel("theta phase")
        ax1.set_xlabel("time, ms")

        ax2 = fig.add_subplot(gs1[len(firing4plot)+1, pyr_idx + 1])

        t = np.linspace(-1, 1, 20)
        Vm = np.random.rand(t.size) # intracellular_group[ indicesofpyr[ pyrfirsort[pyr_idx] ] ][:]


        ax2.plot(t, Vm, color="red")
        ax2.set_ylabel("mV")
        ax2.set_xlabel("time, ms")



# fig.savefig(figfilepath)
plt.show()