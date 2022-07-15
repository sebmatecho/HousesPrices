from re import template
from PIL import Image
import streamlit as st
import pandas as pd
import joblib
import numpy as np
# import boto3
import tempfile

st.set_page_config(page_title='App - Pronóstico',
                    layout="wide", 
                    page_icon='🚀',  
                    initial_sidebar_state="expanded")

st.title("Pronosticando precios de casas")
st.sidebar.markdown("Características")

@st.cache
def get_data():
     url = 'https://raw.githubusercontent.com/sebmatecho/CienciaDeDatos/master/ProyectoPreciosCasas/data/kc_house_data.csv'
     return pd.read_csv(url)

data = get_data()




# client = boto3.client('s3',
#         aws_access_key_id =  st.secrets["AWSAccessKeyId"],
#         aws_secret_access_key = st.secrets["AWSSecretKey"]
#         )

X = pd.DataFrame()
banhos = st.sidebar.select_slider(
          'Número de Baños',
          options=list(sorted(set(data['bathrooms']))), value = 1.5)

X.loc[0,'bathrooms'] = banhos
scaler = joblib.load('./parameters/bathrooms.sav')
X[['bathrooms']] = scaler.transform(X[['bathrooms']])

# pisos = st.sidebar.select_slider(
#           'Número de Pisos',
#           options=list(sorted(set(data['floors']))))

# X.loc[0,'floors'] = pisos
# scaler = joblib.load('../parameters/floors.sav')
# X[['floors']] = scaler.transform(X[['floors']])


habitaciones = st.sidebar.select_slider(
          'Número de habitaciones',
          options=list(sorted(set(data['bedrooms']))), value = 2)

# st.sidebar.number_input('Número de habitaciones', min_value=1, max_value=10, value=3, step=1)

X.loc[0,'bedrooms'] = habitaciones
scaler = joblib.load('./parameters/bedrooms.sav')

X[['bedrooms']] = scaler.transform(X[['bedrooms']])

area = st.sidebar.select_slider(
          'Área del inmueble (pies cuadrados)',
          options=list(sorted(set(data['sqft_living']))), value = 1000)

# st.sidebar.number_input('', value = 1000)

X.loc[0,'sqft_living'] = area
scaler = joblib.load('./parameters/sqft_living.sav')
X[['sqft_living']] = scaler.transform(X[['sqft_living']])




vista = st.sidebar.select_slider(
          'Puntaje de la vista',
          options=list(sorted(set(data['view']))), value = 0)

# st.sidebar.select_slider(
#      'Puntaje de la vista',
#      (0,1,2,3,4))

X.loc[0,'view'] = vista
scaler = joblib.load('./parameters/view.sav')
X[['view']] = scaler.transform(X[['view']])



condicion = st.sidebar.select_slider(
         'Condición del inmueble',
          options=list(sorted(set(data['condition']))), value = 3)

# st.sidebar.selectbox(
     
#      (0,1,2,3,4))

X.loc[0,'condition'] = condicion
scaler = joblib.load('./parameters/condition.sav')
X[['condition']] = scaler.transform(X[['condition']])


puntaje = st.sidebar.select_slider(
        'Puntaje de construcción',
          options=list(sorted(set(data['grade']))), value = 8)

# st.sidebar.selectbox(
#      'Puntaje de construcción',
#      (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))


X.loc[0,'grade'] = puntaje
scaler = joblib.load('./parameters/grade.sav')
X[['grade']] = scaler.transform(X[['grade']])

edad = st.sidebar.select_slider(
        'Antigüedad de la propiedad', 
        options=list(range(1,80)), value = 10)
# st.sidebar.number_input('Edad', min_value=1, max_value=100, value=20, step=1)

X.loc[0,'property_age'] = edad
scaler = joblib.load('./parameters/property_age.sav')
X[['property_age']] = scaler.transform(X[['property_age']])

waterfront = st.sidebar.selectbox(
     'La propiedad cuenta con vista al agua?',
     ('Sí', 'No'))

if waterfront == 'Sí': 
    waterfront = 1
else:  
    waterfront = 0

X.loc[0,'waterfront'] = waterfront
scaler = joblib.load('./parameters/waterfront.sav')
X[['waterfront']] = scaler.transform(X[['waterfront']])

renovacion = st.sidebar.selectbox(
     'La propiedad ha sido renovada alguna vez?',
     ('Sí', 'No'))

if renovacion == 'Sí': 
    renovacion = 1
else:  
    renovacion = 0

X.loc[0,'yr_renovated_dummy'] = renovacion
scaler = joblib.load('./parameters/yr_renovated_dummy.sav')
X[['yr_renovated_dummy']] = scaler.transform(X[['yr_renovated_dummy']])




df_coord = data[['zipcode','lat','long']].groupby('zipcode').agg({'lat':'mean','long':'mean'}).reset_index()


cod = st.sidebar.selectbox(
     'Código Postal',
     list(set(df_coord['zipcode'])))


X.loc[0,'lat'] = float(df_coord.loc[df_coord['zipcode']==cod,'lat'])
X.loc[0,'long'] = float(df_coord.loc[df_coord['zipcode']==cod,'long'])
variables = ['bedrooms', 'bathrooms', 'sqft_living', 'waterfront', 'view', 'condition', 'grade', 'yr_renovated_dummy', 'property_age','lat','long']

# for nombre in variables: 
#      with tempfile.TemporaryFile() as fp: 
#           client.download_fileobj(Fileobj = fp, 
#                                    Bucket = 'precioscasas',
#                                    Key = nombre+'.sav'
#           )
#           fp.seek(0)
#           scaler = joblib.load(fp)
#           X[[nombre]] = scaler.transform(X[[nombre]])

# @st.cache
# def transformation(nombre): 
#      with tempfile.TemporaryFile() as fp: 
#                client.download_fileobj(Fileobj = fp, 
#                                         Bucket = 'precioscasas',
#                                         Key = nombre+'.sav'
#                )
#                fp.seek(0)
#                scaler = joblib.load(fp)
#      return scaler

     
# for nombre in variables: 
#      scaler_inner = transformation(nombre)
#      X[[nombre]] = scaler_inner.transform(X[[nombre]])


st.markdown("""
Aquí, un modelo de Machine Learning previamente entrenado recomendará el precio de una propiedad basado en sus propidades. El usuario deberá suministrar las características del inmueble utilizando el menú de la barra izquierda. A continuación se definen la información requerida. :
     
- Número de baños: Número de baños de la propiedad a sugerir precio. Valores como 1.5 baños se refiere a la existencia de un baño con ducha y un baño sin ducha. 
- Número de pisos: Número de pisos de la propiedad a sugerir precio
- Número de habitaciones: Número de habitaciones de la propiedad a sugerir precio
- Área del inmueble: Área en pies cuadrados de la propiedad a sugerir precio
- Vista al agua: La propiedad a sugerir precio tiene vista al agua?
- Puntaje de la vista: Puntaje de la vista de la propiedad a sugerir precio.
- Condición del inmueble: Condición general de la propiedad a sugerir precio.
- Puntaje sobre la construcción: Puntja sobre la construcción de la propiedad a sugerir precio
- Renovación: La propiedad a sugerir precio ha sido renovada?
- Edad de la propiedad: La antiguedad de la propiedad a sugerir precio. 
- Código Postal en el que interesa buscar la propiedad
    """)


if st.sidebar.button('Recomendar precio'):

     # with tempfile.TemporaryFile() as fp: 
     #      client.download_fileobj(Fileobj = fp, 
     #                               Bucket = 'precioscasas',
     #                               Key = 'xbg_final.sav'
     #      )
     #      fp.seek(0)
     modelo_final = joblib.load('./models/xbg_final.sav')
     precio = modelo_final.predict(X)[0]
     # st.balloons()
     st.success('Un valor sugerido ha sido calculado')
#     st.write('El precio sugerido es:', )
     st.metric("Valor sugerido", '$'+str(f'{round(np.expm1(precio)):,}')+ ' usd')
else:
     # st.snow()
     st.error('Por favor, seleccione los parámatros de la propiedad a estimar el precio.')
     

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)