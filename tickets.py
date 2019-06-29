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


# получаем XML от биллинга
# TODO: переделать авторизацию на сессии
def api_get(login, password, url, func, additional_params={ }):
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
    response = api_get(config["LOGIN"], config["PASSWORD"], config["URL"], "ticket", additional_params={})
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
