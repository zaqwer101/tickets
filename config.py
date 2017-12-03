import re
from pathlib import Path
import os
from os.path import exists


# дефайним Изначальные Директивы
LOGIN = ""
PASSWORD = ""
URL = "https://my.ispsystem.com/billmgr?"
TIMEOUT = 10

def fine():
    pass

class ConfigIsNotGood(Exception):
    pass


CONF_DIR = str(Path.home()) + "/.config/tickets/"
CONF_NAME = "tickets"


def oops(e):
    print("Oops!\n" + str(e))


def bye():
    print("Bye!")


def create_config():
    if exists(CONF_DIR):
        fine()
        if exists(CONF_DIR + CONF_NAME):
            os.remove(CONF_DIR + CONF_NAME)
            print("Предыдущий конфиг удален")
    else:
        create_dir()

    file = open(CONF_DIR + CONF_NAME, 'w')
    print("Создал дефолтный конфиг в " + CONF_DIR + CONF_NAME + ', но дальше вы не пройдете, пока не заполните бумаги:\n')
    url = input("URL биллинга? (По умолчанию - ISPsystem)\n")
    login = input("Логин в биллинге?\n")
    password = input("Пароль от аккаунта?\n")
    q = input("Дефолтный таймаут опроса биллинга - 10 секунд. Пойдёт? (y/n) ")
    if q == 'y':
        print("Отлично, да будет так.")
    elif q == 'n':
        print("Ну тогда сам руками поменяешь в конфиге.")
    else:
        print("Ты бы ещё консервных банок насобирал! Будет по умолчанию значит.")

    if url != '':
        URL = url
    if login != '':
        LOGIN = login
    if password!= '':
        PASSWORD = password

    file.write("URL = " + URL + ";\n")
    file.write("LOGIN = " + LOGIN + ";\n")
    file.write("PASSWORD = " + PASSWORD + ";\n")
    file.write("TIMEOUT = " + TIMEOUT + ";\n")


def create_dir():
    os.makedirs(CONF_DIR)



def read_config(config):  # крутой алгоритм, над которым я работал несколько дней (я не очень умный)
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

    return conf

if exists(CONF_DIR):
    if exists(CONF_DIR + CONF_NAME):
        conf = read_config(open(CONF_DIR + CONF_NAME, 'r').readlines())
    else:
        oops("Конфига не существует")
        create_config()
        print("Создан дефолтный конфиг")
        bye()
else:
    oops("Директории не существует")
    create_dir()
    print("Создана директория\nСоздан дефолтный конфиг")
    bye()