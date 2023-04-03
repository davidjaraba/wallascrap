import logging
import asyncio
import telegram
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot,InlineKeyboardButton, InlineKeyboardMarkup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import sys
import random
import undetected_chromedriver as uc
# OFFERS_URL ='https://es.wallapop.com/app/search?latitude=40.32432432432432&longitude=-3.781357301971911&category_ids=100&min_sale_price=1000&max_sale_price=6000&distance=100000&order_by=newest&country_code=ES&gearbox=manual&min_km=10000&max_km=170000&min_year=2005&favorite_search_id=532e4c05-2929-48bd-a97c-99ca18cd0c64&filters_source=stored_filters'


TOKEN = '6267117945:AAGmojNJIm1EvnRlq7x3r8uYmio-sMKigJI'


## NORMAL CHROME
# Configura las opciones de Chrome
# chrome_options = Options()
# chrome_options.add_argument("--disable-blink-features=AutomationControlled") # deshabilita la automatización de la interfaz de usuario
# driver = webdriver.Chrome(options=chrome_options)
#
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {
#             "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)


# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--window-size=1920,1080')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
# Crea una instancia de webdriver con las opciones de Chrome






## ALTERNATIVE CHROME
# HAY QUE HACER UNA INSTANCIA PARA EVITAR SER DETECTADO COMO ROBOT POR MIL ANUNCIOS, SIN COMENTAR EL CODIGO





# conecto al bot de telegram
bot = telegram.Bot(token=TOKEN)
sleep(1)

async def send_message(txt):
    logging.info(txt)
    with open("wallapop_encontrados.txt", "a") as archivo:
        archivo.write("\n"+txt)

    try:
        txtList = txt.split('#@#@#')

        button = InlineKeyboardButton(text='Ver', url=txtList[3])

        # Crea una lista de botones
        buttons = [[button]]

        # Crea una marca de teclado en línea con la lista de botones
        reply_markup = InlineKeyboardMarkup(buttons)

        text = "<b>{}</b> \nPrecio: {}\n{}\n<a href='{}'>>></a>".format(txtList[0],txtList[1], txtList[2],txtList[5])

        ##MIO
        # await bot.send_message('393154264', text, parse_mode='HTML', reply_markup=reply_markup)

        ##PP
        # await bot.send_message('5875517685', text, parse_mode='HTML', reply_markup=reply_markup)

    except Exception as e:
        logging.error(e)

def validate_wall_cookies():
    try:
        driver.get('https://es.wallapop.com/')
        # Esperar a que aparezca el mensaje de consentimiento
        wait = WebDriverWait(driver, 2)
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ot-sdk-container')))
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ot-sdk-container')))

        # Cerrar el mensaje de consentimiento
        cerrar_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cerrar_btn.click()
    except TimeoutException:
        print('no hay cons')

def validate_coches_cookies():
    try:
        print('coches')
        ## ACCEDER A COCHES.NET SIN SER BLOQUEADO

        uc.TARGET_VERSION = 85
        driver = uc.Chrome()
        driver.get('https://coches.net')

        # Esperar a que aparezca el mensaje de consentimiento
        wait = WebDriverWait(driver, 2)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sui-MoleculeModal-dialog')))
        sleep(1)
        cerrar_btn = element.find_element(By.XPATH, '//button[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center"]')
        cerrar_btn.click()
    except TimeoutException:
        print('no hay cons')

def validate_mila_cookies():
    try:
        print('mila')
        ## ACCEDER A MILANUNCIOS SIN SER BLOQUEADO
        driver.get('https://www.milanuncios.com/')




        # Esperar a que aparezca el mensaje de consentimiento
        # wait = WebDriverWait(driver, 2)
        # # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ot-sdk-container')))
        # element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sui-MoleculeModal-dialog')))
        # sleep(3)
        # # Cerrar el mensaje de consentimiento
        # cerrar_btn = element.find_element(By.CLASS_NAME, 'sui-AtomButton')
        # cerrar_btn.click()
    except TimeoutException:
        print('no hay cons')

async def wallapop_check():


    filters = []
    with open("filters_wallapop.txt", "r") as archivo_fil:
        filters = archivo_fil.readlines()
        filters = [fl.rstrip("\n") for fl in filters]


    for fls in filters:
        driver.get(fls)
        sleep(2)

        # OBTENEMOS LOS COCHES YA ENVIADOS
        lineas = []
        with open("wallapop_encontrados.txt", "r") as archivo:
            lineas = archivo.readlines()
            lineas = [linea.rstrip("\n") for linea in lineas]


        sleep(1)

        cards = driver.find_elements(By.CLASS_NAME, 'ItemCardList__item')
        if (cards is not None):
            logging.info('Coches encontrados: ')
            print('Coches encontrados: ')
            for e in cards:
                try:

                    precio = e.find_element(By.CLASS_NAME, 'ItemCardWide__price').text
                    titulo = e.find_element(By.CLASS_NAME, 'ItemCardWide__title').text
                    property = e.find_element(By.CLASS_NAME, 'ItemExtraInfo').text
                    image = e.find_element(By.TAG_NAME, 'img').get_attribute('src')

                    # Obtener las ventanas del navegador antes de hacer clic en el enlace
                    windows_before = driver.window_handles

                    enlace = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(e))

                    e.click()

                    wait = WebDriverWait(driver, 2)

                    # Esperar a que se cargue la nueva ventana
                    wait.until(EC.number_of_windows_to_be(2))

                    # Obtener las ventanas del navegador después de hacer clic en el enlace
                    windows_after = driver.window_handles

                    new_window = [x for x in windows_after if x not in windows_before][0]
                    driver.switch_to.window(new_window)

                    # Obtener la URL de la nueva ventana
                    enlace = driver.current_url

                    driver.close()

                    # Cambiar el controlador de Selenium a la ventana principal
                    driver.switch_to.window(windows_before[0])


                    # reservada
                    reservada = False

                    try:
                        reservada_element = e.find_element(By.CLASS_NAME, 'reserved')
                        if (reservada_element is not None):
                            reservada = True
                    except NoSuchElementException:
                        reservada = False

                    res = '{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}'.format(titulo,precio, property.replace("\n"," "),
                                                                                                               enlace,
                                                                                                               str(reservada),image)

                    if (res not in lineas):
                        await send_message(res)

                except NoSuchElementException as ex:
                    print(f"Error: no se encontró el elemento. Detalles: {ex}")
                except TimeoutException as ex:
                    print(f"Error: se superó el tiempo de espera. Detalles: {ex}")
                except Exception as ex:
                    print(f"Error inesperado. Detalles: {ex}")

                # except:
                #     pass

async def coches_check():


    filters = []
    with open("filters_coches.txt", "r") as archivo_fil:
        filters = archivo_fil.readlines()
        filters = [fl.rstrip("\n") for fl in filters]


    for fls in filters:
        driver.get(fls)
        sleep(2)

        # OBTENEMOS LOS COCHES YA ENVIADOS
        lineas = []
        with open("coches_encontrados.txt", "r") as archivo:
            lineas = archivo.readlines()
            lineas = [linea.rstrip("\n") for linea in lineas]


        sleep(1)

        cards = driver.find_elements(By.CLASS_NAME, 'sui-AtomCard')
        if (cards is not None):
            logging.info('Coches encontrados: ')
            print('Coches encontrados: ')
            for e in cards:
                try:

                    precio = e.find_element(By.CLASS_NAME, 'mt-TitleBasic-title').text
                    titulo = e.find_element(By.CLASS_NAME, 'mt-CardBasic-title').text
                    property = e.find_element(By.CLASS_NAME, 'mt-CardBasic-title').text
                    image = e.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    enlace = e.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    # reservada
                    reservada = False

                    try:
                        reservada_element = e.find_element(By.CLASS_NAME, 'reserved')
                        if (reservada_element is not None):
                            reservada = True
                    except NoSuchElementException:
                        reservada = False

                    res = '{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}'.format(titulo,precio, property.replace("\n"," "),
                                                                                                               enlace,
                                                                                                               str(reservada),image)

                    if (res not in lineas):
                        await send_message(res)

                except NoSuchElementException as ex:
                    print(f"Error: no se encontró el elemento. Detalles: {ex}")
                except TimeoutException as ex:
                    print(f"Error: se superó el tiempo de espera. Detalles: {ex}")
                except Exception as ex:
                    print(f"Error inesperado. Detalles: {ex}")

                # except:
                #     pass


async def main():
    validate_wall_cookies()
    validate_coches_cookies()
    # validate_mila_cookies()
    while (True):
        # await coches_check()
        # await wallapop_check()
        logging.info('Esperando 3 minutos para volver a buscar...')
        print('Esperando 3 minutos para volver a buscar...')
        sleep(300)
    driver.quit()


if __name__ == '__main__':
    logging.info('Iniciando el bot...')
    print('Iniciando el bot...')
    asyncio.run(main())



# print('- Coche: titulo: {} precio: {} enlace: {} reservada: {}'.format(titulo,precio,enlace.get_attribute('href'),str(reservada)))
                # bot.send_message(chat_id='393154264', text=res)