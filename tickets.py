import requests
from bs4 import BeautifulSoup

from config import *


class Ticket:
    def __init__(self, id, title, client, is_unread):
        self.id = id
        self.is_unread = is_unread
        self.title = title
        self.client = client


# получаем XML от биллинга
# TODO: переделать авторизацию на сессии
def get_response():
    return requests.get(URL + "?", params={
        'func': 'ticket',
        'out': 'xml',
        'authinfo': LOGIN + ":" + PASS
    }, verify=False).content


# получаем список тикетов, построенных в класс Ticket
def get_tickets():
    response = get_response()
    soup = BeautifulSoup(response, "xml")
    tickets = soup.find_all("elem")
    list = []
    for ticket in tickets:
        id = ticket.find_all("id")[0].string
        client = ticket.find_all("client")[0].string
        title = ticket.find_all("name")[0].string
        try:
            unread = ticket.find_all("unread")[0].string
        except:
            unread = "off"
        if unread == "on":
            is_unread = True
        else:
            is_unread = False
        list.append(Ticket(id, title, client, is_unread))
    return list
