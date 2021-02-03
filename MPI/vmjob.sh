#!/bin/bash -e
#SBATCH -t 3:00 -N 1 --mem=100M

for ncores in {1..16}

    MPI_CPU = $ncores

do

mpirun -n $MPI_CPU ./vector-matrix
