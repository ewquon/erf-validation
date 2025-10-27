#!/usr/bin/env python
import pandas as pd
from herbie import Herbie

def int_to_AAA(n):
    """Convert an integer (0-17575) to a 3-letter string (AAA-ZZZ)"""
    result = ""

    # Convert to base 26, building string from right to left
    for i in range(3):  # 3 positions for AAA format
        result = chr(ord('A') + (n % 26)) + result
        n //= 26

    return result

if __name__ == '__main__':
    from os import symlink
    from glob import glob

    start_date = pd.to_datetime('2021-07-20 00:00')
    end_date   = pd.to_datetime('2021-07-21 00:00')
    end_date   = pd.to_datetime('2021-07-21 01:00')
    forecast_hour = 2

    # download all grib files over datetime range
    hr_offset = pd.to_timedelta(forecast_hour, unit='h')
    all_datetimes = pd.date_range(start_date - hr_offset,
                                  end_date - hr_offset,
                                  freq='1h')
    gribfiles = []
    for dt in all_datetimes:
        # get data at pressure levels
        H = Herbie(dt, model='hrrr', product='prs', fxx=forecast_hour)
        print('valid time :',H.inventory()['valid_time'].iloc[0])
        H.download(verbose=True)
        fpath = H.find_grib()[0]
        gribfiles.append(fpath)

    # link grib files
    for i,fpath in enumerate(gribfiles):
        ext = int_to_AAA(i)
        linkname = f'GRIBFILE.{ext}'
        print(f'{linkname} --> {fpath}')
        symlink(fpath, linkname)
