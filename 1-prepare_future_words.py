import json
from glob import glob
import os
from tqdm import tqdm

def check_paraula_valida(paraula_input, resultat, lletra, ind_lletra, paraula):
    if resultat == 'I':
        if paraula_input.count(lletra) == 1:
            # si la lletra nomes apareix una vegada a la paraula introduida
            if lletra not in paraula:
                return True
        else:
            # si la lletra apareix mes de una vegada a la paraula introduida
            if paraula.count(lletra) == 1: # descarta les paraules en que apareix mes de una vegada
                return True

    elif resultat == 'M':
        if lletra in paraula and lletra != paraula[ind_lletra]:
            return True

    elif resultat == 'C':
        if lletra == paraula[ind_lletra]:
            return True

    return False

def calcular_paraules_possibles(paraula_input, resultats, diccionari_possibles):
    paraules_possibles = list(diccionari_possibles.keys())
    for ind_lletra, (lletra, resultat) in enumerate(zip(paraula_input, resultats)):
        paraules_possibles[:] = [x for x in paraules_possibles if check_paraula_valida(paraula_input, resultat, lletra, ind_lletra, x)]

    diccionari_possibles_new = {}
    for paraula in paraules_possibles:
        diccionari_possibles_new[paraula] = diccionari_possibles[paraula]

    return diccionari_possibles_new

def get_possibles_lists(posibilities, lenn):

    to_return = []
    for i in posibilities:
        if lenn > 1:
            lowers = get_possibles_lists(posibilities, lenn-1)
            for lower in lowers:
                to_return.append(i+lower)
        else:
            to_return.append(i)

    return to_return


if __name__ == "__main__":

    diccionary_file = r"diccionari.json"
    futur_file = r"futures_paraules.json"

    with open(diccionary_file, 'r') as fo:
        diccionari = json.load(fo)

    diccionari_possibles = {}
    for x in diccionari.keys():
        if len(x) == 5 and ' ' not in x:
            diccionari_possibles[x] = diccionari[x]

    resultats = get_possibles_lists(['I', 'M', 'C'], 5)

    futures_paraules = {}
    for word in tqdm(diccionari_possibles.keys()):
    # for word in tqdm(list(diccionari_possibles.keys())[:30]):
        futures_paraules[word] = {}

        for resultat in resultats:
            futures_paraules_calc = calcular_paraules_possibles(word, resultat, diccionari_possibles)
            futures_paraules[word][resultat] = list(futures_paraules_calc.keys())

    d1 = {key:futures_paraules[key] for i, key in enumerate(futures_paraules) if i % 2 == 0}
    d2 = {key:futures_paraules[key] for i, key in enumerate(futures_paraules) if i % 2 == 1}

    with open(futur_file.replace('.json', '_1.json'), 'w') as fo:
        json.dump(d1, fo)
    with open(futur_file.replace('.json', '_2.json'), 'w') as fo:
        json.dump(d2, fo)