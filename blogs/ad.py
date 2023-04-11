#!/usr/lib/python3
'''
Created by paolocremonese.com
2023/04/11
'''

# upload packages

import os
import sys
import subprocess
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import data as data
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# define variables

trip = data.trip
print(trip)
kmtoml = 1.60934

# functions

def get_lat_long_from_address(address, to_plot=False):
   locator = Nominatim(user_agent='myGeocoder')
   location = locator.geocode(address)
   if to_plot:
      return location.longitude, location.latitude
   else:
       return location.latitude, location.longitude
lat_long_v = np.vectorize(get_lat_long_from_address)

# prove

def print_itinerary(all=False):
# for n,where in enumerate(trip['where'].values):
    if all:
        for n in range(len(trip)):
            print('\nafter {} miles and {} hours\non the {}'\
                .format(trip['distances'].iloc[n], 
                        trip['travel_time'].iloc[n],
                        trip.index[n]))
            print('{}\n{}'.format(trip['where'].iloc[n], trip['what'].iloc[n]))
            print(get_lat_long_from_address(trip['where'].iloc[n]))

    print('\nTotal distance: {} miles\n                {} km\nTotal Time: {}'\
        .format(trip['distances'].sum(), 
                round(trip['distances'].sum()*kmtoml,2), 
                'TBD'))

print_itinerary(False)

def make_plot():
    plt.subplots(1,1)
    plt.plot(*lat_long_v(trip['where'], to_plot=True))
    plt.show()

make_plot()

def main():
    print_itinerary(False)
    make_plot()

if __name__ == "__main__":
    main()
