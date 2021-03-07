#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:39:02 2020

@author: ivan
"""

import os
import sys

sys.path.append("../")
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    from basic_parameters import basic_params
else:
    basic_params = None

basic_params = comm.bcast(basic_params, root=0)


print(basic_params, rank)