import asyncio
import os
import threading
import telegram
import logging
import tracemalloc
from telegram.ext import Updater, CommandHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

## RECOLECTOR DE BASURA
tracemalloc.start()

# OFFERS_URL ='https://es.wallapop.com/app/search?latitude=40.32432432432432&longitude=-3.781357301971911&category_ids=100&min_sale_price=1000&max_sale_price=6000&distance=100000&order_by=newest&country_code=ES&gearbox=manual&min_km=10000&max_km=170000&min_year=2005&favorite_search_id=532e4c05-2929-48bd-a97c-99ca18cd0c64&filters_source=stored_filters'


TOKEN = '6267117945:AAGmojNJIm1EvnRlq7x3r8uYmio-sMKigJI'

# Configura las opciones de Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

# Crea una instancia de webdriver con las opciones de Chrome
driver = webdriver.Chrome(options=chrome_options)

## ALTERNATIVO
uc.TARGET_VERSION = 85
driver_atl_options = uc.ChromeOptions()
driver_atl_options.add_argument('--headless')
driver_atl_options.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

driver_alt = uc.Chrome(options=driver_atl_options)

# conecto al bot de telegram
bot = telegram.Bot(token=TOKEN)
updater = Updater("6267117945:AAGmojNJIm1EvnRlq7x3r8uYmio-sMKigJI", use_context=True)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! ¡Bienvenido al CARS SCRAP BOT!")


def check(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="FUNCIONANDO :D")


def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="PARANDO EL BOT")
    os._exit(0)


sleep(1)


async def send_message(txt, platform):
    debug_log_info(txt)
    with open(platform + "_encontrados.txt", "a") as archivo:
        archivo.write("\n" + txt)
    try:
        txtList = txt.split('#@#@#')

        button = InlineKeyboardButton(text='Ver', url=txtList[3])

        # Crea una lista de botones
        buttons = [[button]]

        # Crea una marca de teclado en línea con la lista de botones
        reply_markup = InlineKeyboardMarkup(buttons)

        platformStr = ''
        if (platform == 'coches'):
            platformStr = 'COCHES.NET'
        elif (platform == 'wallapop'):
            platformStr = 'WALLAPOP'
        elif (platform == 'mila'):
            platformStr = 'MILANUNCIOS'

        text = "<em>{}</em>\n<strong>{}</strong> \n<b>Precio: {}</b>\n{}\n<a href='{}'>_</a>".format(platformStr,
                                                                                                     txtList[0],
                                                                                                     txtList[1],
                                                                                                     txtList[2],
                                                                                                     txtList[5])

        ##MIO
        bot.send_message('393154264', text, parse_mode='HTML', reply_markup=reply_markup)

        ##PP
        bot.send_message('5875517685', text, parse_mode='HTML', reply_markup=reply_markup)

    except Exception as e:
        debug_log_info(e)


def validate_wall_cookies():
    try:
        try:
            driver.get('https://es.wallapop.com/')
        except ConnectionRefusedError:
            debug_log_info("Se ha rechazado la conexion a la URL especificada")
        except ConnectionError:
            debug_log_info("No se puede conectar a la URL especificada")
        except Exception as e:
            debug_log_info(f"Se ha producido una excepción: {e}")

        # Esperar a que aparezca el mensaje de consentimiento
        wait = WebDriverWait(driver, 2)
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ot-sdk-container')))
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ot-sdk-container')))

        # Cerrar el mensaje de consentimiento
        cerrar_btn = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cerrar_btn.click()
    except TimeoutException:
        debug_log_info('no hay cons')


def validate_coches_cookies():
    try:
        ## ACCEDER A COCHES.NET SIN SER BLOQUEADO
        try:
            driver_alt.get('https://coches.net')
        except ConnectionRefusedError:
            debug_log_info("Se ha rechazado la conexion a la URL especificada")
        except ConnectionError:
            debug_log_info("No se puede conectar a la URL especificada")
        except Exception as e:
            print(f"Se ha producido una excepción: {e}")

        # Esperar a que aparezca el mensaje de consentimiento
        wait = WebDriverWait(driver_alt, 2)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sui-MoleculeModal-dialog')))
        sleep(1)
        cerrar_btn = element.find_element(By.XPATH,
                                          '//button[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center"]')
        cerrar_btn.click()
        sleep(2)
    except TimeoutException:
        debug_log_info('no hay cons')


async def wallapop_check():
    filters = []
    with open("filters_wallapop.txt", "r") as archivo_fil:
        filters = archivo_fil.readlines()
        filters = [fl.rstrip("\n") for fl in filters]

    for fls in filters:
        try:
            driver.get(fls)
        except ConnectionRefusedError:
            debug_log_info("Se ha rechazado la conexion a la URL especificada")
        except ConnectionError:
            debug_log_info("No se puede conectar a la URL especificada")
        except Exception as e:
            debug_log_info(f"Se ha producido una excepción: {e}")

        sleep(2)

        # OBTENEMOS LOS COCHES YA ENVIADOS
        lineas = []
        with open("wallapop_encontrados.txt", "r") as archivo:
            lineas = archivo.readlines()
            lineas = [linea.rstrip("\n") for linea in lineas]

        sleep(1)

        actions = ActionChains(driver_alt)
        actions.send_keys(Keys.PAGE_DOWN).perform()

        sleep(1)

        cards = driver.find_elements(By.CLASS_NAME, 'ItemCardList__item')
        if (cards is not None):
            debug_log_info('WALLAPOP | Encontrados: ')
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

                    res = '{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}'.format(titulo, precio, property.replace("\n", " "),
                                                                         enlace,
                                                                         str(reservada), image)

                    if (res not in lineas):
                        await send_message(res, 'wallapop')

                except NoSuchElementException as ex:
                    debug_log_info(f"Error: no se encontró el elemento. Detalles: {ex}")
                except TimeoutException as ex:
                    debug_log_info(f"Error: se superó el tiempo de espera. Detalles: {ex}")
                except Exception as ex:
                    debug_log_info(f"Error inesperado. Detalles: {ex}")

                # except:
                #     pass


async def coches_check():
    filters = []
    with open("filters_coches.txt", "r") as archivo_fil:
        filters = archivo_fil.readlines()
        filters = [fl.rstrip("\n") for fl in filters]

    for fls in filters:
        try:
            driver_alt.get(fls)
        except ConnectionRefusedError:
            debug_log_info("Se ha rechazado la conexion a la URL especificada")
        except ConnectionError:
            debug_log_info("No se puede conectar a la URL especificada")
        except Exception as e:
            print(f"Se ha producido una excepción: {e}")

        # OBTENEMOS LOS COCHES YA ENVIADOS
        lineas = []
        with open("coches_encontrados.txt", "r") as archivo:
            lineas = archivo.readlines()
            lineas = [linea.rstrip("\n") for linea in lineas]

        for i in range(20):
            sleep(0.2)
            driver_alt.execute_script("window.scrollBy(0, 600)")

        sleep(3)

        cards = driver_alt.find_elements(By.CLASS_NAME, 'sui-AtomCard')
        if (cards is not None):
            debug_log_info('CochesNET | encontrados: ')
            for e in cards:
                try:

                    precio = e.find_element(By.CLASS_NAME, 'mt-TitleBasic-title').text
                    titulo = e.find_element(By.CLASS_NAME, 'mt-CardBasic-title').text
                    property = e.find_element(By.CLASS_NAME, 'mt-CardAd-attr').text
                    image = e.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    enlace = e.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    # reservada
                    reservada = False

                    # try:
                    #     reservada_element = e.find_element(By.CLASS_NAME, 'reserved')
                    #     if (reservada_element is not None):
                    #         reservada = True
                    # except NoSuchElementException:
                    #     reservada = False

                    res = '{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}'.format(titulo, precio, property.replace("\n", " "),
                                                                         enlace,
                                                                         str(reservada), image)

                    if (res not in lineas):
                        await send_message(res, 'coches')

                except NoSuchElementException as ex:
                    pass
                    # print(f"Error: no se encontró el elemento. Detalles: {ex}")
                except TimeoutException as ex:
                    debug_log_info(f"Error: se superó el tiempo de espera. Detalles: {ex}")
                except Exception as ex:
                    debug_log_info(f"Error inesperado. Detalles: {ex}")
                except:
                    pass



async def mila_check():
    filters = []
    with open("filters_mila.txt", "r") as archivo_fil:
        filters = archivo_fil.readlines()
        filters = [fl.rstrip("\n") for fl in filters]

    for fls in filters:

        if (driver_alt.current_url == fls):
            driver_alt.quit()

        sleep(1)

        try:
            driver_alt.get(fls)
        except ConnectionRefusedError:
            debug_log_info("Se ha rechazado la conexion a la URL especificada")
        except ConnectionError:
            debug_log_info("No se puede conectar a la URL especificada")
        except Exception as e:
            debug_log_info(f"Se ha producido una excepción: {e}")

        sleep(1)

        try:
            wait = WebDriverWait(driver_alt, 2)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sui-MoleculeModal-dialog')))
            sleep(1)
            cerrar_btn = element.find_element(By.XPATH,
                                              '//button[@class="sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center "]')
            cerrar_btn.click()
            sleep(2)
        except:
            pass

        # submitBtn = driver_alt.find_element(By.CLASS_NAME, 'sui-AtomButton')
        # submitBtn.click()

        # OBTENEMOS LOS COCHES YA ENVIADOS
        lineas = []
        with open("mila_encontrados.txt", "r") as archivo:
            lineas = archivo.readlines()
            lineas = [linea.rstrip("\n") for linea in lineas]

        for i in range(20):
            sleep(0.2)
            driver_alt.execute_script("window.scrollBy(0, 600)")

        sleep(3)

        cards = driver_alt.find_elements(By.CLASS_NAME, 'ma-AdCardV2')
        if (cards is not None):
            debug_log_info('MILANUNCIOS | encontrados: ')
            for e in cards:
                try:
                    precio = e.find_element(By.CLASS_NAME, 'ma-AdPrice-value').text
                    titulo = e.find_element(By.CLASS_NAME, 'ma-AdCardV2-row').text
                    property = e.find_element(By.XPATH,
                                              './/div[@class="ma-AdCardV2-row ma-AdCardV2-row--margin12 ma-AdCardV2-row--wrap"]').text
                    # property = e.find_elements(By.CSS_SELECTOR, '.ma-AdCardV2-row.ma-AdCardV2-row--margin12.ma-AdCardV2-row--wrap').text
                    image = e.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    enlace = e.find_element(By.CLASS_NAME, 'ma-AdCardListingV2-TitleLink').get_attribute('href')

                    location = e.find_element(By.XPATH,
                                              './/span[@class="ma-SharedText ma-AdLocation-text ma-AdLocation-text--isCardListingLocation ma-SharedText--s ma-SharedText--gray"]').text

                    if ('(Madrid)' not in location):
                        break

                    # reservada
                    reservada = False

                    # try:
                    #     reservada_element = e.find_element(By.CLASS_NAME, 'reserved')
                    #     if (reservada_element is not None):
                    #         reservada = True
                    # except NoSuchElementException:
                    #     reservada = False

                    res = '{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}#@#@#{}'.format(titulo, precio, property.replace("\n", " "),
                                                                         enlace,
                                                                         str(reservada), image)

                    if (res not in lineas):
                        await send_message(res, 'mila')

                except NoSuchElementException as ex:
                    # pass
                    debug_log_info(f"Error: no se encontró el elemento. Detalles: {ex}")
                except TimeoutException as ex:
                    debug_log_info(f"Error: se superó el tiempo de espera. Detalles: {ex}")
                except Exception as ex:
                    debug_log_info(f"Error inesperado. Detalles: {ex}")
                # except:
                #     pass


def start_bot_async():
    updater.start_polling()
    updater.idle()


def start_bot():
    start_handler = CommandHandler('start', start)
    check_handler = CommandHandler('check', check)
    stop_handler = CommandHandler('stop', stop)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(check_handler)
    updater.dispatcher.add_handler(stop_handler)


async def search_cars():
    debug_log_info('Buscando coches...')
    # validate_wall_cookies()
    validate_coches_cookies()
    while (True):
        # await wallapop_check()
        await coches_check()
        await mila_check()
        debug_log_info('Esperando 6 minutos para volver a buscar...')
        sleep(360)


def run_async_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(search_cars())


def debug_log_info(txt):
    # print(txt)
    logging.info(txt)


if __name__ == '__main__':
    debug_log_info('Iniciando el bot...')
    # start_bot()
    t = threading.Thread(target=run_async_in_thread)
    t.start()
    # start_bot_async()

# print('- Coche: titulo: {} precio: {} enlace: {} reservada: {}'.format(titulo,precio,enlace.get_attribute('href'),str(reservada)))
# bot.send_message(chat_id='393154264', text=res)