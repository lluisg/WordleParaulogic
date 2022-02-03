import csv
import json
import unidecode
import re
from glob import glob
import os

if __name__ == "__main__":

# REDUIM EL TAMANY DEL INPUT---------------------------------------------------------------------------------------
    words = []

    files = glob(os.path.join(r"DBzips\raw_ca", '*'))
    for f in files:
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
    words = []

    with open('DB/DIEC2_CTILC_senseCG.csv', newline='', encoding='latin1') as f:
        reader = csv.reader(f)
        for row in reader:
            words.append(row[0].split(';')[0])

    with open('DB/DIEC2_GLISSANDO_senseCG.csv', newline='', encoding='latin1') as f:
        reader = csv.reader(f)
        for row in reader:
            words.append(row[0].split(';')[0])

    print(len(words), 'total words')
    words = [unidecode.unidecode(x).upper() for x in words]
    words = list(set(words))
    print(len(words), 'unique words')

    with open('diccionari.json', 'w') as fo:
        json.dump(words, fo)
