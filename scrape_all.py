##
import joblib
import yaml
from bs4 import BeautifulSoup
from rich.console import Console
from pathlib import Path
import json
import requests
import pandas as pd
from tqdm import tqdm
from pqdm.threads import pqdm
from joblib import dump, load
from page_scrapers import get_all_companies_urls, get_this_company_info
##


def main():


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
    Console().print(f"Total Countries: {len(data['Country'])}")
    ##
    # 🔵 Iterate over each country urls, open that page and get all the urls of listed companies


    args = _URLS
    this_country_companies = pqdm(args, get_all_companies_urls, n_jobs=12, colour='magenta')

    # List[List[str]] ---> List[str]
    flatten = lambda x : [j for k in x for j in k]
    this_country_companies = flatten(this_country_companies)
    dump(this_country_companies, "this_country_companies.joblib")
    ##

#     # 🔴 open company page and get information
    args = this_country_companies
    result = pqdm(args, get_this_company_info, n_jobs=30, colour='green')

    dump(result, "all_details.joblib")
#     dump result to json
    with open('data.yaml', 'w') as f:
        # f.write(str(det))
        yaml.dump(result, f, default_flow_style=False)



if __name__ == "__main__":
    main()
