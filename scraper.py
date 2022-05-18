import os
import requests
from bs4 import BeautifulSoup as bs
import re

DOMAIN = "https://www.cryptodatadownload.com"
url = "https://www.cryptodatadownload.com/data/binance/"

# Load the web page content

r = requests.get(url, verify=False)
 # Beautiful soup object
soup = bs(r.content, "html.parser")
n=int(input("Enter the number of cryptocurrencies you wish to download:"))

files = []

# Parsing for the links (daily prices)


for item in soup.find_all('a'):
    if re.sub(r'\s+','',item.get_text())=='[Daily]':
        link=item.get('href')
        name=link.split('/')[-1]
        files.append(link.split('/'))
        if len(files) < n:
         print(f"Downloading {name}...")
         with open (name,'wb') as file:
            try:
                resp = requests.get(link,
                                    verify=False, timeout=5)
                file.write(resp.content)
            except requests.exceptions.ConnectionError:
                print("Site not reachable",link)
        else:
            pass
print("Download completed")



