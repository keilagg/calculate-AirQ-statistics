#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:37:18 2023

@author: keilagonzalez

Air quality statistics helper.

This script allows users to get yearly statistics form hourly air
quality measurements. The descriptive statistics obtained are these
defined as relevant by the World Health Organization.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This tool accepts pandas DataFrames but examples on how the
import could be done using csv files are also shown.

This file can also be imported as a module and contains the following
functions:

    * get_valid_measurements - returns valid lectures
    * get_mean - returns the yearly mean values
    * main - the main function of the script
"""

import pandas as pd
import numpy as np
import geopandas as gpd
import valid_hours

# generation of dataframes
def get_valid_measurements(df:pd.DataFrame, option:int)-> pd.DataFrame:
    """Delivers valid air quality measurement values

    Args:
    df (pd.DataFrame): The DataFrame with yearly air measurements
    option (int): Indicates the data origin:
        option =1 -> if data is taken from Madrid's opendata website
        option =2 -> if data has been taken fromt the EEA webpage

    Returns:
    pd.DataFrame: a DataFrame with valid lectures
    """

    if option == 1:

        stats_df = valid_hours.stats_valid_hours_madrid(df)
        df['valid_lectures'] = stats_df.valid_hours
        df['unvalid_lectures'] = stats_df.unvalid_lectures
        return df
    
    if option == 2:
        stats_df = valid_hours.stats_valid_hours_eeuu(df)
        df = stats_df.valid_hours
        return df

# means of valid included in a single list
def get_mean(df:pd.DataFrame, stations_col:str, measurements:str)-> pd.DataFrame:
    """Delivers mean concentration for specific pollutant.

    Args:
    df (pd.DataFrame): The DataFrame with valid values for specific pollutant
    stations_col (str): Name of the column with the measurement stations identificator.
    measurements (str): Name of the column with valid measurements.

    Returns:
    pd.DataFrame: a DataFrame the mean values per station.
    """
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

def get_mean(df, stations_col:str, measurements:str) -> pd.DataFrame:
    """Delivers maximum concentration for specific pollutant.

    Args:
    df (pd.DataFrame): The DataFrame with valid values for specific pollutant
    stations_col (str): Name of the column with the measurement stations identificator.
    measurements (str): Name of the column with valid measurements.

    Returns:
    pd.DataFrame: a DataFrame the maximum values per station.
    """
     
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
    """Delivers the 99th percentile for a specific pollutant.

    Args:
    df (pd.DataFrame): The DataFrame with valid values for specific pollutant
    stations_col (str): Name of the column with the measurement stations identificator.
    measurements (str): Name of the column with valid measurements.

    Returns:
    pd.DataFrame: a DataFrame the 99th percentile values per station.
    """
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