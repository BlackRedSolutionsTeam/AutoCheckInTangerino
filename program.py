from selenium import webdriver
from selenium.webdriver.common.by import By
from workalendar.america import Brazil
import configparser
import datetime
import time
import random
import logging

# Config's Files
config = configparser.ConfigParser()
config.read("./configfile.ini")  # Example config: "hour = config["schedule"]"
logging.basicConfig(format='%(asctime)s %(message)s', filename='execution.log', encoding='utf-8', level=logging.INFO)

# Vars
cal = Brazil()
actual_date = datetime.datetime.now()
minutes_variation = random.randint(0, int(config["schedule"]["minutes_variation"]))


def main():
    logging.info('[] Programa AutoCheckInTangerino iniciado []')

    if not is_holiday() and is_work_day():
        do_check_in()

    logging.info('[] O programa encerrara em 5 segundos.. []')

    time.sleep(5)
    logging.info('[] Programa encerrado []')


def is_work_day():
    work_day = cal.is_working_day(actual_date)

    if not work_day:
        logging.info('[] Como hoje nao eh um dia que voce trabalha, nao iremos bater o ponto.. []')

    return work_day


def is_holiday():
    holiday = cal.is_holiday(actual_date)

    if holiday:
        logging.info('[] Como hoje eh feriado, nao iremos bater o ponto.. []')

    return holiday


def do_check_in():
    logging.info('[] O ponto sera batido em ' + str(minutes_variation) + ' minuto(s). []')

    time.sleep(minutes_variation * 60)

    browser = get_browser()
    browser.get(config["tangerino"]["check_in_url"])
    logging.info('[] Entrando no site... []')

    logging.info('[] Procurando input com id: codigoEmpregador []')
    input_employer_code = browser.find_element(By.ID, 'codigoEmpregador')

    input_employer_code.send_keys(config["infos"]["employer_code"])
    logging.info('[] Digitei o codigo empregador: ' + config["infos"]["employer_code"] + ' []')

    logging.info('[] Procurando input com id: codigoPin []')
    input_codigo_pin = browser.find_element(By.ID, 'codigoPin')

    input_codigo_pin.send_keys(config["infos"]["pin"])
    logging.info('[] Digitei o PIN ' + config["infos"]["pin"] + ' []')

    logging.info('[] Procurando button com id: registraPonto []')
    btn_check_in = browser.find_element(By.ID, 'registraPonto')

    btn_check_in.click()
    logging.info('[] Cliquei no button []')

    time.sleep(3)

    logging.info('[] Ponto batido! []')
    browser.quit()


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 1,
    })
    browser = webdriver.Chrome(options)
    return browser


if __name__ == '__main__':
    main()