#!/usr/bin/env python3
import time
import urllib3
from tickets import *

urllib3.disable_warnings()

LOG_FILE = str(Path.home()) + "/.tickets.log"


def log(text):
    LOG = open(LOG_FILE, "w")
    text = time.ctime() + ": " + text
    LOG.write(text + "\n")
    LOG.close()


def get_tickets_ids(tickets):
    _tickets = {}
    for ticket in tickets:
        _tickets[int(ticket.ticket)] = ticket
    return _tickets


# получаем id всех активных в данный момент тикетов
old = get_tickets_ids(get_tickets()).keys()

print(old)
diff = []

while True:

    # получаем список всех тикетов
    try:
        tickets = get_tickets()
    except:
        continue

    # вытаскиваем словарь соответствия id: Ticket
    new = get_tickets_ids(tickets)

    # получаем массив ключей (id)
    new_ids = new.keys()

    # получаем список новых тикетов
    diff = set(new_ids) - set(old)
    new_tickets = []

    for i in diff:
        # если тикет новый, но уже был прочитан, не считаем его новым
        if new[i].is_unread:
            new_tickets.append(new[i])

    # тут обрабатываем тикеты
    for d in new_tickets:
        os.system("notify-send \"" + d.title + "\n-----\nТеперь их " + str(len(tickets)) + "\"")
        log(d.title + "(" + d.client + ") " + "- " + str(d.ticket))

    old = new_ids
    time.sleep(TIMEOUT)
    # колесо Сансары дало оборот
