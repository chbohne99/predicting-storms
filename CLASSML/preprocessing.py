import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler


def preprocessing(df):
    '''
    Preprocess the data for the classification task
    '''
    tornados = df[df['EVENT_TYPE'] == 'Tornado']

    # remove all the duplicates
    tornados.drop_duplicates(inplace=True)

    # transform Begin date time and end date time to datetime
    tornados['BEGIN_DATE_TIME'] = pd.to_datetime(tornados['BEGIN_DATE_TIME'])
    tornados['END_DATE_TIME'] = pd.to_datetime(tornados['END_DATE_TIME'])

    # create the duration of the tornados in minutes
    tornados['DIFF'] = tornados.END_DATE_TIME - tornados.BEGIN_DATE_TIME
    def total_seconds(row):
        row = row.total_seconds()/60
        return row
    tornados['DIFF'] = tornados['DIFF'].map(total_seconds)

    # replace the 0 duration with the mean duration
    tornados.DIFF.replace(0, np.nanmean(tornados.DIFF), inplace=True)

    data_torn = tornados[['STATE', 'BEGIN_DATE_TIME','END_DATE_TIME','TOR_F_SCALE',
                      'TOR_LENGTH', 'TOR_WIDTH','BEGIN_LAT', 'BEGIN_LON',
                      'END_LAT', 'END_LON', 'DIFF']]

    data_torn.drop(index = data_torn[data_torn.STATE.isin(['VIRGIN ISLANDS', 'ALASKA', 'DISTRICT OF COLUMBIA',
                    'RHODE ISLAND','Kentucky','HAWAII', 'VERMONT', 'DELAWARE', 'NEW HAMPSHIRE', 'OREGON',
                    'CONNECTICUT', 'WASHINGTON', 'UTAH', 'MAINE','WEST VIRGINIA', 'NEW JERSEY', 'MASSACHUSETTS',
                    'PUERTO RICO', 'NEVADA'])].index, inplace=True)
    data_torn.reset_index(inplace=True)
    data_torn.drop(columns = 'index', inplace=True)

    data_torn.dropna(subset=['TOR_LENGTH'], inplace=True)

    def extract_m(row):
        row = row.month
        return row
    def extract_y(row):
        row = row.year
        return row
    def extract_d(row):
        row = row.dayofyear
        return row

    data_torn['MONTH'] = data_torn.BEGIN_DATE_TIME.map(extract_m)
    data_torn['YEAR'] = data_torn.BEGIN_DATE_TIME.map(extract_y)
    data_torn['DAY'] = data_torn.BEGIN_DATE_TIME.map(extract_d)

    data_torn.YEAR.replace([2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060,
       2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071,
       2072], [1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960,
       1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971,
       1972], inplace=True)

    data_torn.reset_index(inplace=True)
    data_torn.drop(columns = 'index', inplace=True)

    data_torn['Month_sin']=data_torn.MONTH.apply(lambda x:
        np.sin(2*np.pi*x/12))
    data_torn['Month_cosin']=data_torn.MONTH.apply(lambda x:
        np.cos(2*np.pi*x/12))
    data_torn.drop(columns = 'MONTH', inplace=True)

    data_torn['Day_sin']=data_torn.DAY.apply(lambda x:
        np.sin(2*np.pi*x/365))
    data_torn['Day_cosin']=data_torn.DAY.apply(lambda x:
        np.cos(2*np.pi*x/365))
    data_torn.drop(columns = 'DAY', inplace=True)

    data_torn['AREA'] = data_torn.TOR_WIDTH * data_torn.TOR_LENGTH

    data_torn.drop(index=((data_torn[data_torn.TOR_F_SCALE == 'EFU']).index), inplace=True)

    data_torn.dropna(subset=['TOR_F_SCALE'],inplace=True)
    print('Created all the variables needed!')

    data_torn.replace(['F0', 'F1', 'F2', 'F3', 'F4', 'F5'], ['EF0', 'EF1', 'EF2',
                                                       'EF3', 'EF4', 'EF5'], inplace=True)



    # Instantiate the Ordinal Encoder
    ordinal_encoder = OrdinalEncoder(categories = [["EF0", 'EF1', 'EF2',
                                                    'EF3', 'EF4', 'EF5']])

    # Fit it
    ordinal_encoder.fit(data_torn[["TOR_F_SCALE"]])

    # Display the learned categories

    # Transforming categories into ordered numbers
    data_torn["encoded_f_scale"] = ordinal_encoder.transform(data_torn[["TOR_F_SCALE"]])

    # Showing the transformed classes
    data_torn.drop(columns = ['TOR_F_SCALE'], inplace=True)

    print('Encoded the target variable!')

    # Instantiate the OneHotEncoder
    ohe = OneHotEncoder(sparse = False)

    # Fit encoder
    data_torn = pd.concat([data_torn,pd.get_dummies(data_torn['STATE'])], axis = 1)
    data_torn.drop(columns = ["STATE"], inplace = True)

    print('Encoded the states!')

    data_torn.drop(columns =  ['BEGIN_DATE_TIME', 'END_DATE_TIME','END_LAT',
                               'END_LON', 'BEGIN_LAT', 'BEGIN_LON'], inplace=True)

    # scale the data
    mm_scaler = MinMaxScaler()

    # Step 1- Fit the scaler to the `GrLiveArea`
    # to "learn" the median value and the IQR

    mm_scaler.fit(data_torn[['TOR_LENGTH','TOR_WIDTH','DIFF','AREA']])

    # 2-Scale/Transform
    # <-> apply the transformation (value - median) / IQR for every house

    data_torn[['TOR_LENGTH','TOR_WIDTH','DIFF','AREA']]\
                           = mm_scaler.transform(data_torn[['TOR_LENGTH',
                            'TOR_WIDTH','DIFF','AREA']])

    data_torn.dropna(inplace=True)

    return data_torn
