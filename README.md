Code of a CA1 field model
=========================

This is a large-scale biologically plausible network model of rhythms in the hippocampal CA1 field.

Dependencies
-----------------------------------
Model is runned under Python 7. OS is Ubuntu 18.04, another os in not tested.

Packages for simulations:
* NEURON 7.6
* LFPsimpy with our modifications <https://github.com/ivanmysin/LFPsimpy>
* mpi4py

Packages for saving, processing and plotting:
* numpy, scipy, matplotlib
* h5py
* elephant


Directories and files
-----------------------------------
Подробно написать, что делает каждый файл!!!

     /cells - directory with models of cells (hoc files)
     /mod - directory with mechanisms for cells (mod files)
     /Results - directory for saving simulation results and plots
     base_model.py - main python file
     basic_parameters.py - python file containing all parameters of simulation
     nontheta_state_params.py - parameters for non-theta state
     presimulation_lib.py - helper functions for calculating some simulation parameters
     simulation_parallel.py - содержит функцию   , которая собирает и запускает симуляцию.
     process.py - обрабатывает hdf5 file
     processingLib.py
     plot_result.py
     figure_1(2-6).py
     
     run_from_notebook.ipynb
     



How to run
-----------------------------------
You need:
* Install NEURON (see [instaction](https://www.neuron.yale.edu/neuron/download/compile_linux) )
  and another dependencies via *pip*
* Clone this repository and repository with LFPsimpy <https://github.com/ivanmysin/LFPsimpy> to same directory.
* Run in terminal:
  
        mpiexec -n nthreads python base_model.py
  
where *nthreads* is numbers of CPU cores used for simulation
Simulation results are saved to hdf5 file.
* To process the results, run *process.py*.  It will process and save
in the same file, wavelet spectra, bands, distribution of neurons by rhythm phases, etc.
  
      python process.py

* Run one of the *figure_1(2-6).py* file to plot figure. For example:

      python figure_1.py

Full simulation need 70 Gb RAM.
Full simulation: 9000 pyramidal cell, ...  

Structure of HDF5 file with results
-----------------------------------
You can use any convenient program for viewing hdf5 files,
for example, HDF COMPASS or hdfview.

Structure

      -root

        -- time dataset
  
        -- extracellular group

            --- electrode_1 group

              ---- firing group
                  ----- origin_data group
                        ------- group for each neuron type
                        ------------ datasets are firing times of each neuron
                  ----- processing group
              

              ---- lfp group

   
        -- intracellular group