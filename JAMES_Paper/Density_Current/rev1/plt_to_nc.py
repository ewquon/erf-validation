#!/usr/bin/env python
import glob
import xarray as xr
from erftools.postprocessing import Plotfile

pltfiles = sorted([pf for pf in glob.glob('plt*')
                   if not '.old.' in pf])

dslist = [
    Plotfile(dpath,verbose=True).to_xarray().isel(y=0)
    for dpath in pltfiles
]

ds = xr.concat(dslist,'t')
ds = ds.sortby('t')

#ds = ds.assign_coords(x=ds.coords['x']/1000.,
#                      z=ds.coords['z']/1000.)

ds.to_netcdf('combined_pltfiles.nc')
