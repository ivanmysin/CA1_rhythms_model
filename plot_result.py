import numpy as np
import matplotlib.pyplot as plt
import h5py
from basic_parameters import basic_params

def plot_v(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        intracellular_group = h5file["intracellular/origin_data"]
        
        intracell_keys = intracellular_group.keys()
        
        
        fig, axes = plt.subplots(nrows=len(intracell_keys))
        
        for idx, key in enumerate(intracell_keys):
            v = intracellular_group[key][:]
        
            axes[idx].plot(t, v, label = intracellular_group[key].attrs["celltype"] )
            axes[idx].legend()
            
        plt.show()


def plot_spike_raster(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
                
        uniq_celltypes = raster_group.keys()
        
        fig, axes = plt.subplots(nrows=len(uniq_celltypes))
        
        
        
        for sp_idx, key in enumerate(uniq_celltypes):
            for cell_key, firing in raster_group[key].items():
                celltype_idx = int(cell_key.split("_")[-1])
            
                axes[celltype_idx].scatter(firing,  np.zeros(firing.size) + sp_idx + 1, color="b", s=1 )
        
        
        
        for celltype_idx, celltype in enumerate(uniq_celltypes):
            axes[celltype_idx].set_title(celltype)
        
        
        plt.show()


def plot_lfp(filepath):
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        lfp_group = h5file["extracellular/electrode_1/lfp/origin_data"]

        lfp_keys = sorted(lfp_group.keys())
    
        
        fig, axes = plt.subplots(nrows=len(lfp_keys))

        for key_idx, key in enumerate(lfp_keys):
            axes[key_idx].plot(t[1:-1], lfp_group[key][:], label=key )
            axes[key_idx].legend()
        
        
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






path = "/home/ivan/Data/CA1_simulation/test.hdf5"

# plot_v(path)
# plot_spike_raster(path)
# plot_lfp(path)
plot_phase_disrtibution(path)





