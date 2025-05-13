import streamlit as st
import pandas as pd
import numpy as np
import requests as req
import os
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("api_key")


def misure(d):
    C = 273.15
    data = {
        # "tem_mean": round(d["main"]["temp"]-C,2),
        "umid": d['main']["humidity"],
        'wind':d['wind']['speed'],
        "pres": d['main']["pressure"],
        "coordinate": d["coord"],
        "name": d["name"],
        "giornata": d["weather"][0]["main"],
        "paese": d["sys"]["country"],
        "time": d["timezone"]//1000,
        "visi": d["visibility"],
        'liv_sea': d['main']["sea_level"],
    }
    return data


# 
# {'coord': {'lon': 11.4333, 'lat': 44.4667}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
# 'base': 'stations', 'main': {'temp': 293.5, 'feels_like': 293.31, 'temp_min': 292.37, 'temp_max': 294.4,
#  'pressure': 1014, 'humidity': 66, 'sea_level': 1014, 'grnd_level': 999}, 'visibility': 10000, 
#  'wind': {'speed': 2.24, 'deg': 80, 'gust': 4.47}, 'clouds': {'all': 77}, 'dt': 1747140809,
#    'sys': {'type': 2, 'id': 2004497, 'country': 'IT', 'sunrise': 1747108148, 'sunset': 1747161133},
#  'timezone': 7200, 'id': 3181927, 'name': 'Bologna', 'cod': 200}


if __name__ == "__main__":
    st.header("Dati meteorologici")

    city = st.text_input(
        label="Inserirsci una città italiana o straniera🌍", placeholder="city..."
    ).capitalize()
    if st.button("invia"):
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
        )
        stato = req.get(url)
        metriche = stato.json()
        data = misure(metriche)

        emoji={'Clouds': '☁️','Clear':'☀️','Rain':'🌧️','Snow':'🌨️',}

        #grafiche
        nam,cou= st.columns(2)
        col7,col8 = st.columns(2)
        colx,coly,colz, = st.columns(3)
        col1,col2,col3, = st.columns(3)
        col4,col5 = st.columns(2) #,col6
        colx,coly,colz= st.columns(3)

        # {'tem_mean': 20.52, 'umid': 67, 'wind': 1.79, 'pres': 1014, 'coordinate': {'lon': 11.4333, 'lat': 44.4667},
        #   'name': 'Bologna', 'giornata': 'Clouds', 'paese': 'IT', 'visi': 10000, 'liv_sea': 1014}
        nam.success(data['name'])
        cou.success(data['paese'])
        
        col7.metric("Longitudine", f"{data['coordinate']['lon']}°", border=True)
        col8.metric("Latitudine", f"{data['coordinate']['lat']}°",  border=True)
        
        col1.metric("Temperature", f"{data['tem_mean']}°C", border=True)
        col2.metric("Tempo", f"{data['giornata']}{emoji[data['giornata']]}", border=True)
        col3.metric("Humidity", f"{data['umid']}%", border=True)
        
        col4.metric("Pressure", f"{data['pres']} inHg",  border=True)
        col5.metric("Timezone", f"{data['time']}", border=True)

        colx.metric("livello sul mare", f"{data['liv_sea']}m", border=True)
        coly.metric("visibilità", f"{data['tem_mean']}m", border=True)
        colz.metric("Wind", f"{data['wind']} Km/H", border=True)
        # col6.metric
        cordin= pd.DataFrame([[data['coordinate']['lat'],data['coordinate']['lon']]], columns=['LAT','LON'])
        st.map(data=cordin, height=500,width=500)
        #ksjfadsklf
