#!/bin/bash -l
#SBATCH -J hvd_effnet_1
#SBATCH -o hvd_out_effnet_1.txt
#SBATCH -e hvd_err_effnet_1.txt
#SBATCH -t 1:00:00
#SBATCH --nodes 1
#SBATCH -p short
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
time $PYTHON -u cifar10_hvd_effnet.py
mkdir $HOME/ml_assignment/job_ml_effnet_1
cp logs  $HOME/ml_assignment/
