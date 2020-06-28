import numpy as np
import matplotlib.pyplot as plt


def run_simulation(params, h):

    
    neurons = h.List()


    for idx in range(params["Npyr"]):
        cell = h.poolosyncell(0, 0)

        neurons.append(cell)

    for idx in range(params["Npvbas"]):
        cell = h.pvbasketcell(0, 0)
        neurons.append(cell)

    for idx in range(params["Nolm"]):
        cell = h.olmcell(0, 0)
        neurons.append(cell)

    for idx in range(params["Ncckbas"]):
        cell = h.cckcell(0, 0)
        neurons.append(cell)

    for idx in range(params["Nivy"]):
        cell = h.ivycell(0, 0)
        neurons.append(cell)

    for idx in range(params["Nngf"]):
        cell = h.ngfcell(0, 0)
        neurons.append(cell)

    for idx in range(params["Nbis"]):
        cell = h.bistratifiedcell(0, 0)
        neurons.append(cell)

    for idx in range(params["Naac"]):
        cell = h.axoaxoniccell(0, 0)
        neurons.append(cell)

    for idx in range(params["Nsca"]):
        cell = h.scacell(0, 0)
        neurons.append(cell)

    
    connections = h.List()
    synapses = h.List()
    # set connection
    for pre_idx, presynaptic_cell in enumerate(neurons):
        
        # print(presynaptic_cell.celltype)
        for post_idx, postsynaptic_cell in enumerate(neurons):
            
            if pre_idx == post_idx:
                continue
                       
            try:
                
                conn_name = presynaptic_cell.celltype + "2" + postsynaptic_cell.celltype
                conn_data = params[conn_name]
                
            except AttributeError:
                continue
            except KeyError:
                continue

            
            print(conn_name)
            
            pre_comp = getattr( presynaptic_cell, conn_data["sourse_compartment"] )[0]
            post_comp = getattr( postsynaptic_cell, conn_data["target_compartment"] )[0]
            print(pre_comp)
            
            syn = h.Exp2Syn( post_comp(0.5) ) # !!!!
            syn.e = conn_data["Erev"]
            syn.tau1 = conn_data["tau_rise"]
            syn.tau2 = conn_data["tau_decay"]
                

            
            conn = h.NetCon(pre_comp(0.5)._ref_v, syn, sec=pre_comp) # !!!!
                       
            conn.delay = conn_data["delay"]
            conn.weight[0] = conn_data["gmax"] 
               
            connections.append(conn)
            synapses.append(syn)


    
    cell1 = neurons[0]
    cell2 = neurons[1]
    
    
 
    stim1 = h.IClamp(0.5, sec=cell1.soma[0])
    stim1.dur   = 100
    stim1.delay = 0
    stim1.amp = 0.5

    # stim2 = h.IClamp(0.5, sec=cell2.soma[0])
    # stim2.dur   = 100
    # stim2.delay = 0
    # stim2.amp = 0.8
    
    
    
    soma1_v = h.Vector()
    soma1_v.record(cell1.soma[0](0.5)._ref_v)

    soma2_v = h.Vector()
    soma2_v.record(cell2.soma[0](0.5)._ref_v)

    


    t = h.Vector()
    t.record(h._ref_t)

    # run simulation
    h.tstop = 100 # set the simulation time
    h.run()
    
    plt.plot(t, soma1_v, color="blue", label="Pyr")
    plt.plot(t, soma2_v, color="red", label="PVBas")
    plt.legend()
    plt.show()
    
    
    print("End of the simultion!")
    return
