import numpy as np
import presimulation_lib as prelib
from copy import deepcopy
import mpi4py
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

ca3_spatial - CA3 pyramidal cells with place cells dynamics
ca3_non_spatial - CA3 pyramidal cells without place cells dynamics

mec - stellate cells of the medial entorhinal cortex
lec - FAN cells of the lateral entorhinal cortex


"""

def get_basic_params():

    Nelecs = 1 # number of electrodes

    basic_params = {
        "elecs" : {
            "el_x" : np.zeros(Nelecs),
            "el_y" : np.zeros(Nelecs), # np.linspace(-200, 600, Nelecs),
            "el_z" : np.zeros(Nelecs),
        },
        "PyrDencity" : 0.2, # pyramidal cells / micrometer^2

        "file_results":  "../../Data/CA1_simulation/test.hdf5", # None, #
        "duration" : 3000, # 10000 # 10 sec simulation time
        
        "del_start_time" : 0, # 400, # time after start for remove
        
        
        "CellNumbersInFullModel" : {
            "Npyr" :   9000,
            "Npvbas" : 200,
            "Nolm" :   80,
            "Ncckbas" : 160,
            "Nivy" :    260,
            "Nngf" :    130,
            "Nbis" :    70,
            "Naac" :    60,
            "Nsca" :    40,
            
            
            "Nca3_spatial" : 3500,
            "Nca3_non_spatial" : 3500,
            "Nmec" : 9000, 
            "Nlec" : 9000,  
            "Nmsteevracells" : 200,
            "Nmskomalicells" : 200,
            "Nmsach"         : 150,
        },
        
        "CellNumbers" : {
            "Npyr" : 1400,
            "Npvbas" :  200,
            "Nolm" : 80,
            "Ncckbas" : 160,
            "Nivy" :  260, # 130,
            "Nngf" :  130, # 65,
            "Nbis" :  70, # 35,
            "Naac" :  60, # 30,
            "Nsca" :  40, # 20,
            
            
            "Nca3_spatial" :  3500,
            "Nca3_non_spatial" :  3500,
            "Nmec" : 3500, # 3500
            "Nlec" : 0, ## 500,
            "Nmsteevracells" :  200,
            "Nmskomalicells" : 0, #200,
            "Nmsach"         :  150,
        },
        
        "CellParameters" : {
            "ca3_spatial" : {
                "cellclass" : "ArtifitialPlaceCell",
                "Rtheta" : 0.4,
                "low_mu" : 1.5,

                "Rgamma" : 0.6,
                "high_mu" : 0.0,

                "spike_rate" : 1000000.0,   # 100000.0,
                "latency" : 10.0,

                "place_center_t" : 500,
                "place_t_radius" : 1500, # 
            
                "low_freqs" : 5.0,
                "high_freqs" : 30.0,

                "delta_t" : 0.2,
            },
            
            "ca3_non_spatial" : {
                "cellclass" : "ArtifitialCell",
                "R" : 0.4,
                "mu" : 1.5,
                "freqs" : 5.0,
                "spike_rate" : 5.0,   # 100000.0,
                "latency" : 10.0,
                "delta_t" : 0.2,
                
                
            },
            
            "mec" : {
                "cellclass" : "ArtifitialGridCell",  # "ArtifitialPlaceCell", #  

                "Rtheta": 0.4,
                "low_mu": 1.5,

                "Rgamma": 0.6,
                "high_mu": 0.0,

                "spike_rate": 100000.0,  # 100000.0,
                "latency": 10.0,

                "delta_t" : 0.2,
                
                "low_freqs" : 5.0,
                "high_freqs" : 110.0,
                
                "Rgrid" : 0.8,
                "grid_freqs" : 0.5,
                "grid_phase" : 0, 
            },
            
            "lec" : {
                "cellclass" : "ArtifitialCell",
                "R" : 0.1,
                "mu" : 0.0,
                "freqs" : 5.0,
                "latency" : 10.0,
                "spike_rate": 5.0,  
                
                "delta_t" : 0.2,  
            },
            
            "msteevracells" : {
                "cellclass" : "ArtifitialCell",
                "R" : 0.6,
                "mu" : np.pi,
                "freqs" : 5.0,
                "latency" : 4.0,
                "spike_rate": 15.0,
                
                "delta_t" : 0.2,   
            },
            
            "mskomalicells" : {
                "cellclass" : "ArtifitialCell",
                "R" : 0.6,
                "mu" : 0.0,  # !!!!
                "freqs" : 5.0,
                "latency" : 4.0,
                "spike_rate": 15.0,  
                
                "delta_t" : 0.2, 
            },
            
            "msach" : {
                "cellclass" : "ArtifitialCell",
                "R" : 0.4,
                "mu" : np.pi,  # !!!!
                "freqs" : 5.0,
                "latency" : 10.0,
                "spike_rate": 3.0,
                
                "delta_t" : 0.2,     
            },
            
            "pyr" : {
                "cellclass" : "CA1PyramidalCell", # "poolosyncell", # 
                "iext" : 0.0, # 0.002,
                "iext_std" : 0.0002,
            },
            
            "pvbas" : {
                "cellclass" : "pvbasketcell",
                "iext" : 0.0,
                "iext_std" : 0.0002,
            },
            
            "cckbas" : {
                "cellclass" : "cckcell",
                "iext" : 0.002, #!!! 0.003,
                "iext_std" : 0.004,
            },

            "olm" : {
                "cellclass" : "olmcell",
                "iext" : 0.0,
                "iext_std" : 0.002,
            },
            
            "aac" : {
                "cellclass" : "axoaxoniccell",
                "iext" : 0.0,
                "iext_std" : 0.0002,
            },
            
            "ngf" : {
                "cellclass" : "ngfcell",
                "iext" : 0.002,
                "iext_std" : 0.002,
            },
            
            "ivy" : {
                "cellclass" : "ivycell",
                "iext" : 0.002,
                "iext_std" : 0.002,
            },
        
            "bis" : {
                "cellclass" : "CA1BistratifiedCell", # "bistratifiedcell",
                "iext" : 0.005,
                "iext_std" : 0.002,
            },
            
            "sca" : {
                "cellclass" : "scacell",
                "iext" : 0.001,
                "iext_std" : 0.002,
            },
        
        },
        
        "save_soma_v" : {
            "pyr" :  [0, ] , # [range(20, 30)],    # [0, ],
            "pvbas" : [0, ], #
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
            
            # connection to pyramidal neurons
            "ca3_spatial2pyr": {
                "gmax": 20, # 0.016,
                "gmax_std" : 0.002,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.06,
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "rad_list",

                "NMDA" : {
                    "gNMDAmax" : 0.01, # mS
                    "gmax_std" : 0.001,
                    "tcon" : 2.3,   # ms
                    "tcoff" : 95.0, # ms
                    "enmda" : 0,
                },
            },
            
            "ca3_non_spatial2pyr": {
                "gmax": 0.016,
                "gmax_std" : 0.002,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.06,
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "rad_list",

                "NMDA" : {
                    "gNMDAmax" : 0.01, # mS
                    "gmax_std" : 0.001,
                    "tcon" : 2.3,   # ms
                    "tcoff" : 95.0, # ms
                    "enmda" : 0, 
                },
            },
            
           "mec2pyr": {
                "gmax": 80, # 8, #0.1, # 0.06,
                "gmax_std" : 0.007,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.06,
                
                "delay": 10,
                "delay_std" : 2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "lm_list",
                # "NMDA" : {
                #     "gNMDAmax" : 0.01, # mS
                #     "gmax_std" : 0.001,
                #     "tcon" : 2.3,   # ms
                #     "tcoff" : 95.0, # ms
                #     "enmda" : 0,
                # },
            },
            
            "lec2pyr": {  # need to optimize
                "gmax": 0.06,
                "gmax_std" : 0.007,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.07,
                
                "delay": 10,
                "delay_std" : 2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "lm_list",
            },
            

            "pyr2pyr": {
                "gmax": 5.0, # 0.01,
                "gmax_std" : 0.007,

                "Erev": 0.0,
                "tau_rise": 0.1,
                "tau_decay": 1.5,

                "prob": 0.009,

                "delay": 1.2,
                "delay_std" : 0.2,


                "sourse_compartment" : "axon",
                "target_compartment" : "basal_list",
                
                "NMDA" : {
                    "gNMDAmax" : 0.05, # mS
                    "gmax_std" : 0.001,
                    "tcon" : 2.3,   # ms
                    "tcoff" : 95.0, # ms
                    "enmda" : 0, 
                },
            },
            
            "cckbas2pyr": {
                "gmax": 2.5,
                "gmax_std" : 1.2,
                
                "Erev": -75,
                "tau_rise": 0.2,
                "tau_decay": 4.2,

                "prob": 0.63,
                
                "delay": 2.5,
                "delay_std" : 1.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "soma_list",
            },

          
           "ivy2pyr": {
                "gmax": 0.053,
                "gmax_std" : 0.02,
                
                "Erev": -75,
                "tau_rise": 1.1,
                "tau_decay": 11,

                "prob": 0.13,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "lm_list",
            },
            
            
           "aac2pyr": {
                "gmax": 20.5,
                "gmax_std" : 10,

                "Erev": -75,
                "tau_rise": 0.28,
                "tau_decay": 8.4,

                "prob": 0.29,

                "delay": 1.2,
                "delay_std" : 0.2,


                "sourse_compartment" : "soma",
                "target_compartment" : "axon_list",
            },
            
           "olm2pyr": {
                "gmax": 1.7,
                "gmax_std" : 0.9,
                
                "Erev": -75,
                "tau_rise": 0.13,
                "tau_decay": 11,

                "prob": 0.29,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "lm_list",
            },
            
           "pvbas2pyr": {
                "gmax": 20.0, # 0.05,
                "gmax_std" : 0.025,
                
                "Erev": -75,
                "tau_rise": 0.3,
                "tau_decay": 6.2,

                "prob": 0.29,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "soma_list",
            },
            
           "bis2pyr": {
                "gmax": 0.009,
                "gmax_std" : 0.005,

                "Erev": -75,
                "tau_rise": 0.11,
                "tau_decay": 9.7,

                "prob": 0.14,

                "delay": 1.2,
                "delay_std" : 0.2,


                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },

           "ngf2pyr": {
                "gmax": 0.098,
                "gmax_std" : 0.05,

                "Erev": -75,
                "tau_rise": 9,
                "tau_decay": 39,

                "prob": 0.29,

                "delay": 1.2,
                "delay_std" : 0.2,


                "sourse_compartment" : "soma",
                "target_compartment" : "lm_list",
            },

           "sca2pyr": {
                "gmax": 0.098, # 3 
                "gmax_std" : 0.05,

                "Erev": -75,
                "tau_rise": 0.3,
                "tau_decay": 6.2,

                "prob": 0.29,

                "delay": 1.2,
                "delay_std" : 0.2,


                "sourse_compartment" : "soma",
                "target_compartment" : "rad_list",
            },
            # end connection to pyramids
            
            # connection to pvbas
            "ca3_spatial2pvbas": {
                "gmax": 7.0, # 0.7,
                "gmax_std" : 0.2,
                
                "Erev": 0,
                "tau_rise": 2.0,
                "tau_decay": 6.3,

                "prob": 0.05, # 0.02
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
                
                #"NMDA" : {
                #    "gNMDAmax" : 0.01, # mS
                #    "gmax_std" : 0.001,
                #    "tcon" : 2.3,   # ms
                #    "tcoff" : 95.0, # ms
                #    "enmda" : 0, 
                #},
            },
            
            "ca3_non_spatial2pvbas": {
                "gmax": 0.7,
                "gmax_std" : 0.1,
                
                "Erev": 0,
                "tau_rise": 2.0,
                "tau_decay": 6.3,

                "prob": 0.05,
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
                
                #"NMDA" : {
                #    "gNMDAmax" : 0.01, # mS
                #    "gmax_std" : 0.001,
                #    "tcon" : 2.3,   # ms
                #    "tcoff" : 95.0, # ms
                #    "enmda" : 0, 
                #},
            },
            
            "pyr2pvbas": {
                "gmax": 0.5,  # !!! 0.05,
                "gmax_std" : 0.04,
                
                "Erev": 0,
                "tau_rise": 0.07,
                "tau_decay": 0.2,

                "prob": 0.13,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "axon",
                "target_compartment" : "dendrite_list",
                
                #"NMDA" : {
                #    "gNMDAmax" : 0.01, # mS
                #    "gmax_std" : 0.001,
                #    "tcon" : 2.3,   # ms
                #    "tcoff" : 95.0, # ms
                #    "enmda" : 0, 
                #},
            },
            
            "pvbas2pvbas": {
                "gmax": 800, # 0.08, # 0.05 # !!!! 0.023,
                "gmax_std" : 0.01, #  0.01,
                
                "Erev": -75,
                "tau_rise": 0.8,
                "tau_decay": 4.8,

                "prob": 0.7,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "soma",
            },
            
            "cckbas2pvbas": {
                "gmax": 10.0, #!!! 1.0,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.43,
                "tau_decay": 4.49,

                "prob": 0.38,
                
                "delay": 4.5,
                "delay_std" : 2.0,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "soma",
            },
            
            "olm2pvbas": {
                "gmax": 0.73,
                "gmax_std" : 0.35,
                
                "Erev": -75,
                "tau_rise": 0.25,
                "tau_decay": 7.5,

                "prob": 0.2, # optimized
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            # hypotetical connections
            "bis2pvbas": {
                "gmax": 1.1,
                "gmax_std" : 0.05,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "ngf2pvbas": {
                 "gmax": 1.0,
                 "gmax_std" : 0.05,
            
                 "Erev": -75,
                 "tau_rise": 0.5,
                 "tau_decay": 4.0,
            
                 "prob": 0.5,
            
                 "delay": 1.2,
                 "delay_std" : 0.2,
            
            
                 "sourse_compartment" : "soma",
                 "target_compartment" : "dendrite_list",
             },
            
            "ivy2pvbas": {
                "gmax": 1.1,
                "gmax_std" : 0.5,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "sca2pvbas": {
                 "gmax": 1.1,
                 "gmax_std" : 0.05,
            
                 "Erev": -75,
                 "tau_rise": 0.5,
                 "tau_decay": 4.0,
            
                 "prob": 0.5,
            
                 "delay": 1.2,
                 "delay_std" : 0.2,
            
            
                 "sourse_compartment" : "soma",
                 "target_compartment" : "dendrite_list",
            },
            
            # end connection to pvbas
            
            # connections to cckbas
            "msteevracells2cckbas" : {
                "gmax" : 0.5, # !!!! 
                "gmax_std" : 0.5, # !!!!
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 5.0,
                
                "prob": 0.5,
                
                "delay": 10.5,
                "delay_std" : 2.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "pvbas2cckbas": {
                "gmax": 1.5, #!!! 1.0
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.29,
                "tau_decay": 2.67,

                "prob": 0.15,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "soma",
            },
            
           
           "cckbas2cckbas": {
                "gmax": 0.5, #  0.2, # 
                "gmax_std" : 0.2, 
                
                "Erev": -75,
                "tau_rise": 0.2,
                "tau_decay": 4.2,

                "prob": 0.63,
                
                "delay": 2.7,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            
            # hypotetical connections
            "olm2cckbas": {
               "gmax": 1.0,
               "gmax_std" : 0.7,
               
               "Erev": -75,
               "tau_rise": 0.5,
               "tau_decay": 4.0,

              "prob": 0.2, 
                
               "delay": 1.2,
               "delay_std" : 0.2,
                

               "sourse_compartment" : "soma",
               "target_compartment" : "dendrite_list",
            },
            
            "bis2cckbas": {
                "gmax": 1.0,
                "gmax_std" : 0.7,
                
               "Erev": -75,
               "tau_rise": 0.5,
               "tau_decay": 4.0,

              "prob": 0.2, 
                
               "delay": 1.2,
               "delay_std" : 0.2,
                

               "sourse_compartment" : "soma",
               "target_compartment" : "dendrite_list",
            },
            
            "ngf2cckbas": {
                "gmax": 2.5,
                "gmax_std" : 0.7,
            
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,
            
                "prob": 0.2,
            
                "delay": 1.2,
                "delay_std" : 0.2,
                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            #"ivy2cckbas": {
            #    "gmax": 0.5,
            #    "gmax_std" : 0.2,
            #    "Erev": -75,
            #    "tau_rise": 0.5,
            #    "tau_decay": 4.0,

            #    "prob": 0.2,

            #    "delay": 1.2,
            #    "delay_std" : 0.2,

            #    "sourse_compartment" : "soma",
            #    "target_compartment" : "dendrite_list",
            #},
            
            # end connections to cckbas
            
            
            # connections to aac
            "msteevracells2aac" : {
                "gmax" : 1.5, # !!!! 
                "gmax_std" : 0.7, # !!!!
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 3,
                
                "prob": 0.5,
                
                "delay": 10.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "soma",
            },
            
            "pyr2aac": {
                "gmax": 0.04,
                "gmax_std" : 0.02,
                
                "Erev": 0,
                "tau_rise": 0.3,
                "tau_decay": 0.6,

                "prob": 0.07,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "axon",
                "target_compartment" : "dendrite_list",
            },
            
            "ca3_spatial2aac": {
                "gmax": 0.7,
                "gmax_std" : 0.2,
                
                "Erev": 0,
                "tau_rise": 2,
                "tau_decay": 6.3,

                "prob": 0.01,
                
                "delay": 2.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            "ca3_non_spatial2aac": {
                "gmax": 0.7,
                "gmax_std" : 0.2,
                
                "Erev": 0,
                "tau_rise": 2,
                "tau_decay": 6.3,

                "prob": 0.01,
                
                "delay": 2.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            
            # hypotetical connections
            "mec2aac": {
                "gmax": 0.1,
                "gmax_std" : 0.05,
                
                "Erev": 0,
                "tau_rise": 2,
                "tau_decay": 6.3,

                "prob": 0.04,
                
                "delay": 8.0,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "lec2aac": {
                "gmax": 0.1,
                "gmax_std" : 0.05,
                
                "Erev": 0,
                "tau_rise": 2,
                "tau_decay": 6.3,

                "prob": 0.003,
                
                "delay": 8.0,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "olm2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "bis2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "pvbas2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, # 0.8, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "cckbas2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "ivy2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "sca2aac": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.1, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            # end connections to aac
            
            # connections to olm
            "msach2olm" : {
                "gmax" : 0.5, 
                "gmax_std" : 0.1,
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,
                
                "prob": 0.05,
                
                "delay": 10.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "soma",
            },

           "pyr2olm": {
                "gmax": 0.031,
                "gmax_std" : 0.0015,
                
                "Erev": 0,
                "tau_rise": 0.3,
                "tau_decay": 0.6,

                "prob": 0.081,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "axon",
                "target_compartment" : "dendrite_list",
            },
           
           
           # hypotetical connections
           "ivy2olm": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
           
           "sca2olm": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            # end connections to olm
            
            # connections to bis
           "pyr2bis": {
                "gmax": 0.14,
                "gmax_std" : 0.07,
                
                "Erev": 0,
                "tau_rise": 1.3,
                "tau_decay": 8.0,

                "prob": 0.14,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "axon",
                "target_compartment" : "dendrite_list",
            },
            
           "pvbas2bis": {
                "gmax": 0.035,
                "gmax_std" : 0.015,
                
                "Erev": -75,
                "tau_rise": 0.29,
                "tau_decay": 2.67,

                "prob": 0.2,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "cckbas2bis": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "sca2bis": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.05,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            # hypotetical connetions to bis
            
            
            # end connections to bis
            "bis2bis": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            # connections to ivy    
           "pyr2ivy": {
                "gmax": 0.041,
                "gmax_std" : 0.021,
                
                "Erev": 0,
                "tau_rise": 0.3,
                "tau_decay": 0.6,

                "prob": 0.13,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "axon",
                "target_compartment" : "dendrite_list",
            },
            
            # hypotetical connections
            "ivy2ivy": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },

            "pvbas2ivy": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.5, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },

            "cckbas2ivy": {
                "gmax": 0.5,
                "gmax_std" : 0.07,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.1, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "sca2ivy": {
                "gmax": 1.5,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.1, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
             # end connections to ivy
            
           
            # connections to ngf
            "ca3_spatial2nfg": {
                "gmax": 1.42,
                "gmax_std" : 0.6 ,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.05, #!! 0.1,
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "ca3_non_spatial2nfg": {
                "gmax": 1.42,
                "gmax_std" : 0.6 ,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.05, #!! 0.1,
                
                "delay": 1.5,
                "delay_std" : 0.5,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "mec2ngf": {
                "gmax": 0.7,
                "gmax_std" : 0.3,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.2, # ! need to optimize
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "lec2ngf": {
                "gmax": 0.7,
                "gmax_std" : 0.3,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 3,

                "prob": 0.05, # ! need to optimize
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "olm2ngf": {
                "gmax": 2.5, #!! 1.27,
                "gmax_std" : 0.6,
                
                "Erev": -75,
                "tau_rise": 1.3,
                "tau_decay": 10.2,

                "prob": 0.2,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
           "ngf2ngf": {
                "gmax": 0.75,
                "gmax_std" : 0.7,
                
                "Erev": -75,
                "tau_rise": 3.1,
                "tau_decay": 42,

                "prob": 0.7,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
     
            # no hypotetical connections
            # end of connections to ngf
            
            
            # connections to sca
           "olm2sca": {
                "gmax": 1.3,
                "gmax_std" : 0.6,
                
                "Erev": -75,
                "tau_rise": 0.07,
                "tau_decay": 29,

                "prob": 0.1,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            

           "sca2sca": {
                "gmax": 0.03,
                "gmax_std" : 0.015,
                
                "Erev": -75,
                "tau_rise": 4 ,
                "tau_decay": 34.3,

                "prob": 0.3,
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            # hypotetical connections
            "ca3_spatial2sca": {
                "gmax": 0.05,
                "gmax_std" : 0.02,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.09, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "ca3_non_spatial2sca": {
                "gmax": 0.05,
                "gmax_std" : 0.02,
                
                "Erev": 0,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.09, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "acell",
                "target_compartment" : "dendrite_list",
            },
            
            "ivy2sca": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.1, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "ngf2sca": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.2, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
            
            "bis2sca": {
                "gmax": 0.5,
                "gmax_std" : 0.2,
                
                "Erev": -75,
                "tau_rise": 0.5,
                "tau_decay": 4.0,

                "prob": 0.1, 
                
                "delay": 1.2,
                "delay_std" : 0.2,
                

                "sourse_compartment" : "soma",
                "target_compartment" : "dendrite_list",
            },
      

        }, # end of connetion settings
        
        "gap_junctions_params" : {
            "pvbas2pvbas" : {
                "r" : 1e5, # 100000 1e5
                "r_std" : 1e4,
                "prob": 0.1,
                "compartment1" : "dendrite_list",
                "compartment2" : "dendrite_list",
            },
            
            "ngf2ngf" : {
                "r" : 1e5, # 1e5
                "r_std" : 1e3,
                "prob": 0.7,
                "compartment1" : "dendrite_list",
                "compartment2" : "dendrite_list",
            },
        },

    }
    
    return basic_params

def get_object_params(Nthreads=1):
    basic_params = get_basic_params()

    OBJECTS_PARAMS = []
    for _ in range(Nthreads):
        thread_param = {
            "neurons" : [],
            "save_soma_v" : None,
            "gids_of_celltypes" : [],
            "synapses_params" : [],
            "gap_junctions" : [],
            "common_params" : {},
        }

        OBJECTS_PARAMS.append(thread_param)

    cell_types_in_model = []
    gids_of_celltypes = {}

    for celltype, numbers in sorted(basic_params["CellNumbers"].items()):

        celltype = celltype[1:]
        start_idx = len(cell_types_in_model)
        cell_types_in_model.extend( [celltype, ] * numbers )
        end_idx = len(cell_types_in_model)
        gids_of_celltypes[celltype] = np.arange(start_idx, end_idx)
    
    Ncells = len(cell_types_in_model)
    
    
    neurons_by_threads = np.tile(np.arange(Nthreads), int(np.ceil(Ncells/Nthreads)) )
    neurons_by_threads = neurons_by_threads[:Ncells]
    # basic_params["celltypes"] = cell_types_in_model
    # print(neurons_by_threads)


    save_soma_v_idx = np.empty(shape=0, dtype=np.int)

    for celltype, list_idx in basic_params["save_soma_v"].items():

        if celltype == "vect_idxes": continue

        # list_idx = np.arange(basic_params["CellNumbers"]["N"+celltype] )
        
        indices = [i for i, x in enumerate(cell_types_in_model) if x == celltype]
        if len(indices) == 0:
            continue

        indices = np.asarray(indices)
        list_idx = np.asarray(list_idx)
        
        save_soma_v_idx = np.append(save_soma_v_idx, indices[list_idx])

    for th_idx in range(Nthreads):
        if th_idx == 0:
            OBJECTS_PARAMS[th_idx]["save_soma_v"] = save_soma_v_idx
        else:
            save_soma_v_idx_tmp = save_soma_v_idx[neurons_by_threads[save_soma_v_idx] == th_idx]
            OBJECTS_PARAMS[th_idx]["save_soma_v"] = save_soma_v_idx_tmp # !!!!!!!

        OBJECTS_PARAMS[th_idx]["gids_of_celltypes"] = np.arange(len(cell_types_in_model))[neurons_by_threads == th_idx]
    OBJECTS_PARAMS[0]["cell_types_in_model"] = cell_types_in_model

    for celltypename, cellparam in basic_params["CellParameters"].items():


        if cellparam["cellclass"] == "ArtifitialPlaceCell":
            Rtheta = cellparam["Rtheta"]
            Rgamma = cellparam["Rgamma"]

            theta_kappa, theta_i0 = prelib.r2kappa(Rtheta)
            gamma_kappa, gamma_i0 = prelib.r2kappa(Rgamma)
            cellparam["low_kappa"] = theta_kappa
            cellparam["high_kappa"] = gamma_kappa
            cellparam["low_I0"] = theta_i0
            cellparam["high_I0"] = gamma_i0

            cellparam["place_center_t"] = 500  # !!!!!
        
        elif cellparam["cellclass"] == "ArtifitialGridCell":
            Rtheta = cellparam["Rtheta"]
            Rgamma = cellparam["Rgamma"]
            Rgrid = cellparam["Rgrid"]

            theta_kappa, theta_i0 = prelib.r2kappa(Rtheta)
            gamma_kappa, gamma_i0 = prelib.r2kappa(Rgamma)
            grid_kappa, grid_I0 = prelib.r2kappa(Rgrid)
            
            cellparam["low_kappa"] = theta_kappa
            cellparam["high_kappa"] = gamma_kappa
            cellparam["low_I0"] = theta_i0
            cellparam["high_I0"] = gamma_i0
            
            cellparam["grid_kappa"] = grid_kappa
            cellparam["grid_I0"] = grid_I0

        elif cellparam["cellclass"] == "ArtifitialCell":
            Rgen = cellparam["R"]
            kappa, I0 = prelib.r2kappa(Rgen)
            cellparam["kappa"] = kappa
            cellparam["I0"] = I0
        
        else:
            continue


    Npyr = basic_params["CellNumbers"]["Npyr"]  
    Npvbas = basic_params["CellNumbers"]["Npvbas"]
    Nca3 = basic_params["CellNumbers"]["Nca3_spatial"]
    Nmec = basic_params["CellNumbers"]["Nmec"]


    pyr_coord_x = np.cumsum( np.zeros(Npyr) + 3 ) # np.zeros(Npyr) + 1500   # 
    pyr_coord_x[pyr_coord_x.size//2:] = np.nan

    pvbas_coord_x = np.cumsum( np.zeros(Npvbas) + 50)  #  50
    ca3_coord_x =  np.cumsum( np.zeros(Nca3) + 3 )

    mec_grid_phases = np.linspace(-np.pi, np.pi, Nmec)  # rad  !!!!!!!!!!!
    mec_grid_freqs = np.zeros(Nmec) + 0.5    # Hz


    ca3_coord_x_iter = iter(ca3_coord_x)
    mec_grid_phases_iter = iter(mec_grid_phases)
    mec_grid_freqs_iter = iter(mec_grid_freqs)

    # neurons_tmp = []
    for cell_idx, celltype in enumerate(cell_types_in_model):
        cell_param = basic_params["CellParameters"][celltype]
        
        neuron = {
            "celltype" : celltype, 
            "cellclass" : cell_param["cellclass"],
            "cellparams" : {},
            "gid" : cell_idx,
        }
        neuron["cellparams"] = deepcopy(cell_param)

            
        if cell_param["cellclass"] == "ArtifitialPlaceCell":
            neuron["cellparams"]["place_center_t"] = next(ca3_coord_x_iter)

        elif cell_param["cellclass"] == "ArtifitialGridCell":
            neuron["cellparams"]["grid_freqs"] = next(mec_grid_freqs_iter)
            neuron["cellparams"]["grid_phase"] = next(mec_grid_phases_iter)
            
        elif cell_param["cellclass"] == "ArtifitialCell":
            pass
        else:
            if cell_param["iext"] > 0:
                neuron["cellparams"]["iext"] = np.random.lognormal( np.log(cell_param["iext"]), cell_param["iext_std"]   )
            else:
                neuron["cellparams"]["iext"] = np.random.normal(cell_param["iext"], cell_param["iext_std"] )
            
            # if cell_idx == 4:
            #    neuron["cellparams"]["iext"] = 0.005




        th_idx = int(neurons_by_threads[cell_idx])
        OBJECTS_PARAMS[th_idx]["neurons"].append(neuron)




    var_conns_on_pyr = 100.0
    var_conns_on_pvbas =  var_conns_on_pyr * 3
    var_conns_pvbas2pvbas = var_conns_on_pyr * 50
    # synapses = []

    # Ncells = len( basic_params["celltypes"] )
    # Wpyrbas = np.zeros( [Ncells, Ncells],  dtype=np.float)


    for presynaptic_cell_idx, pre_celltype in enumerate(cell_types_in_model):
        for postsynaptic_cell_idx, post_celltype in enumerate(cell_types_in_model):
            dist_normalizer = 0


            if presynaptic_cell_idx == postsynaptic_cell_idx: continue

            try:
                conn_name = pre_celltype + "2" + post_celltype
                conn_data = basic_params["connections"][conn_name]
                    
            except AttributeError:
                continue
            except KeyError:
                continue
            
            number_connections = int( np.floor(conn_data["prob"]) )
            if (np.random.rand() < (conn_data["prob"] - number_connections) ):
                number_connections += 1

            gmax = conn_data["gmax"]

            if conn_name == "ca3_spatial2pyr":
                pyr_idx = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                pyr_coord = pyr_coord_x[pyr_idx]
                
                if not ( np.isnan(pyr_coord) ):
                    ca3_idx = presynaptic_cell_idx - gids_of_celltypes["ca3_spatial"][0]
                    dist = pyr_coord - ca3_coord_x[ca3_idx]
                    dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pyr ) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ) )


                    if dist_normalizer > 0.01:
                        number_connections += 1

                    gmax = gmax * dist_normalizer
               
                else:
                    gmax = basic_params["connections"]["ca3_non_spatial2pyr"]["gmax"]
                
                
            elif conn_name == "mec2pyr":
                pyr_idx = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                pyr_coord = pyr_coord_x[pyr_idx]
                
                if not ( np.isnan(pyr_coord) ):
                    mec_idx = presynaptic_cell_idx - gids_of_celltypes["mec"][0]
                    grid_freq = mec_grid_freqs[mec_idx]
                    grid_phase = mec_grid_phases[mec_idx]
                    grid_centers = 1000 * prelib.get_grid_centers(grid_freq, grid_phase, basic_params["duration"]*0.001)

                    gmax_tmp = 0
                    for cent in grid_centers:
                        dist = pyr_coord - cent

                        dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pyr ) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))
                        if dist_normalizer > 0.01:
                            number_connections += 1
                        gmax_tmp += gmax * dist_normalizer
                        
                    gmax = gmax_tmp
                    # if gmax > 0.5:
                    #     print(grid_phase)
                else:
                    gmax = 0.02 * gmax # !!!!!

                
            elif conn_name == "pyr2pyr":
                pyr_idx1 = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                pyr_idx2 = presynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                
                pyr_coord1 = pyr_coord_x[pyr_idx1]
                pyr_coord2 = pyr_coord_x[pyr_idx2]
                
                if not ( np.isnan(pyr_coord1) or  np.isnan(pyr_coord2) ):
                    dist = pyr_coord_x[pyr_idx1] - pyr_coord_x[pyr_idx2]
                    dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pyr ) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))
                    if dist_normalizer > 0.01:
                        number_connections += 1
                    gmax = gmax * dist_normalizer
                else:
                    gmax = gmax * 0.02 # !!!!!!!

            elif conn_name == "pvbas2pyr":
                pyr_idx = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                pyr_coord = pyr_coord_x[pyr_idx]
                
                if not ( np.isnan(pyr_coord) ):
                    
                    pvbas_idx = presynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
                    dist = pyr_coord - pvbas_coord_x[pvbas_idx]
                    dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pyr ) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))

                    # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer

                    if dist_normalizer > 0.01:
                        number_connections += 1

                    gmax = gmax * dist_normalizer
                
                else:
                    gmax = gmax * 0.02 # !!!!

            elif conn_name == "pyr2pvbas":
                pyr_idx = presynaptic_cell_idx - gids_of_celltypes["pyr"][0]
                pyr_coord = pyr_coord_x[pyr_idx]
                
                if not ( np.isnan(pyr_coord) ):
                    pvbas_idx = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
                    dist = pyr_coord_x[pyr_idx] - pvbas_coord_x[pvbas_idx]
                    dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pvbas ) / (np.sqrt(var_conns_on_pvbas * 2 * np.pi ))

                    if dist_normalizer > 0.01:
                        number_connections += 1

                    gmax = gmax * dist_normalizer
                
                else:
                    gmax = gmax * 0.1 # !!!!

            elif conn_name == "ca3_spatial2pvbas":
                pvbas_idx = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
                ca3_idx = presynaptic_cell_idx - gids_of_celltypes["ca3_spatial"][0]

                dist = pvbas_coord_x[pvbas_idx] - ca3_coord_x[ca3_idx]
                dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pvbas ) / (np.sqrt(var_conns_on_pvbas * 2 * np.pi ))

                if dist_normalizer > 0.01:
                    number_connections += 1
                gmax = gmax * dist_normalizer


            elif conn_name == "pvbas2pvbas":
                pvbas_idx1 = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
                pvbas_idx2 = presynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
                dist = pvbas_coord_x[pvbas_idx1] - pvbas_coord_x[pvbas_idx2]
                dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_pvbas2pvbas ) / (np.sqrt(var_conns_pvbas2pvbas * 2 * np.pi ))

                #if dist_normalizer > 0.001:
                #    number_connections += 1
                #gmax = gmax * dist_normalizer
                #print(gmax)


            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer
            if gmax < 1e-5:
                number_connections = 0


            for _ in range(number_connections):

                delay = np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"]) 
                if delay <= 0.5:
                    delay = 0.5
                
                gmax_syn =  np.random.normal(loc=gmax, scale=conn_data["gmax_std"])
                #np.random.lognormal(mean=np.log(gmax), sigma=conn_data["gmax_std"])


                if gmax_syn < 0.000001: # or gmax_syn > 50:
                    continue

                connection = {
                    "pre_gid" : presynaptic_cell_idx,
                    "post_gid" : postsynaptic_cell_idx,
                    
                    "gmax" : gmax_syn,
                    "Erev" : conn_data["Erev"],
                    "tau_rise" : conn_data["tau_rise"],
                    "tau_decay" : conn_data["tau_decay"],
                    "delay" : delay,
                    
                    "sourse_compartment" : conn_data["sourse_compartment"],
                    "target_compartment" : conn_data["target_compartment"],

                }
                
                try: 
                    gmax_nmda = conn_data["NMDA"]["gNMDAmax"]
                    gmax_nmda =  np.random.lognormal(mean=np.log(gmax_nmda), sigma=conn_data["NMDA"]["gmax_std"])
                    
                    connection["NMDA"] = {
                        "gNMDAmax" : gmax_nmda,
                        "tcon" : conn_data["NMDA"]["tcon"],   
                        "tcoff" : conn_data["NMDA"]["tcoff"], 
                        "enmda" : conn_data["NMDA"]["enmda"], 
                    }

                except KeyError:
                    pass

                connection["gmax"] *= 0.001  # recalulate nS to micromhos
                connection["delay"] += 1.5  # add delay on spike generation
                try:
                    connection["NMDA"]["delay"] += 1.5
                    connection["NMDA"]["gNMDAmax"] *= 0.001
                except KeyError:
                    pass
                # synapses.append(connection)

                th_idx = int(neurons_by_threads[postsynaptic_cell_idx])
                OBJECTS_PARAMS[th_idx]["synapses_params"].append(connection)




    #OBJECTS_PARAMS["synapses_params"] = synapses


    gap_juncs = []
    sgid_gap = 0

    for cell1_idx, celltype1 in enumerate(cell_types_in_model):
        for cell2_idx, celltype2 in enumerate(cell_types_in_model):

            if cell1_idx == cell2_idx: continue

            try:
                conn_name = celltype1 + "2" + celltype2
                conn_data = basic_params["gap_junctions_params"][conn_name]
                    
            except AttributeError:
                continue
            except KeyError:
                continue

            if (np.random.rand() > conn_data["prob"]): continue
           
            gap = {
                "gid1" : cell1_idx,
                "gid2" : cell2_idx,
                "r" : np.random.normal(conn_data["r"], conn_data["r_std"], 1),
                
                "compartment1" : conn_data["compartment1"],
                "compartment2" : conn_data["compartment2"],
                
                "sgid_gap" : sgid_gap,
            }
            
            gap_juncs.append(gap)
            sgid_gap += 2

            th_idx = int(neurons_by_threads[cell1_idx])
            OBJECTS_PARAMS[th_idx]["gap_junctions"].append(gap)
            
            th_idx2 = int(neurons_by_threads[cell2_idx])
            if th_idx2 != th_idx:
                OBJECTS_PARAMS[th_idx2]["gap_junctions"].append(gap)

    
    for th_idx in range(Nthreads):
        OBJECTS_PARAMS[th_idx]["elecs"] = deepcopy(basic_params["elecs"])
        OBJECTS_PARAMS[th_idx]["duration"] = deepcopy(basic_params["duration"])
        OBJECTS_PARAMS[th_idx]["file_results"] = deepcopy(basic_params["file_results"])
        OBJECTS_PARAMS[th_idx]["del_start_time"] = deepcopy(basic_params["del_start_time"])

        # OBJECTS_PARAMS["common_params"] = {}
        OBJECTS_PARAMS[th_idx]["common_params"]["radius4piramids"] = np.sqrt( basic_params["CellNumbers"]["Npyr"] / basic_params["PyrDencity"] ) / np.pi
    
    return OBJECTS_PARAMS


if __name__ == "__main__":
    Nthreads = 4
    objc_p = get_object_params(Nthreads=Nthreads)

    # for ith in range(Nthreads):
    #     neurons = objc_p[ith]["neurons"]
    #     for neuron in neurons:
    #         print(neuron["gid"], ith)



    #     if neuron["celltype"] == "mec":
    #         print(neuron["cellparams"]["grid_phase"])



    for ith in range(Nthreads):
        # neurons = objc_p[ith]["neurons"]
        for syn in objc_p[ith]["synapses_params"]:
            pre_gid = syn["pre_gid"]
            pre_ith = int (pre_gid % Nthreads)
            neuron_idx = int(pre_gid / Nthreads )
            pre = objc_p[pre_ith]["neurons"][neuron_idx]

            if pre["celltype"] == "mec":
                if (syn["pre_gid"] != pre["gid"]):
                    print("Hello")
                ph = pre["cellparams"]["grid_phase"]
                print(ph)



# import matplotlib.pyplot as plt

# plt.imshow(Wpyrbas)
# plt.show()

























