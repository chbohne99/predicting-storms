from registry import load_model
from preprocessing import preprocessing
import pandas as pd

def prediction(X_pred=None):

    if X_pred is None:
        X_pred = pd.DataFrame(dict(
            begin_date=[pd.Timestamp("2013-07-06", tz='UTC')],
            tornado_length=[50.02],
            tornado_width=[103.10],
            duration=[10.2],
            state=['TEXAS'],
            ))

    X_processed = preprocessing(X_pred)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=42)
    y_pred = []
    return y_pred
