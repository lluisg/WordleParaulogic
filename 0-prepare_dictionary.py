import csv
import json
import unidecode
import re
from glob import glob
import os
from tqdm import tqdm
import urllib.request
import re

def ObtenirFreqWord_URL(list_words):

    freqs = {}
    for word in list_words:
      url = "https://ctilc.iec.cat/scripts/CTILCQConc_Lemes2.asp?cadlema="+word+"&cadlemacond=0&seccio=CTILC1"
      file = urllib.request.urlopen(url)

      for line in file:
        decoded_line = line.decode("utf-8")

        if 'NAME="Qlocali" ID="Qlocali" VALUE' in decoded_line:
            freqs[word] = re.findall('VALUE="([0-9]*)"', decoded_line)[0]

    return freqs

if __name__ == "__main__":

# REDUIM EL TAMANY DEL INPUT---------------------------------------------------------------------------------------
    if False:
        words = []

        files = glob(os.path.join(r"DB\raw_ca", '*'))
        for f in tqdm(files):
            with open(f, encoding='latin1') as fo:
                data = fo.read()

            words.extend(re.findall('title="(.*?)"', data))

        print(len(words), 'total words raw')
        words = [unidecode.unidecode(x).upper() for x in words]
        words = list(set(words))
        print(len(words), 'unique words raw')

        with open('diccionari_rawfile.json', 'w') as fo:
            json.dump(words, fo)

# ---------------------------------------------------------------------------------------------------------------
    words = {}

    if True:
        with open('DB/DIEC2_CTILC_senseCG.csv', newline='', encoding='latin1') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                words[row[0].split(';')[0]] = int(row[0].split(';')[2])

    if False:
        with open('DB/DIEC2_GLISSANDO_senseCG.csv', newline='', encoding='latin1') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                words[row[0].split(';')[0]] = row[0].split(';')[2]

    print(len(words), 'total words')
    words_clean = {}
    for word in tqdm(words.keys()):
        if unidecode.unidecode(word).upper() in words_clean.keys():
            words_clean[unidecode.unidecode(word).upper()] += words[word]
        else:
            words_clean[unidecode.unidecode(word).upper()] = words[word]
    print(len(words_clean), 'unique words')

    with open('diccionari.json', 'w') as fo:
        json.dump(words_clean, fo)
