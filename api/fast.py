import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CLASSML.preprocessing import preprocessing
from CLASSML.registry import load_model
import numpy as np

app = FastAPI()
app.state.model=load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict_scale")
def predict_scale(
        pickup_datetime: str,  # 2013-07-06 17:18:00
        pickup_longitude: float,    # -73.950655
        pickup_latitude: float,     # 40.783282
        dropoff_longitude: float,   # -73.984365
        dropoff_latitude: float,    # 40.769802
        passenger_count: int
    ):      # 1
    """
    Make a single course prediction.
    Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitly refers to the "US/Eastern" timezone (as any user in New York City would naturally write)
    """
    pickup_date = pd.Timestamp(datetime.strptime(pickup_datetime,"%Y-%m-%d %H:%M:%S"), tz='UTC')
    X_pred = pd.DataFrame(dict(
        pickup_datetime=[pickup_date],
        pickup_longitude=[float(pickup_longitude)],
        pickup_latitude=[float(pickup_latitude)],
        dropoff_longitude=[float(dropoff_longitude)],
        dropoff_latitude=[float(dropoff_latitude)],
        passenger_count=[int(passenger_count)],
    ))
    print(type(X_pred))
    X_processed = preprocess_features(X_pred)
    print(type(X_processed))
    model = load_model()
    y_pred = app.state.model.predict(X_processed)
    print(y_pred)
    return {
        'fare_amount':float(np.round(y_pred,2))
    }

@app.get("/predict_frequency")
def predict_frequency(year):
    year=int(year)


@app.get("/")
def root():
    return {
    'response': '200'
        }
