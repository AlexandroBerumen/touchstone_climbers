from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://competitions.touchstoneclimbing.com'
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')

link = soup.find_all('a')

link_list =[]
for links in link:
    link_list.append(links.get('href'))
del link_list[0:3]

#alot of soup

all_comp_links =[]

for link in link_list:
    all_comp_links.append(url+link)

