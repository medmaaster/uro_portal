# -*- coding: utf-8 -*
import requests
import os
import  winsound
from stem.control import Controller
from stem import Signal
from multiprocessing import Pool
from bs4 import BeautifulSoup

# search the directory, if not found create a new one
directory = "1-Suche/"
if not os.path.exists(directory):
    os.makedirs(directory)
x = 0


url = "https://www.urologenportal.de/patienten/urologensuche.html?tx_urosearch_pi1[action]=list&tx_urosearch_pi1[controller]=Adresse&cHash=5edf1223c9f1fd3874d64d32ed0f192a"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
                 ""
}


def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session
session = get_tor_session()
# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="callofdutty23")
        controller.signal(Signal.NEWNYM)


def load_zipcode(plz):
    global x, session
    url_search = url +str(plz)
    #session = requests.Session()
    filename = plz + ".html"
    if not os.path.isfile(directory + filename):
        payload = {
        "tx_urosearch_pi1[__referrer][@extension]": "Urosearch",
        "tx_urosearch_pi1[__referrer][@controller]": "Adresse",
        "tx_urosearch_pi1[__referrer][@action]": "search",
        "tx_urosearch_pi1[__referrer][arguments]": "YTowOnt9e8ec05f5605384e1669befc4e0245794c148a3b8",
        "tx_urosearch_pi1[__referrer][@request]": "{\"@extension\":\"Urosearch\",\"@controller\":\"Adresse\",\"@action\":\"search\"}387f133e68e1d0d0ba67023805186926bb2f8e8e",
        "tx_urosearch_pi1[__trustedProperties]": "{\"search\":{\"location\":1,\"radius\":1,\"name\":1,\"choice\":[1,1,1,1]}}1333c6e8c29f137567e29a0734fdf2a9dd4bd4d2",
        "tx_urosearch_pi1[search][location]": str(plz),
        "tx_urosearch_pi1[search][radius]": "20",
        "tx_urosearch_pi1[search][name]": "",
        "tx_urosearch_pi1[search][choice]": ""
        }
        x += 1
        if x > 10:
            print(session.get("http://httpbin.org/ip").text)
            renew_connection()
            session = get_tor_session()
            print(session.get("http://httpbin.org/ip").text)
            x = 0
        try :
            r = session.post(url, data=payload,timeout= 10)
        except:
            winsound.Beep(1000,500)
        #r = requests.post(url, data=payload,timeout= 20)
        #r = requests.get(url_search, headers =headers)
        soup = BeautifulSoup(r.text, "html.parser")
        print(filename+ "\t"+ str(r.status_code) + "\t" + str(x))
        with open(directory + filename,'w+') as f:
            f.write(r.text)


if __name__ == '__main__':

    with open("PLZ_DE.csv", "r") as f:
        zipcodes = [line.replace("\n", "").split(";")[0] for line in f.readlines()[1:]]

    with Pool(4) as p:
        p.map(load_zipcode, zipcodes)