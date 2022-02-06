import csv
import os
import time
import requests
from bs4 import BeautifulSoup as bs
from crypto_task import cryptodata




DOMAIN = "https://www.cryptodatadownload.com"
url = "https://www.cryptodatadownload.com/data/binance/"

# Load the web page content

r = requests.get(url, verify=False)

 # Beautiful soup object

soup = bs(r.content, "html.parser")

files = []

# Parsing for the links

for item in soup.find_all('a'):
     link = item.get('href')
     if 'BTCUSDT_d' in link or 'ETHUSDT_d' in link:
         print(link.split('/')[-1])
         files.append(link.split('/'))
         with open(link.split('/')[-1], 'wb') as file:
             resp = requests.get(DOMAIN + link, verify= False)
             file.write(resp.content)



# Find all *csv files
csv_files = [file for file in os.listdir(os.getcwd()) if file.endswith('.csv')]

if __name__=="__main__":
    for i in range(len(csv_files)):
        data = cryptodata(csv_files[i])
        dataset, conn = data.toDataFrame()

else:
    print("Nothing")


