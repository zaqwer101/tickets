#!/usr/bin/env python3

from tickets import *


def get_tickets_ids(tickets):
    ids = {}
    for ticket in tickets:
        ids[int(ticket.id)] = ticket
    return ids


# получаем id всех активных в данный момент тикетов
old = get_tickets_ids(get_tickets()).keys()

print(old)
diff = []

while True:
    notify2.init("Тикет")

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
        notify2.Notification(d.client, message=(d.title + "\nТеперь их " + len(tickets))).show()

    old = new_ids
    time.sleep(TIMEOUT)
    # колесо Сансары дало оборот
