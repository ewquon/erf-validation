#!/bin/bash
WPS_DIR='/projects/erf/WPS-PrgEnv-gnu-8.5.0'
ICBC_DIR='ERA5'
REAN_PREFIX='ERA5' # from ungrib prefix in namelist.wps

#
# SETUP
#
ln -sf $WPS_DIR/geogrid.exe .
ln -sf $WPS_DIR/ungrib.exe .
ln -sf $WPS_DIR/metgrid.exe .
ln -sf $WPS_DIR/geogrid/GEOGRID.TBL
ln -sf $WPS_DIR/metgrid/METGRID.TBL

#
# GEOGRID
#
if [ ! -f 'geo_em.d01.nc' ]; then
    ./geogrid.exe
fi

if [ -z "`ls met_em.*`" ]; then
    #
    # UNGRIB
    #
    ungribbed=`ls ${REAN_PREFIX}:*`
    if [ -z "$ungribbed" ]; then
        cp $WPS_DIR/link_grib.csh .
        ./link_grib.csh $ICBC_DIR/* .

        ln -sf $WPS_DIR/ungrib/Variable_Tables/Vtable.ERA-interim.pl Vtable
        ./ungrib.exe
    fi

    #
    # METGRID
    #
    ./metgrid.exe
fi
