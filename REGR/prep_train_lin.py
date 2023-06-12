from pandas import pd
from sklearn.linear_model import LinearRegression

def prep_train_lin(df, year):
    # only tornadoes
    torn = df[df.EVENT_TYPE == 'Tornado']

    torn.BEGIN_DATE_TIME = pd.to_datetime(torn.BEGIN_DATE_TIME)

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


    torn.DAMAGE_PROPERTY = torn.DAMAGE_PROPERTY.map(transform_money)
    torn.DAMAGE_CROPS = torn.DAMAGE_CROPS.map(transform_money)

    merg = pd.DataFrame(torn.groupby(by = ['YEAR']).count()['EVENT_ID'].reset_index())
    X = merg.drop(columns = 'EVENT_ID')
    y = merg['EVENT_ID']

    lr = LinearRegression()
    lr.fit(X,y)

    slope = lr.coef_
    inter = lr.intercept_


    y_pred = lr.predict([year])

    return y_pred
