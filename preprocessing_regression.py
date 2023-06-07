import math
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df = pd.read_csv('data.csv')
#------------------------------------------------------------------------------#

def preprocessing(data):
    # Implement preprocessing from notebook because we are best team.




    # Drop the columns that doens't have values in DAMAGE_PROPERTY & 'DAMAGE_CROPS'
    data = data.dropna(subset=['DAMAGE_PROPERTY', 'DAMAGE_CROPS'], how='all')
    # Transform values object/str to float
    data['DAMAGE_CROPS'] = data.DAMAGE_CROPS.map(transform_money)

    #Sum up the Damage Crops and Damage Property into one new column

    data['TOTAL_DAMAGE'] = data['DAMAGE_CROPS'] + data['DAMAGE_PROPERTY']

    #Convert the Year Month into datetime
    data['EVENT_YM_B'] = pd.to_datetime(data['EVENT_YM_B'])

    # Create a new column Month
    data['MONTH'] = data.EVENT_YM_B.map(month)

    # Transform Month values to sin and cos values
    data['COS_MONTH'] = data.MONTH.map(to_cos)
    data['SIN_MONTH'] = data.MONTH.map(to_sin)

    #We now Filter the dataFrame based on the event types we are interested in.
    values_to_filter = ['Tornado', 'Thunderstorm Wind', 'Hail', 'Flash Flood','Flood','Heavy Rain']
    data = data[data['EVENT_TYPE'].isin(values_to_filter)]

    # Drop Columns that are not needed to use
    # Create a list of column names to drop
    columns_to_drop = ['Unnamed: 0', 'BEGIN_DAY', 'BEGIN_TIME', 'END_DAY',
                          'END_TIME', 'EPISODE_ID', 'BEGIN_DATE_TIME',
                          'END_DATE_TIME', 'INJURIES_DIRECT', 'INJURIES_INDIRECT',
                          'DEATHS_DIRECT', 'DEATHS_INDIRECT', 'DAMAGE_PROPERTY','DAMAGE_CROPS',
                          'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON', 'YEARMONTH',
                          'LATITUDE', 'LONGITUDE','EVENT_YM_B', 'EVENT_YM_E']
    # Drop the columns using the drop() function
    data.drop(columns=columns_to_drop, axis=1, inplace=True)


     # Instanciate the OneHotEncoder
    ohe = OneHotEncoder(sparse=False)

    # Fit data STATE with OneHotEncoder
    ohe.fit(data[['STATE']])

    # Transform the current "STATE column
    data[ohe.get_feature_names_out()] = ohe.transform(data[['STATE']])
    data.drop(columns=['STATE'], inplace=True )

    # Fit the data EVENT_TYPE with OneHotEncoder
    ohe.fit(data[['EVENT_TYPE']])

    # Transform the current EVENT_TYPE column
    data[ohe.get_feature_names_out()] = ohe.transform(data[['EVENT_TYPE']])


    #Instantiate the Scaler
    scaler = MinMaxScaler()

    #Fit the data YEAR with MinMaxScaler
    scaler.fit(data[['YEAR']])

    #Transforming the data YEAR with MinMaxScaler
    data['SCALED_YEAR'] = (scaler.transform(data[['YEAR']]))

    data.drop(columns=['YEAR','EVENT_ID','EVENT_TYPE'], inplace=True )



    return data




# Functions

def to_sin(MONTH):
    return math.sin(2*math.pi*MONTH/12)


def to_cos(MONTH):
    return math.cos(2*math.pi*MONTH/12)


def transform_money(row):
  if 'K' in str(row):
    row = float(row.strip('K'))*1_000
  elif 'M' in str(row):
    row = float(row.strip('M'))*1_000_000
  elif 'B' in str(row):
    row = float(row.strip('B'))*1_000_000_000
  return float(row)


def month(line):
    line = line.month
    return line
