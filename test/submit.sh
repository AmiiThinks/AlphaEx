#!/bin/bash

#SBATCH --output=test/output/submit_%a.txt
#SBATCH --error=test/error/submit_%a.txt

export OMP_NUM_THREADS=1

module load python/3.7

echo "${python_module}" "${SLURM_ARRAY_TASK_ID}" "${config_file}"
python -m "${python_module}" "${SLURM_ARRAY_TASK_ID}" "${config_file}"