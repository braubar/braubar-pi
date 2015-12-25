import requests
from bs4 import BeautifulSoup


class Steckdose:
    url = None
    PLUG_1 = 'cte1'
    PLUG_2 = 'cte2'
    PLUG_3 = 'cte3'
    PLUG_4 = 'cte4'
    ON = 1
    OFF = 0
    status = {
        PLUG_1: 0,
        PLUG_2: 0,
        PLUG_3: 0,
        PLUG_4: 0
    }

    def __init__(self, url='http://192.168.2.36/', password='braubar'):
        self.url = url
        self.status = self.login(password)

    def login(self, password):
        values = {"pw": password}
        return self.request(referrer="login.html", values=values)

    def logout(self):
        values = {}
        self.status = self.request(referrer="login.html", values=values)
        return self.status

    def switch(self, plug, value):
        values = {plug: value}
        self.status = self.request(values=values)
        return self.status

    def request(self, referrer='', values=''):
        url = self.url + referrer
        r = requests.post(url, data = values)
        return self.parse_response(r.text)

    def parse_response(self, response_data):
        soup = BeautifulSoup(response_data, 'html.parser')
        status = {}
        if soup.script.string[:8] == 'function':
            print("logged out")
        if soup.script.string[4:14] == 'sockstates':
            soup.script.string[17:26]
            status[Steckdose.PLUG_1] = soup.script.string[18]
            status[Steckdose.PLUG_2] = soup.script.string[20]
            status[Steckdose.PLUG_3] = soup.script.string[22]
            status[Steckdose.PLUG_4] = soup.script.string[24]
        return status
