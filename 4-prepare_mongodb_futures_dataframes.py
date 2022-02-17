import pandas as pd
import json
from tqdm import tqdm
import os
from glob import glob

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

    input_path = r"futur_files"
    dest_path = r"futur_csvs"
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    files = glob(os.path.join(input_path, '*.json'))
    for f in files:
        fname = f.split('\\')[-1]

        with open(f, 'r') as fo:
            data = json.load(fo)
        print('--- Loaded', fname)

        column_names = get_possibles_lists(['I', 'M', 'C'], 5)
        df = pd.DataFrame(columns = column_names)

        llistat_paraula = []
        llistat_resultat = []
        llistat_paraula_poss = []
        for paraula in tqdm(data.keys()):
            for resultat in data[paraula].keys():
                for paraula_poss in data[paraula][resultat]:
                    llistat_paraula.append(paraula)
                    llistat_resultat.append(resultat)
                    llistat_paraula_poss.append(paraula_poss)

        df = pd.DataFrame()
        df['Paraula'] = llistat_paraula
        df['Resultat'] = llistat_resultat
        df['Paraula_poss'] = llistat_paraula_poss

        print(df.shape)
        # # WRITING EXCEL WITH NEW TABLE ------------------------------------------------
        df.to_csv(os.path.join(dest_path, fname.replace('futures_paraules_', 'wordsFutures').replace('.json', '.csv')), index=False)
        print('Table saved')
    print('Done')
