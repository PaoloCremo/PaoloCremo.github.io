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

from adjustText import adjust_text
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import data.data as data
# %load_ext autoreload
# %autoreload 2
# %matplotlib inline

# define variables

trip = data.trip
# print(trip)
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
    
    print(trip)
    
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


def make_plot_basemap(lat=34.495207, long= -114.320239, save=False):
    fig = plt.figure(figsize=(10, 6))
    m = Basemap(projection='lcc', resolution='f', 
                    lat_0=lat, lon_0=long,
                    width=1.05E6, height=8.E5)
    m.plot(longitude_list, latitude_list, 
               latlon=True, linewidth=1.5, 
               color='firebrick')
    m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)
    m.drawcountries(color='sienna', linewidth=1)
    m.drawstates(color='dimgray', linewidth=1)
    m.drawcoastlines(color='sienna')
    m.scatter(longitude_list, latitude_list, 
                  latlon=True, s=25, color='firebrick')
    texts = []
    for n,place in enumerate(trip['where']):
        if len(place) > 30:
            place = trip['what'].iloc[n]
        if not place in str(texts):
            x,y = m(longitude_list[n], latitude_list[n]) # *1.005)
            # plt.plot(x, y, 'ok', markersize=5)
            texts.append(plt.text(x, y, str(n+1)+'. '+place, fontsize=10, 
                                  color='k'))
    adjust_text(texts, only_move={'points':'y', 'texts':'y'}, 
                arrowprops=dict(arrowstyle="->", color='firebrick', lw=0.5))

    if save:
        plt.savefig('data/map.png', bbox_inches='tight', 
                    transparent=True, dpi=400)
    else:
        plt.show()
# make_plot_basemap(34.495207, -114.320239, True)

def get_prices(expense='other', print_recap=False):
    # if expense == 'nights':
    expenses = ['Night', 'Park' , 'other']
    if not expense in expenses :
        raise ValueError("expense must be one of {}".format(expenses))
    if expense == 'other':
        mask = [not ('Park' in whats or 'Night' in whats) for whats in  trip['what'].values]
    else:
        mask = [expense in whats for whats in  trip['what'].values]
    trip_exp_value = trip[mask]
    total_price = trip_exp_value.prices.sum()
    if print_recap:
        _, tn = get_prices('Night', False)
        _, tp = get_prices('Park', False)
        _, to = get_prices('other', False)
        print('Total nights :  {} $\
             \nTotal parks  :  {} $\
             \nTotal other  : {} $\
           \n\nTotal        : {} $'\
              .format(tn, tp, to, tn+tp+to))
    else:
        return trip_exp_value, total_price

def get_durations(print_all=True):
    durations_in_minutes = []
    for duration in trip.travel_time:
        h,m = duration.split(':')
        durations_in_minutes.append(int(h)*60+int(m))
    car_trips = durations_in_minutes[3:-1]
    total_car_minutes = np.array(car_trips).sum()
    mean_per_day = total_car_minutes/12
    hour_min_total = str(total_car_minutes//60) + ':' + str(total_car_minutes%60)
    hour_min_mean = str(int(mean_per_day//60)) + ':' + str(int(mean_per_day%60))
    if print_all:
        print('Total minutes: {}\
              \nMinutes/day: {}\
              \nTotal hours: {}\
              \nHours/day: {}'\
              .format(total_car_minutes, mean_per_day, hour_min_total, hour_min_mean))
    else:
        return total_car_minutes, mean_per_day, hour_min_total, hour_min_mean

def get_daily_info(print_all=True, save=False):
    start_date = '2023-08-07'
    end_date = '2023-08-18'
    current_date = start_date
    # if not print_all:
    df = pd.DataFrame(columns=['Expenses', 'Time', 'Distance'])
    while current_date < end_date:
        year,month,day = current_date.split('-')
        tomorrow = '{}-{}-{:02}'.format(year,month,int(day)+1)
        df_day = trip[current_date:tomorrow]

        durations_in_minutes = []
        for duration in df_day.travel_time:
            h,m = duration.split(':')
            durations_in_minutes.append(int(h)*60+int(m))
        total_car_minutes = np.array(durations_in_minutes).sum()
        hour_min_total = '{:02}:{:02}'.format(total_car_minutes//60,total_car_minutes%60)
        if print_all:
            print('{}\nTotal expenses: {}\
                \nTotal Travel Time: {}\
                \nTotal Trave Distance: {}\n'\
                .format(current_date,
                        df_day.prices.sum(),
                        hour_min_total,
                        df_day.distances.sum()))
        else:
            today_df = pd.DataFrame({'Expenses':df_day.prices.sum(),
                                     'Time':hour_min_total,
                                     'Distance':df_day.distances.sum()},
                                     index=[current_date])
            df = pd.concat((df,today_df))
        current_date = tomorrow
    if not print_all and save:
        df.to_html('data/recap_days.html')
    else:
        return df
# df = get_daily_info(False, True)        


def main():
    print_itinerary(all=False)
    # make_plot_basemap(34.495207, -114.320239)
    # make_plot()

if __name__ == "__main__":
    main()
