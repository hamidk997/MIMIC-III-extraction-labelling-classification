import pandas as pd
import os.path
import argparse
import datetime
from tqdm import tqdm
import sys


def split_chart_events():

    num_cols = []

    df = pd.read_csv('bq-results-20200802-021832-lqosive705ty.csv')
    patients = set(df['SUBJECT_ID'])

    for patient in tqdm(patients):
        new_file_path = os.path.join(args.save_dir, 'p' + str(patient).zfill(6) + '.csv')

        data = df[df['SUBJECT_ID'] == patient]
        num_cols.append(
                        len(data.columns)
                        )

        if os.path.exists(new_file_path):
            with open(new_file_path, 'a') as fd:
                data.to_csv(fd, header=False, index = False)

        else:
            with open(new_file_path, 'w') as fd:
                data.to_csv(fd, header=True, index = False)

    print(datetime.datetime.now())



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("chartevents_path", help="Path to CHARTEVENTS file")
    parser.add_argument("save_dir", help="Directory to be saved in")

    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    n = split_chart_events()

