import json
import psycopg2
from bs4 import BeautifulSoup
import requests
from main import all_comp_links
import pandas as pd

url = all_comp_links[0]
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')

title = soup.find_all('title')[0].text.replace('<title>','')

script_tag = soup.find_all('script')[2].text.replace('<script>','').replace('window.eventData = ','').replace(';','')

results = json.loads(script_tag)
results_list=(results['results']['results'])

print(title)
# print(results_list)
#
conn = psycopg2.connect(
    database="touchstone_competitions",
    user='postgres',
    password='1231',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()
dict_values = []
print(results_list)
for d in results_list:
        dict_values.append(tuple(d.values()))


for d in dict_values:
    cursor.execute("INSERT into climbing_results(name,score,bumped,gender,category,age_group) VALUES (%s, %s,%s, %s,%s, %s)",d)
    print(d)

conn.commit()
conn.close()




