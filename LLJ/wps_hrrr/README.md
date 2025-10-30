These files were used to generate WRF ICs/BCs for ERF to compare against PINACLES LES.

Preliminary results with the "medium" (dx=dy=1000 km grid) and 200 vertical
levels (approximately 50 m grid spacing, specified through `eta_levels` in the
WRF namelist.input) were used in the FY25 Q4 report.

The eta levels were estimated with this snippet:
```python
from erftools.wrf import get_eta_levels
nz = 200
ztop = 10e3

dz = ztop / nz
zlevels = np.arange(0,nz+1) * dz

eta_levels, ptop = get_eta_levels(zlevels)
```
