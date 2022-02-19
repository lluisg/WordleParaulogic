import csv
import json
import unidecode
import re
from glob import glob
import os
from tqdm import tqdm
import urllib.request
import re

def ObtenirFreqWord_URL(word):

    url = "https://ctilc.iec.cat/scripts/CTILCQConc_Lemes2.asp?cadlema="+word+"&cadlemacond=0&seccio=CTILC1"
    file = urllib.request.urlopen(url)

    freq = 0
    for line in file:
        decoded_line = line.decode("utf-8")

        if 'NAME="Qlocali" ID="Qlocali" VALUE' in decoded_line:
            freq = re.findall('VALUE="([0-9]*)"', decoded_line)[0]
            break

    return int(freq)


if __name__ == "__main__":
    
    words = {}

    with open('DB/DIEC2_CTILC_senseCG.csv', newline='', encoding='latin1') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            words[row[0].split(';')[0]] = int(row[0].split(';')[2])


    print(len(words), 'total words')
    words_clean = {}
    for word in tqdm(words.keys()):
        if unidecode.unidecode(word).upper() in words_clean.keys():
            words_clean[unidecode.unidecode(word).upper()] += words[word]
        else:
            words_clean[unidecode.unidecode(word).upper()] = words[word]
    # words_clean = {x:words_clean[x] for x in words_clean.keys() if len(x) == 5 and words_clean[x] >= 10}

    print('Cleaning words')
    words_clean5 = []
    index_dict = {}
    word_dict = {}
    ind_w = 0
    for word in tqdm(words_clean.keys()):
        if len(word) == 5 and ' ' not in word:
            if words_clean[word] >= 50:
                words_clean5.append({'word':word, 'freq':words_clean[word], 'ind': ind_w})
                word_dict[word] = ind_w
                index_dict[ind_w] = word
                ind_w += 1
            elif words_clean[word] >= 10:
                try:
                    freq = ObtenirFreqWord_URL(word)
                    if freq >= 25:
                        words_clean5.append({'word':word, 'freq':words_clean[word], 'ind': ind_w})
                        word_dict[word] = ind_w
                        index_dict[ind_w] = word
                        ind_w += 1
                except:
                    pass

    print(len(words_clean5), 'unique words')

    with open('diccionari5.json', 'w') as fo:
        json.dump(words_clean5, fo)

    with open('dict_ind2word.json', 'w') as fo:
        json.dump(index_dict, fo)
    with open('dict_word2ind.json', 'w') as fo:
        json.dump(word_dict, fo)
