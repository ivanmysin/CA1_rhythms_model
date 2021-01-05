import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0 as bessel

RNG = np.random.default_rng()

def r2kappa(R):
    if R < 0.53:
        kappa = 2 * R + R**3 + 5/6 * R**5

    elif R >= 0.53 and R < 0.85:
        kappa = -0.4 + 1.39 * R + 0.43 / (1 - R)

    elif R >= 0.85:
        kappa = 1 / (3*R - 4*R**2 + R**3)


    I0 = bessel(kappa)

    return kappa, I0



def set_test_connections(h, conndata, pre_name, phase, cell, basic_params):
    
    generators = []
    synapses = []
    connections = []
    
    # Ray length of generators
    try:
        Rgens = basic_params[pre_name]["R"]
        freqs = basic_params[pre_name]["freqs"]
        spike_rate = basic_params[pre_name]["spike_rate"]
    except KeyError: 
        Rgens = 0.4
        freqs = 5
        spike_rate = 5
    
    kappa, I0 = r2kappa(Rgens)
    
    Nsourses = int( basic_params["CellNumbers"]["N"+pre_name] * conndata["prob"] )

    
    delay_mean = np.log(conndata["delay"])
    delay_sigma = conndata["delay_std"]

    gmax_mean = np.log(conndata["gmax"])
    gmax_sigma = conndata["gmax_std"]
    
    post_name = conndata["target_compartment"]
    
    post_list = getattr(cell, post_name)
    len_postlist = sum([1 for _ in post_list])
    
    
    for idx in range(Nsourses):
        
        if len_postlist == 1:
            post_idx = 0
        else:
            post_idx = np.random.randint(0, len_postlist-1)
        for idx, post_comp_tmp in enumerate(post_list):
            if idx == post_idx: post_comp = post_comp_tmp
        
        gen = h.ArtifitialCell(0, 0)
        gen.acell.mu = phase
        gen.acell.latency = 1
        gen.acell.freqs = 5
        gen.acell.spike_rate = 5
        gen.acell.kappa = kappa
        gen.acell.I0 = I0
        gen.acell.myseed = np.random.randint(0, 1000000, 1)

        syn = h.Exp2Syn( post_comp(0.5) ) 
        syn.e = conndata["Erev"]
        syn.tau1 = conndata["tau_rise"]
        syn.tau2 = conndata["tau_decay"]
            
        conn = h.NetCon(gen.acell, syn, sec=post_comp)
                    
        conn.delay = RNG.lognormal(delay_mean, delay_sigma)  
        conn.weight[0] = RNG.lognormal(gmax_mean, gmax_sigma)  
            
            
        generators.append(gen)
        synapses.append(syn)
        connections.append(conn)
    
    
    
    return generators, synapses, connections
    

def get_grid_centers(grid_w, grid_phase, duration):

    n_max = int (2 * (grid_w * duration + grid_phase / (2 * np.pi) + 1) )
    n = np.arange(0, n_max)
    tgrid = (n + grid_phase / (2 * np.pi)) / grid_w
    
    tgrid = tgrid[(tgrid >= 0)&(tgrid <= duration)]
   
 
    return tgrid
    
    
    
    
    
    
    
