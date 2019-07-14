#!/bin/bash
#SBATCH --time=00:01:00
#SBATCH --account=def-sutton
#SBATCH --output=%x-%j.out
echo 'Hello, world!'
sleep 30