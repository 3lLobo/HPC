#!/bin/bash -l
#SBATCH -J hvd_$1_$2
#SBATCH -o hvd_$1_$2_out.txt
#SBATCH -e hvd_$1_$2_err.txt

#SBATCH -t 1:00:00

#SBATCH --partition shared

#SBATCH --nodes $2
#SBATCH --ntasks-per-node=4




module purge
module load 2020
module load OpenMPI/4.0.3-GCC-9.3.0
module load Python/3.8.2-GCCcore-9.3.0
export PYTHONPATH="~/miniconda3/bin/python"

time mpirun -np 4  PYTHONPATH ~/cifar10_hvd_$1.py
