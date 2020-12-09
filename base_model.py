from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()



from simulation_parallel import run_simulation

if rank == 0:
    from basic_parameters import get_object_params
    basic_params = get_object_params() 
else:
    basic_params = None

basic_params = comm.bcast(basic_params, root=0)

run_simulation(basic_params)

