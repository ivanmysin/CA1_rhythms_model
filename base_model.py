from time import time

from simulation_parallel import run_simulation   # 
from basic_parameters import basic_params

timer = time()
run_simulation(basic_params)
print("Simulation time in sec ", time() - timer)
