import csv
import os
import time
import requests
from bs4 import BeautifulSoup as bs

import re


DOMAIN = "https://www.cryptodatadownload.com"
url = "https://www.cryptodatadownload.com/data/binance/"

# Load the web page content

r = requests.get(url, verify=False)

 # Beautiful soup object

soup = bs(r.content, "html.parser")

files = []

# Parsing for the links (daily prices)
for item in soup.find_all('a'):
    if re.sub(r'\s+','',item.get_text())=='[Daily]':
        link=item.get('href')
        name=link.split('/')[-1]
        print(name)
        files.append(link.split('/'))

        with open (name,'wb') as file:
            try:
                file.write(requests.get(link,verify=False).content)
            except requests.exceptions.ConnectionError:
                print("Site not reachable",link)




