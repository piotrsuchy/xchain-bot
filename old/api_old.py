import requests
import pandas as pd
from pandas.io.json import json_normalize

# import http.client
#
# conn = http.client.HTTPSConnection("xchain.io")
#
# payload = ""
#
# headers = {
#     'authority': "xchain.io",
#     'accept': "application/json, text/javascript, */*; q=0.01",
#     'accept-language': "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
#     'cookie': "_ga=GA1.2.540574753.1651160962; _gid=GA1.2.108218237.1661114428; __cflb=0H28vTMs9qB7586DojojQU31oryYZWCRk1WnpFdQzPw",
#     'referer': "https://xchain.io/",
#     'sec-ch-ua': "^\^Chromium^^;v=^\^104^^, ^\^"
#     }
#
# conn.request("GET", "/explorer/dispenses?start=0&length=100&_=1661115259212", payload, headers)
#
# res = conn.getresponse()
# data = res.read()
#
# print(data.decode("utf-8"))

url = "https://xchain.io/explorer/dispenses"

results_list = []
for st in range(1, 5):
    querystring = {"start":f"{st}","length":"100","_":"1661115259212"}

    headers = {
        "authority": "xchain.io",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": "_ga=GA1.2.540574753.1651160962; _gid=GA1.2.108218237.1661114428; __cflb=0H28vTMs9qB7586DojojQU31oryYZWCRk1WnpFdQzPw",
        "referer": "https://xchain.io/",
        "sec-ch-ua": "^\^Chromium^^;v=^\^104^^, ^\^"
    }

    r = requests.request("GET", url, headers=headers, params=querystring)

    data_ = r.json()
    for asset in data_['data']:
        results_list.append(asset)

#print(len(results_list))
#
# data_frame = pd.io.json.json_normalize(results_list)
#
# data_frame.to_csv('first_try.csv')