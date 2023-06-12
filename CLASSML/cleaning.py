import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
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
                      'END_LAT', 'END_LON', 'DIFF']]

    # azimuth direction -> angle relativeley to geographical North
    data_torn['DIR'] = np.arctan((data_torn.END_LON - data_torn.BEGIN_LON)/
                                 (data_torn.END_LAT - data_torn.BEGIN_LAT))
    # fill missing values with the mean traveling direction of the tornado
    data_torn.DIR.fillna(np.nanmean(data_torn.DIR), inplace=True)
    data_torn.reset_index(inplace=True)

    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r
    harv_dist = []
    for i in range(len(data_torn)):
        harv_dist.append(haversine(data_torn.BEGIN_LON[i], data_torn.BEGIN_LAT[i],
                                   data_torn.END_LON[i],data_torn.END_LAT[i]))

    data_torn['HARV_DIST'] = harv_dist

    data_torn.dropna(subset=['TOR_LENGTH'], inplace=True)
    data_torn.HARV_DIST.fillna(np.nanmean(data_torn.HARV_DIST), inplace=True)

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
    data_torn['Month_sin']=data_torn.MONTH.apply(lambda x:
        np.sin(2*np.pi*data_torn.MONTH[x]/12))
    data_torn['Month_cosin']=data_torn.MONTH.apply(lambda x:
        np.cos(2*np.pi*data_torn.MONTH[x]/12))
    data_torn.drop(columns = 'MONTH', inplace=True)

    data_torn['YEAR'] = data_torn.BEGIN_DATE_TIME.map(extract_y)
    data_torn['DAY'] = data_torn.BEGIN_DATE_TIME.map(extract_d)

    data_torn['AREA'] = data_torn.TOR_WIDTH * data_torn.TOR_LENGTH

    data_torn.drop(columns = 'index', inplace=True)
    data_torn.drop(index=((data_torn[data_torn.TOR_F_SCALE == 'EFU']).index), inplace=True)

    print('Created all the variables needed!')

    data_torn.replace(['F0', 'F1', 'F2', 'F3', 'F4'], ['EF0', 'EF1', 'EF2',
                                                       'EF3', 'EF4'], inplace=True)
    return data_torn
