#!/usr/bin/env python
import pandas as pd
from mmctools.wrf.preprocessing import ERA5

start_date = pd.to_datetime('2021-07-19 12:00')
end_date   = pd.to_datetime('2021-07-21 00:00')
datetimes  = pd.date_range(start_date, end_date, freq='3h')

icbc = ERA5()

# retrieval for WRF
icbc.download(datetimes, path='era5')
