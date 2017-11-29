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


# пытаемся создать новую директорию и новый файл конфига
try:
    create_empty_dir()
    create_empty_config()
    bye()
except FileExistsError:  # значит директория уже есть
    try:
        file = open(CONF_DIR + CONF_NAME, 'r')
        content = file.readlines()
        print(content)
    except FileNotFoundError:  # значит нет файла конфига
        create_empty_config()
        bye()
