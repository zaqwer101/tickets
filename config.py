import re
from pathlib import Path
import os
from os.path import exists

# дефайним Изначальные Директивы
import time

LOGIN = ""
PASSWORD = ""
URL = "https://my.ispsystem.com/billmgr?"
TIMEOUT = 10
CONF_DIR = str(Path.home()) + "/.config/tickets/"
CONF_NAME = "tickets"
LOG_FILE = str(Path.home()) + "/.tickets_config.log"


def log(text):
    LOG = open(LOG_FILE, "w")
    text = time.ctime() + ": " + text
    LOG.write(text + "\n")
    LOG.close()
    print(text)


def oops(e):
    log("Oops!\n" + str(e))


def check_config():
    if exists(CONF_DIR):
        if exists(CONF_DIR + CONF_NAME):
            log("Конфиг найден")
            return True
        else:
            log("Конфиг не найден")
            return False
    else:
        log("Директория конфига не найдена")
        return False


def bye():
    log("Bye!")


def create_config(_LOGIN=LOGIN, _PASSWORD=PASSWORD, _URL=URL, _TIMEOUT='10'):
    if exists(CONF_DIR):
        if exists(CONF_DIR + CONF_NAME):
            os.remove(CONF_DIR + CONF_NAME)
            log("Предыдущий конфиг удален")
    else:
        os.mkdir(CONF_DIR)

    file = open(CONF_DIR + CONF_NAME, 'w')
    print(
        "Создал дефолтный конфиг в " + CONF_DIR + CONF_NAME + ', необходимо заполнить параметры:\n')
    url = input("URL биллинга? (По умолчанию - ISPsystem)\n")
    login = input("Логин в биллинге?\n")
    password = input("Пароль от аккаунта?\n")
    q = input("Дефолтный таймаут опроса биллинга - 10 секунд. Пойдёт? (y/n) ")
    if q == 'y':
        print("Да будет так.")
    elif q == 'n':
        print("Необходимо изменение конфига вручную\n")
    else:
        print("Будет по умолчанию.\n")

    if url != '':
        _URL = url
    if login != '':
        _LOGIN = login
    if password != '':
        _PASSWORD = password

    file.write("URL = " + _URL + ";\n")
    file.write("LOGIN = " + _LOGIN + ";\n")
    file.write("PASSWORD = " + _PASSWORD + ";\n")
    file.write("TIMEOUT = " + _TIMEOUT + ";\n")

    print("\nДа будет так.")


# TODO: Валидатор вводимых значений
def read_config():
    try:
        file = open(CONF_DIR + CONF_NAME, 'r')
    except:
        create_config()
        file = open(CONF_DIR + CONF_NAME, 'r')
    config = file.readlines()
    status = check_config()
    if status:
        log("Читаем конфиг...")
    else:
        log("Конфиг содержит ошибки, пересоздаём")
        create_config()
    conf = {}
    for line in config:
        a = line.split('#')
        if len(a) == 1:
            data = line
        elif len(a) > 1 and a[0] == '':
            data = ''
        elif len(a) > 1 and a[0] != '':
            data = a[0]

        if data != '':
            data = re.sub('[\s+]', '', data)
            for a in data.split(';'):
                if a != '':
                    var = a.split('=')[0]
                    val = a.split('=')[1]
                    conf[var] = val

    # теперь нужно проверить, всё ли в конфиге хорошо
    try:
        conf['TIMEOUT'] = int(conf['TIMEOUT'])
    except Exception as e:
        log("Ошибка при попытке конвертации типа директивы TIMEOUT")
        conf['TIMEOUT'] = TIMEOUT
    log("Конфиг в порядке")
    return conf
