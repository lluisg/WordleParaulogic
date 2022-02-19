import json
from glob import glob
import os
import random
import math
from itertools import combinations
import copy

def paraula_mes_comuna(paraules_possibles):
    lletres_comunes = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}
    for paraula in paraules_possibles:
        for ind, lletra in enumerate(paraula):

            if lletra not in lletres_comunes[ind].keys():
                lletres_comunes[ind][lletra] = 0
            lletres_comunes[ind][lletra] += 1

    millor_paraula = None
    max_punt = 0
    for paraula in paraules_possibles:
        if len(list(set(paraula))) == 5:
            punt = 0
            for ind, lletra in enumerate(paraula):
                punt += lletres_comunes[ind][lletra]

            if punt > max_punt:
                max_punt = punt
                millor_paraula = paraula

    return millor_paraula


def demanar_input():

    paraula_valida = False
    resultat_valid = False
    while not paraula_valida or not resultat_valid:
        paraula_valida = False
        resultat_valid = False

        # we ask for the word
        paraula = input("Quina paraula has introduit?:")
        paraula = paraula.upper()
        if len(paraula) == 5 and paraula.isalpha():
            paraula_valida = True
        else:
            print('Paraula introduida no valida')

            # we ask for the results
        resultats = input("Com ha resultat cada lletra?\n(C: lletra posicio correcte, M: moguda, I:incorecte):")
        resultats = resultats.upper()
        if len(resultats) == 5 and paraula.isalpha():
            for lletra in resultats:
                if lletra != 'C' and lletra != 'M' and lletra != 'I':
                    break
            else:
                resultat_valid = True
        else:
            print('Resultats no valids. Siusplau fixat en la llegenda.')

    return paraula, resultats

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

def calcular_paraules_possibles(paraula_input, resultats, diccionari_possibles, file_data):

    paraules_possibles = file_data[paraula_input][resultats]

    diccionari_possibles_new = {}
    for paraula in paraules_possibles:
        if paraula in diccionari_possibles.keys():
            diccionari_possibles_new[paraula] = diccionari_possibles[paraula]

    return diccionari_possibles_new

def entropia_value(prob):
    return -1 * prob * math.log2(prob) if prob > 0 else 0

def get_combinations(posibilities, lenn):

    to_return = []
    for i in posibilities:
        if lenn > 1:
            lowers = get_combinations(posibilities, lenn-1)
            for lower in lowers:
                to_return.append(i+lower)
        else:
            to_return.append(i)

    return to_return

def seleccio_per_entropia(diccionari_possibles, data):
    resultats_entropia = {}
    resultats = get_combinations(['I', 'M', 'C'], 5)

    for paraula_possible in sorted(list(diccionari_possibles.keys())):
    # for paraula_possible in sorted(list(diccionari_possibles.keys())[:30]):
        entropia_paraula = 0
        for resultat in resultats:

            futures_paraules = calcular_paraules_possibles(paraula_possible, resultat, diccionari_possibles, data)
            prob = float(len(futures_paraules))/float(len(diccionari_possibles.keys()))
            entropia = entropia_value(prob)
            entropia_paraula += entropia

        print(paraula_possible, entropia_paraula)
        resultats_entropia[paraula_possible] = entropia_paraula

    # print(resultats_entropia)
    return max(resultats_entropia, key=resultats_entropia.get)

def diccionary_frequencies(diccionari):
    total_prob = sum(diccionari.values())
    for k in diccionari.keys():
        diccionari[k] = diccionari[k]/total_prob
    return diccionari

def seleccio_per_entropia_probabilidad(diccionari_possibles, data):
    resultats_entropia = {}
    resultats = get_combinations(['I', 'M', 'C'], 5)

    for paraula_possible in sorted(list(diccionari_possibles.keys())):
        entropia_paraula = 0
        for resultat in resultats:

            futures_paraules = calcular_paraules_possibles(paraula_possible, resultat, diccionari_possibles, data)
            prob = float(len(futures_paraules))/float(len(diccionari_possibles.keys()))
            entropia = entropia_value(prob)
            entropia_paraula += entropia

        resultats_entropia[paraula_possible] = entropia_paraula

    qualitat_paraula = {}
    diccionari_prob = diccionary_frequencies(diccionari_possibles)
    for paraula in diccionari_possibles.keys():
        entropia = resultats_entropia[paraula]
        prob = diccionari_prob[paraula]
        print(paraula, entropia, prob)
        qualitat_paraula[paraula] = entropia+prob*2

    print(qualitat_paraula)
    return max(qualitat_paraula, key=qualitat_paraula.get)

def seleccionar_seguent_paraula(diccionari_possibles, data, ALGORITME = "random"):
    if ALGORITME == "random":
        return random.choice(list(diccionari_possibles.keys()))
    elif ALGORITME == "entropia":
        return seleccio_per_entropia(diccionari_possibles, data)
    elif ALGORITME == "prob":
        return seleccio_per_entropia_probabilidad(diccionari_possibles, data)


if __name__ == "__main__":

    diccionary_file = r"diccionari.json"
    with open(diccionary_file, 'r') as fo:
        diccionari = json.load(fo)
    print('Loaded dictionary')

    with open('futures_paraules_1.json', 'r') as fo:
        data1 = json.load(fo)
    print('Loaded future 1')
    with open('futures_paraules_2.json', 'r') as fo:
        data2 = json.load(fo)
    print('Loaded future 2')
    with open('futures_paraules_3.json', 'r') as fo:
        data3 = json.load(fo)
    print('Loaded future 3')
    data = {**data1, **data2, **data3}

    diccionari_possibles = {}
    for x in diccionari.keys():
        if len(x) == 5 and ' ' not in x:
            diccionari_possibles[x] = diccionari[x]

    # print({k: v for k, v in sorted(diccionari_possibles.items(), key=lambda item: item[1])})

    diccionari_possibles = {x:diccionari_possibles[x] for x in list(diccionari_possibles.keys())}

    win = False
    tirades = 0
    print(len(diccionari_possibles.keys()), 'paraules possibles')
    print('per començar prova amb:', seleccionar_seguent_paraula(diccionari_possibles, data, 'prob'))
    while not win and tirades <= 6:
        print('------------------------------------------------------------------------------')
        print('TORN', tirades+1)

        paraula, resultats = demanar_input()
        # paraula, resultats = 'QOECR', 'ICMIC'
        diccionari_possibles = calcular_paraules_possibles(paraula, resultats, diccionari_possibles, data)
        print('Queden', len(diccionari_possibles), 'paraules possibles')

        if len(diccionari_possibles) == 1:
            seguent_paraula = list(diccionari_possibles.keys())[0]
            print('Hem guanyat!\nParaula guanyadora: ', '--'+seguent_paraula+'--', '\n')
            win = True

        else:
            seguent_paraula = seleccionar_seguent_paraula(diccionari_possibles, data, 'prob')

            print('proxima paraula: ', '--'+seguent_paraula+'--', '\n')
            tirades += 1

        if tirades > 6:
            print('Hem perdut... :(')
