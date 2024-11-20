# Squall Line

Results presented herein were generated with ERF hash: **9428c70** and [inputs file](https://github.com/erf-model/ERF/blob/9428c70c5c299fd8c11bc0b15634b917e16bdf7b/Exec/MoistRegTests/SquallLine_2D/inputs_moisture_Gabersek) .

Raw data and python script for the rain accumulation figure are provided in the `Rain_Accum` directory.
    
A domain size of $(L_x, L_z) = (150\times 10^3, 24\times 10^3)$ [m], with grid resolution $(\Delta x, \Delta z) = (100, 100)$ [m] was employed. The simulation was run for 2.5 hours, with an RK3 time step of 0.25 [s] and 4 acoustic sub-steps in the last RK stage. Lateral walls utilized an open boundary while the bottom wall employed a free-slip condition and the top wall was a high-order outflow -- i.e., linear extrapolation for scalar quantities and a Neumann condition for velocity. The 3$^\text{rd}$ order upwind scheme was used for advection while the Kessler microphysics were employed for moisture. Constant diffusivities of $\nu = \alpha_{i} = 200$ [m$^2$/s] were utilized for momentum and all scalars; no turbulence model was employed.
    
