#!/bin/bash
#SBATCH -J hvd_effnet_1
#SBATCH -o hvd_out_effnet_1.txt
#SBATCH -e hvd_err_effnet_1.txt
#SBATCH -N 1
#SBATCH -t 1:11:00
#SBATCH -p gpu_titanrtx_shared
#SBATCH --gres=gpu:1
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
CUDA_LAUNCH_BLOCKING=1
# Copy input data from home to scratch
cp -R $HOME/$PATH_TO_SOURCE $TMPDIR
cd $TMPDIR/$PATH_TO_SOURCE
time $PYTHON -u cifar10_hvd_effnet.py
mkdir $HOME/ml_assignment/job_ml_effnet_1
cp logs  $HOME/ml_assignment/
