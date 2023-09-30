# -*- coding: utf-8 -*-
"""GoogleLinkBringer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KbMoWxXVztiNaov6fD8bAwEr5t-ub9xE
"""


import requests
from bs4 import BeautifulSoup

def getGooglePages(query, numLinks=10):
  url=f'https://www.google.com/search?q={query}'
  headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.567 Safari/537.36"}
  response=requests.get(url=url, headers=headers)
  #print(response.text)
  soup = BeautifulSoup(response.text, 'html.parser')
  links=soup.find_all('a')
  allinks=[]
  for i, link in enumerate(links):
    if len(allinks)>=numLinks:
      break
    else:
     href=link.get('href')
     if href is not None:
       if href.startswith('/url?q='):
        linkurl = href.lstrip('/url?q=')
        allinks.append(linkurl)
       elif href=='#' or href.startswith('/search?') or 'google' in href:
         continue
       else:
         allinks.append(href)
  return list(set(allinks))
