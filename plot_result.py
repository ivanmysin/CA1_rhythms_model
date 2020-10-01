import numpy as np
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
        
        meanpyrV = 0
        pyrVgroup = h5file["intracellular/origin_data"]
        for v_dset in pyrVgroup.values():
            if v_dset.attrs["celltype"] == "pyr":
                meanpyrV += v_dset[:]
        
        # meanpyrV /= 100
        # plt.plot(t, meanpyrV)
        meanpyrV -= np.mean(meanpyrV)
        meanpyrV /= np.std(meanpyrV)
        
        
        lfp_group = h5file["extracellular/electrode_1/lfp/origin_data"]

        lfp_keys = sorted(lfp_group.keys(), key = lambda x: int(x.split("_")[1]), reverse=True )
        
        
        fig, axes = plt.subplots( nrows=len(lfp_keys), figsize=(15, 10))
        for key_idx, key in enumerate(lfp_keys):
            
            # axes[key_idx].set_title(key)
            lfp = lfp_group[key][:]
            axes[key_idx].plot(t[:lfp_group[key].size], lfp, label=key, color="blue" )
            
            meanpyrVnorm = meanpyrV * lfp.std()  + np.mean(lfp)
            axes[key_idx].plot(t, meanpyrVnorm, label="soma V", color="red" )
            
            axes[key_idx].set_xlim(0, 2000)
            # lfp = h5file["extracellular/electrode_1/lfp/processing/"+key+"_bands/theta"]
            # axes.plot(t, lfp, label=key, color="red" )
            axes[key_idx].legend()
            
            
        
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.4)
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
        
        lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_3"][:]
        
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



if __name__ == "__main__":
    filepath = basic_params["file_results"]   #"/home/ivan/Data/CA1_simulation/test.hdf5"

    #plot_v(filepath)
    # plot_spike_raster(filepath)
    # plot_lfp(filepath)
    # plot_phase_disrtibution(filepath)
    plot_pyr_layer_lfp_vs_raster(filepath)





