import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import h5py
from basic_parameters import basic_params

def plot_v(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
        intracellular_group = h5file["intracellular/origin_data"]
        
        intracell_keys = intracellular_group.keys()
        
        for idx, key in enumerate(intracell_keys):
            fig, axes = plt.subplots()
            
            v = intracellular_group[key][:]
            celltype = intracellular_group[key].attrs["celltype"]
         
            axes.plot(t, v, label = celltype )
            
            firings = raster_group[celltype][key][:]
            
            firings_y = np.zeros_like(firings) - 5
            axes.scatter(firings, firings_y, s=20, color="red")
            
            
            axes.legend()
            
        plt.show()


def plot_spike_raster(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
                
        uniq_celltypes = raster_group.keys()

        for celltype in uniq_celltypes:
            fig, axes = plt.subplots()
            fig.suptitle(celltype)
            sp_idx = 0
            for cell_key,firing in raster_group[celltype].items():
                # celltype_idx = int(cell_key.split("_")[-1])
            
                axes.scatter(firing,  np.zeros(firing.size) + sp_idx + 1, color="b", s=1 )
        
                sp_idx += 1
        
       
        
        
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

        lfp_keys = sorted(lfp_group.keys(), key = lambda x: int(x.split("_")[-1]), reverse=True )
        
        
        fig, axes = plt.subplots( nrows=len(lfp_keys), figsize=(6, 6), sharex=True, sharey=True)
        for key_idx, key in enumerate(lfp_keys):
            
            # axes[key_idx].set_title(key)
            lfp = lfp_group[key][:]
            axes[key_idx].plot(t[:lfp_group[key].size], lfp,  color="blue", label=key)
            
            # meanpyrVnorm = meanpyrV * lfp.std()  + np.mean(lfp)
            # axes[key_idx].plot(t, meanpyrVnorm, label="soma V", color="red" )
            
            axes[key_idx].set_xlim(t[0], t[-1])
            # axes[key_idx].legend()
            
            axes[key_idx].spines['right'].set_visible(False)
            axes[key_idx].spines['top'].set_visible(False)

            axes[key_idx].set_ylabel("mV")
            
            
            # axes[key_idx].axis('off')
            
            if key_idx == len(lfp_keys) - 1:
                axes[key_idx].set_xlabel("time, ms")
            
            else:
                
                # axes[key_idx].spines['left'].set_visible(False)
                axes[key_idx].spines['bottom'].set_visible(False)
                axes[key_idx].tick_params(labelbottom=False, bottom=False)
        # plt.tight_layout(pad=0, w_pad=0, h_pad=0)
        plt.show()


def plot_phase_disrtibution(filepath):
    with h5py.File(filepath, 'r') as h5file:
        distr_group = h5file["extracellular/electrode_1/firing/processing/theta"]
        
        keys = distr_group.keys()
        
        fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(16, 11))

        row_idx = 0
        cols_idx = 0
        for key_idx, key in enumerate(keys):
            
            if row_idx > 4:
                row_idx = 0
                cols_idx += 1
            
            phase_distr = distr_group[key][:]
            
            phases = np.linspace(-np.pi, np.pi, phase_distr.size)
            axes[row_idx, cols_idx].plot( phases, phase_distr, label=key )
            axes[row_idx, cols_idx].legend()
            
            row_idx += 1
        
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.4)
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
        theta_signal = h5file["extracellular/electrode_1/lfp/processing/bands/channel_1/theta"][:]
        theta_phases = np.angle( hilbert(theta_signal) )

        firing_group =  h5file["extracellular/electrode_1/firing/origin_data/pyr"]

        sampling_rate *= 0.001

        fig_in, ax_in = plt.subplots()
        fig_out, ax_out = plt.subplots()


        ax_in.set_title("In")
        ax_out.set_title("Out")

        for firing in firing_group.values():
            if firing.size < 10: continue
            indexes = (firing * sampling_rate).astype(np.int)

            place_center = np.median(firing)



            firing_during_place = firing - place_center

            is_inside = np.abs(firing_during_place) < 2000

            phases_during_place = theta_phases[indexes]

            firing_during_place = firing_during_place[is_inside]
            phases_during_place = phases_during_place[is_inside]


            if np.abs(place_center - 5000) < 100:
                ax_in.scatter(firing_during_place, phases_during_place, s=2)
            else:
                ax_out.scatter(firing_during_place, phases_during_place, s=2)
    plt.show()

###################################################################################
def plot_current_source_density(filepath, band_name):
    from scipy.ndimage import zoom
    with h5py.File(filepath, 'r') as h5file:
        sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]
        sampling_rate *= 0.001 
        csd = h5file["extracellular/electrode_1/lfp/processing/current_source_density/" + band_name][:]
        csd = zoom(csd, zoom=(20, 1), mode="nearest")
        # print(csd.shape)
        
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
        


def main_plots(filepath):
    plot_lfp(filepath)
    
    
    
    return
    
    
    
    
    
if __name__ == "__main__":
    filepath = "/home/ivan/Data/CA1_simulation/test_server.hdf5"  # basic_params["file_results"]  # 
    
    # main_plots(filepath)
    # plot_lfp(filepath)
    plot_current_source_density(filepath, "theta")
    
    
    # plot_v(filepath)
    # plot_spike_raster(filepath)
    
    # plot_phase_disrtibution(filepath)
    # plot_pyr_layer_lfp_vs_raster(filepath)
    # plot_phase_precession(filepath)





