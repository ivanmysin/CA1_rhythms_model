import numpy as np
import matplotlib.pyplot as plt

import h5py
import os
import neuron
import sys
h = neuron.h
h.load_file("stdgui.hoc")
h.load_file("import3d.hoc")
neuron.load_mechanisms("./mods/")
h.cvode.use_fast_imem(1)


sys.path.append("../LFPsimpy/")
from LFPsimpy import LfpElectrode


cell_path = "./cells/"
for file in os.listdir(cell_path):
    if file.find(".hoc") != -1:
        h.load_file(cell_path + file)


def run_simulation(params):

    
    all_cells = h.List()
    hh_cells = h.List()
    artificial_cells = h.List()
    
    
    pyramidal_sec_list = h.SectionList()
 
    radius_for_pyramids = np.sqrt( params["Npyr"] / params["PyrDencity"] ) / np.pi 
    
    spike_count_obj = []
    spike_times_vecs = []
    
    
    for idx in range(params["Npyr"]):
        cell = h.poolosyncell(0, 0)
        
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        
        for sec in cell.all:
            pyramidal_sec_list.append(sec)
        
        pyr_coord_in_layer_x = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  
        pyr_coord_in_layer_y = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  
        
        
        cell.position(pyr_coord_in_layer_x, 0, pyr_coord_in_layer_y) 
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Npvbas"]):
        cell = h.pvbasketcell(0, 0)
        
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Nolm"]):
        cell = h.olmcell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Ncckbas"]):
        cell = h.cckcell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Nivy"]):
        cell = h.ivycell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Nngf"]):
        cell = h.ngfcell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Nbis"]):
        cell = h.bistratifiedcell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Naac"]):
        cell = h.axoaxoniccell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    for idx in range(params["Nsca"]):
        cell = h.scacell(0, 0)
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.005
            sec.mean_IextNoise = 0.0005
        
        hh_cells.append(cell)
        all_cells.append(cell)

    # set artificial cells
    for idx in range(params["Nca3"]):
        cell = h.ArtifitialCell()
        cell.celltype = "ca3"
        cell.acell.freqs = 5
        
        artificial_cells.append(cell)
        all_cells.append(cell)
    
    
    for idx in range(params["Nmec"]):
        cell = h.ArtifitialCell()
        cell.celltype = "mec"
        
        artificial_cells.append(cell)
        all_cells.append(cell)
    
    for idx in range(params["Nlec"]):
        cell = h.ArtifitialCell()
        cell.celltype = "lec"
        
        artificial_cells.append(cell)
        all_cells.append(cell)
    
    
    for idx in range(params["Nmsteevracells"]):
        cell = h.ArtifitialCell()
        cell.celltype = "msteevracells"
        
        artificial_cells.append(cell)
        all_cells.append(cell)
    
    for idx in range(params["Nmskomalicells"]):
        cell = h.ArtifitialCell()
        cell.celltype = "mskomalicells"
        
        artificial_cells.append(cell)
        all_cells.append(cell)
    
    
    # set counters for spike generation
    list_of_celltypes = []
    for cell in hh_cells:
        firing = h.APCount(cell.soma[0](0.5))
        fring_vector = h.Vector()
        firing.record(fring_vector)
        spike_count_obj.append(firing)
        spike_times_vecs.append(fring_vector)
        list_of_celltypes.append(cell.celltype)

    
    # set connection
    connections = h.List()
    synapses = h.List()
    
    for pre_idx, presynaptic_cell in enumerate(all_cells):
       
        for post_idx, postsynaptic_cell in enumerate(all_cells):
            
            if pre_idx == post_idx:
                continue
                       
            try:
                
                conn_name = presynaptic_cell.celltype + "2" + postsynaptic_cell.celltype
                conn_data = params[conn_name]
                
            except AttributeError:
                continue
            except KeyError:
                continue

            
            
            
            if np.random.rand() > conn_data["prob"]:
                continue
            
            print(conn_name)
            
            if presynaptic_cell.is_art() == 1:
                pre_comp = getattr( presynaptic_cell, conn_data["sourse_compartment"] )
            else:
                pre_comp = getattr( presynaptic_cell, conn_data["sourse_compartment"] )[-1]
            
            
            post_comp = np.random.choice( getattr( postsynaptic_cell, conn_data["target_compartment"] ) )
            
            # print(post_comp)
             
            
            
            syn = h.Exp2Syn( post_comp(0.5) ) 
            syn.e = conn_data["Erev"]
            syn.tau1 = conn_data["tau_rise"]
            syn.tau2 = conn_data["tau_decay"]
            
            if presynaptic_cell.is_art() == 1:
                conn = h.NetCon(pre_comp, syn, sec=post_comp)
            else:
                conn = h.NetCon(pre_comp(1.0)._ref_v, syn, sec=pre_comp) 
            
            
            # choce synaptic delay and weight from lognormal distribution 
            conn.delay = 0  # np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"])   
            conn.weight[0] = conn_data["gmax"] # np.random.lognormal(mean=np.log(conn_data["gmax"]), sigma=conn_data["gmax_std"]) 

            connections.append(conn)
            synapses.append(syn)
            
        if (presynaptic_cell.is_art() == 1):
        
            fring_vector = h.Vector()
            conn.record(fring_vector)
            spike_times_vecs.append(fring_vector)
            list_of_celltypes.append(presynaptic_cell.celltype)
        
        

    
    Nelecs = params["Nelecs"]
    el_x = np.zeros(Nelecs)
    el_y = np.linspace(0, 1000, Nelecs)
    el_z = np.zeros(Nelecs)
    
    electrodes = []
    
    for idx_el in range(Nelecs):
        le = LfpElectrode(x=el_x[idx_el], y=el_y[idx_el], z=el_z[idx_el], sampling_period=h.dt, sec_list=pyramidal_sec_list)
        electrodes.append(le)
    
    
    
    
    # cell1 = all_cells[0]
    # cell2 = all_cells[1]
    
    
 
    # stim1 = h.IClamp(0.5, sec=cell1.soma[0])
    # stim1.dur   = 100
    # stim1.delay = 0
    # stim1.amp = 0.5

    # stim2 = h.IClamp(0.5, sec=cell2.soma[0])
    # stim2.dur   = 100
    # stim2.delay = 0
    # stim2.amp = 0.8
    
    soma_v_vecs = []
    soma_v_cell_idx = []
    
    for cell_type, list_of_idxes in params["save_soma_v"].items():
        
        for idx_v in list_of_idxes:
            
            try:
                idxinall = list_of_celltypes.index(cell_type)
            except ValueError:
                break
                
                
            cell = all_cells[idxinall + idx_v]
            soma_v_cell_idx.append(idxinall + idx_v)
            if cell.celltype == cell_type:
            
                soma_v = h.Vector()
                soma_v.record(cell.soma[0](0.5)._ref_v)
                soma_v_vecs.append(soma_v)
        
        #print(cell_type)
        
    
    # print(len(soma_v_vecs))
    
    """
    soma1_v = h.Vector()
    soma1_v.record(cell1.soma[0](0.5)._ref_v)

    soma2_v = h.Vector()
    soma2_v.record(cell2.soma[0](0.5)._ref_v)
    """
    


    t = h.Vector()
    t.record(h._ref_t)

    # run simulation
    h.tstop = 100 # set the simulation time
    h.run()
    
    
    
    if params["file_results"] != None:
        with h5py.File(params["file_results"], 'w') as h5file:
            
            h5file.create_dataset("time", data=t)
            
            extracellular_group = h5file.create_group("extracellular")
            ele_group = extracellular_group.create_group('electrode_1')
            lfp_group = ele_group.create_group('lfp')
            lfp_group.attrs['fd'] = 1 / h.dt
            
            
            for idx_el, el in enumerate(electrodes):
                lfp_group.create_dataset("channel_" + str(idx_el+1), data = el.values)
            
    
            spike_raster_group = h5file.create_group("spike_raster")
            
            for cell_idx, sp_times in enumerate(spike_times_vecs):
                cell_spikes_dataset = spike_raster_group.create_dataset("neuron_" + str(cell_idx+1), data=sp_times)
                cell_spikes_dataset.attrs["celltype"] = list_of_celltypes[cell_idx]
    
    
            intracellular_group = h5file.create_group("intracellular")
            
            for v_idx, soma_v in enumerate(soma_v_vecs):
                soma_v_dataset = intracellular_group.create_dataset("neuron_" + str(soma_v_cell_idx[v_idx]+1) , data=soma_v)
                soma_v_dataset.attrs["celltype"] = list_of_celltypes[soma_v_cell_idx[v_idx]]
    
    """
    plt.plot(t, soma_v_vecs[0], color="blue", label="Pyr")
    plt.plot(t, soma_v_vecs[1], color="red", label="PVBas")
    plt.scatter(spike_times_vecs[-1], np.zeros_like(spike_times_vecs[-1]) + 50)
    plt.legend()
    
    
    plt.figure()
    
  
    for sp_t_idx, sp_t in enumerate(spike_times_vecs):
        
        if len(sp_t) > 0:
            plt.scatter(sp_t, np.zeros(len(sp_t)) + sp_t_idx + 1, s = 1, color="blue")
    
    
    plt.show()
    """
    
    print("End of the simultion!")
    return
