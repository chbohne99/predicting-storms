import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fitting(df):

    # change begin_date to
    def extract_m(row):
        row = row.month
        return row
    def extract_y(row):
        row = row.year
        return row
    def extract_d(row):
        row = row.dayofyear
        return row

    df['MONTH'] = df.begin_date.map(extract_m)
    df['YEAR'] = df.begin_date.map(extract_y)
    df['DAY'] = df.begin_date.map(extract_d)

    df.reset_index(inplace=True)
    df.drop(columns = 'index', inplace=True)

    df['Month_sin']=df.MONTH.apply(lambda x:
        np.sin(2*np.pi*x/12))
    df['Month_cosin']=df.MONTH.apply(lambda x:
        np.cos(2*np.pi*x/12))
    df.drop(columns = 'MONTH', inplace=True)

    df['Day_sin']=df.DAY.apply(lambda x:
        np.sin(2*np.pi*x/365))
    df['Day_cosin']=df.DAY.apply(lambda x:
        np.cos(2*np.pi*x/365))
    df.drop(columns = 'DAY', inplace=True)

    df.drop(columns = 'begin_date', inplace=True)

    df['AREA'] = df.tornado_width * df.tornado_length

    # encoding
    feature_list = ['ALABAMA','ARIZONA','ARKANSAS','CALIFORNIA','COLORADO','FLORIDA','GEORGIA',
     'IDAHO','ILLINOIS','INDIANA','IOWA','KANSAS','KENTUCKY','LOUISIANA','MARYLAND',
     'MICHIGAN','MINNESOTA','MISSISSIPPI','MISSOURI','MONTANA','NEBRASKA',
     'NEW MEXICO','NEW YORK','NORTH CAROLINA','NORTH DAKOTA','OHIO','OKLAHOMA',
     'PENNSYLVANIA','SOUTH CAROLINA','SOUTH DAKOTA','TENNESSEE','TEXAS','VIRGINIA',
     'WISCONSIN','WYOMING']

    d = pd.DataFrame(0, index=[0], columns=feature_list)
    d['state'] = 1

    data_torn = pd.concat([df,d], axis = 1)
    data_torn.drop(columns = ["state"], inplace = True)


    # Step 0 - Instanciate MINMAX Scaler

    mm_scaler = MinMaxScaler()

    # Step 1- Fit the scaler to the `GrLiveArea`
    # to "learn" the median value and the IQR

    mm_scaler.fit(data_torn[['tornado_length','tornado_width','duration','AREA']])

    # 2-Scale/Transform
    # <-> apply the transformation (value - median) / IQR for every house

    data_torn[['tornado_length','tornado_width','duration','AREA']]\
                           = mm_scaler.transform(data_torn[['tornado_length',
                                                            'tornado_width',
                                                            'duration','AREA']])
    data_torn.rename(columns = {'tornado_length':'TOR_LENGTH', 'tornado_width':'TOR_WIDTH',
                         'duration':'DIFF'}, inplace=True)

    return data_torn
