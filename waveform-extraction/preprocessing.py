import os
import pandas as pd
import pickle
from tqdm import tqdm

def get_patient_ids(path_to_data):

    patient_ids_list = list()

    for subdirectory in os.listdir(path_to_data):
        if subdirectory.startswith('p'):
            subdirectory_ids = [f for f in os.listdir(os.path.join(path_to_data,subdirectory)) if f.startswith('p')]
            patient_ids_list.append([f for f in subdirectory_ids])

    patient_ids = [y for x in patient_ids_list for y in x]

    return patient_ids

def build_dict_rhythms(args, patient_ids):
    dict_rhythms = {}

    for file in (patient_ids):
        path_to_file = os.path.join(args.clinical_path, file + '.csv')
        if os.path.exists(path_to_file):
            print(path_to_file)
            df = pd.read_csv(path_to_file)
            rhythms1 = set(df[df['ITEMID'] == 212]['VALUE'])
            rhythms2 = set(df[df['ITEMID'] == 220048]['VALUE'])
            rhythms = rhythms1.union(rhythms2)
            dict_rhythms[file] = rhythms


    with open('dict_rhythms.pickle', 'wb') as handle:
        pickle.dump(dict_rhythms, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return dict_rhythms


def preprocess_split_names_gaps_samples(row):
    return row.str.replace("~", "~ ")
