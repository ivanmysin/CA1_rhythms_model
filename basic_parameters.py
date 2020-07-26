
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
    
    "file_results":  "/home/ivan/Data/CA1_simulation/test.hdf5", # None, #
    
    "celltypes" : [],
    
    "CellNumbers" : {
        "Npyr" : 2,
        "Npvbas" : 2,
        "Nolm" : 2,
        "Ncckbas" : 2,
        "Nivy" : 0,
        "Nngf" : 0,
        "Nbis" : 0,
        "Naac" : 0,
        "Nsca" : 0,
        
        
        "Nca3" : 1,
        "Nmec" : 1,
        "Nlec" : 1,
        "Nmsteevracells" : 2,
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
    
    
    
    },


    "connections" : {
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
            "gmax": 0.005,
            "gmax_std" : 0.0001,
            
            "sourse_compartment" : "acell",
            "target_compartment" : "dend",
        },

    },

}


cell_types_in_model = []

for celltype, numbers in sorted(basic_params["CellNumbers"].items()):
    
    celltype = celltype[1:]
    cell_types_in_model.extend( [celltype, ] * numbers )

basic_params["celltypes"] = cell_types_in_model



# print(cell_types_in_model)



"""
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
