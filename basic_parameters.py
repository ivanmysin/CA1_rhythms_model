import numpy as np
"""
pyr - CA1 piramidal cells
olm - Oriens-Lacunosum/Moleculare (OLM) Cells
pvbas - parvalbumin positive basket cells
cckbas - cholecystokinin positive basket cells
ivy - Ivy cells
ngf - neurogliaform cells
bis - bistratifered cells
aac - axo-axonal cells
csa - Schaffer collateral-associated cells


ca3 - CA3 pyramidal cells
mec - stellate cells of the medial entorhinal cortex
lec - FAN cells of the lateral entorhinal cortex


"""


basic_params = {
    "Nelecs" : 3,      # number of electrodes
    "PyrDencity" : 0.2, # pyramidal cells / micrometer^2
    
    "file_results":  "../../Data/CA1_simulation/test.hdf5", # None, #
    "duration" : 250, # simulation time
    
    "celltypes" : [],
    
    "CellNumbers" : {
        "Npyr" : 1,    # 
        "Npvbas" : 1,
        "Nolm" : 0,
        "Ncckbas" : 0,
        "Nivy" : 0,
        "Nngf" : 0,
        "Nbis" : 0,
        "Naac" : 0,
        "Nsca" : 0,
        
        
        "Nca3" : 1,
        "Nmec" : 1,
        "Nlec" : 1,
        "Nmsteevracells" : 1,
        "Nmskomalicells" : 1,
    },
    
    "save_soma_v" : {
        "pyr" : [0, ],
        "pvbas" : [0, ],
        "olm" : [0, ],
        "cckbas" : [0, ],
        "ivy" : [0, ],
        "ngf" : [0, ],
        "bis" : [0, ],
        "aac" : [0, ],
        "sca" : [0, ],
    
        "vect_idxes" : [],
    
    },


    "connections" : {
        "ca32pyr": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.05,
            "gmax_std" : 0.0001,

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },
        
        "ca32pvbas": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.05,
            "gmax_std" : 0.0001,

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },
        

    }, # end of connetion settings

}


cell_types_in_model = []

for celltype, numbers in sorted(basic_params["CellNumbers"].items()):
    
    celltype = celltype[1:]
    cell_types_in_model.extend( [celltype, ] * numbers )

basic_params["celltypes"] = cell_types_in_model



save_soma_v_idx = np.empty(shape=0, dtype=np.int)
for celltype, list_idx in basic_params["save_soma_v"].items(): 
    
    
    indices = [i for i, x in enumerate(basic_params["celltypes"]) if x == celltype]
    if len(indices) == 0:
        continue

    indices = np.asarray(indices)
    list_idx = np.asarray(list_idx)
    
    save_soma_v_idx = np.append(save_soma_v_idx, indices[list_idx])
    
    
basic_params["save_soma_v"]["vect_idxes"] = save_soma_v_idx

# print(save_soma_v_idx)



"""
"pyr2pvbas" : {
            "prob" : 1.0,
            "tau_rise" : 0.5,
            "tau_decay" : 5.0,
            
            "delay" : 1.0,
            "delay_std" : 0.2,
            
            "Erev" : 0.0,
            "gmax" : 0.05,
            "gmax_std" : 0.0001,
            
            "sourse_compartment" : "axon",
            "target_compartment" : "dend",
            
            
        },
        
        "cckbas2pvbas": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.005,
            "gmax_std" : 0.0001,
            
            "sourse_compartment" : "acell",
            "target_compartment" : "dend",
        },
        
    "pyr2olm": {
        "prob": 0.5,
        "tau_rise": 0.5,
        "tau_decay": 5.0,
        "delay": 1.0,
        "Erev": 0.0,
        "gmax": 0.01,
        
        "sourse_compartment" : "soma",
        "target_comartment" : "dend",
    },


    "pyr2cckbas": {
        "prob": 0.5,
        "tau_rise": 0.5,
        "tau_decay": 5.0,
        "delay": 1.0,
        "Erev": 0.0,
        "gmax": 0.01,
    },



    
    
    "pvbas2pvbas" : {
    
        "prob" : 0.5,
        "tau_rise" : 0.5,
        "tau_decay" : 5.0,
        "delay" : 1.0,
        "Erev" : -70.0,
        "gmax" : 0.1,
    
    },
"""
