import pandas as pd
import numpy as np
from data.constants import metric_constants

def get_daily_rainfall_data(start_year=2009, end_year=2018):
    df = pd.read_csv('/Users/alexa/projects/prawn-app/api/data/environmental_data/proserpineRainfallData.csv')
    df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    df = df[(df['Month'] != 2) | (df['Day'] != 29)]  # remove leap year day
    df = df[['Month', 'Day', 'Rainfall']]
    mean_daily_df = df.groupby(['Month', 'Day']).mean() 

    daily_rain = mean_daily_df['Rainfall'].values # starting 01/01
    daily_rain_production_year = np.concatenate((daily_rain[183:], daily_rain[:183])) # starting 01/07

    return daily_rain_production_year

def get_daily_evaporation_data():
    df = pd.read_csv('/Users/alexa/projects/prawn-app/api/data/environmental_data/proserpineEvaporationData.csv')
    df['evaporation'].fillna(value=6.9, inplace=True) # replace missing data with avg
    daily_evaporation = df['evaporation'].values # starting 01/01

    daily_evaporation_production_year = np.concatenate((daily_evaporation[183:], daily_evaporation[:183])) # starting 01/07

    return daily_evaporation_production_year

def get_net_daily_water_from_evap_and_rain_per_ha():
    rain = (get_daily_rainfall_data() / metric_constants['MILIMETRES_IN_METRE']) * metric_constants['METERS_IN_HECTARES'] * metric_constants['LITRES_IN_M3']
    evaporation = (get_daily_evaporation_data() / metric_constants['MILIMETRES_IN_METRE']) * metric_constants['METERS_IN_HECTARES'] * metric_constants['LITRES_IN_M3']

    return rain - evaporation

yearly_evap_and_rain_per_ha = get_net_daily_water_from_evap_and_rain_per_ha()