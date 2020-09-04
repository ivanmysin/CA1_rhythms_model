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
            
            print(celltype)
        
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
        
        lfp_group = h5file["extracellular/electrode_1/lfp/origin_data"]

        lfp_keys = sorted(lfp_group.keys(), key = lambda x: int(x.split("_")[1]), reverse=True )
        
        

        for key_idx, key in enumerate(lfp_keys):
            fig, axes = plt.subplots()
            axes.set_title(key)
            axes.plot(t[:lfp_group[key].size], lfp_group[key][:], label=key, color="blue" )
            
            #lfp = h5file["extracellular/electrode_1/lfp/processing/"+key+"_bands/theta"]
            # axes.plot(t, lfp, label=key, color="red" )
            
        
        
        plt.show()


def plot_phase_disrtibution(filepath):
    with h5py.File(filepath, 'r') as h5file:
        distr_group = h5file["extracellular/electrode_1/firing/processing/theta"]
        
        keys = distr_group.keys()
        
        fig, axes = plt.subplots(nrows=len(keys), figsize=(4, 20))

        for key_idx, key in enumerate(keys):
            
            phase_distr = distr_group[key][:]
            
            phases = np.linspace(-np.pi, np.pi, phase_distr.size)
            axes[key_idx].plot(phases, phase_distr, label=key )
            axes[key_idx].legend()
        
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        plt.show()





if __name__ == "__main__":
    path = basic_params["file_results"]   #"/home/ivan/Data/CA1_simulation/test.hdf5"

    plot_v(path)
    # plot_spike_raster(path)
    # plot_lfp(path)
    # plot_phase_disrtibution(path)





