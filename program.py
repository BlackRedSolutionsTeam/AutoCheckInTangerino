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
logging.basicConfig(filename='execution.log', encoding='utf-8', level=logging.INFO)

# Vars
cal = Brazil()
actual_date = datetime.datetime.now()
minutes_variation = random.randint(0, int(config["schedule"]["minutes_variation"]))


def main():
    logging.info('[] Programa AutoCheckInTangerino iniciado []')

    if not is_holiday() and is_work_day:
        execute_program()

    logging.info('[] O programa encerrara em 5 segundos.. []')

    time.sleep(5)
    logging.info('[] Programa encerrado []')


def execute_program():
    if actual_date.hour == int(config["schedule"]["start_office_hour"]):
        logging.info('[] O ponto de INICIO de expediente sera batido daqui a ' + str(minutes_variation) + ' minuto(s). []')
        do_check_in()
    elif actual_date.hour == int(config["schedule"]["end_office_hour"]):
        logging.info('[] O ponto de FIM de expediente sera batido daqui a ' + str(minutes_variation) + ' minuto(s). []')
        do_check_in()
    else:
        logging.info('[] Voce nao esta no horario de bater ponto ainda...[]')


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
    time.sleep(minutes_variation * 60)

    browser = get_browser()
    browser.get(config["tangerino"]["check_in_url"])
    logging.info('[] Entrando no site... []')

    logging.info('[] Procurando elemento com id: codigoEmpregador []')
    input_employer_code = browser.find_element(By.ID, 'codigoEmpregador')
    input_employer_code.send_keys(config["infos"]["employer_code"])
    logging.info('[] Digitei o codigo empregador: ' + config["infos"]["employer_code"] + ' []')

    logging.info('[] Procurando elemento com id: codigoPin []')
    input_employer_code = browser.find_element(By.ID, 'codigoPin')
    input_employer_code.send_keys(config["infos"]["pin"])
    logging.info('[] Digitei o PIN ' + config["infos"]["employer_code"] + ' []')

    logging.info('[] Ponto batido em: ' + str(actual_date) + '. []')
    browser.quit()


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options)
    return browser


if __name__ == '__main__':
    main()
