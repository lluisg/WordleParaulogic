import json
from glob import glob
import os
import random

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

def evaluar_moviment(paraula, resultats, paraules_possibles, lletres_correctes):

    for ind_lletra, (lletra, resultat) in enumerate(zip(paraula, resultats)):
        new_paraules_possibles = []

        for ind_paraula, paraula in enumerate(paraules_possibles):
            if resultat == 'I':
                if lletra not in paraula:
                    new_paraules_possibles.append(paraula)

            elif resultat == 'M':
                if lletra in paraula and lletra != paraula[ind_lletra]:
                    new_paraules_possibles.append(paraula)

            elif resultat == 'C':
                if lletra == paraula[ind_lletra]:
                    new_paraules_possibles.append(paraula)

        paraules_possibles = new_paraules_possibles

    return paraules_possibles


def seleccionar_seguent_paraula(paraules_possibles, lletres_correctes):
    return random.choice(paraules_possibles)


if __name__ == "__main__":

    diccionary_file = r"diccionari.json"

    with open(diccionary_file, 'r') as fo:
        paraules = json.load(fo)

    paraules_possibles = []
    for x in paraules:
        if len(x) == 5 and ' ' not in x:
            paraules_possibles.append(x)

    win = False
    tirades = 0
    lletres_correctes = []
    print(len(paraules_possibles), 'paraules possibles')
    print('per començar prova amb:', paraula_mes_comuna(paraules_possibles))
    # while not win or tirades <= 6:
    while not win or tirades <= 0:
        print('------------------------------------------------------------------------------')
        print('TORN', tirades+1)

        paraula, resultats = demanar_input()
        paraules_possibles = evaluar_moviment(paraula, resultats, paraules_possibles, lletres_correctes)
        print('Queden', len(paraules_possibles), 'paraules possibles')

        if len(paraules_possibles) == 1:
            seguent_paraula = paraules_possibles[0]
            print('Hem guanyat!\nParaula guanyadora: ', '--'+seguent_paraula+'--', '\n')
            win = True

        else:
            seguent_paraula = seleccionar_seguent_paraula(paraules_possibles, lletres_correctes)

            print('proxima paraula: ', '--'+seguent_paraula+'--', '\n')
            tirades += 1
