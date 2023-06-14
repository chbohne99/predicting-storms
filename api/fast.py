import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CLASSML.fitting import fitting
from CLASSML.registry import *
import numpy as np
import datetime

app = FastAPI()
app.state.model_scale=load_model_scale()
app.state.model_linear=load_linear_model()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict_scale")
def predict_scale(
        Tornado_width,
        Tornado_length,
        Duration,
        Date,
        State
    ):      # 1
    """
    Make a single course prediction.
    Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitly refers to the "US/Eastern" timezone (as any user in New York City would naturally write)
    """
    date = pd.Timestamp(datetime.strptime(Date,"%Y-%m-%d"), tz='UTC')
    X_pred = pd.DataFrame(dict(
        begin_date=[date],
        tornado_length=[float(Tornado_length)],
        tornado_width=[float(Tornado_width)],
        duration=[float(Duration)],
        state=[str(State).upper()],
        ))

    X_processed = fitting(X_pred)

    y_pred = app.state.model_scale.predict(X_processed)
    dic = {0:'Light Damage (EF0)', 1:'Moderate Damage (EF1)', 2:'Considerable Damage (EF2-EF5)'}

    y_predict = dic[y_pred[0]]

    return {
        'f_scale':y_predict
    }

@app.get("/predict_frequency")
def predict_frequency(year):
    year=int(year)

    d = {'YEAR': [year]}
    year_df = pd.DataFrame(d)
    y_pred=app.state.model_linear.predict(year_df)

    return {
        'frequency':round(y_pred[0])
    }


@app.get("/")
def root():
    return {
    'response': '200'
        }
