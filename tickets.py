import requests
from bs4 import BeautifulSoup
import time
import os
from config import *

config = read_config()


class Ticket:
    def __init__(self, id, title, client, is_unread, ticket):
        self.id = id
        self.is_unread = is_unread
        self.title = title
        self.client = client
        self.ticket = ticket


class Message:
    def __init__(self, id, message_user, date_post, message):
        self.id = id
        self.message_user = message_user
        self.date_post = date_post
        self.message = message


# получаем XML от биллинга
# TODO: переделать авторизацию на сессии
def api_get(func, additional_params={}):
    login = config["LOGIN"]
    password = config["PASSWORD"]
    url = config["URL"]

    request_params = {
        'func': func,
        'out': 'xml',
        'authinfo': login + ":" + password
    }

    for key in additional_params:
        request_params[key] = additional_params[key]

    content = requests.get(url + "?", params=request_params, verify=False).content

    return content


# получаем список тикетов, построенных в класс Ticket
def get_tickets():
    response = api_get("ticket", additional_params={})
    soup = BeautifulSoup(response, "xml")
    tickets = soup.find_all("elem")
    list = []
    for ticket in tickets:
        id = ticket.find_all("id")[0].string
        client = ticket.find_all("client")[0].string
        title = ticket.find_all("name")[0].string
        ticket = ticket.find_all("ticket")[0].string

        try:
            unread = ticket.find_all("unread")[0].string
        except:
            unread = "off"

        if unread == "on":
            is_unread = True
        else:
            is_unread = False
        list.append(Ticket(id, title, client, is_unread, ticket))
    return list


def get_ticket_messages(elid):
    response = api_get("ticket_all.message", {"elid": elid})
    soup = BeautifulSoup(response, "xml")
    messages = soup.find_all("elem")
    list = []
    for message in messages:
        id = str(message.find_all("id")[0].string)
        message_user = str(message.find_all("message_user")[0].string)
        date_post = str(message.find_all("date_post")[0].string)
        _message = str(message.find_all("message")[0].string)
        list.append(Message(id, message_user, date_post, _message))
    return list
