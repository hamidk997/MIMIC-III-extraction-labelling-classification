import os
from urllib.request import urlopen
from tqdm import tqdm
import argparse

path_to_patient_ids = 'https://archive.physionet.org/physiobank/database/mimic3wdb/matched/RECORDS'

f = urlopen(path_to_patient_ids)
patient_paths = f.read().decode('utf-8').split('\n')

parser = argparse.ArgumentParser()
parser.add_argument("save_dir", nargs='?', default=0)
args = parser.parse_args()

print('DOWNLOADING HEADER FILES')


for patient in tqdm(patient_paths):
    save_path = os.path.join(args.save_dir,patient)

    os.makedirs((save_path), exist_ok=True)
    command = f"rsync -CaLvz -q --delete  --include='*.hea'    --include='*/' --exclude='*' --prune-empty-dirs  " \
              f"physionet.org::mimic3wdb-matched/{patient} {save_path}"

    os.system(command)
