#!/bin/bash 
#SBATCH -t 15:00
#SBATCH --tasks-per-node 16
#SBATCH -N 1
#SBATCH --partition=shared
 
mpirun --mca pml ob1 --mca btl ^openib ./vector-matrix
