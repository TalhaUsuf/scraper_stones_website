#%%
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup 
import json

page = requests.get("https://www.stoneadd.com/suppliers.asp")

soup = BeautifulSoup(page.content, 'html.parser')




# get left top URLs
urls_left_top = []
for k in soup.find_all(id="mbox"):
    for j in k.find_all(id="dir"):
        for m in j.find_all("li"):
            urls_left_top.append(m.a.get('href'))


#%%
page = requests.get("https://www.stoneadd.com/suppliers.asp")

soup = BeautifulSoup(page.content, 'html.parser')

# get left bottom URLs
urls_left_bottom = []
for k in soup.find_all(id="mbox"):
    for j in k.find_all(id="dir"):
        for m in j.find_all("div", class_="list"):
            for n in m.find_all("span", class_="lb"):
                urls_left_bottom.append(n.a.get('href'))


#%%
from pathlib import Path
urls = urls_left_top + urls_left_bottom
Path("all_urls.json").write_text(json.dumps(urls))

print(f"{len(urls)} major urls have been found")

#%%

# for index, u in tqdm(enumerate(urls), colour='green'):
#     page = requests.get(f"{u}")

#     soup = BeautifulSoup(page.content, 'html.parser')

#     sub_urls = []
#     for k in soup.find_all('div', class_='ppd'):
#         for j in k.find_all('div', class_='cmn'):
#             for m in j.find_all('div', class_='rq'):
#                 sub_urls.append(m.find('a').get('href'))


#     print(sub_urls)

#     data = {}
#     for idx, url_ in tqdm(enumerate(sub_urls), colour='green', desc="URL"):
#         page = requests.get(url_)

#         soup = BeautifulSoup(page.content, 'html.parser')
#         print(soup.prettify())

#         #%%


#         keys = ['Email', 'Telephone', 'WhatsAPP', 'Website', 'Contact Person', 'WeChat', 'Fax']
#         # find <div class="jj"> in soup
#         for k in soup.find_all('div', class_='jj'):
#             contents_filter = {}
#             for key in keys:
#                 contents = [j.strip() for j in k.text.split("\n") if (not j.strip() == '' and  j.strip().startswith(f"{key}"))]
#                 print(contents)
#                 contents_filter.setdefault(key, []).append(contents)
#         data[url_] = contents_filter
#     # %%
#     with open(f"{index}_data.json", "w") as f:
#         json.dump(data, f, indent=4)