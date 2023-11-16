import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="touchstone_competitions", user='postgres', password='1231', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database TOUCHSTONE_COMPETITIONS''';

#Creating a database

# creating table
sql = '''CREATE TABLE climbing_results(
 id  SERIAL NOT NULL primary key,
 name varchar(50) not null,
 score varchar(50) not null,
  bumped varchar(50) not null,
 gender varchar(50) not null,
  category varchar(50) not null,
 age_group varchar(50) not null
)'''

cursor.execute(sql)
print("Database created successfully........")
conn.close()