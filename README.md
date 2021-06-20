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

    ./cells - directory with models of cells (hoc files)
    ./mod - directory with mechanisms for cells (mod files)
    ./test_scripts - directory with scipts for testing some properties of the models
     base_model.py - main python file
     basic_parameters.py - python file containing
     nontheta_state_params.py
     simulation_parallel.py
     process.py
     processingLib.py
     plot_result.py
     figure_1(2-6).py
     
     run_from_notebook.ipynb
     



How to run
-----------------------------------
You need:
* Install NEURON (see [instaction](https://www.neuron.yale.edu/neuron/download/compile_linux) )
  and another dependencies via *pip*
* Clone this repository and repository with LFPsimpy <https://github.com/ivanmysin/LFPsimpy> to one directory.
* Run in terminal:
  
        mpiexec -n nthreads python base_model.py
  where *nthreads* is numbers of CPU cores used for simulation

Full simulation need 70 Gb RAM.
Full simulation: 10000 pyramidal cell, 
Результаты симуляции сохраняются в hdf5 файл.

How to process
-----------------------------------
Если запустить функцию из файла process.py, но она обработает и сохранит
в том же файле вейвлет спектры, полосы, распределение нейронов по фазам ритмов и т.д.

How to plot
-----------------------------------
Функции в файлах умеют свчитывать из hdf5 файла предобработанные данные и строить графики.
