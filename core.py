#!/usr/bin/env python3
import time
import urllib3
from tickets import *
from threading import Thread

urllib3.disable_warnings()

LOG_FILE = str(Path.home()) + "/.tickets.log"


def log(text):
    print(text)
    log_file = open(LOG_FILE, "w")
    text = time.ctime() + ": " + text
    log_file.write(text + "\n")
    log_file.close()


def notify_send(message):
    os.system("notify-send \"" + message + "\"")
    log(message)

def main_loop():
    # # получаем id всех активных в данный момент тикетов
    # old = get_tickets_ids(get_tickets()).keys()
    # print(old)
    # diff = []
    # while True:
    #     # получаем список всех тикетов
    #     try:
    #         tickets = get_tickets()
    #     except:
    #         continue
    #
    #     # вытаскиваем словарь соответствия id: Ticket
    #     new = get_tickets_ids(tickets)
    #
    #     # получаем массив ключей (id)
    #     new_ids = new.keys()
    #
    #     # получаем список новых тикетов
    #     diff = set(new_ids) - set(old)
    #     new_tickets = []
    #
    #     for i in diff:
    #         new_tickets.append(new[i])
    #
    #     # тут обрабатываем тикеты
    #     for d in new_tickets:
    #         os.system("notify-send \"" + d.title + "\n-----\nТеперь их " + str(len(tickets)) + "\"")
    #         log(d.title + "(" + d.client + ") " + "- " + str(d.ticket))
    #
    #     old = new_ids
    #     time.sleep(TIMEOUT)
    #     # колесо Сансары дало оборот

    while True:
        old_tickets = get_tickets()
        old_ids = get_tickets_ids(old_tickets)
        time.sleep(5)
        new_tickets = get_tickets()
        new_ids = get_tickets_ids(new_tickets)

        for new_ticket_id in get_tickets_ids(new_tickets):
            if old_ids.__contains__(new_ticket_id):  # если тикет не новый
                ticket = find_ticket_by_ticket(new_tickets, new_ticket_id)
                if ticket.is_unread and not find_ticket_by_ticket(old_tickets,
                                                                  new_ticket_id).is_unread:  # если старый тикет был прочитан, а новый - нет, то в него было добавлено сообщение от клиента
                    notify = "New message in ticket " + str(ticket.title)
                    notify_send(notify)
            else:
                messages = get_ticket_messages(new_ticket_id)
                if messages[-1].first_message:
                    notify = "New ticket: \"" + find_ticket_by_ticket(new_tickets, new_ticket_id).title + "\""
                    notify_send(notify)
                else:
                    notify = "Ticket returned: \"" + find_ticket_by_ticket(new_tickets, new_ticket_id).title + "\""
                    notify_send(notify)


thread = Thread(target=main_loop, daemon=True)


def start():
    thread.start()


def stop():
    thread.stop()
