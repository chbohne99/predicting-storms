import pandas as pd
import numpy as np

def cleaning(df):
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
    tornados.DIFF.replace(0, np.mean(tornados.DIFF), inplace=True)

    data_torn = tornados[['STATE', 'BEGIN_DATE_TIME','END_DATE_TIME','TOR_F_SCALE',
                      'TOR_LENGTH', 'TOR_WIDTH','BEGIN_LAT', 'BEGIN_LON',
                      'END_LAT', 'END_LON', 'DIFF', 'DAMAGE_PROPERTY', 'DAMAGE_CROPS',
                      'INJURIES_DIRECT', 'INJURIES_INDIRECT',
                        'DEATHS_DIRECT', 'DEATHS_INDIRECT']]

    # transform the money to actual numbers
    def transform_money(row):
        if 'K' in str(row):
            if row.strip('K') == '':
                row = 1_000
            else:
                row = float(row.strip('K'))*1_000
        elif 'M' in str(row):
            if row.strip('M') == '':
                row = 1_000_000
            else:
                row = float(row.strip('M'))*1_000_000
        elif 'B' in str(row):
            if row.strip('B') == '':
                row = 1_000_000_000
            else:
                row = float(row.strip('B'))*1_000_000_000
        elif 'T' in str(row):
            if row.strip('T'):
                row = 1_000_000_000_000
            else:
                row = float(row.strip('T'))*1_000_000_000_000
        return float(row)


    data_torn.DAMAGE_PROPERTY = data_torn.DAMAGE_PROPERTY.map(transform_money)
    data_torn.DAMAGE_PROPERTY.fillna(0, inplace=True)
    data_torn.DAMAGE_CROPS = data_torn.DAMAGE_CROPS.map(transform_money)
    data_torn.DAMAGE_PROPERTY.fillna(0, inplace=True)
    data_torn['DAMAGES'] = data_torn.DAMAGE_PROPERTY + data_torn.DAMAGE_CROPS


    data_torn.drop(index = data_torn[data_torn.STATE.isin(['VIRGIN ISLANDS', 'ALASKA', 'DISTRICT OF COLUMBIA',
                    'RHODE ISLAND','Kentucky','HAWAII', 'VERMONT', 'DELAWARE', 'NEW HAMPSHIRE', 'OREGON',
                    'CONNECTICUT', 'WASHINGTON', 'UTAH', 'MAINE','WEST VIRGINIA', 'NEW JERSEY', 'MASSACHUSETTS',
                    'PUERTO RICO', 'NEVADA'])].index, inplace=True)
    data_torn.reset_index(inplace=True)

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

    data_torn['AREA'] = data_torn.TOR_WIDTH * data_torn.TOR_LENGTH

    data_torn.drop(columns = 'index', inplace=True)
    data_torn.drop(index=((data_torn[data_torn.TOR_F_SCALE == 'EFU']).index), inplace=True)

    print('Created all the variables needed!')

    data_torn.replace(['F0', 'F1', 'F2', 'F3', 'F4','F5'], ['EF0', 'EF1', 'EF2',
                                                       'EF3', 'EF4', 'EF5'], inplace=True)
    return data_torn
