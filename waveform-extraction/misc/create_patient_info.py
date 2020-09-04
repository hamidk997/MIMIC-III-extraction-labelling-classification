import pandas as pd
import os
import re
from datetime import datetime
from dateutil.relativedelta import *
from tqdm import tqdm

admissions_df = pd.read_csv('ADMISSIONS.csv')
patient_df = pd.read_csv('PATIENTS.csv')
transfers_df = pd.read_csv('TRANSFERS.csv')
patients = set(patient_df.SUBJECT_ID)

table = pd.DataFrame(columns=['ID', 'HADM_ID', 'AGE', 'SEX', 'WARD'])


def getAgeAtAdmission(patient, admission_time):
    DOB = list(patient_df[patient_df.SUBJECT_ID == patient]['DOB'])[0]

    DOB_dt = datetime.strptime(DOB, '%Y-%m-%d %H:%M:%S')
    admission_time_dt = datetime.strptime(admission_time, '%Y-%m-%d %H:%M:%S')

    a = relativedelta(admission_time_dt, DOB_dt).years
    return a

def getSex(patient):

    sex = list(patient_df[patient_df.SUBJECT_ID == patient]['GENDER'])[0]

    return sex

def getWard(hadm):
    wards = list(transfers_df[transfers_df['HADM_ID'] == hadm]['CURR_CAREUNIT'])
    wards = [f for f in wards if str(f) not in ['nan', 'Nan']]
    if wards == []:
        return 'NaN'
    ward = wards[0]
    return ward

for patient in tqdm(patients):
    patient_hadm_data = admissions_df[admissions_df.SUBJECT_ID == patient]

    sex = getSex(patient)
    hadms = list(patient_hadm_data.HADM_ID)

    for hadm in hadms:
        admission_time = list(patient_hadm_data[patient_hadm_data.HADM_ID == hadm]['ADMITTIME'])[0]

        age = getAgeAtAdmission(patient, admission_time)
        ward = getWard(hadm)

        row = ({'ID': patient, 'HADM_ID': hadm, 'AGE': age, 'SEX': sex,
                'WARD' : ward})

        table = table.append(row, ignore_index=True)

table.to_csv('PATIENT_DATA.csv', index = False)