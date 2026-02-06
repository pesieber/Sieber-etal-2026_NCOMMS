#!/usr/bin/env python3

## Functions for calculations
## Petra Sieber, Dec 2025

import numpy as np
import pandas as pd
import scipy
import xarray as xr
import numpy as np
import xarray as xr

# Recalculate fractions (albedo, EF) after sub-annual aggregation
def recalculate_frac(ds):
    if 'ALBEDO' in list(ds.keys()):
        ds['ALBEDO'] = ds['SWup']/ds['SWdown'].assign_attrs(units='-')
    if 'EF' in list(ds.keys()):
        ds['EF'] = ds['LH']/(ds['Rnet']).assign_attrs(units='-')
    return ds

# Seasonal climatology (weight by days in month if calculated from monthly series)
def seasonal_clim(ds):
    month_length = ds.time.dt.days_in_month
    month_weights = (month_length.groupby('time.season') / month_length.groupby('time.season').sum()) # weights as fraction of 120 months in 10 years
    with xr.set_options(keep_attrs=True): # to preserve the units
        ds_seas = (ds * month_weights).groupby('time.season').sum(dim='time')
        ds_seas = ds_seas.where(ds.isel(time=0, drop=True).notnull()) # set to nan instead of 0
    if isinstance(ds, xr.Dataset):
        ds_seas = recalculate_frac(ds_seas)
    return ds_seas

# Temporal aggregation
def agg_clim(ds, agg=None):
    if agg == 'seas-climatology':
        ds_agg = seasonal_clim(ds) 
    elif agg == 'seas-series':
        ds_agg = ds.resample(time='QS-DEC', keep_attrs=True).mean(dim='time', keep_attrs=True) # quarterly, starting on December 1
        ds_agg = recalculate_frac(ds_agg)            
    elif agg == 'seas-variability':
        ds_agg = ds.resample(time='QS-DEC', keep_attrs=True).mean(dim='time', keep_attrs=True) # quarterly, starting on December 1
        ds_agg = 100*(ds_seas.groupby('time.month').std(dim='time')/ds_seas.groupby('time.month').mean(dim='time')) # CV in %
        ds_agg = ds_seas.rename({'month': 'season'}).assign_coords(season=['MAM','JJA','SON','DJF']) # after aggregating across years, create season coordinate
    elif agg in ['ann-series', 'ann-climatology']:
        month_length = ds.time.dt.days_in_month
        month_weights = (month_length.groupby('time.year') / month_length.groupby('time.year').sum()) # weights as fraction of 120 months in 10 years
        with xr.set_options(keep_attrs=True): # to preserve the units
            ds_agg = (ds * month_weights).groupby('time.year').sum(dim='time')
            ds_agg = ds_agg.where(ds.isel(time=0, drop=True).notnull()) # set to nan instead of 0
        ds_agg = recalculate_frac(ds_agg)
        if agg == 'ann-climatology':
            ds_agg = ds_agg.mean(dim='year')
            ds_agg = recalculate_frac(ds_agg)
    return ds_agg

# Weighted by PFT fractions
def veg_seasonal_mean(surf, variable):
    with xr.set_options(keep_attrs=True): # to preserve the units
        cell_mean = (surf[variable]*surf['pct_pft']/100).sum(dim='lsmpft')
        seas = seasonal_clim(cell_mean)
        seas = seas.where(surf['AREA'].notnull()) # set to nan instead of 0
    return seas

# Weighted by PFT fractions and vegetated area (NATVEG+CROP)
def gridcell_seasonal_mean(surf, variable):
    with xr.set_options(keep_attrs=True): # to preserve the units
        cell_mean = (surf[variable]*surf['pct_pft']/100).sum(dim='lsmpft') *(surf['PCT_NATVEG']+surf['PCT_CROP'])/100 # scale from vegetated to gridcell
        seas = seasonal_clim(cell_mean)
        seas = seas.where(surf['AREA'].notnull()) # set to nan instead of 0
    return seas

# Split rainfed and irrigated crop PFT on surface dataset
def split_crop(surf):
    surf['PCT_CROP_rain'] = surf['PCT_CROP']*surf['PCT_CFT'].isel(cft=0)/100
    surf['PCT_CROP_irr'] = surf['PCT_CROP']*surf['PCT_CFT'].isel(cft=1)/100
    return surf

# Difference with very small noise around zero masked
def diff_masked(ds1, ds2, noise=10**-5):
    diff = ds1-ds2
    return diff.where((diff < -noise) | (diff > noise))

def masked(ds, noise=10**-5):
    return ds.where((ds < -noise) | (ds > noise))

# Correlation between array and each variable of a dataset
def da_ds_corr(da1, ds2, dim=['lat','lon'], weights=None):
    data_vars = dict()
    for var, da2 in ds2.data_vars.items():
        corr = xr.corr(da1, da2, dim=dim, weights=weights)
        data_vars[var] = corr    
    return xr.Dataset(data_vars)

# Correlation between each variable of two datasets
def ds_ds_corr(ds1, ds2, dim=['lat','lon'], weights=None):
    data_vars = dict()
    for var1, da1 in ds1.data_vars.items():
        for var2, da2 in ds2.data_vars.items():
            corr = xr.corr(da1, da2, dim=dim, weights=weights)
            data_vars[var1, var2] = corr    
    return xr.Dataset(data_vars)

# Correlation between two datasets per variable (taking variables from ds1)
def ds_corr(ds1, ds2, dim=['lat','lon'], weights=None):
    data_vars = dict()
    for var in list(ds1.keys()):
        corr = xr.corr(ds1[var], ds2[var], dim=dim, weights=weights)
        data_vars[var] = corr    
    return xr.Dataset(data_vars)

# Replace method for xarray using pandas (https://github.com/pydata/xarray/issues/6377)
def xr_replace(da, to_replace, value):
    df = pd.DataFrame()
    df["values"] = da.values.ravel()
    df["values"].replace(to_replace, value, inplace=True)
    return da.copy(data=df["values"].values.reshape(da.shape))

# Calculate weighted average across rows, with weights being the weight of each row (e.g. grid cell area)
def weighted_average(df, weights):
    val = dataframe[value]
    wt = dataframe[weight]
    return (df * weights).sum() / wt.sum()

# Compute confidence interval of the mean for a dataframe (variables in columns)
def confidence_interval(df, group_dim=None, confidence=0.95):
    from scipy import stats
    if group_dim:
        mean = df.groupby(group_dim).mean()
        std = df.groupby(group_dim).std()
        n = df.groupby(group_dim).size()[0] # assumes same number of elements within each group (here 15 years)
    else:
        mean = df.mean()
        std = df.std()
        n = len(df)
    ci_upper = std/np.sqrt(n) * stats.t.ppf(1-(1-confidence)/2, n-1)
    return ci_upper