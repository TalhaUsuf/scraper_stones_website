import requests
from bs4 import BeautifulSoup

def get_all_companies_urls(country_url):
    """
    given a country url, get all the companies urls

    Parameters
    ----------
    country_url : str
        url of a given country

    Returns
    -------
    List[str]
        list of company urls

    """
    this_country_companies = []
    response = requests.get(country_url)
    # Console().print(f"🛠️\tprocessing {_URLS[0]}")
    soup = BeautifulSoup(response.content, 'html.parser')
    for j in soup.find_all("div", class_="xxb"):
        for k in j.find_all('div', class_='wz'):
            for n in k.find_all('div', class_='gs'):
                this_country_companies.append(n.a.get('href'))

    return this_country_companies