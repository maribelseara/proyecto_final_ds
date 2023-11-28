import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from time import sleep
import random
from datetime import date

#Abrimos los archivos que contienen anteriores datos de scrapeo
#si es la primera vez los creamos
fname="vehiculos_usados.csv"
fdescriptions="descripciones_vehiculos.csv"

if os.path.isfile(fname):
    df=pd.read_csv(fname)
else:
    cols=['Fecha extrac', 'Enlace']
    df=pd.DataFrame(columns=cols)

if os.path.isfile(fdescriptions):
    df_descriptions=pd.read_csv(fdescriptions)
else:
    cols=['Enlace', 'Descripción']
    df_descriptions=pd.DataFrame(columns=cols)

#Abrimos el navegador con la url de la página
url="https://www.autoscout24.es/"
opts = Options()
opts.add_argument('-headless=new')
browser = Firefox(options=opts)
browser.get(url)
sleep(random.randint(1, 4))

#Aceptamos las cookies si es necesario
accept_cookies_button=browser.find_element(By.CLASS_NAME, '_consent-accept_p8dbx_111')
if accept_cookies_button:
    accept_cookies_button.click()
sleep(random.randint(1, 5))

#Click en el enlace de búsqueda, sin indicarle parámetros
# El único filtro automático que coloca es ubicados en España
search_link=browser.find_element(By.ID, "search-mask-search-cta")
search_link.click()
sleep(random.randint(2, 6))

#Iniciamos bucle de scrapeo hasta que llegue a la última página de resultados
#Cada búsqueda en la página proporciona 400 resultados máximo.
while True:
    nuevo=0
    #Se espera a que la página esté cargada esperando a que cargue un elementeo en concreto. Si no carga lanza una excepción
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, "SaveSearchButton_buttonChildren__o_r9y"))
        WebDriverWait(browser, 10).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")
        break
        
    listings=browser.find_elements(By.CLASS_NAME, "ListItem_wrapper__J_a_C")
    for listing in listings:
        try:
            link=listing.find_element(By.TAG_NAME, "a")
            link_address=link.get_attribute("href")
        except:
            browser.back()
            break
        if link_address not in df['Enlace'].values:
            link.click()
            #Se espera a que la página esté cargada eligiendo un elemento por el cual esperar. Si no carga lanza una excepción
            try:
                element_present = EC.presence_of_element_located((By.ID, "lead-form-lightbox-desktop-button"))
                WebDriverWait(browser, 10).until(element_present)
            except TimeoutException:
                print ("Timed out waiting for page to load")
                break
            atributos=browser.find_elements(By.CLASS_NAME, "VehicleOverview_itemText__V1yKT")
            #A veces no está dentro de un anuncio y los atributos petaban
            try:
                dicc_vehic={
                    'Fecha extrac' : date.today(),
                    'Enlace' : link_address,
                    'Marca' : browser.find_element(By.CLASS_NAME, "StageTitle_boldClassifiedInfo__L7JmO").text,
                    'Modelo' : browser.find_element(By.CLASS_NAME, "StageTitle_model__pG_6i").text,
                    'Precio' : browser.find_element(By.CLASS_NAME, "PriceInfo_price__JPzpT").text,
                    'Localización': browser.find_element(By.CLASS_NAME, "LocationWithPin_locationItem__pHhCa").get_attribute("href"),
                    'Potencia' : atributos[4].text,
                    'Tipo vendedor' : atributos[5].text,    
                }
            except:
                continue
            datos_columnas=browser.find_elements(By.CLASS_NAME, "DataGrid_defaultDtStyle__yzRR_")
            datos_valores=browser.find_elements(By.CLASS_NAME, "DataGrid_defaultDdStyle__29SKf")
            for i,columna in enumerate(datos_columnas):
                dicc_vehic[columna.text]=datos_valores[i].text
            df_new=pd.DataFrame(dicc_vehic, index=[0])
            df=pd.concat([df, df_new])
            #Algunos anuncios daban error por no tener descripción, lo gestionamos
            try:
                description=browser.find_element(By.CLASS_NAME, "SellerNotesSection_content__S5suY").text
            except:
                description=""
            df_descriptions=pd.concat([df_descriptions, pd.DataFrame([{'Enlace': link_address, 'Descripción' : description}])])
            nuevo=1
            #Se simula que un humano está leyendo el anuncio con un sleep random entre 5 y 10 segundos
            sleep(random.randint(4, 6))
            # Duda sobre si el siguiente comando falla a veces (porque a veces intenta hacer listings en la ficha de vehículo), cambiar por clic en el enlace "Volver a la lista de vehículos"
            browser.back()
            #back_button=browser.find_element(By.CLASS_NAME, "BackButton_link__UwOji Link_link__pjU1l")
            #back_button.click()
            sleep(random.randint(3, 6))
            #Al volver a la página anterior se han perdido algunas variables, así que se reinicia el bucle
            break
    #Si ha llegado al final de los listings sin añadir ninguno nuevo se cambia de página (para evitar que cambie de pag con el break de almacenar anuncio)
    #Se espera a que cargue el link para hacer click para que no crashee
    if not nuevo: 
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "FilteredListPagination_button__41hHM"))
            WebDriverWait(browser, 10).until(element_present)
            pag_siguiente=browser.find_elements(By.CLASS_NAME, "FilteredListPagination_button__41hHM")[-1]
            if not pag_siguiente.get_attribute("disabled"):
                pag_siguiente.click()
                sleep(random.randint(2, 6))
            else:
                #Hemos llegado a la última página de resultados y rompemos el bucle
                break
        except TimeoutException:
            print ("Timed out waiting for page to load")
            continue
browser.quit()

# En ocasiones crea columnas Unnamed que no nos sirven, las eliminamos
for column in df.columns:
    if "Unnamed" in column:
        df=df.drop([column], axis=1)
for column in df_descriptions.columns:
    if "Unnamed" in column:
        df_descriptions=df_descriptions.drop([column], axis=1)

# Guardamos los datos a los archivos
df.to_csv("vehiculos_usados.csv")
df_descriptions.to_csv("descripciones_vehiculos.csv")