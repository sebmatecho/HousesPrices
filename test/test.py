import streamlit as st
import pandas as pd
import geopandas as gpd
import folium 
from folium.plugins           import MarkerCluster
from streamlit_folium         import folium_static

st.title('Esto es una prueba')

def get_geofile( url ):
    geofile = gpd.read_file( url )
    return geofile
# get geofile
url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
geofile = get_geofile( url )


def extract():
     url = 'https://raw.githubusercontent.com/sebmatecho/CienciaDeDatos/master/ProyectoPreciosCasas/data/kc_house_data.csv'
     data = pd.read_csv(url)
     return data
data = extract()
geofile = geofile[geofile['ZIP'].isin(list(set(data['zipcode'])))]
data_aux = data[['id','zipcode']].groupby('zipcode').count().reset_index()
custom_scale = (data_aux['id'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
folium.Choropleth(geo_data=geofile, 
     data=data_aux,
     key_on='feature.properties.ZIP',
     columns=['zipcode', 'id'],
     threshold_scale=custom_scale,
     fill_color='YlOrRd',
     highlight=True).add_to(mapa)
folium_static(mapa)