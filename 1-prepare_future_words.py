import json
from glob import glob
import os
from tqdm import tqdm

def check_paraula_valida(paraula_input, resultats, lletra, ind_lletra, paraula):
    resultat = resultats[ind_lletra]

    # casos basiccs que es compleixen sempre:
    # la C te prioritat sempre
    if resultat == 'C':
        if lletra == paraula[ind_lletra]:
            return True
        else:
            return False
    else:
        if lletra == paraula[ind_lletra]:
            return False
    # la M significa que almenys apareix la lletra 1 vegada
    if resultat == 'M':
        if lletra not in paraula:
            return False


    if paraula_input.count(lletra) == 1:
        # cas apareix 1 vegada la lletra a la paraula input
        if resultat == 'I':
            # si la lletra nomes apareix una vegada a la paraula introduida
            if lletra not in paraula:
                return True
            else:
                return False

        elif resultat == 'M':
            if lletra != paraula[ind_lletra]:
                return True
            else:
                return False

    else:
        # cas la lletra apareix mes de 1 vegada a la paraula input

        # busquem lindex de laltre resultat amb la mateixa lletra
        indices = [i for i, x in enumerate(paraula_input) if x == lletra]
        for ind in indices:
            if ind != ind_lletra:
                if resultats[ind_lletra] == 'I' and resultats[ind] == "I":
                    # si els dos cops que apareix son incorrectes
                    if lletra not in paraula:
                        return True
                    else:
                        return False

                elif (resultats[ind_lletra] == "I" and resultats[ind] == 'M') or \
                    (resultats[ind_lletra] == 'I' and resultats[ind] == "C") or \
                    (resultats[ind_lletra] == 'M' and resultats[ind] == "I") or \
                    (resultats[ind_lletra] == 'C' and resultats[ind] == "I"):
                        if paraula.count(lletra) > 1:
                            return False

                elif (resultats[ind_lletra] == "M" and resultats[ind] == 'M') or \
                    (resultats[ind_lletra] == 'M' and resultats[ind] == "C") or \
                    (resultats[ind_lletra] == 'C' and resultats[ind] == "M") or \
                    (resultats[ind_lletra] == 'C' and resultats[ind] == "C"):
                        if paraula.count(lletra) <= 1:
                            return False

    # print('endend', paraula_input, paraula, resultats, resultat, ind_lletra)
    return True


def calcular_paraules_possibles(paraula_input, resultats, diccionari_possibles):
    paraules_possibles = list(diccionari_possibles.keys())
    for ind_lletra, lletra in enumerate(paraula_input):
        paraules_possibles[:] = [x for x in paraules_possibles if check_paraula_valida(paraula_input, resultats, lletra, ind_lletra, x)]

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
    futur_path = r"futur_files"
    if not os.path.exists(futur_path):
        os.mkdir(futur_path)
    futur_file = os.path.join(futur_path, r"futures_paraules.json")

    with open(diccionary_file, 'r') as fo:
        diccionari = json.load(fo)

    diccionari_possibles = {}
    for x in diccionari.keys():
        if len(x) == 5 and ' ' not in x:
            diccionari_possibles[x] = diccionari[x]

    resultats = get_possibles_lists(['I', 'M', 'C'], 5)

    # diccionari_possibles = {'aaaaa':0.3, 'zzzzz':0.2, 'papid':0.5, 'paear':0.5}
    # diccionari_possibles = {'esser':0.5, 'nalga':0.5}
    # resultats = ['CCMII']
    # resultats = ['IIIII']

    futures_paraules = {}
    for word in tqdm(diccionari_possibles.keys()):
    # for word in tqdm(['tarar']):
        futures_paraules[word] = {}

        for resultat in resultats:
            futures_paraules_calc = calcular_paraules_possibles(word, resultat, diccionari_possibles)
            # print('--', word, resultat)
            # print(futures_paraules_calc)
            futures_paraules[word][resultat] = list(futures_paraules_calc.keys())

    print('Creant diccionaris')
    d_lletres = {}
    for i in range(1, 27):
        d_lletres[i] = {}

    for paraula in tqdm(futures_paraules.keys()):
        primera_lletra = paraula[0]
        number = ord(primera_lletra) - 96
        d_lletres[number][paraula] = futures_paraules[paraula]

    for i in range(1, 27):
        with open(futur_file.replace('.json', '_'+str(i)+'.json'), 'w') as fo:
            json.dump(d_lletres[i], fo)
