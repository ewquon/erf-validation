#!/bin/bash
#SBATCH --job-name=preprocess
#SBATCH --account=erf
#SBATCH --time=03:33:00
#SBATCH --ntasks=384
#SBATCH -N 4
#SBATCH --exclusive
#####SBATCH --qos=high

source ~/.bash_profile
wrf-gnu-env

WRF_DIR='/projects/erf/WRF.PrgEnv-gnu-8.5.0'
ln -sf $WRF_DIR/run/real.exe .
ln -sf $WRF_DIR/run/aerosol* .

#srun -n 1 ./real.exe

srun -N${SLURM_JOB_NUM_NODES} -n${SLURM_NTASKS} --ntasks-per-node=96 --distribution=cyclic:cyclic --cpu_bind=cores ./real.exe

