import json
from glob import glob
import os

def demanar_input():

    paraula_valida = False
    resultat_valid = False
    while not paraula_valida or not resultat_valid:
        paraula_valida = False
        resultat_valid = False

        lletres = input("Quines lletres estan disponibles?:")
        lletres = lletres.upper()
        if len(lletres) == 6 and lletres.isalpha():
            paraula_valida = True
        else:
            print('Lletres introduides no valides')

        lletra = input("Quina es la lletra central?:")
        lletra = lletra.upper()
        if len(lletra) == 1 and lletra.isalpha():
            resultat_valid = True
        else:
            print('Lletra no valida.')

    return lletres, lletra

if __name__ == "__main__":

    diccionary_file = r"diccionari.json"

    with open(diccionary_file, 'r') as fo:
        paraules = json.load(fo)

    lletres, lletra_central = demanar_input()
    # lletres = ["TREGJA"]
    # lletra_central = "U"

    lletres = [x for x in lletres]
    lletres.append(lletra_central)
    print('lletres', lletres)

    paraules_possibles = []
    for word in paraules:
        if len(word) > 2:
            if lletra_central in word:
                for lletra in word:
                    if lletra not in lletres:
                        break
                else:
                    paraules_possibles.append(word)
    paraules_possibles.sort()

    print(len(paraules_possibles), 'paraules_possibles')
    print(paraules_possibles)

    len_max = 0
    paraules_llargues = []
    for paraula in paraules_possibles:
        if len(paraula) > len_max:
            paraules_llargues = [paraula]
            len_max = len(paraula)
        elif len(paraula) == len_max:
            paraules_llargues.append(paraula)

    print('paraules mes llargues:', paraules_llargues)
