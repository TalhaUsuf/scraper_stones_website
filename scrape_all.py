##
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

##
# 🔵 Iterate over each country urls, open main page and get all the urls of companies
this_country_companies = []
# for k in tqdm(range(len(_URLS)), colour='red'):
response = requests.get(_URLS[0])
Console().print(f"🛠️\tprocessing {_URLS[0]}")
soup = BeautifulSoup(response.content, 'html.parser')
for j in soup.find_all("div", class_="xxb"):
    for k in j.find_all('div', class_='wz'):
        for n in k.find_all('div', class_='gs'):
            this_country_companies.append(n.a.get('href'))


Console().print(this_country_companies)

##

# 🔴 open company page and get information
this_company_details = {}
for url_ in tqdm(this_country_companies, colour='green', desc="URL"):
    page = requests.get(url_)

    soup = BeautifulSoup(page.content, 'html.parser')



    keys = ['Email', 'Telephone', 'WhatsAPP', 'Website', 'Contact Person', 'WeChat', 'Fax']
    # find <div class="jj"> in soup
    for k in soup.find_all('div', class_='jj'):
        contents_filter = {}
        for key in keys:
            contents = [j.strip() for j in k.text.split("\n") if (not j.strip() == '' and  j.strip().startswith(f"{key}"))]
            print(contents)
            contents_filter.setdefault(key, []).append(contents)
    this_company_details[url_] = contents_filter


Console().print_json(this_company_details, indent=4)


# pd.DataFrame.from_dict(data).to_csv("records.csv", index=False)



