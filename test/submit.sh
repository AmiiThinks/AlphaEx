#!/bin/bash

#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name submit.sh
#SBATCH --output=test/output/submit_%a.txt
#SBATCH --error=test/error/submit_%a.txt

export OMP_NUM_THREADS=1

module load python/3.6

echo "${python_module}" "${SLURM_ARRAY_TASK_ID}" "${config_file}"
python -m "${python_module}" "${SLURM_ARRAY_TASK_ID}" "${config_file}"