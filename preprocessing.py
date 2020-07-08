import os
import pandas as pd
import pickle


def get_patient_ids(path):
    patient_ids = [f[1:].strip("0") for f in os.listdir(path)
     if os.path.isdir(os.path.join(path, f)) if f[0] == 'p']
    return patient_ids

def build_dict_rhythms(patient_ids):
    dict_rhythms = {}

    for file in patient_ids:
        path_to_file = '../merged/' + file + '.csv'
        if os.path.exists(path_to_file):
            df = pd.read_csv(path_to_file)
            rhythms1 = set(df[df['ITEMID'] == 212]['VALUE'])
            rhythms2 = set(df[df['ITEMID'] == 220048]['VALUE'])
            rhythms = rhythms1.union(rhythms2)
            dict_rhythms[file] = rhythms

        print(file)
    with open('dict_rhythms.pickle', 'wb') as handle:
        pickle.dump(dict_rhythms, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return dict_rhythms


def preprocess_split_names_gaps_samples(row):
    return row.str.replace("~", "~ ")
