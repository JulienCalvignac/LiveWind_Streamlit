import pandas as pd
import streamlit as st
# import json
from urllib3 import request
from datetime import datetime,timezone,timedelta
# from bs4 import BeautifulSoup
#import time
#import os
import plotly.express as px
# import pytz #was causing compatibilties issues with python version
# from sklearn.linear_model import LinearRegression

station_id = "1671" #Club ULM Héric 1671

start="last-day"
stop="now"
# str_stationadress_live = "http://api.pioupiou.fr/v1/live/"
str_stationadress_base = "http://api.pioupiou.fr/v1/archive/"

print("=== Getting historical station data: ===")
url_request = str_stationadress_base + station_id +   "?start=" + start + "&stop=" + stop

# print("=== Getting lates station data: ===")
# url_request = str_stationadress_live + station_id
# print("Station URL adress: " + url_request)

response = request("GET", url_request)
print(response.status)  #printing status code of the answer
# print(response.data)
resp_json=response.json()   #coverting answer into dictionnary

print(type(resp_json))  #checking type of the response
print(resp_json.keys())  #checking number of rows in the data part of the response

st.write("Live wind measurement: Heric weather station")
# slider_timehorizon = st.slider("History duration")
zoomhistory_select = st.segmented_control("Time history", ["1h","2h","4h","8h"], selection_mode="single", default="4h")


# === loading json reply data into a DataFrame
data = resp_json["data"]                                 #getting data part of the json reply as a dicitonnary
df = pd.DataFrame(data, columns = resp_json["legend"])   #initiating dataframe with data and columns names
                      #naming columns after DF initilization


def kmh_to_kt(kmh):
    """Convertit des km/h en noeuds (nds)."""
    return kmh / 1.852

# Conversion des colonnes de vitesse du vent en nds
df["wind_speed_min_nds"] = df["wind_speed_min"].apply(kmh_to_kt)
df["wind_speed_avg_nds"] = df["wind_speed_avg"].apply(kmh_to_kt)
df["wind_speed_max_nds"] = df["wind_speed_max"].apply(kmh_to_kt)

df['time'] = pd.to_datetime(df['time'])
print(df.head(5))

def get_start_time(depth_hours):
    
    tz_local = timezone(timedelta(hours=2),name= "LocalSpring") #fixing local timezone for 
    start_time_aware = (datetime.now(tz=tz_local)-pd.Timedelta(hours=depth_hours))

    print(start_time_aware)
    return start_time_aware

def update_df(df, start_time_aware):
    df_filtered=df[df['time'] > start_time_aware]
    df_filtered.info()
    return df_filtered

start_time_aware = get_start_time(int(zoomhistory_select[0]))
df_filtered = update_df(df, start_time_aware)
# model_reglin_wingavg = LinearRegression()
# model_reglin_wingavg.fit(df_filtered.time,df_filtered.wind_speed_max_nds)

if zoomhistory_select:
   start_time_aware = get_start_time(int(zoomhistory_select[0]))
   df_filtered = update_df(df, start_time_aware)
   print(df_filtered.describe())

df_filtered.describe()
dict_wind_measurements={
    "wind_speed_min_nds": "Vitesse min",
    "wind_speed_max_nds": "Rafales",
    "wind_speed_avg_nds": "Vitesse moyenne"
}

fig = px.line(df_filtered, x="time", y=["wind_speed_min_nds","wind_speed_avg_nds", "wind_speed_max_nds"], markers=True, labels=dict_wind_measurements)
fig.add_hline(y=df_filtered["wind_speed_max_nds"].mean(), line_dash="dash", line_color="red", annotation_text="Moyenne", annotation_position="top left")
fig.add_hline(y=df_filtered["wind_speed_avg_nds"].mean(), line_dash="dash", line_color="blue", annotation_text="Moyenne", annotation_position="top left")
fig.add_hline(y=df_filtered["wind_speed_min_nds"].mean(), line_dash="dash", line_color="blue", annotation_text="Moyenne", annotation_position="top left")
fig.update_layout(
    xaxis_title="Temps",  # Set the label for the x-axis
    yaxis_title="Vitesse [nds]",  # Set the label for the y-axis
)
st.plotly_chart(fig, use_container_width=True)


wind_polar = px.bar_polar(df_filtered, r="wind_speed_avg", theta="wind_heading",
                   color="wind_speed_avg", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Plasma_r)
st.plotly_chart(wind_polar, use_container_width=True)

# st.line_chart(df, x=df.index, y=["wind_speed_min","wind_speed_avg", "wind_speed_max"])
lat = df.iloc[0, 1]
lon = df.iloc[0, 2]
st.write(lat)
st.write(lon)

map_data=pd.DataFrame([[lat,lon]], columns=['lat', 'lon'])
st.map(map_data)

input_dummy = st.text_input("Please leave a message:", key="message")
# print(st.session_state.message)

