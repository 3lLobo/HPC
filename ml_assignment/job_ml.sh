#!/bin/bash -l
#SBATCH -J hvd_test
#SBATCH -o hvd_test_out.txt
#SBATCH -e hvd_test_err.txt

#SBATCH -t 0:30:00

#SBATCH --partition shared

#SBATCH --nodes 1
#SBATCH --ntasks-per-node=4

###SBATCH -n 2




module purge
module load 2020
module load OpenMPI/4.0.3-GCC-9.3.0
module load Python/3.8.2-GCCcore-9.3.0
export PYTHONPATH="~/miniconda3/bin/python"

time mpirun -np 4  PYTHONPATH cifar_hvd_2.py
