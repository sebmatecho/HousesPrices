import json
# from tkinter import N
from matplotlib import gridspec, ticker
import folium
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
# import pyautogui

from st_aggrid                import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from PIL                      import Image
from plotly                   import express as px
from folium.plugins           import MarkerCluster
from streamlit_folium         import folium_static
from matplotlib.pyplot        import figimage
from distutils.fancy_getopt   import OptionDummy


def folium_static(fig, width=1200, height=750):
# width, height=1300, 800#pyautogui.size()
    """
    Renders `folium.Figure` or `folium.Map` in a Streamlit app. This method is 
    a static Streamlit Component, meaning, no information is passed back from
    Leaflet on browser interaction.
    Parameters
    ----------
    width : int
        Width of result
    
    Height : int
        Height of result
    Note
    ----
    If `height` is set on a `folium.Map` or `folium.Figure` object, 
    that value supersedes the values set with the keyword arguments of this function. 
    Example
    -------
     m = folium.Map(location=[45.5236, -122.6750])
     folium_static(m)
    """

    # if Map, wrap in Figure
    if isinstance(fig, folium.Map):
        fig = folium.Figure().add_child(fig)
        return components.html(
            fig.render(), height=(fig.height or height) + 10, width=width
            )

    # if DualMap, get HTML representation
    elif isinstance(fig, plugins.DualMap):
        return components.html(
            fig._repr_html_(), height=height + 10, width=width
        )

@st.cache(allow_output_mutation=True)
def get_file():
     url = 'https://raw.githubusercontent.com/sebmatecho/CienciaDeDatos/master/ProyectoPreciosCasas/data/kc_house_data.csv'
     data = pd.read_csv(url)
     return data

@st.cache(allow_output_mutation=True)
def get_geofile():
     url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
     geofile = gpd.read_file(url)
     return geofile
# get geofile

def dashboard (data):
     plt.rcParams.update(plt.rcParamsDefault)
     plt.style.use('bmh')
     fig = plt.figure(figsize = (24,12), constrained_layout = True)
     gs = gridspec.GridSpec(2, 2, figure = fig)
     fig.add_subplot(gs[0,:])
     # primer gráfico
     df = data[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
     sns.lineplot(df['yr_built'], df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('Year of construction', fontsize = 20)
     plt.xticks(fontsize=16)
     plt.yticks(fontsize=16)
     


     # Segundo gráfico 
     fig.add_subplot(gs[1,0])
     df = data[['bedrooms','price']].groupby('bedrooms').mean().reset_index()

     sns.barplot(df['bedrooms'], df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('No. of bedrooms', fontsize = 20)
     plt.xticks(fontsize=16)
     plt.yticks(fontsize=16)
     # Tercer gráfico
     fig.add_subplot(gs[1,1])
     df = data[['bathrooms','price']].groupby('bathrooms').mean().reset_index()
     sns.barplot(df['bathrooms'], df['price'], color = 'orange')
     plt.ylabel('Price (Millions of Dollars)', fontsize = 20)
     plt.xlabel('No. of bathrooms', fontsize = 20)
     plt.xticks(fontsize=16)
     plt.yticks(fontsize=16)
     st.pyplot(fig)
     return None

def mapa1(data,width=1100, height=750):
     ZIP_list =  list(set(data['zipcode'])) 
     geofile = get_geofile() 
     geofile = geofile[geofile['ZIP'].isin(ZIP_list)]
     data_aux = data[['id','zipcode']].groupby('zipcode').count().reset_index()
     custom_scale = data_aux['id'].quantile([0,0.2,0.4,0.6,0.8,1]).tolist()
     
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(
                         geo_data=geofile, 
                          data=data_aux,
     #                     key_on='feature.properties.ZIPCODE',
     #                     columns=['zipcode', 'id'],
     #                     threshold_scale=custom_scale,
     #                     fill_color='YlOrRd',
        highlight=True).add_to(mapa)
     folium_static(mapa, width=0.45*width, height=0.45*width)
     return None

def mapa2(data,geo_info,width=1100, height=750):
     data_aux = data[['price','zipcode']].groupby('zipcode').mean().reset_index()
     custom_scale = (data_aux['price'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(geo_data=geo_info, 
                    data=data_aux,
                    key_on='feature.properties.ZIPCODE',
                    columns=['zipcode', 'price'],
                    threshold_scale=custom_scale,
                    fill_color='YlOrRd',
                    highlight=True).add_to(mapa)
     folium_static(mapa, width=0.45*width, height=0.45*width)
     return None

def mapa3(data,geo_info,width=1000, height=750):
     data_aux = data[['price/sqft','zipcode']].groupby('zipcode').mean().reset_index()
     custom_scale = (data_aux['price/sqft'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=8)
     folium.Choropleth(geo_data=geo_info, 
                    data=data_aux,
                    key_on='feature.properties.ZIPCODE',
                    columns=['zipcode', 'price/sqft'],
                    threshold_scale=custom_scale,
                    fill_color='YlOrRd',
                    highlight=True).add_to(mapa)
     folium_static(mapa, width=0.45*width, height=0.45*width)
     return None

def info_geo(data,width=1000, height=750):
     mapa = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=9)
     markercluster = MarkerCluster().add_to(mapa)
     for nombre, fila in data.iterrows():
          folium.Marker([fila['lat'],fila['long']],
                         popup = 'Precio: ${}, \n Fecha: {} \n {} habitaciones \n {} baños \n constuida en {} \n área de {} pies cuadrados \n Precio por pie cuadrado: {}'.format(
                         fila['price'],
                         fila['date'],
                         fila['bedrooms'],
                         fila['bathrooms'],
                         fila['yr_built'], 
                         fila['sqft_living'], 
                         fila['price/sqft'])
          ).add_to(markercluster)
     folium_static(mapa, width=width, height=0.45*width)
     return None

def descriptiva(data):
     att_num = data.select_dtypes(include = ['int64','float64'])
     media = pd.DataFrame(att_num.apply(np.mean))
     mediana = pd.DataFrame(att_num.apply(np.median))
     std = pd.DataFrame(att_num.apply(np.std))
     maximo = pd.DataFrame(att_num.apply(np.max))
     minimo = pd.DataFrame(att_num.apply(np.min))
     df_EDA = pd.concat([minimo,media,mediana,maximo,std], axis = 1)
     df_EDA.columns = ['Mínimo','Media','Mediana','Máximo','Variabilidad (DE)']
     df_EDA = df_EDA.drop(index =['id', 'lat', 'long','yr_built','yr_renovated'], axis = 0 )

     df_EDA['Variable'] =['Precio','No. Cuartos', 'No. Baños', 'Área construida (pies cuadrados)', 
                         'Área del terreno (pies cuadrados)', 'No. pisos', 'Vista agua (dummy)',
                         'Puntaje de la vista', 'Condición','Evaluación propiedad (1-13)',
                         'Área sobre tierra', 'Área sótano', 'Área construída 15 casas más próximas', 
                         'Área del terreno 15 casas más próximas', 'Precio por pie cuadrado']
     df_EDA = df_EDA[['Variable','Mínimo','Media','Mediana','Máximo','Variabilidad (DE)']]  
     return df_EDA 

def filt_opc(data):
     tier = st.multiselect(
          'Cuartil de precios', 
          list(data['price_tier'].unique()),
          list(data['price_tier'].unique())
          )
     data = data[data['price_tier'].isin(tier)]

     OptFiltro = st.multiselect(
          'Variables a incluir en los filtros:',
          ['Habitaciones', 'Baños', 'Área construida (pies cuadrados)','Pisos','Vista al agua','Evaluación de la propiedad','Condición', 'Código Postal'],
          ['Habitaciones', 'Baños'])

     if 'Código Postal' in OptFiltro:
          zipcod = st.multiselect(
               'Códigos postales',
               list(sorted(set(data['zipcode']))),
               list(sorted(set(data['zipcode']))))
          data = data[data['zipcode'].isin(zipcod)]

     if 'Habitaciones' in OptFiltro: 
          if data['bedrooms'].min() < data['bedrooms'].max():
               min_habs, max_habs = st.sidebar.select_slider(
               'Número de Habitaciones',
               options=list(sorted(set(data['bedrooms']))),
               value=(data['bedrooms'].min(),data['bedrooms'].max()))
               data = data[(data['bedrooms']>= min_habs)&(data['bedrooms']<= max_habs)]
          else:
               st.markdown("""
                    El filtro **Habitaciones** no es aplicable para la selección actual de valores
                    """)
     if 'Baños' in OptFiltro: 
          if data['bathrooms'].min() < data['bathrooms'].max():
               min_banhos, max_banhos = st.sidebar.select_slider(
               'Número de baños ',
               options=list(sorted(set(data['bathrooms']))),
               value=(data['bathrooms'].min(), data['bathrooms'].max()))
               data = data[(data['bathrooms']>= min_banhos)&(data['bathrooms']<= max_banhos)]
          else:
               st.markdown("""
                    El filtro **Baños** no es aplicable para la selección actual de valores
                    """)
     if 'Área construida (pies cuadrados)' in OptFiltro: 
          if data['sqft_living'].min() < data['sqft_living'].max():
               area = st.sidebar.slider('Área construida menor a', int(data['sqft_living'].min()),int(data['sqft_living'].max()),2000)
               data = data[data['sqft_living']<area]
          else:  
               st.markdown("""
                    El filtro **Área construida (pies cuadrados)** no es aplicable para la selección actual de valores
                    """)

     if 'Pisos' in OptFiltro: 
          if data['floors'].min() < data['floors'].max():
               min_pisos, max_pisos = st.sidebar.select_slider(
               'Número de Pisos',
               options=list(sorted(set(data['floors']))),
               value=(data['floors'].min(),data['floors'].max()))
               data = data[(data['floors']>= min_pisos)&(data['floors']<= max_pisos)]
          else:
               st.markdown("""
                    El filtro **Pisos** no es aplicable para la selección actual de valores
                    """)

     if 'Vista al agua' in OptFiltro: 
          if data['view'].min() < data['view'].max():
               min_vista, max_vista = st.sidebar.select_slider(
               'Puntaje de vista al agua',
               options=list(sorted(set(data['view']))),
               value=(data['view'].min(),data['view'].max()))
               data = data[(data['view']>= min_vista)&(data['view']<= max_vista)]
          else:
               st.markdown("""
                    El filtro **Vista al agua** no es aplicable para la selección actual de valores
                    """)
     if 'Evaluación de la propiedad' in OptFiltro:
          if data['grade'].min() < data['grade'].max():
               min_cond, max_cond = st.sidebar.select_slider(
               'Índice de evaluación de la propiedad',
               options=list(sorted(set(data['grade']))),
               value=(data['grade'].min(),data['grade'].max()))
               data = data[(data['grade']>= min_cond)&(data['grade']<= max_cond)]
          else:
               st.markdown("""
                    El filtro **Evaluación de la propiedad** no es aplicable para la selección actual de valores
                    """)

     if 'Condición' in OptFiltro:
          if data['condition'].min() < data['condition'].max():
               min_condi, max_condi = st.sidebar.select_slider(
               'Condición de la propiedad',
               options=list(sorted(set(data['condition']))),
               value=(data['condition'].min(),data['condition'].max()))
               data = data[(data['condition']>= min_condi)&(data['condition']<= max_condi)]
          else:
               st.markdown("""
                    El filtro **Condición** no es aplicable para la selección actual de valores
                    """)
     return data

st.set_page_config(page_title='App - Venta de casas',
                    layout="wide", 
                    page_icon=':house',  
                    initial_sidebar_state="expanded")

### Transform

def transform(data): 
     data['date'] = pd.to_datetime(data['date'], format = '%Y-%m-%d').dt.date
     data['yr_built']= pd.to_datetime(data['yr_built'], format = '%Y').dt.year
     # data['yr_renovated'] = data['yr_renovated'].apply(lambda x: pd.to_datetime(x, format ='%Y') if x >0 else x )
     # data['id'] = data['id'].astype(str)

     #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
     data['house_age'] = 'NA'
     #llenar la columna anterior con new_house para fechas anteriores a 2015-01-01
     data.loc[data['yr_built']>1990,'house_age'] = 'new_house' 
     #llenar la columna anterior con old_house para fechas anteriores a 2015-01-01
     data.loc[data['yr_built']<1990,'house_age'] = 'old_house'

     data['zipcode'] = data['zipcode'].astype(str)


     data.loc[data['yr_built']>=1990,'house_age'] = 'new_house' 
     data.loc[data['yr_built']<1990,'house_age'] = 'old_house'

     data.loc[data['bedrooms']<=1, 'dormitory_type'] = 'studio'
     data.loc[data['bedrooms']==2, 'dormitory_type'] = 'apartment'
     data.loc[data['bedrooms']>2, 'dormitory_type'] = 'house'

     data.loc[data['condition']<=2, 'condition_type'] = 'bad'
     data.loc[data['condition'].isin([3,4]), 'condition_type'] = 'regular'
     data.loc[data['condition']== 5, 'condition_type'] = 'good'

     data['price_tier'] = data['price'].apply(lambda x: 'Primer cuartil' if x <= 321950 else
                                                       'Segundo cuartil' if (x > 321950) & (x <= 450000) else
                                                       'Tercer cuartil' if (x > 450000) & (x <= 645000) else
                                                       'Cuarto cuartil')

     data['price/sqft'] = data['price']/data['sqft_living']
     return data

### Load

def load(data):
     data_ref = data.shape[0]
     st.sidebar.markdown("# Parámetros")

     st.title('Dinámica Inmobiliaria en King County')
     st.markdown(
     """
     ##### Propuesto por [Sébastien Lozano-Forero](https://www.linkedin.com/in/sebastienlozanoforero/)

     En Estados Unidos el mercado inmobiliario representa entre el 3% y el 5% del Producto Interno Bruto doméstico y continuamente recibe importantes inyecciones de capital que buscan optimizar la rentabilidad. Por tanto, existe una ventana de oportunidad interesante para integrar algunas de las tendencias globales en uso de información histórica y capacidades tecnológicas, que asistan la toma decisiones en varios puntos de los flujogramas de proceso de entidades inmobiliarias. 

     Este dashboard se deriva del estudio de un de año de actividad inmobiliaria (entre 2014 y 2015) en King County, WA - USA, que cuenta con ~2.2 millones de habitantes, los datos originales están disponibles [aquí](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). La idea principal es facilitar la presentación y manipulación de tal información con miras a un entendimiento más profundo de las tendencias en este mercado inmobiliario. 

     La pestaña **Dashboard** permite al usuario incorporar filtros que permitan estudiar tales tendencias de forma desagregada ([Paradoja de Simpson](https://en.wikipedia.org/wiki/Simpson%27s_paradox)). La pestaña **Recomendando Precios** incorpora un modelo de Machine Learning previamente entrenado para recomendar un precio a partir de las principales características del inmueble. El repositorio de este proyecto se encuentre disponible [acá](https://github.com/sebmatecho/HousesPrices)

     ## Filtro Requerido

     Las casas han sido divididas en cuatro grupos de igual tañamo, basadas en su precio. 
     -  El Primer Cuartil contendrá información de las propiedades que cuestan menos de \$321.950 
     -  El Segundo Cuartil contendrá información de las propiedades que cuestan entre \$321.950 y \$450.000
     -  El Tercer Cuartil contendrá información de las propiedades que cuestan entre \$450.000 y \$645.000
     -  El Cuarto Cuartil contendrá información de las propiedades que cuestan más de \$645.000

     El código postal puede utilizarse como proxy para lo localización de un inmueble en King County. Consulte [aquí](https://www.zipdatamaps.com/king-wa-county-zipcodes) para más información. 

     ### Filtros opcionales
     Con el objetivo de facilitar la exploración de lo datos, el usuario es libre de seleccionar los filtros necesarios. Una vez se seleccione la variable que se quiere usar como filtro del siguiente menú, utilice las sliders del banner izquierdo para manipular los valores permitidos de la variable. Tenga en cuenta que la inclusión y uso de los filtros también modificará las figuras presentadas en el resto de esta página. 

     """)
     
     data = filt_opc(data)
    
     ## Dashboard general 
     dashboard(data)

     # Mapas
     st.header('Distribución por Código Postal')
     
     # col1, col2 = st.columns(2)
     # with col1: 
     #      st.header("Densidad de casas disponibles")
     mapa1(data)
     # st.dataframe(geoData)

     # with col2: 
     #      # df = data[['id','zipcode']].groupby('zipcode').count().reset_index().rename(columns= {'zipcode':'Postal code','id':'Count'}).sort_values('Count', ascending= False)
     #      # st.dataframe(df)
     #      st.header("Precios de casas disponibles")
     #      mapa2(data,geo_data)

     # col1, col2 = st.columns(2)
     # with col1: 
     #      st.header("Costo de pie cuadrado")
     #      mapa3(data,geo_data)
          
     # with col2: 
     #      st.header('Valores por código postal')
     #      df = data[['id','zipcode','price','price/sqft']].groupby('zipcode').agg({'id':'count','price':'mean','price/sqft':'mean'}).reset_index().rename(columns= {'zipcode':'Postal code','id':'Count','price':'Average price','price/sqft':'Average price/sqft'})
     #      # st.dataframe(df)
     #      AgGrid(df,fit_columns_on_grid_load=True)


     st.header("Información geográfica de las propiedades disponibles")

     info_geo(data)

     # Estadística Descriptiva 

     st.markdown(
          """
     ### Información complementaria
     Finalmente, el resumen numérico de todas las variables consideradas en esta base de datos se presenta a continuación. Dicha información puede ser útil para encontrar tendencias dentro de clusters que sean de interés. 
          
          """)

     col1, col2 = st.columns(2)
     col1.metric("No. Casas", data.shape[0],str(100*round(data.shape[0]/data_ref,4))+'% de las casas disponibles',delta_color="off")
     col2.metric("No. Casas Nuevas (Construida después de 1990)",data[data['house_age'] == 'new_house'].shape[0],str(100*round(data[data['house_age'] == 'new_house'].shape[0]/data_ref,4))+'% de las casas disponibles',delta_color="off")
     AgGrid(descriptiva(data),fit_columns_on_grid_load=True)  
     return None


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ =='__main__':
     # Extract
     data = get_file() 
     # Transform
     data2 = transform(data)
     # Load
     load(data2)