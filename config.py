import re
from pathlib import Path
import os

CONF_DIR = str(Path.home()) + "/.config/tickets/"
CONF_NAME = "tickets"


def oops(e):
    print("Oops!\n" + str(e))


def bye():
    print("Bye!")


def create_empty_config():
    try:
        try:
            os.remove(CONF_DIR + CONF_NAME)  # удаляем прошлый, ибо он какой-то не такой
        except FileNotFoundError:
            None  # Окей, файла и не было
        file = open(CONF_DIR + CONF_NAME, 'w')
        file.write \
                (
                """
        # Before we start:
            LOGIN   = ;
            PASS    = ;
            URL     = ;
            TIMEOUT = ;
""")
        print("Config file not found, i\'we generated new one for you (" + CONF_DIR + CONF_NAME + ")\
        \nYou must set up variables in this config to continue!")
    except Exception as e:
        oops(e)


def create_empty_dir():
    os.makedirs(CONF_DIR)
    print("Config directory not found, i\'we created new one for you (" + CONF_DIR + ")")


def parse_config(config): # крутой алгоритм, над которым я работал несколько дней (я не очень умный)
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
    return conf

# пытаемся создать новую директорию и новый файл конфига
try:
    create_empty_dir()
    create_empty_config()
    bye()
except FileExistsError:  # значит директория уже есть
    try:
        file = open(CONF_DIR + CONF_NAME, 'r')
        content = file.readlines()
        print(parse_config(content))
    except FileNotFoundError:  # значит нет файла конфига
        create_empty_config()
        bye()
