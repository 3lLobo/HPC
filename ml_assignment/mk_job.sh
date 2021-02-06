#!/bin/bash

rm -r jobs/*

runtime=0



# mv "$job" "${job// /_}"
exp_name="job_ml_"$1"_"$2""
echo $exp_name

echo "#!/bin/bash -l" > "jobs/""$exp_name"".sh"

echo "#SBATCH -J hvd_"$1"_"$2"" >> "jobs/""$exp_name"".sh"
echo "#SBATCH -o hvd_out_"$1"_"$2".txt" >> "jobs/""$exp_name"".sh"
echo "#SBATCH -e hvd_err_"$1"_"$2".txt" >> "jobs/""$exp_name"".sh"

echo "#SBATCH -t "$runtime":30:00" >> "jobs/""$exp_name"".sh"
echo "#SBATCH --nodes "$2"" >> "jobs/""$exp_name"".sh"
echo "#SBATCH --ntasks-per-node=4" >> "jobs/""$exp_name"".sh"
echo "# Loading modules" >> "jobs/""$exp_name"".sh"


echo "module purge" >> "jobs/""$exp_name"".sh"
echo "module load 2020" >> "jobs/""$exp_name"".sh"
echo "module load OpenMPI/4.0.3-GCC-9.3.0" >> "jobs/""$exp_name"".sh"
echo "module load Python/3.8.2-GCCcore-9.3.0" >> "jobs/""$exp_name"".sh"

echo "source \$HOME/.bashrc" >> "jobs/""$exp_name"".sh"
echo "ENV='ml'" >> "jobs/""$exp_name"".sh"
echo "PYTHON=~/miniconda3/envs/\${ENV}/bin/python" >> "jobs/""$exp_name"".sh"
echo "PIP=~/miniconda3/envs/\${ENV}/bin/pip" >> "jobs/""$exp_name"".sh"
echo "export PATH_TO_SOURCE="ml_assignment"" >> "jobs/""$exp_name"".sh"
echo "# Copy input data from home to scratch" >> "jobs/""$exp_name"".sh"
echo "cp -R \$HOME/"\$PATH_TO_SOURCE" "\$TMPDIR"" >> "jobs/""$exp_name"".sh"
echo "cd "\$TMPDIR"/\$PATH_TO_SOURCE" >> "jobs/""$exp_name"".sh"

echo "time \$PYTHON -u cifar10_hvd_"$1".py" >> "jobs/""$exp_name"".sh"
echo "cp logs " "\$HOME"/"ml_assignment"/>> "jobs/""$exp_name"".sh"
echo "mkdir "\$HOME"/"ml_assignment"/"$exp_name"">> "jobs/""$exp_name"".sh"
echo "cp logs " "\$HOME"/"ml_assignment"/>> "jobs/""$exp_name"".sh"

sbatch jobs/$exp_name".sh"
