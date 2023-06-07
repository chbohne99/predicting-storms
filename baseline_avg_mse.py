
from preprocessing_regression import preprocessing
import numpy as np

def baseline_avg_mse(df):
    df_prep = preprocessing(df)
    y = df_prep['TOTAL_DAMAGE']
    average = np.mean(y)
    difference = y - average # find the the difference between the actual and predicted value
    mse = np.mean(difference ** 2) # it takes the square of all diferences
    return (average,mse, np.sqrt(mse))




# #------------------------------------------------------------------------------#
