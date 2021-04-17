import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
plt.rcParams.update(params)


# from matplotlib import gridspec
import h5py
from plot_result import plotting_param
filepath = "/home/ivan/Data/CA1_simulation/test_10000.hdf5"   # theta_state_full_cells
figfilepath = "/home/ivan/Data/CA1_simulation/figure_5.png"

firing4plot = ["pyr", "pvbas", "ca3_spatial", "mec"]
simtime = 10000
npyr4preces = 3
intracell_pyr_neuron = "neuron_12110"


gridspec_kw = {
    "width_ratios" : [0.01, 0.5, 0.5, 0.5, 0.5, 1],
}
# fig, axes = plt.subplots(nrows=14, ncols=6, gridspec_kw=gridspec_kw, constrained_layout=True)
pyr_dx = 3
Npyr = 9000
fig = plt.figure(constrained_layout=True, figsize=(15, 15))
pyr_coords = np.cumsum( np.zeros(Npyr) + pyr_dx )
pyr_coords[pyr_coords.size//2:] = np.nan

place_centers = []
indicesofpyr = []
pyrfirsize = []

with h5py.File(filepath, 'r') as h5file:
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
    intracellular_group = h5file["intracellular/origin_data"]
    theta_signal = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/theta".format(plotting_param["number_pyr_layer"])][:]
    theta_phases = np.angle(hilbert(theta_signal))
    # theta_phases[theta_phases < 0] += 2 * np.pi
    sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]


    gs1 = fig.add_gridspec(nrows=5, ncols=npyr4preces+1)  # , left=0.05, right=0.48, wspace=0.05

    for fir_idx, celltype in enumerate(firing4plot):

        celltype_firings = raster_group[celltype]

        firings_x = np.empty(0, dtype=np.float)
        firings_y = np.empty(0, dtype=np.float)

        for cell_idx, cell_number in enumerate(sorted(celltype_firings.keys(), key=lambda x: int(x.split("_")[-1]))):
            firings_x = np.append(firings_x, celltype_firings[cell_number][:])
            firings_y = np.append(firings_y, np.zeros(celltype_firings[cell_number].size) + cell_idx)

            if celltype == "pyr" and cell_idx < 3500: # and cell_idx > 100
                pyrfirsize.append(celltype_firings[cell_number].size)
                indicesofpyr.append(cell_number)
                place_centers.append(pyr_coords[cell_idx])

                if cell_number == intracell_pyr_neuron:
                    intracell_center = pyr_coords[cell_idx]

        ax0 = fig.add_subplot(gs1[fir_idx, 0])
        ax0.set_xlim(0, 1)
        ax0.set_ylim(0, 1)
        ax0.axis('off')

        ax1 = fig.add_subplot(gs1[fir_idx, 1:])
        ax1.scatter(firings_x, firings_y, s=0.2, color=plotting_param["neuron_colors"][celltype])
        ax1.set_xlim(0, simtime)
        ax1.set_ylim(0, cell_idx+1)

        ax0.text(0.5, 0.5, celltype, fontsize="xx-large")

        if fir_idx == 0:
            ax1.set_title("Raster of spikes")
        if fir_idx == len(firing4plot)-1:
            ax1.set_xlabel("time, ms")

    pyrfirsort = np.argsort(-1*np.asarray(pyrfirsize) )

    ax1 = fig.add_subplot(gs1[len(firing4plot), 1])
    for pyr_idx in range(3500): # npyr4preces
        # ax1 = fig.add_subplot(gs1[len(firing4plot), pyr_idx + 1])

        fir = 0.001 * raster_group["pyr"][ indicesofpyr[ pyrfirsort[pyr_idx] ] ][:]



        place_center = place_centers[ pyrfirsort[pyr_idx] ] * 0.001 # np.median(fir)
        if np.isnan(place_center):
            continue

        fir_during_place = fir - place_center - 0.2


        is_inside = np.abs(fir_during_place) < 2.0

        # if firing.size < 12: continue
        if np.sum(is_inside) < 8: continue


        fir_phases = theta_phases[np.floor(fir*sampling_rate).astype(np.int) - 1]



        ax1.scatter(fir_during_place, fir_phases, s=2, color=plotting_param["neuron_colors"]["pyr"])

    ax1.set_xlim(-1.5, 1.5)
    # ax1.set_xticklabels(ax1.get_xticks(), rotation = -45)
    ax1.set_ylim(-np.pi, np.pi)
    ax1.set_ylabel("theta phase, rad")
    ax1.set_xlabel("time, sec")

    ax2 = fig.add_subplot(gs1[len(firing4plot), 2])

    print(intracell_center)
    Vm = intracellular_group[intracell_pyr_neuron][:] # np.random.rand(t.size) # indicesofpyr[ pyrfirsort[0] ]
    t = h5file["time"][:]

    intracell_center = intracell_center + 200
    Vm_pl = Vm[ np.abs(t - intracell_center) < 2000]
    t_pl = t[ np.abs(t - intracell_center) < 2000] - intracell_center

    t_pl = 0.001 * t_pl
    ax2.plot(t_pl, Vm_pl, color="red")
    ax2.set_ylabel("mV")
    ax2.set_xlabel("time, sec")



fig.savefig(figfilepath)
# plt.show()