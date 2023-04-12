#!/usr/lib/python3
'''
Created by paolocremonese.com
2023/04/11
'''

# upload packages

import os
import sys
import gmplot
import subprocess
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import data.data as data
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# define variables

trip = data.trip
print(trip)
kmtoml = 1.60934
dolpermil_tesla = 0.05
dolpermil_ice = 0.17


# functions 1

def get_lat_long_from_address(address, to_plot=False):
   locator = Nominatim(user_agent='myGeocoder')
   location = locator.geocode(address)
   if to_plot:
      return location.longitude, location.latitude
   else:
       return location.latitude, location.longitude

# other variables

lat_long_v = np.vectorize(get_lat_long_from_address)
longitude_list, latitude_list = lat_long_v(trip['where'], to_plot=True)


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
    total_distance = trip['distances'].sum()
    distance_per_day = total_distance/12
    print('\nTotal distance: {} miles - {} miles/day\
           \n {:>22} km - {} km/day\
           \nTotal Time: {}\
           \nCost Tesla: {:.2f} $ w/ {:.2f} $/mile\
           \nCost ICE: {:>8.2f} $ w/ {:.2f} $/mile'\
        .format(total_distance, 
                distance_per_day,
                round(total_distance*kmtoml,2), 
                round(distance_per_day*kmtoml,2), 
                'TBD',
                total_distance * dolpermil_tesla,
                dolpermil_tesla,
                total_distance * dolpermil_ice,
                dolpermil_ice))

def save_itinerary():
    trip.to_html('data/recap_stops.html')

def make_plot(lat=0, long=0, zoom = 3, ptype = 'minimal'):
    '''
    source: https://www.geeksforgeeks.org/python-plotting-google-map-using-gmplot-package/
            https://towardsdatascience.com/mapping-with-matplotlib-pandas-geopandas-and-basemap-in-python-d11b57ab5dac
            https://matplotlib.org/basemap/users/geography.html
    '''
    if ptype == 'minimal' :
        plt.subplots(1,1)
        plt.plot(latitude_list, longitude_list)
        plt.show()
    
    elif ptype == 'gmaps':
        gmap1 = gmplot.GoogleMapPlotter(lat, long, zoom)
        gmap1.scatter(latitude_list, longitude_list, '#FF0000',
                              size = 40, marker = True )
        gmap1.plot(latitude_list, longitude_list, 
           'cornflowerblue', edge_width = 2.5)
        gmap1.draw('/Users/paolocremonese/Documents/gmplot.html')
    
    elif ptype == 'basemap':
        fig = plt.figure(figsize=(8, 8))
        m = Basemap(projection='lcc', resolution='f', 
                    lat_0=lat, lon_0=long,
                    width=1.05E6, height=1.2E6)
        # m.bluemarble()
        m.plot(longitude_list, latitude_list, 
               latlon=True, linewidth=1.5, 
               color='firebrick')
        # m.shadedrelief()
        # m.fillstates(color='coral',lake_color='aqua')
        m.drawcountries(color='k', linewidth=1)
        m.drawstates(color='dimgray', linewidth=1)
        m.drawcoastlines(color='coral')
        m.scatter(longitude_list, latitude_list, 
                  latlon=True, s=25, color='firebrick')
# make_plot(34.495207, -114.320239, zoom=7, ptype='gmaps')


def make_plot_basemap(lat=0, long=0, save=False):
    fig = plt.figure(figsize=(10, 8))
    m = Basemap(projection='lcc', resolution='f', 
                    lat_0=lat, lon_0=long,
                    width=1.05E6, height=8.E5)
    m.plot(longitude_list, latitude_list, 
               latlon=True, linewidth=1.5, 
               color='firebrick')
    m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
    m.drawcountries(color='k', linewidth=1)
    m.drawstates(color='dimgray', linewidth=1)
    m.drawcoastlines(color='k')
    m.scatter(longitude_list, latitude_list, 
                  latlon=True, s=25, color='firebrick')
    if save:
        plt.savefig('data/map.png', bbox_inches='tight', transparent=True, dpi=400)
    else:
        plt.show()
# make_plot_basemap(34.495207, -114.320239)

def main():
    print_itinerary(all=False)
    # make_plot_basemap(34.495207, -114.320239)
    # make_plot()

if __name__ == "__main__":
    main()
    # print('Hola')
