import streamlit as st
import pandas as pd
import json
from urllib3 import request
# from bs4 import BeautifulSoup
#import time
#import os
import plotly.express as px


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

# printing some data for live measurement

# print("Station ID:", resp_json["data"]["id"])
# print("Station Name:", resp_json["data"]["meta"]["name"])

# print("Date mesure:", resp_json["data"]["measurements"]["date"])
# print("Direction vent:", resp_json["data"]["measurements"]["wind_heading"])
# print("Vitesse vent min:", resp_json["data"]["measurements"]["wind_speed_min"])
# print("Vitesse vent max:", resp_json["data"]["measurements"]["wind_speed_max"])
# print("Vitesse vent avg:", resp_json["data"]["measurements"]["wind_speed_avg"])
# print("Date location:", resp_json["data"]["location"]["date"])

print(type(resp_json))  #checking type of the response
print(resp_json.keys())  #checking number of rows in the data part of the response
# with open("resp_json_output.json", "w", encoding="utf-8") as f:
#     json.dump(resp_json, f, ensure_ascii=False, indent=4)
st.write("Live wind measurement: Heric weather station")

# === loading json reply data into a DataFrame
data = resp_json["data"]                                 #getting data part of the json reply as a dicitonnary
df = pd.DataFrame(data, columns = resp_json["legend"])   #initiating dataframe with data and columns names
                      #naming columns after DF initilization

print(df.head(5))
df.info()

# === dataframe for lvie measurements
# df=pd.DataFrame({
#                 "date_measurement": [resp_json["data"]["measurements"]["date"]],
#                 "wind_speed_min": [resp_json["data"]["measurements"]["wind_speed_min"]],
#                 "wind_speed_avg": [resp_json["data"]["measurements"]["wind_speed_avg"]],
#                 "wind_speed_max": [resp_json["data"]["measurements"]["wind_speed_max"]]
#                 })
# df=pd.DataFrame({
#                 "date_measurement": [resp_json["data"]["measurements"]["date"]],
#                 "measure": "wind_speed_avg",
#                 "value": [resp_json["data"]["measurements"]["wind_speed_avg"]],
#                 })

# df=df.append({
#                 "date_measurement": [resp_json["data"]["measurements"]["date"]],
#                 "measure": "wind_speed_min",
#                 "value": [resp_json["data"]["measurements"]["wind_speed_min"]],
#                 })
# df_melted = df.melt(id_vars="date_measurement", value_vars=["wind_speed_min", "wind_speed_max", "wind_speed_avg"], var_name="measure_type", value_name="measurement_value")
# df_melted = df_melted.set_index("date_measurement")

df = df.set_index("time")
def kmh_to_kt(kmh):
    """Convertit des km/h en noeuds (nds)."""
    return kmh / 1.852

# Conversion des colonnes de vitesse du vent en nds
df["wind_speed_min_nds"] = df["wind_speed_min"].apply(kmh_to_kt)
df["wind_speed_avg_nds"] = df["wind_speed_avg"].apply(kmh_to_kt)
df["wind_speed_max_nds"] = df["wind_speed_max"].apply(kmh_to_kt)
print(df.info)
# print(df_melted.info)
# st.line_chart(df)

fig = px.line(df, x=df.index, y=["wind_speed_min_nds","wind_speed_avg_nds", "wind_speed_max_nds"], markers=True)
# fig = px.line(df_melted, x=df_melted.index, y="measurement_value", color="measure_type", markers="True")
# fig.show()
st.plotly_chart(fig, use_container_width=True)

# st.line_chart(df, x=df.index, y=["wind_speed_min","wind_speed_avg", "wind_speed_max"])
lat = df.iloc[0, 0]
lon = df.iloc[0, 1]
st.write(lat)
st.write(lon)

map_data=pd.DataFrame([[lat,lon]], columns=['lat', 'lon'])

st.map(map_data)

print(df)
slider_dummy = st.slider("This is a slider")
input_dummy = st.text_input("Please leave a message:", key="message")
# print(st.session_state.message)

