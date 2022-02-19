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
    df_total = pd.DataFrame()
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
                llistat_paraula.append(paraula)
                llistat_resultat.append(resultat)
                # for paraula_poss in data[paraula][resultat]:
                llistat_paraula_poss.append(data[paraula][resultat])


        df = pd.DataFrame()
        df['ind_word'] = llistat_paraula
        df['resultat'] = llistat_resultat
        df['ind_possibles'] = llistat_paraula_poss

        df_total = pd.concat([df_total, df], axis=0)

        print(df.shape)
        # # WRITING EXCEL WITH NEW TABLE ------------------------------------------------
        df.to_csv(os.path.join(dest_path, fname.replace('futures_paraules_', 'wordsFutures').replace('.json', '.csv')), index=False)
        print('Table saved')

    df_total.to_csv(os.path.join(dest_path, 'wordsFuturesTotal.csv'), index=False)
    print(df_total.shape)
    print('Table saved')
    print('Done')
