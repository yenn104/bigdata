# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:19:37 2023

@author: Yuta
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import re


URL = "https://katjewelry.vn/new-collection"
parsed_url = urlparse(URL)
domain = parsed_url.netloc.split('.')[0]

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
quotes=[]  # a list to store quotes

netloc = parsed_url.netloc;

if domain == 'katjewelry':
    table = soup.find('section', attrs = {'class':'products-view products-view-grid test1'})
    for row in table.findAll('div',attrs = {'class', 'col-xs-6 col-sm-4 col-md-4 col-lg-3'}):
        quote = {}
        quote['ProductLink'] = netloc + row.a['href']
        quote['ProductName'] = row.find('a',attrs = {'class','line-clamp'}).text.strip().replace('\u00a0','').replace('\u20ab','').replace('.','')
        quote['ProductPrice'] = row.find('span',attrs = {'class','price product-price'}).text.replace('\u00a0','').replace('\u20ab','').replace(',','')
        quote['ProductImg'] = row.find('img')['data-lazyload']
        quotes.append(quote)

    filename = domain + '.json'
    with open(filename, 'w') as f:
        json.dump(quotes, f)


