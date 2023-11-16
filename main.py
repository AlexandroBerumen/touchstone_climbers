from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import psycopg2

link_list =[]
url = 'https://competitions.touchstoneclimbing.com'
all_comp_links = []
final_climbing_data = []

def scrape_links(url):

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    link = soup.find_all('a')
    for links in link:
        link_list.append(links.get('href'))
    del link_list[0:3]

    for link in link_list:
        all_comp_links.append(url + link)


def scrape_climbing_data():
    for link in all_comp_links[:1]:
            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'html.parser')
            date_of_competition = {'date': soup.find_all('small')[0].text.replace('<small>', '')}
            event = {'event': soup.find_all('title')[0].text.replace('<title>', '')}
            script_tag = soup.find_all('script')[2].text.replace('<script>','').replace('window.eventData = ','').replace(';','')
            results = json.loads(script_tag)
            results_list = (results['results']['results'])
            # comp_rank = {'rank': soup.select('.result__rank')[0].text.replace('<div>', '')}
            for dict in results_list:
                final_climbing_data.append({**event, **date_of_competition,**dict})


def create_pg_table():
    # establishing the connection
    conn = psycopg2.connect(
        database="touchstone_competitions", user='postgres', password='1231', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing query to create a database
    sql = '''CREATE database TOUCHSTONE_COMPETITIONS'''
    # dropping table if it exists already
    drop = '''DROP TABLE res'''
    cursor.execute(drop)
    # Creating a database
    # creating table
    sql = '''CREATE TABLE res(
     id  SERIAL NOT NULL primary key,
     event varchar(150) not null,
     date DATE not null,
     name varchar(50) not null,
     score varchar(50) not null,
      bumped varchar(50) not null,
     gender varchar(50) not null,
      category varchar(50) not null,
     age_group varchar(50) not null
    )'''
    cursor.execute(sql)
    dict_values = []

    for d in final_climbing_data:
        dict_values.append(tuple(d.values()))

    for d in dict_values:
        cursor.execute(
            "INSERT into res(event,date,name,score,bumped,gender,category,age_group) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)",
            d)

    print("Database created successfully........")
    conn.close()



scrape_links(url)
scrape_climbing_data()
create_pg_table()

