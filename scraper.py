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
n=int(input("Enter the number files you wish to download:"))

# Parsing for the links (daily prices)
counter=0
for item in soup.find_all('a'):
    if re.sub(r'\s+','',item.get_text())=='[Daily]':
        link=item.get('href')
        name=link.split('/')[-1]
        counter+=1
        print(f"Downloading {name}...")
        with open (name,'wb') as file:
            try:
                resp = requests.get(link,
                                    verify=False, timeout=5)
                file.write(resp.content)
            except requests.exceptions.ConnectionError:
                print("Site not reachable",link)
        if counter >= n:
            break

print("Download completed")



