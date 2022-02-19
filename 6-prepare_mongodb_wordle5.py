import pandas as pd
import json
from tqdm import tqdm
import os

# MIRAR LA POSSIBILITAT DE REDUIR LA INFORMACIO EN LES DBS
# AFEGINT UN INDEX A CADA PARAULA AL DB BASE
# I A LES ALTRES GUARDAR EL INDEX NOMES
# (LA FREQ I EL NOM ES PODEN MIRAR A PARTIR DE L'INDEX)

# RUUUUUUUUUN -----------> 1, 2, 4, 5, 6
# I MIRARSE COM CANVIARIA EL CAS DE EL SOLVER EN SI


if __name__ == "__main__":

    input_path = r"futur_csvs"
    dest_path = r"mongoDB_DBs"
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    #GETTING THE ENV VARIABLES --------------------------------------------------
    from dotenv import load_dotenv
    load_dotenv()
    import os
    CONNECTION_URL = os.getenv("CONNECTION_URL")

    #PREPARING THE MONGO DB -------------------------------------------------------
    from pymongo import MongoClient
    myclient = MongoClient(CONNECTION_URL)
    print('entering DB')

    dblist = myclient.list_database_names()
    if "wordleDB" in dblist:
        print("The database exists.")
    else:
        print("A database will be created")

    mydb = myclient["wordleDB"]

    #UPDATING THE MONGO DB -------------------------------------------------------
    print('--caso TOTAL')

    name_inputfile = os.path.join(input_path, 'wordsFuturesTotal.csv')

    df = pd.read_csv(name_inputfile)
    print('size: ', df['ind_word'].size)

    if df['ind_word'].size != 0: # si no hi ha elements ens pot donar problemes

        # SORT ALHABETICALLY
        df.sort_values(by=['ind_word'], inplace=True, ascending=False)

        # ADD COUNTING INDEX ID
        df.insert(0, '_id', range(len(df)))
        mylist = df.to_dict("records")

        # UPDATE MONGODB
        NAMEDB = "wordsFuturesTotal"
        collist = mydb.list_collection_names()
        if NAMEDB in collist:
          print("The collection exists. It will be reseted")
          mycol = mydb[NAMEDB]
          mycol.drop()
        else:
          print("The collection does not exists. One will be created.")

        mycol = mydb[NAMEDB]
        x = mycol.insert_many(mylist)
        print('Collection inserted')

        # WRITING EXCEL WITH NEW TABLE ------------------------------------------------
        df.to_csv(os.path.join(dest_path, NAMEDB+'.csv'), index=False)
        print('Table saved')
    print('Done')
