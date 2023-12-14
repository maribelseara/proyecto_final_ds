# Análisis y predicción del precio de vehículos segunda mano

## Introducción

El mercado de vehículos de segunda mano siempre ha estado activo en España pero la demanda se ha visto aumentada notablemente tras la pandemia del COVID19 con la escasez de materiales para fabricar coches nuevos. Clientes que tradicionalmente compraban vehículos nuevos se han desplazado al mercado de segunda mano. En consecuencia cabe esperar que los precios hayan aumentado en relación a antes de la pandemia y por el aumento de demanda. Aunque este aumento puede haberse suavizado por el restablecimiento de la fabricación de vehículos nuevos, la reciente crisis tras la invasión de Ucrania ha conllevado un aumento general de los precios, así que se espera encontrar dicho aumento de precio en los anuncios actuales.

## Los datos

El dataset principal es el resultado de un scrapeado de unos 15000 registros realizado por mí en la web Autoscout24 la segunda mitad de noviembre de 2023. Este proceso requirió varias semanas ya que cada búsqueda solo devolvía un máximo de 400 resultados y algunos de ellos no se incorporaban por haberse obtenido en búsquedas anteriores. Podéis encontrar el dataset en 'data\raw\vehiculos_usados.csv'

Para poder realizar análisis comparativo se han utilizado otros dos datasets obtenidos de Kaggle ambos provenientes de scrapeos de la web Autoscout24:
-Dataset con más de 100.000 registros de 2018 en España. Disponible en https://www.kaggle.com/datasets/harturo123/online-adds-of-used-cars/

-Dataset con más de 250.000 registros de 2023 en Alemania. Disponible en https://www.kaggle.com/datasets/wspirat/germany-used-cars-dataset-2023

Para la asignación de las provincias se usó el dataset postalcat.csv disponible en https://postal.cat/

## La limpieza

La limpieza de los datos se ha realizado en el archivo 'cleaning.ipynb', sobretodo temas de formato y NaN, así como creación de nuevas columnas.

## El análisis

Al empezar el análisis se percibió que había que realizar más limpieza de datos, en este caso por valores incoherentes (Ejemplo: Un vehículo pesa 1kg). Esta parte de la limpieza se encuentra junto al análisis en el archivo 'EDA.ipynb'

Se empezó por análisis del dataset principal con los datos de scrapeo de España en 2023 y se seguió con comparación con los datos de España 2018 y Alemania 2023. Todo el análisis junto con los gráficos se puede encontrar en el archivo 'EDA.ipynb'. Parte de los gráficos también están disponibles en png en la carpeta 'graphs'

## Machine Learning

Toda la parte de Machine Learning se puede encontrar en el archivo 'ML.ipynb'. Se han utilizado Pipelines durante todo el proceso, empezando por una de preprocesado dividido por tipo de columnas, posteriormente pca ya que tras el OneHotEncoder de marcas y modelos había más de 2900 columnas y finalmente prueba de varios modelos con parámetros por defecto inicialmente y tuneando hiperparámetros finalmente. La mayoría de las pruebas no dieron muy buenos resultados de puntuación R2, pero finalmente RandomForestRegressor obtuvo 0.898.

A continuación usando la librería joblib se guarda la pipeline con mejor resultado para usarla en el archivo 'web.py'

## La web

Gracias a la librería streamlit se ha creado un formulario web donde poder insertar los datos para generar predicciones. Esto se hace importando los datos y la pipeline con el mejor modelo y creando el formulario con un botón que genera la predicción. Este sistema funciona en local, ejecutando el comando 'streamlit run web.py' desde la terminal en la cual uséis python (en mi caso Anaconda Prompt) y estando en la carpeta del proyecto.

Nota: El archivo 'model.joblib' no está subido a Github porque supera los límites de almacenamiento. Se puede crear ejecutando el archivo 'ML.ipynb' (lo cual tarda unos 90 minutos dependiendo del equipo) o descargar del siguiente enlace e incorporarlo al proyecto https://drive.google.com/file/d/1iJqrspU6wCiwISxegolKoqiVqTcTi8la/view?usp=sharing

## Librerías de python necesarias

Se pueden encontrar en el archivo 'requeriments.txt'
Para instalarlas se puede crear un nuevo entorno con 'conda create nombre_entorno', activarlo con 'conda activate nombre_entorno' e instalar las librerías con 'python -m pip install -r requirements.txt'