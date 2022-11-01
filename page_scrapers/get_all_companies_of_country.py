import requests
from bs4 import BeautifulSoup
from tqdm import trange
from rich.console import Console
from pqdm.threads import pqdm
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

    # ist of all read the total number of pages in the ist try
    with Console().status("[bold green] Finding total no. of pages .... ", spinner="aesthetic") as status:
        data = []
        for k in soup.find_all("div", class_="to"):
            data.append(k.text)

        assert len(data) == 1, "data is not a list of length 1"
        total_pages = int(data[0].split("Total")[-1].split("Pages")[0].strip())
        Console().print(f":zap: Country URL {country_url} && Total pages: {total_pages}")

    with Console().status(f"[bold green] Processing individual {total_pages} pages in parallel .... ", spinner="aesthetic") as status:
        # use pqdm to call individual pages in parallel among all total pages listing a country's comapnies
        args = [(country_url, i) for i in range(total_pages)]
        all_companies_of_this_country = pqdm(args, _get_companies_on_a_single_page, n_jobs=12, argument_type='args')
        flatten = lambda x : [j for k in x for j in k]
        Console().print(f"Total companies: {len(flatten(all_companies_of_this_country))}")
        all_companies_of_this_country = flatten(all_companies_of_this_country)

        return all_companies_of_this_country




def _get_companies_on_a_single_page(base_url, page_number):
    this_page_companies = []
    response = requests.get(base_url + f"/{page_number+1}")
    soup = BeautifulSoup(response.content, 'html.parser')
    for j in soup.find_all("div", class_="xxb"):
        for k in j.find_all('div', class_='wz'):
            for n in k.find_all('div', class_='gs'):
                this_page_companies.append(n.a.get('href'))

    return this_page_companies


if __name__ == "__main__":

    pass