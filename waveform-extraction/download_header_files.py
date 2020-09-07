import os
from urllib.request import urlopen
from tqdm import tqdm
import argparse

path_to_patient_ids = 'https://archive.physionet.org/physiobank/database/mimic3wdb/matched/RECORDS'
save_dir = "/Volumes/Elements/all_header_files/"

f = urlopen(path_to_patient_ids)
patient_paths = f.read().decode('utf-8').split('\n')

parser = argparse.ArgumentParser()
parser.add_argument("lim1", nargs='?', default=0)
parser.add_argument("lim2", nargs='?', default=len(patient_paths))
args = parser.parse_args()

print(args.lim1, args.lim2)
print('DOWNLOADING HEADER FILES')

i = 0

for patient in tqdm(patient_paths[678:680]):
    if i == 0:
        print(patient_paths[int(args.lim1)])
        print(patient_paths[int(args.lim2) - 1])
        i = i + 1

    save_path = os.path.join(save_dir,patient)

    os.makedirs((save_path), exist_ok=True)
    command = f"rsync -CaLvz -q --delete  --include='*.hea'    --include='*/' --exclude='*' --prune-empty-dirs  " \
              f"physionet.org::mimic3wdb-matched/{patient} {save_path}"

    os.system(command)
