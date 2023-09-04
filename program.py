from selenium import webdriver
from selenium.webdriver.common.by import By
from workalendar.america import Brazil
import configparser
import datetime
import time
import random
import winsound

# Sound Config
frequency = 2500
duration = 1000

# Config File
config = configparser.ConfigParser()
config.read("./configfile.ini")  # Example config: "hour = config["schedule"]"

# Vars
cal = Brazil()
actual_date = datetime.datetime.now()
minutes_variation = random.randint(0, int(config["schedule"]["minutes_variation"]))


def main():
    print('[] Programa Auto Bater Ponto iniciado []')

    if not is_holiday() and is_work_day:
        execute_program()

    print('[] O programa encerrara em 5 segundos.. []')

    time.sleep(5)
    print('[] Programa encerrado []')


def execute_program():
    if actual_date.hour == int(config["schedule"]["start_office_hour"]):
        print('[] O ponto de INICIO de expediente sera batido daqui a', minutes_variation, 'minuto(s). []')
        do_check_in()
    elif actual_date.hour == int(config["schedule"]["end_office_hour"]):
        print('[] O ponto de FIM de expediente sera batido daqui a', minutes_variation, 'minuto(s). []')
        do_check_in()
    else:
        print('[] Voce nao esta no horario de bater ponto ainda...[]')


def is_work_day():
    work_day = cal.is_working_day(actual_date)

    if not work_day:
        print('[] Como hoje eh um dia que você trabalha, não iremos bater o ponto.. []')

    return work_day


def is_holiday():
    holiday = cal.is_holiday(actual_date)

    if holiday:
        print('[] Como hoje eh feriado, nao iremos bater o ponto.. []')

    return holiday


def do_check_in():
    time.sleep(minutes_variation)

    browser = get_browser()
    browser.get(config["tangerino"]["check_in_url"])

    input_employer_code = browser.find_element(By.ID, 'codigoEmpregador')
    input_employer_code.send_keys(config["infos"]["employer_code"])

    input_employer_code = browser.find_element(By.ID, 'codigoPin')
    input_employer_code.send_keys(config["infos"]["pin"])

    btn_check_in = browser.find_element(By.ID, 'registraPonto')
    btn_check_in.click()

    winsound.Beep(frequency, duration)
    print('[] Ponto batido em: ', actual_date, '. []')
    browser.quit()


def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options)
    return browser


if __name__ == '__main__':
    main()
