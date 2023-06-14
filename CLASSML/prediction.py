from registry import *
from fitting import fitting
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

    X_processed = fitting(X_pred)

    model=load_model_scale()
    y_pred = model.predict(X_processed)
    return y_pred
