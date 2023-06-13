import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import toml
import folium
import datetime
from datetime import date

# Read the config file
config = toml.load("streamlit/config.toml")
theme = config.get("theme", {})

# Access theme values
primary_color = theme.get("primaryColor")
background_color = theme.get("backgroundColor")
secondary_background_color = theme.get("secondaryBackgroundColor")
text_color = theme.get("textColor")
font = theme.get("font")

st.title('Tornado Impact Estimator')

image = Image.open('storm.jpg')

st.image(image)
###########################################################################


st.markdown('''
Welcome to the Tornado-impact estimator. Here you can get an estimate of the damage
caused by a tornado based on the Fujita-scale.
The Fujita-scale rates the intensity of a tornado based on the damage inflicted
on buildings and vegetation.
''')

image = Image.open('Enhanced_Fujita_Scale.jpg')
st.image(image, width=600)
st.caption('https://www.iccsafe.org/building-safety-journal/bsj-dives/how-damage-determines-a-tornados-rating-from-fujita-to-enhanced-fujita/')
#df = pd.read_csv("raw_data/dataframe.csv")
#\\wsl.localhost\Ubuntu\home\oscardolk\code\OscarDolk\chbohne99\predicting-storms

#df = pd.DataFrame(
#np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#    columns=['lat', 'lon'])

#st.map(df)

# Set the initial center coordinates for the map
initial_coords = [37.0902, -95.7129]

# Create the map object using folium
m = folium.Map(location=initial_coords, zoom_start=4)

STATE = st.selectbox(
    'Which State do you want to select?',
    ('FLORIDA', 'ILLINOIS', 'OKLAHOMA', 'CALIFORNIA', 'MINNESOTA',
       'TEXAS', 'TENNESSEE', 'ALABAMA', 'WYOMING', 'WISCONSIN', 'OHIO',
       'NEBRASKA', 'INDIANA','GEORGIA', 'VIRGINIA', 'MISSOURI',
       'NORTH CAROLINA', 'COLORADO','NORTH DAKOTA', 'KANSAS', 'NEW YORK',
       'IOWA', 'MARYLAND','ARKANSAS', 'SOUTH CAROLINA', 'MONTANA',
       'SOUTH DAKOTA', 'IDAHO','PENNSYLVANIA','MICHIGAN', 'ARIZONA',
       'MISSISSIPPI', 'LOUISIANA','NEW MEXICO'))

st.write('You selected:', STATE)
st.markdown('####')

#option = st.selectbox(
#    'What is the width of the Tornado',
#    ('0-2 meters', '2-5 meters', '> 5 meters'))

#st.write('You selected:', option)
#
#option = st.selectbox(
#    'What is the length of the Tornado',
#    ('0-2 meters', '2-5 meters', '> 5 meters'))


#Tornado duration selection.####################################################
st.markdown('''
The typical lifetime for a strong Tornado is about eight minutes.
In exceptional cases, violent events can last more than three hours.
Please select the duration of your Tornado:
''')
DURATION= st.slider('',0, 180, 8)
st.write("You selected a duration of:", DURATION, 'minutes.')
st.markdown('####')

#Tornado width selection########################################################
st.markdown('''
The width of Tornados can vary greatly. On average, a tornado is about 45 meters wide.
Please select the width of your Tornado:
''')
TOR_WIDTH = st.slider('', 0, 1395, 45)
st.write("You selected a width of:", TOR_WIDTH, 'meters.')
st.markdown('####')

#Tornado length selection########################################################
st.markdown('''
The length a Tornado travels can vary greatly. On average, a tornado travels a distance of 4,5 km before dissapearing.
Please select the travel length of your Tornado:
''')
TOR_LENGTH = st.slider('', 0, 100, 4)
st.write("Ýou selected a travel length of:", TOR_LENGTH, 'kilometers.')
st.markdown('####')
#The max lenght of tornados from the dataset is 643,737 kilometers.

#Convert Tornado Width to meters.
#Width of the tornado or tornado segment while on the ground (in feet).
tornado_width = TOR_WIDTH /3.281

#Convert Tornado Length to meters.
#Length of the tornado or tornado segment while on the ground (in miles to the tenth).
tornado_length = TOR_LENGTH * 1.6093435

#Tornado date selection#########################################################
st.markdown('''
Tornados can happen at any time and anywhere.
But most tornados occur between March and June. Please select a date for your Tornado.
''')
today = date.today()
min_date = today #+ datetime.timedelta(days=1)
BEGIN_DATE = st.date_input(
    '', min_value=min_date)
    #datetime.date(today.year, today.month, today.day))
#st.write('You have selected this date:', BEGIN_DATE)


#Prediction#####################################################################
st.title('Predict the Damage for your tornado')
damage_predict = st.button('Click here for Damage Prediction')
st.write(damage_predict)

url = 'http://localhost:8000/predict'
url = 'https://api.example.com/data'

params = {
    'Tornado_width': TOR_WIDTH,
    'Tornado_length': TOR_LENGTH,
    'Duration': DURATION,
    'Date': BEGIN_DATE,
    'State': STATE
}

# Make a request to the API
if damage_predict:
    # Make a request to the API

    response = requests.get(url, params=params)

# Handle the response
    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.write(f"Error: {response.status_code}")


#Frequency Prediction#####################################################################
st.title('Predict the frequency of tornados')

YEAR = st.selectbox('Choose a Year:', ('2023', '2024'))

frequency_predict = st.button('Click here for Frequency Prediction')
st.write(frequency_predict)

params_frequency = {
    'Year': YEAR
}

# Make a request to the API
if frequency_predict:
    # Make a request to the API

    response = requests.get(url, params=params_frequency)

# Handle the response
    if response.status_code == 200:
        data = response.json()
        st.write(data)
    else:
        st.write(f"Error: {response.status_code}")
