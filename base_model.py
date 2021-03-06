from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nthreads = comm.Get_size()


from simulation_parallel import run_simulation

if rank == 0:
    from basic_parameters import get_object_params
    basic_params = get_object_params(nthreads) # get parameters

    for th_idx, p in enumerate(basic_params):
        if th_idx == 0: continue
        comm.send(p, dest=th_idx, tag=th_idx) # sent parameters to threads

    basic_params = basic_params[0]
else:
    basic_params = comm.recv(source=0, tag=rank)

run_simulation(basic_params)  # run simulation

