#!/bin/bash
REAN_PREFIX='ERA5' # from ungrib prefix in namelist.wps

rm -f GRIBFILE.*
rm -f $REAN_PREFIX:*
rm -f *.TBL
rm -f *.asc
rm -f *.bin
rm -f *.formatted
rm -f bulk*
rm -f CAM*
rm -f CCN*
rm -f CLM*
rm -f co2_trans
rm -f create_p3_lookupTable_*
rm -f ETA*
rm -f kernels.asc_s_0_03_0_9
rm -f p3_*
rm -f RRTM*
rm -f SOILPARM*
