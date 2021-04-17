import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
from matplotlib import gridspec
import h5py
from basic_parameters import get_object_params
import processingLib as proclib

# basic_params = get_object_params()

plotting_param = {
    "neuron_colors" : {
        "pyr" : (1.0, 0.0, 0.0), # red
        "pvbas": (0.0, 0.0, 1.0), # blue
        "olm": (0.0, 0.0, 0.5), #
        "cckbas": (0.0, 1.0, 0.0), # green
        "ivy": (0.0, 0.5, 0.5), #
        "ngf": (0.5, 0.5, 0.5), #
        "bis": (0.1, 0.0, 0.5), #
        "aac": (1.0, 0.0, 0.5), #
        "sca": (0.0, 1.0, 0.5), #

        "ca3_spatial": (0.5, 0.5, 0.0), #
        "ca3_non_spatial": (0.5, 0.5, 0.0), #
        "mec": (0.5, 1.0, 0.0), #
        "lec": (0.9, 0.7, 0.0), #
        "msteevracells": (0.0, 0.8, 0.5), #
        "mskomalicells": (0.0, 0.5, 0.9), #
        "msach": (0.8, 0.2, 0.0), #
    },

    "neuron_order" : ["pyr", "pvbas", "cckbas", "olm", "aac", "ivy", "bis", "sca", "ngf", "ca3_spatial", "ca3_non_spatial", "mec",  "msteevracells", "msach"], # "mskomalicells","lec",
    "rhytms_order" : ["theta", "slow gamma", "middle gamma", "fast gamma"],

    "number_pyr_layer" : 3,  # number of chennel from pyramidal layer

    "frequencies4wavelet" : [2, 30],
}

#####################################################################################
def plot_spike_raster(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        t0 = h5file["time"][0]
        t1 = h5file["time"][-1]
        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
                
        fig = plt.figure(figsize=(15, 10))
        
        neurons_num = len(plotting_param["neuron_order"])
        gs = gridspec.GridSpec(neurons_num, 1, height_ratios=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        for celltype_idx, celltype in enumerate(plotting_param["neuron_order"]):
            try:
                celltype_group = raster_group[celltype]
                axes = plt.subplot(gs[celltype_idx])
           
                for sp_idx, (cell_key, firing) in enumerate(sorted(celltype_group.items(), key=lambda x: int(x[0].split("_")[-1]),)):
                    # sp_idx += 1
                    # cell_key = int(cell_key.split("_")[-1])
                    axes.scatter(firing,  np.zeros(firing.size)+sp_idx+1, color=plotting_param["neuron_colors"][celltype], s=0.2 )

                axes.set_ylim(1, sp_idx)
                axes.set_xlim(t0, t1)
                axes.set_ylabel(celltype, rotation='horizontal', labelpad=20)

                if celltype_idx == len(plotting_param["neuron_order"]) - 1:
                    axes.set_xlabel("time, ms")
                else:
                    axes.tick_params(labelbottom=False, bottom=False)
            except KeyError:
                continue
        fig.tight_layout()
        plt.show()


def plot_lfp(filepath):
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        
        # meanpyrV = 0
        # pyrVgroup = h5file["intracellular/origin_data"]
        # for v_dset in pyrVgroup.values():
            # if v_dset.attrs["celltype"] == "pyr":
                # meanpyrV += v_dset[:]
        # meanpyrV -= np.mean(meanpyrV)
        # meanpyrV /= np.std(meanpyrV)
        
        
        lfp_group = h5file["extracellular/electrode_1/lfp/origin_data"]
        wavelet_group = h5file["extracellular/electrode_1/lfp/processing2/wavelet"]

        lfp_keys = sorted(lfp_group.keys(), key = lambda x: int(x.split("_")[-1]), reverse=True )
        
        nrows = len(lfp_keys)
        
            
        fig, axes = plt.subplots( nrows=nrows, ncols=2, figsize=(5, 10))
        for key_idx, key in enumerate(lfp_keys):
            lfp = lfp_group[key][:]
            freqs = wavelet_group[key]["frequecies"][:]


            freqs_sl = proclib.slice_by_bound_values(freqs, plotting_param["frequencies4wavelet"][0], plotting_param["frequencies4wavelet"][1])
            freqs = freqs[freqs_sl]
            w_coefs = np.abs(wavelet_group[key]["wavelet_coeff"][freqs_sl, :])
            
            if nrows == 1:
                this_axes1 = axes[0]
                this_axes2 = axes[1]
            else:
                this_axes1 = axes[key_idx, 0]
                this_axes2 = axes[key_idx, 1]

            this_axes1.plot(t[:lfp.size], lfp,  color="blue", label=key)

            gr = this_axes2.pcolormesh(t[:lfp.size], freqs, w_coefs,  cmap="rainbow", shading='auto')
            cbar = fig.colorbar(gr, ax=this_axes2)
            # meanpyrVnorm = meanpyrV * lfp.std()  + np.mean(lfp)
            # axes[key_idx].plot(t, meanpyrVnorm, label="soma V", color="red" )
            
            this_axes1.set_xlim(t[0], t[-1])
            this_axes2.set_xlim(t[0], t[-1])

            
            this_axes1.spines['right'].set_visible(False)
            this_axes1.spines['top'].set_visible(False)

            this_axes1.set_ylabel("mV")
            this_axes2.set_ylabel("Hz")


            if key_idx == len(lfp_keys) - 1:
                this_axes1.set_xlabel("time, ms")
                this_axes2.set_xlabel("time, ms")

            else:
                
                # axes[key_idx].spines['left'].set_visible(False)
                this_axes1.spines['bottom'].set_visible(False)
                this_axes1.tick_params(labelbottom=False, bottom=False)
                this_axes2.spines['bottom'].set_visible(False)
                this_axes2.tick_params(labelbottom=False, bottom=False)

        plt.tight_layout(pad=0, w_pad=1, h_pad=0)
        plt.show()


def plot_modulation_index(filepath):
    with h5py.File(filepath, 'r') as h5file:

        mi_group = h5file["extracellular/electrode_1/lfp/processing2/modulation_index/channel_"+str(plotting_param["number_pyr_layer"])]
        mi = mi_group["modulation_index"][:]
        freqs4ampl = mi_group["freqs4ampl"][:]
        freqs4phase = mi_group["freqs4phase"][:]

        fig, axes = plt.subplots()
        gr = axes.pcolormesh(freqs4phase, freqs4ampl, mi, cmap="rainbow", shading='auto')
        axes.set_ylabel("frequencies for amplitude, Hz")
        axes.set_xlabel("frequencies for phase, Hz")
        cbar = fig.colorbar(gr)

    plt.show()


def plot_phase_by_amplitude_coupling(filepath):
    with h5py.File(filepath, 'r') as h5file:

        coup_group = h5file["extracellular/electrode_1/lfp/processing2/theta_gamma_coupling/channel_"+str(plotting_param["number_pyr_layer"])]
        coupling = coup_group["coupling_matrix"][:]
        gamma_freqs = coup_group["gamma_freqs"][:]
        theta_phase = coup_group["theta_phase"][:]

        theta_signal = np.cos(theta_phase)

        fig = plt.figure(figsize=(5, 5))
        gs = gridspec.GridSpec(2, 2, figure=fig, height_ratios=[1, 10], width_ratios=[10, 1], hspace=0 )

        axes = plt.subplot(gs[0, 0])
        axes.plot(theta_phase, theta_signal, color="black")
        axes.set_xlim(-np.pi, np.pi)
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.spines['left'].set_visible(False)
        axes.spines['bottom'].set_visible(False)
        axes.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)

        axes = plt.subplot(gs[1, 0])
        gr = axes.pcolormesh(theta_phase, gamma_freqs, coupling, cmap="rainbow", shading='auto')
        axes.set_xlim(-np.pi, np.pi)
        axes.set_ylabel("gamma frequency, Hz")
        axes.set_xlabel("theta phase, rad")

        axes = plt.subplot(gs[1, 1])
        cbar = fig.colorbar(gr, cax=axes)

    plt.show()

############################################################################
def plot_v(filepath):
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]

        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
        intracellular_group = h5file["intracellular/origin_data"]

        intracell_keys = sorted(intracellular_group.keys(), key=lambda neur_num: int(neur_num.split("_")[-1]) )

        for idx, key in enumerate(intracell_keys):
            fig, axes = plt.subplots()

            v = intracellular_group[key][:]
            celltype = intracellular_group[key].attrs["celltype"]

            axes.plot(t, v, label=celltype)

            firings = raster_group[celltype][key][:]

            firings_y = np.zeros_like(firings) - 5
            axes.scatter(firings, firings_y, s=20, color="red")

            axes.legend()

        plt.show()


def plot_phase_disrtibution(filepath):
    with h5py.File(filepath, 'r') as h5file:
        distr_group = h5file["extracellular/electrode_1/firing/processing2/phase_distrs"]

        fig, axes = plt.subplots(nrows=len(plotting_param["neuron_order"]), ncols=len(plotting_param["rhytms_order"]), figsize=(5, 10))
        for celltypes_idx, celltype in enumerate(plotting_param["neuron_order"]):
            for rhythm_idx, rhythm_name in enumerate(plotting_param["rhytms_order"]):
                try:
                    phase_distr = distr_group[celltype][rhythm_name][:]
                except KeyError:
                    continue
                phases = np.linspace(-np.pi, np.pi, phase_distr.size)
                signal4phase = np.max(phase_distr) * 0.25 * (np.cos(phases) + 1)
                axes[celltypes_idx, rhythm_idx].plot( phases, phase_distr, color=plotting_param["neuron_colors"][celltype] )
                axes[celltypes_idx, rhythm_idx].plot( phases, signal4phase, color="black", linestyle="dotted" )

                axes[celltypes_idx, rhythm_idx].set_xlim(-np.pi, np.pi)
                axes[celltypes_idx, rhythm_idx].set_ylim(0, None)

                if celltypes_idx == 0:
                    axes[celltypes_idx, rhythm_idx].set_title(rhythm_name)

                if rhythm_idx == 0:
                    axes[celltypes_idx, rhythm_idx].set_ylabel(celltype, rotation="horizontal", labelpad=20)

                if celltypes_idx == len(plotting_param["neuron_order"]) - 1:
                    axes[celltypes_idx, rhythm_idx].set_xlabel("phase, rad")
                else:
                    axes[celltypes_idx, rhythm_idx].tick_params(labelbottom=False, bottom=False)


        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0)
        plt.show()


def plot_pyr_layer_lfp_vs_raster(filepath):
    with h5py.File(filepath, 'r') as h5file:
        
        lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_1"][:]
        
        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
        
        sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]
        t = 1000 * np.linspace(0, lfp.size/sampling_rate, lfp.size)
                
        uniq_celltypes = raster_group.keys()

        for celltype in uniq_celltypes:
            fig, axes = plt.subplots(nrows=2, sharex=True)
            fig.suptitle(celltype)
            
            axes[0].plot(t, lfp)
            sp_idx = 0
            for cell_key, firing in raster_group[celltype].items():
                # celltype_idx = int(cell_key.split("_")[-1])
            
                axes[1].scatter(firing,  np.zeros(firing.size) + sp_idx + 1, color="b", s=1 )
        
                sp_idx += 1
            
            axes[1].set_ylim(1, sp_idx)
        
       
        
        
        plt.show()

def plot_phase_precession(filepath):
    with h5py.File(filepath, 'r') as h5file:
        sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]
        theta_signal = h5file["extracellular/electrode_1/lfp/processing2/bands/channel_1/theta"][:]
        theta_phases = np.angle( hilbert(theta_signal) )

        firing_group = h5file["extracellular/electrode_1/firing/origin_data/pyr"] # pyr !!!!

        sampling_rate *= 0.001

        fig_in, ax_in = plt.subplots()
        fig_out, ax_out = plt.subplots()


        ax_in.set_title("In")
        ax_out.set_title("Out")

        for firing in firing_group.values():
            if firing.size < 4: continue

            indexes = (np.floor(firing * sampling_rate) - 1).astype(np.int)

            place_center = np.median(firing)

            firing_during_place = firing - place_center

            #if np.std(firing_during_place) > 5000: continue

            is_inside = np.abs(firing_during_place) < 2000
            phases_during_place = theta_phases[indexes]

            firing_inside = firing_during_place[is_inside]
            phases_inside = phases_during_place[is_inside]

            ax_in.scatter(firing_inside, phases_inside, s=2)

            is_outside = np.logical_not(is_inside)
            firing_outside = firing_during_place[is_outside]
            phases_outside = phases_during_place[is_outside]

            ax_out.scatter(firing_outside, phases_outside, s=2)


    plt.show()

###################################################################################
def plot_current_source_density(filepath, band_name):

    with h5py.File(filepath, 'r') as h5file:
        sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]
        sampling_rate *= 0.001 
        csd = h5file["extracellular/electrode_1/lfp/processing2/current_source_density/" + band_name][:]

        t = np.linspace(0, csd.shape[1]/sampling_rate, csd.shape[1])
        depth = np.linspace(-300, 800, csd.shape[0])
        
        fig, axes = plt.subplots()
        gr = axes.pcolormesh(t, depth, csd, cmap="rainbow", shading='auto')
        axes.set_xlabel("time, ms")
        axes.set_ylabel("depth, mkm")
        
        q1 = np.quantile(csd, 0.05)
        q3 = np.quantile(csd, 0.95)

        cbar = fig.colorbar(gr, ticks=[np.min(csd), q1, 0, q3, np.max(csd)])
        cbar.ax.set_yticklabels(['sink', "{:.2}".format(q1), 0, "{:.2}".format(q3), 'source'])
        
    
    plt.show()
        
def plot_nm_phase_phase_coupling(filepath):
    with h5py.File(filepath, 'r') as h5file:
        gr_name = "extracellular/electrode_1/lfp/processing2/theta_gamma_phase_phase_coupling/channel_"
        gr_name += str(plotting_param["number_pyr_layer"])
        coup_group = h5file[gr_name]
        nmarray = coup_group["nmarray"][:]

        fig, axes = plt.subplots(nrows=1, figsize=(5, 5))
        for key, val in sorted(coup_group.items()):
            splited_key = key.split("_")
            if splited_key[0] != "coupling": continue

            diap = splited_key[-1] + " Hz"
            axes.plot(nmarray, val[:], label=diap)
        axes.legend()
        axes.set_xlabel("n * theta phase")
        axes.set_ylabel("R of (n * theta phase - gamma phase) disrtibution")

    plt.show()

def plot_v_vs_pyr_lfp(filepath):
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_"+str(plotting_param["number_pyr_layer"])][:]


        intracellular_group = h5file["intracellular/origin_data"]
        intracell_keys = intracellular_group.keys()


        fig, axes = plt.subplots(nrows=len(plotting_param["neuron_order"])+1, sharex=True, figsize=(5, 10))
        axes[0].plot(t[:lfp.size], lfp, color="black")
        for celltype_idx, celltype in enumerate(plotting_param["neuron_order"]):
            celltype_idx += 1
            for key in intracell_keys:
                if  intracellular_group[key].attrs["celltype"] != celltype: continue


                v = intracellular_group[key][:]
                celltype = intracellular_group[key].attrs["celltype"]
                axes[celltype_idx].plot(t, v, label=celltype, color=plotting_param["neuron_colors"][celltype])
                axes[celltype_idx].legend()

                axes[celltype_idx].set_xlim(t[0], t[-1])
                axes[celltype_idx].set_ylim(-90, 60)

                if celltype_idx == len(plotting_param["neuron_order"]):
                    axes[celltype_idx].set_xlabel("time, ms")
                    axes[celltype_idx].tick_params(labelbottom=True, bottom=True)
                else:
                    axes[celltype_idx].tick_params(labelbottom=False, bottom=True)
                axes[celltype_idx].set_ylabel("mV")

                break

        plt.show()


#################################################################################
def main_plots(filepath):
    plot_lfp(filepath)
    
    
    
    return
    
    
    
    
    
if __name__ == "__main__":
    filepath = "/home/ivan/Data/CA1_simulation/test.hdf5"  # basic_params["file_results"]  # "/home/ivan/Data/CA1_simulation/artificial_signals.hdf5"
    
    # main_plots(filepath)
    # plot_lfp(filepath)
    # plot_current_source_density(filepath, "theta")
    # plot_spike_raster(filepath)
    # plot_modulation_index(filepath)
    # plot_phase_by_amplitude_coupling(filepath)
    # plot_nm_phase_phase_coupling(filepath)
    plot_phase_disrtibution(filepath)
    plot_v_vs_pyr_lfp(filepath)


    # plot_v(filepath)
    # plot_pyr_layer_lfp_vs_raster(filepath)
    # plot_phase_precession(filepath)





