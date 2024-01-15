#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:37:18 2023

@author: keilagonzalez

Air quality statistics helper

This script allows users to get yearly statistics form hourly air
quality measurements. The descriptive statistics obtained are these
defined as relevant by the World Health Organization.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This tool accepts pandas DataFrames but examples on how the
import could be done using csv files are also shown.

This file can also be imported as a module and contains the following
functions:

    * obtention_pollutants_values - returns valid lectures
    * mean_valid_values - returns the yearly mean values
    * main - the main function of the script
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import valid_hours

# generation of dataframes
def obtention_pollutants_values(df, option):
    ''' This function takes a dataframe with hourly pollutant information and delivers 
        yearly statistics 
        option =1 -> if data is taken from Madrid's opendata website
        option =2 -> if data has been taken fromt the EEA webpage
        
        '''
    if option == 1:

        stats_df = valid_hours.stats_valid_hours_madrid(df)
        df['valid_lectures'] = stats_df.valid_hours
        df['unvalid_lectures'] = stats_df.unvalid_lectures
        df['valid_lectures_count'] = df.valid_lectures.apply(len)
        df['max_avg_gradual'] = df['valid_lectures'].apply(lambda x: max(x) if bool(x) else np.nan)
        df['daily_avg_gradual'] = df.valid_lectures.apply(sum) / df['valid_lectures_count']
        list_valid_values = df['valid_lectures'].tolist()
        df['perc_99_gradual'] = pd.Series([np.percentile(x, 99) if bool(x) else np.nan for x in list_valid_values ])
        return df
    
    if option == 2:
        stats_df = valid_hours.stats_valid_hours_eeuu(df)
        df = stats_df.valid_hours
        return df


# means of valid included in a single list
def mean_valid_values(df:pd.DataFrame, stations_col:str, measurements:str):
    stations_list = df[stations_col].unique()
    mean_valid = []
    for station in stations_list:
        df_valid_values = df.loc[df[stations_col] == station]
        df_valid_values = df_valid_values[measurements]
        value_mean = df_valid_values.explode().mean()
        mean_valid.append(value_mean)
    s_stations_ = pd.Series(stations_list, name = 'stations')
    s_mean_valid_ = pd.Series(mean_valid, name = 'mean_valid_year')
    df_mean_valid = pd.concat([s_stations_,s_mean_valid_], axis = 1)
    return df_mean_valid

def max_valid(df, stations_col:str, measurements:str) -> pd.DataFrame:
    ''' This function creates a list of all valid values and obtains the
        maximum annual of all hourly values of specific stations '''
    max_valid = []
    stations_list = df[stations_col].unique()
    for station in stations_list:
        df_max = df.loc[df[stations_col] == station]
        df_max = df_max[measurements]
        value_max = df_max.explode().max()  #despite the fact that there are some empty lists, with explode this is ignored
        max_valid.append(value_max)
    s_stations_ = pd.Series(stations_list, name = 'stations')
    s_max_valid = pd.Series(max_valid, name = 'max_valid')
    df_max = pd.concat([s_stations_, s_max_valid], axis = 1)
    return df_max

def percentile_99(df, stations_col:str, measurements:str) -> pd.DataFrame:
    ''' This function creates a list of valid values
        and obtains the 99th perc annual of all hourly values of specific stations '''
    quant_valid = []
    stations_list = df[stations_col].unique()
    for station in stations_list:
        df_station = df.loc[df[stations_col] == station]
        df_station = df_station[measurements]
        quantile_ = df_station.explode().quantile(0.99)                         #changes the 365 days hourly lectures of specific station into a single list and gets the percentile
        quant_valid.append(quantile_)
    s_stations_ = pd.Series(stations_list, name = 'stations')
    s_quantile_ = pd.Series(quant_valid, name = 'quant99_valid')
    df_quantile_ = pd.concat([s_stations_,s_quantile_], axis = 1)
    return df_quantile_