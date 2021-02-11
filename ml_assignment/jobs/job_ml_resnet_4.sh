#!/bin/bash -l
#SBATCH -J hvd_resnet_4
#SBATCH -o hvd_out_resnet_4.txt
#SBATCH -e hvd_err_resnet_4.txt
#SBATCH -t 0:30:00
#SBATCH --nodes 1
#SBATCH --ntasks-per-node=4
# Loading modules
module purge
module load 2020
module load OpenMPI/4.0.3-GCC-9.3.0
module load Python/3.8.2-GCCcore-9.3.0
source $HOME/.bashrc
ENV='ml'
PYTHON=~/miniconda3/envs/${ENV}/bin/python
PIP=~/miniconda3/envs/${ENV}/bin/pip
export PATH_TO_SOURCE=ml_assignment
# Copy input data from home to scratch
cp -R $HOME/$PATH_TO_SOURCE $TMPDIR
cd $TMPDIR/$PATH_TO_SOURCE
time mpirun -np 4 $PYTHON -u cifar10_hvd_resnet.py
cp logs  $HOME/ml_assignment/
mkdir $HOME/ml_assignment/job_ml_resnet_4
cp logs  $HOME/ml_assignment/
