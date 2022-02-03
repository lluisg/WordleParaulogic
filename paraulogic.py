import json
from glob import glob
import os

if __name__ == "__main__":

    diccionary_file = r"diccionari.json"

    with open(diccionary_file, 'r') as fo:
        paraules = json.load(fo)

    lletres = ["IUNRSE"]
    lletra_central = "V"
    lletres = [x for x in lletres[0]]
    lletres.append(lletra_central)
    print(lletres)

    paraules_possibles = []
    for word in paraules:
        if lletra_central in word:
            for lletra in word:
                if lletra not in lletres:
                    break
            else:
                paraules_possibles.append(word)

    print(len(paraules_possibles), 'paraules_possibles')
    print(paraules_possibles)
    print('paraula mes llarga:', max(paraules_possibles, key=len))
