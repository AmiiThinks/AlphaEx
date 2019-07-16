#!/bin/bash

#SBATCH --time=02:55:00
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name submit.sh
#SBATCH --output=output/submit_%j.txt
#SBATCH --error=error/submit_%j.txt

export OMP_NUM_THREADS=1
mkdir -p output
mkdir -p error

sleep $((SLURM_ARRAY_TASK_ID / 10))