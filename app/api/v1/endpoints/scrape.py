from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import requests
import yfinance as yf
# import requests.exceptions.HTTPError as HTTPError
from fastapi import FastAPI, HTTPException


agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
headers = {'User-Agent': agent}
url = 'https://finance.yahoo.com/quote/TALIBAN/news/'
data = requests.get(url, headers=headers)
# print(data.read())
soup = BeautifulSoup(data.text)
# print(soup)
# print(soup.json())

# ticker = yf.Ticker('TALIBAN')
# info = None

ticker = yf.Ticker('PENIS')
info = ticker.info
print(info['trailingPegRatio'])
if info['trailingPegRatio'] is None:
    raise HTTPException(status_code=404, detail='Invalid ticker')
  


# headline = soup.findAll('h3', attrs={'class':'clamp yf-18q3fnf'}, limit=None)
no_results = soup.findAll('p')
for n in no_results:
    no_text = n.get_text()
    if 'No results' in no_text:
        print('Fucker')
headline = soup.findAll('h3', class_='clamp yf-18q3fnf', limit=None)
divs = soup.find('div', attrs={'id':'sda-E2E'})
section = soup.find('section', attrs={'class':'mainContent yf-tnbau3'})


print(len(headline))
for title in headline:
   text = title.get_text()
   print(text)