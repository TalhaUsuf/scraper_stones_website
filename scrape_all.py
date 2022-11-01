#%%
from bs4 import BeautifulSoup
from rich.console import Console
from pathlib import Path
import json
import requests
import pandas as pd
from tqdm import tqdm
from pqdm.threads import pqdm

##
# 🔴 go to the page which has all the URLs of countries
response = requests.get("https://www.stoneadd.com/Stone-Suppliers.html")
# make a soup from response
soup = BeautifulSoup(response.content, 'html.parser')

data = {}
_URLS = []
for k in tqdm(soup.find_all("div", class_="xlei"), colour='green'):

    for j in tqdm(k.find_all("li"), colour='red', leave=False):
        # Console().print(j.a.get('href'))

        data.setdefault("Country", []).append(f"{j.text}")
        data.setdefault("url", []).append(f"{j.a.get('href')}")
        _URLS.append(f"{j.a.get('href')}")


# 🔵 Iterate over each country urls, open main page and get all the urls of companies
subs = []
# for k in tqdm(range(len(_URLS)), colour='red'):
response = requests.get(_URLS[0])
soup = BeautifulSoup(response.content, 'html.parser')
for j in soup.find_all("div", class_="xxb"):
    for k in j.find_all('div', class_='wz'):
        for n in k.find_all('div', class_='gs'):
            subs.append(n.a.get('href'))


Console().print(subs)







# pd.DataFrame.from_dict(data).to_csv("records.csv", index=False)



