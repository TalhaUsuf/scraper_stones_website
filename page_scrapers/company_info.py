import requests
from bs4 import BeautifulSoup

def get_this_company_info(url_):
    """
    given a url of a company, get its email, whatsapp and other details

    Parameters
    ----------
    url_ : str
        url of the company

    Returns
    -------
    dict

    """

    this_company_details = {}
    page = requests.get(url_)

    soup = BeautifulSoup(page.content, 'html.parser')



    keys = ['Email', 'Telephone', 'WhatsAPP', 'Website', 'Contact Person', 'WeChat', 'Fax']
    # find <div class="jj"> in soup
    for k in soup.find_all('div', class_='jj'):
        contents_filter = {}
        for key in keys:
            contents = [j.strip() for j in k.text.split("\n") if (not j.strip() == '' and  j.strip().startswith(f"{key}"))]
            # print(contents)
            contents_filter.setdefault(key, []).append(contents)
    this_company_details[url_] = contents_filter

    return this_company_details

