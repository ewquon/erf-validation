#!/bin/bash
#SBATCH --job-name=gabls1_dear
#SBATCH --account=erf
#SBATCH --time=8:00:00
#SBATCH -N 1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64G

. ~/envs/erf-cuda.sh
erf-cuda-env
builddir=/projects/erf/equon/ERF/MyBuildGPU

srun $builddir/Exec/ABL/erf_abl inputs_gabls1_dear &> log

