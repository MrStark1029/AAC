import xarray as xr
import os
import numpy as np
import netCDF4 as nc
import pickle
def loc_extract(file_path):
    nc_dataset = nc.Dataset(file_path, 'r')

    location_group = nc_dataset['location']
    latitude_values = location_group['lat'][640]
    longitude_values = location_group['lon'][640]
    valid_latitudes = np.ma.filled(latitude_values, np.nan)
    valid_longitudes = np.ma.filled(longitude_values, np.nan)

    valid_latitudes = valid_latitudes[~np.isnan(valid_latitudes)]
    valid_longitudes = valid_longitudes[~np.isnan(valid_longitudes)]
    lat.append(valid_latitudes)
    lon.append(valid_longitudes)



directory = "C:/Users/Mr. Anurag/Desktop/dataEMIT"

# Init
g1bd = []
g2bd = []
g1bu = []
g2bu = []
lat = []
lon = []


for filename in os.listdir(directory):
    if filename.endswith(".nc"):

        file_path = os.path.join(directory, filename)

        ds = xr.open_dataset(file_path)


        if 'group_1_band_depth' in ds.variables:
            g1bddat = ds['group_1_band_depth'].values
            g1bd.append(g1bddat)

        if 'group_2_band_depth' in ds.variables:
            g2bddat = ds['group_2_band_depth'].values
            g2bd.append(g2bddat)

        if 'group_1_band_depth_unc' in ds.variables:
            g1budat = ds['group_1_band_depth_unc'].values
            g1bu.append(g1budat)

        if 'group_2_band_depth_unc' in ds.variables:
            g2budat = ds['group_2_band_depth_unc'].values
            g2bu.append(g2budat)

        loc_extract(file_path)

        ds.close()


#saving the data
with open('data.pkl', 'wb') as f:
    pickle.dump([g1bd, g2bd, g1bu, g2bu, lat, lon], f)
