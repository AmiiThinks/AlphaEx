#!/bin/bash

#SBATCH --time=02:55:00
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name submit.sh
#SBATCH --output=test/output/submit_%a.txt
#SBATCH --error=test/error/submit_%a.txt

export OMP_NUM_THREADS=1

echo $SLURM_ARRAY_TASK_ID