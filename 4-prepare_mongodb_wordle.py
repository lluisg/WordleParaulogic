import pandas as pd
import json

words = pd.read_json('diccionari5.json')
print(words.info())

print('size: ', words['word'].size)

# SORT ALHABETICALLY
words.sort_values(by=['word'], inplace=True, ascending=False)

# ADD COUNTING INDEX ID
words.insert(0, '_id', range(len(words)))
mylist = words.to_dict("records")

#
#GETTING THE ENV VARIABLES --------------------------------------------------
from dotenv import load_dotenv
load_dotenv()
import os
CONNECTION_URL = os.getenv("CONNECTION_URL")

#UPDATING THE MONGO DB -------------------------------------------------------
from pymongo import MongoClient

myclient = MongoClient(CONNECTION_URL)
print('entering DB')

dblist = myclient.list_database_names()
if "wordleDB" in dblist:
    print("The database exists.")
else:
    print("A database will be created")

mydb = myclient["wordleDB"]

NAMEDB = "wordsCatalan5"
collist = mydb.list_collection_names()
if NAMEDB in collist:
  print("The collection exists. It will be reseted")
  mycol = mydb[NAMEDB]
  mycol.drop()
else:
  print("The collection does not exists. One will be created.")

mycol = mydb[NAMEDB]
x = mycol.insert_many(mylist)

# WRITING EXCEL WITH NEW TABLE ------------------------------------------------
words.to_csv('./mongoDB_DBs/'+NAMEDB+'.csv', index=False)
print('Table saved')
print('Done')
