#!/bin/bash
WRF_DIR='/projects/erf/WRF.PrgEnv-gnu-8.5.0'
ln -sf $WRF_DIR/run/real.exe .
ln -sf $WRF_DIR/run/aerosol* .
./real.exe
