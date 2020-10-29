from mpi4py import MPI
from neuron import h, load_mechanisms
from neuron.units import ms, mV
h.nrnmpi_init()


import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import sys
from time import time

def join_lfp(comm, electrodes):
    # print("Hello from join lfp!")
    rank = comm.Get_rank()

    lfp_data = []
    for el in electrodes:
        if el is None:
            sended = None
        else:
            sended = el.values
        reseved = comm.gather(sended, root=0)
        
        if rank == 0:
            lfp_el = []
            for var_tmp in reseved:
                if not var_tmp is None:
                    lfp_el.append(var_tmp) 
            
            
            if len(lfp_el) > 0:
                lfp_el = np.vstack(lfp_el)
                lfp_el = np.sum(lfp_el, axis=0)
            else:
                lfp_el = np.zeros(2)
            lfp_data.append(lfp_el)
    
    return lfp_data

def join_vect_lists(comm, vect_list, gid_vect):
    rank = comm.Get_rank()
    jointed = []
    all_gid = comm.gather(gid_vect, root=0)
    reseved = comm.gather(vect_list, root=0)

    if rank == 0:
        
        for rev in reseved:
            if len(rev) > 0:
                jointed.extend(rev)
        all_gid = np.hstack(all_gid).ravel()
        jointed = [x for _, x in sorted(zip(all_gid, jointed), key=lambda pair: pair[0])]
        
        
        for idx in range(len(jointed)):
            jointed[idx] = np.asarray(jointed[idx])
        
    return jointed




def run_simulation(params):
    pc = h.ParallelContext()
    
    pc.timeout(20)
    h.load_file("stdgui.hoc")
    h.load_file("stdrun.hoc")
    h.load_file("import3d.hoc")

    RNG = np.random.default_rng()
    
    load_mechanisms("./mods/")
    
    h.cvode.use_fast_imem(1)

    sys.path.append("../LFPsimpy/")
    from LFPsimpy import LfpElectrode


    cell_path = "./cells/"
    for file in os.listdir(cell_path):
        if file.find(".hoc") != -1:
            h.load_file(cell_path + file)
    
    
    ncells = len(params["celltypes"])  # whole number of cells in the model
    gid_vect = np.arange( pc.id(), ncells, pc.nhost(), dtype=np.int )
    
    
    all_cells = h.List()
    hh_cells = h.List()
    # artificial_cells = h.List()
    
    
    pyramidal_sec_list = h.SectionList()
    is_pyrs_thread = False
    radius_for_pyramids = np.sqrt( params["CellNumbers"]["Npyr"] / params["PyrDencity"] ) / np.pi 
    
    spike_count_obj = []
    spike_times_vecs = []
    
    soma_v_vecs = []
    
    
    for gid in gid_vect:
        
        celltypename = params["neurons"][gid]["celltype"] #  params["celltypes"][gid]
        cellclass = getattr(h, params["CellParameters"][celltypename]["cellclass"])
        
        # print(celltypename)
        cell = cellclass(gid, 0)

        pc.set_gid2node(gid, pc.id())
        
        if celltypename == "pyr":
           
            is_pyrs_thread = True
            for sec in cell.all:
                pyramidal_sec_list.append(sec)
        
            pyr_coord_in_layer_x = radius_for_pyramids * 2 * (RNG.random() - 0.5) # density of the pyramidal cells
            pyr_coord_in_layer_y = radius_for_pyramids * 2 * (RNG.random() - 0.5) # density of the pyramidal cells

            cell.position(pyr_coord_in_layer_x, 0, pyr_coord_in_layer_y)
  
        
        
        
        # set counters for spike generation
        if cell.is_art() == 0:
            # print("Hello from real neurons setting")
            for sec in cell.all:
                sec.insert("IextNoise")
                sec.myseed_IextNoise = RNG.integers(0, 1000000000000000, 1)
                sec.sigma_IextNoise = 0.005
                sec.mean_IextNoise = params["neurons"][gid]["cellparams"]["iext"]
                # RNG.normal(params["CellParameters"][celltypename]["iext"], params["CellParameters"][celltypename]["iext_std"])
            
            
            firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
            firing.threshold = -30 * mV

        else:
            # print("Hello from art neurons setting")
            cell.celltype = celltypename
            
            for p_name, p_val in params["neurons"][gid]["cellparams"].items():
                if hasattr(cell.acell, p_name):
                    setattr(cell.acell, p_name, p_val)

            firing = h.NetCon(cell.acell, None)
        
        pc.cell(gid, firing)
        fring_vector = h.Vector()
        firing.record(fring_vector)
        spike_count_obj.append(firing)
        spike_times_vecs.append(fring_vector)
        
        
        
        # check is need to save Vm of soma
        if np.sum(params["save_soma_v"]["vect_idxes"] == gid) == 1:
            soma_v = h.Vector()
            soma_v.record(cell.soma[0](0.5)._ref_v)
            soma_v_vecs.append(soma_v)
        else:
            soma_v_vecs.append(np.empty(shape=0) )
        
      
        

        if cell.is_art() == 0:
            hh_cells.append(cell)
        
        all_cells.append(cell)

    print("End of neurons settings")

    
    # set connection
    connections = h.List()
    synapses = h.List()
    # nmda_synapses = h.List()
    
    
    for syn_params in params["synapses_params"]:
        
        post_idx = np.argwhere( gid_vect == syn_params["post_gid"] ).ravel()
        
        if post_idx.size == 0: continue
        post_idx = post_idx[0]
        
        postsynaptic_cell = all_cells[ post_idx ]
        
        post_list = getattr(postsynaptic_cell, syn_params["target_compartment"])
        len_postlist = sum([1 for _ in post_list])
        
        if len_postlist == 1:
            post_idx = 0
        else:
            post_idx = RNG.integers(0, len_postlist-1)

        for idx_tmp, post_comp_tmp in enumerate(post_list):
            if idx_tmp == post_idx: post_comp = post_comp_tmp
    
        syn = h.Exp2Syn( post_comp(0.5) ) 
        syn.e = syn_params["Erev"]
        syn.tau1 = syn_params["tau_rise"]
        syn.tau2 = syn_params["tau_decay"]
        
        
        conn = pc.gid_connect(syn_params["pre_gid"], syn)
        conn.delay = syn_params["delay"]
        conn.weight[0] = syn_params["gmax"]
        conn.threshold = -30 * mV
        
        connections.append(conn)
        synapses.append(syn)
        
        #print("Hello before nmda sets")
        try:
            
            gmax_nmda = syn_params["NMDA"]["gNMDAmax"]
            
            syn_nmda = h.NMDA(post_comp(0.5), sec=post_comp)
            syn_nmda.tcon = syn_params["NMDA"]["tcon"]
            syn_nmda.tcoff = syn_params["NMDA"]["tcoff"]
            syn_nmda.gNMDAmax = gmax_nmda
            
            conn2 = pc.gid_connect(syn_params["pre_gid"], syn_nmda)  # h.NetCon(pre_pyr.soma[0](0.5)._ref_v, syn_nmda, sec=pre_pyr.soma[0])
            conn2.delay = syn_params["delay"]
            conn2.weight[0] = syn_params["NMDA"]["gNMDAmax"]
            conn2.threshold = -30 * mV
       
            connections.append(conn2)
            synapses.append(syn_nmda)
            
       
        except KeyError:
            pass


    gap_junctions = h.List()
    for gap_params in params["gap_junctions"]:
        
        
        idx1 = np.argwhere( gid_vect == gap_params["gid1"] ).ravel()
        idx2 = np.argwhere( gid_vect == gap_params["gid2"] ).ravel()
        
        if idx1.size != 0 and idx2.size != 0: 
        
            idx1 = idx1[0]
            idx2 = idx2[0]
            
            cell1 = all_cells[ idx1 ]
            cell2 = all_cells[ idx2 ]
            
            comp1_list = getattr(cell1, gap_params["compartment1"])
            len_list = sum([1 for _ in comp1_list])
            
            if len_list == 1:
                idx1 = 0
            else:
                idx1 = RNG.integers(0, len_list-1)

            for idx_tmp, comp_tmp in enumerate(comp1_list):
                if idx_tmp == idx1: comp1 = comp_tmp
            
            comp2_list = getattr(cell2, gap_params["compartment2"])
            len_list = sum([1 for _ in comp2_list])
            
            if len_list == 1:
                idx2 = 0
            else:
                idx2 = RNG.integers(0, len_list-1)

            for idx_tmp, comp_tmp in enumerate(comp2_list):
                if idx_tmp == idx2: comp2 = comp_tmp
            

            gap = h.GAP(comp1(0.5), sec=comp1)
            gap.r = gap_params["r"]
            h.setpointer(comp2(0.5)._ref_v, 'vgap', gap)
            gap_junctions.append(gap)
            
            gap = h.GAP(comp2(0.5), sec=comp2)
            gap.r = gap_params["r"]
            h.setpointer(comp1(0.5)._ref_v, 'vgap', gap)
            gap_junctions.append(gap)
            print("Hello from one thread")
            
        elif  idx1.size != 0 or idx2.size != 0:
            print("Hello")
            if idx1.size != 0:
                this_idx = idx1[0]
                this_gid = gap_params["gid1"]
                out_gid = gap_params["gid2"]
                comp_name = gap_params["compartment1"]
            else:
                this_idx = idx2[0]
                this_gid = gap_params["gid2"]
                out_gid = gap_params["gid1"]
                comp_name = gap_params["compartment2"]
            
            cell = all_cells[ this_idx ]
            comp_list = getattr(cell, comp_name)
            # len_list = sum([1 for _ in comp1_list])
            
            idx1 = 0
            for idx_tmp, comp_tmp in enumerate(comp_list):
                if idx_tmp == idx1: comp = comp_tmp
                
                
            # gap = h.GAP(comp(0.5), sec=comp)
            # gap.r = gap_params["r"]
            
            # pc.source_var(comp1(0.5)._ref_v, 1)
            # pc.target_var(gap._ref_vgap, 0)
            
            # gap_junctions.append(gap)
            
            
            
            
        else:
            pass
        
        
        
        
        

    el_x = params["elecs"]["el_x"]
    el_y = params["elecs"]["el_y"]
    el_z = params["elecs"]["el_z"]

    
    electrodes = []
    
    
    
    for idx_el in range(el_x.size):
        if is_pyrs_thread:
            le = LfpElectrode(x=el_x[idx_el], y=el_y[idx_el], z=el_z[idx_el], sampling_period=h.dt, \
                              method='Line', sec_list=pyramidal_sec_list)
            electrodes.append(le)
        else:
            electrodes.append(None)
    

    # soma1_v = None
    # if pc.id() == 0 :
        # print( len(hh_cells) )
        # print( hh_cells[0].celltype )
        # soma1_v = h.Vector()
        # soma1_v.record(hh_cells[0].soma[0](0.5)._ref_v)

    if pc.id() == 0:
        t_sim = h.Vector()
        t_sim.record(h._ref_t)
    else:
        t_sim = None
        
    h.tstop = params["duration"] * ms
    
    
    pc.set_maxstep(10 * ms)
    h.finitialize()
    
    pc.barrier()
    print("Start simulation")
    timer = time()
    pc.psolve(params["duration"] * ms)
    print("Time of simulation in sec ", time()-timer)
    pc.barrier()
    
    # print(np.asarray(v_tmp))
    # if pc.id() == 0:
    #    soma1_v = np.asarray(soma1_v)
    #    # print(soma1_v)
    #    plt.plot(t_sim, soma1_v)
    #    plt.savefig("../../Data/test.png")
    #    # plt.show()
    
    # unite data from all threads to 0 thread
    comm = MPI.COMM_WORLD
    
    # print(pc.id(), "Join lfp data")
    lfp_data = join_lfp(comm, electrodes)
    
    
    # lfp_data = []
    # if (pc.id() == 0):
    #     for el in electrodes:
    #         lfp_data.append(el.values)
    
    
    # print(pc.id(), "Join spike train")
    spike_trains = join_vect_lists(comm, spike_times_vecs, gid_vect)
    # print(pc.id(), "Join Vm of soma")
    #  print("len of soma_v_vecs",  len(soma_v_vecs) )
    soma_v_list = join_vect_lists(comm, soma_v_vecs, gid_vect)
    
    # print(pc.id(), "Start saving results to file")
    if (pc.id() == 0) and (params["file_results"] != None):
        
        t_sim = np.asarray(t_sim)
        rem_time = params["del_start_time"]
        if rem_time > t_sim[-1]:
            rem_time = 0
        rem_idx = int(rem_time / h.dt)
        
        with h5py.File(params["file_results"], 'w') as h5file:
            
            t_sim = t_sim[rem_idx:]-rem_time 
            h5file.create_dataset("time", data = t_sim)
            
            extracellular_group = h5file.create_group("extracellular")
            ele_group = extracellular_group.create_group('electrode_1')
            lfp_group = ele_group.create_group('lfp')
            
            lfp_group_origin = lfp_group.create_group('origin_data')
            lfp_group_origin.attrs['SamplingRate'] = 1000 / h.dt   # dt in ms 
            
            
            for idx_el, lfp in enumerate(lfp_data):
                lfp_group_origin.create_dataset("channel_" + str(idx_el+1), data = lfp[rem_idx:] )
            
            firing_group = h5file.create_group("extracellular/electrode_1/firing/origin_data")
            
            
            for celltype in set(params["celltypes"]):
                cell_friring_group = firing_group.create_group(celltype)
            
            
                for cell_idx, sp_times in enumerate(spike_trains):
                    if params["celltypes"][cell_idx] != celltype:
                        continue
                    
                    sp_times = sp_times[sp_times >= rem_time] - rem_time
          
                    cell_friring_group.create_dataset("neuron_" + str(cell_idx+1), data=sp_times) # cell_spikes_dataset 
            
    
    
            intracellular_group = h5file.create_group("intracellular")
            intracellular_group_origin = intracellular_group.create_group("origin_data")
            
            for soma_v_idx in params["save_soma_v"]["vect_idxes"]: 
                soma_v = soma_v_list[soma_v_idx]
                
                if soma_v.size == 0: continue
                
                soma_v_dataset = intracellular_group_origin.create_dataset("neuron_" + str(soma_v_idx+1), data=soma_v[rem_idx:] )
                
                cell_type = params["celltypes"][soma_v_idx]
                soma_v_dataset.attrs["celltype"] = cell_type
    
 
    
        
    print("End of the simultion!")
    pc.done()
    h.quit()
    
    
    
    return
