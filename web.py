import pandas as pd
import streamlit as st
from joblib import load
from datetime import date

df=load('vehiculos.df')
model=load('model.joblib')

st.title('Asesor precios anuncios vehículos segunda mano')
marca = st.selectbox('Marca:', sorted(df.Marca.unique()))
modelo = st.selectbox('Modelo:', sorted(df[df['Marca']==marca].Modelo.unique()))
potencia = st.slider('Potencia', min_value=df['Potencia'].min(), max_value=df['Potencia'].max(), step=5.0)
tipo_vendedor=st.selectbox('Tipo de vendedor', df['Tipo vendedor'].unique())
categoria=st.selectbox('Categoría', sorted(df['Categoría'].unique()))
tipo_vehiculo=st.selectbox('Tipo de vehículo', sorted(df['Tipo de vehículo'].unique()))
puertas=st.number_input('Puertas:', min_value=df['puertas'].min(), max_value=df['puertas'].max(), step=1)
garantia=st.selectbox('Garantía en meses:', sorted(df['Garantía'].unique()))
kilometraje=st.number_input('Kilometraje:', min_value=0.0, max_value=df['Kilometraje'].max(), step=5000.0)
mes=st.number_input('Mes de matriculación:', min_value=1, max_value=12, step=1)
year=st.number_input('Año de matriculación:', min_value=df['Año'].min(), max_value=date.today().year)
tipo_cambio=st.selectbox('Tipo de cambio:', sorted(df['Tipo de cambio'].unique())) 
capacidad=st.slider('Capacidad del motor en cm3:', min_value=50.0, max_value=df['Capacidad'].max(), step=10.0)
consumo=st.number_input('Consumo de combustible en litros/100kilómetros:', min_value=0.0, max_value=df['Consumo de combustible'].max(), step=0.5)
color_ext=st.selectbox('Color exterior:', sorted(df['Color exterior'].unique()))
color_ori=st.selectbox('Color original:', sorted(df['Color original'].unique()))
traccion=st.selectbox('Tracción:', sorted(df['Tracción'].unique()))
plazas=st.number_input('Plazas:', min_value=1, max_value=9)
marchas=st.slider('Cantidad de marchas:', min_value=df['Número de marchas'].min(), max_value=df['Número de marchas'].max(), step=1.0)
cilindros=st.slider('Número de cilindros:', min_value=df['Número de cilindros'].min(), max_value=df['Número de cilindros'].max(), step=1.0)
peso=st.slider('Peso:', min_value=df['Peso'].min(), max_value=df['Peso'].max())
tipo_combustible=st.selectbox('Tipo de combustible:', sorted(df['Tipo de combustible'].unique()))
ciudad=st.text_input('Ciudad:')
cp=st.number_input('Código Postal:', min_value=1, max_value=99999, step=1)
#Lo ideal sería coger las provincias del dataset del archivo postalcat.csv en la carpeta data/raw/ esto es solo para una versión rápida de prueba
provincia=st.selectbox('Provincia:', sorted(df['provincia'].unique()))

if st.button('¿A qué precio lo anuncio?'):
    # Creamos un DataFrame con los datos ingresados por el usuario
    input_data = pd.DataFrame([[marca, modelo, potencia, tipo_vendedor, categoria, tipo_vehiculo, puertas, 'España', garantia, kilometraje, year, tipo_cambio, capacidad, consumo, color_ext, color_ori,
                                traccion, plazas, marchas, cilindros, peso, tipo_combustible, mes, ciudad, cp, provincia]],
                               columns=df.columns)

    predict = model.predict(input_data)[0]
    st.text=f"Te recomendamos anunciarlo a {predict} euros"
