import pandas as pd
import os
import re
from datetime import datetime, time
import numpy as np
import datetime as dt


def layout_info (path):
    top_header = pd.read_csv(path + '.hea', header=None, nrows=1).iloc[:,0]
    top_header = top_header.apply(lambda x: pd.Series(str(x).split(" ")))
    leads = top_header.iloc[:,1][0]

    if leads == str(0):
        return None

    header = pd.read_csv(path+'.hea', header=None, skiprows=[0]).iloc[:,0]
    header = header.apply(lambda x: pd.Series(str(x).split(" ")))

    header_columns = ['~', 'units', '~', '~', '~', '~', '~', '~','Leads']
    last_col = header.iloc[:,-1]
    a =  last_col.isnull().values.any()

    if a:
        header = header.iloc[:, :-1]

    header.columns = header_columns

    return header

def get_hadm_id(patient, date):
    num_id = patient[1:].lstrip('0')
    df = pd.read_csv('/Volumes/My Passport for Mac/merged/%s.csv'%(num_id))
    hadm_in_df = set(df['HADM_ID'])
    hadm_list = []

    for hadm in hadm_in_df:
        hadm_df = df[df['HADM_ID'] == hadm]

        charttimes = sorted(hadm_df['CHARTTIME'])
        start_str = (charttimes[0])
        start_dt = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
        end_str = (charttimes[-1])
        end_dt = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
        hadm_list.append((hadm, start_dt, end_dt))

    date = date
    HADM = []
    for entry in hadm_list:
        check = is_time_between(entry[1], entry[2], date)
        if check == True:
            HADM = entry[0]
            return HADM
        else:
            HADM.append(entry[0])

    HADM = 'NONE'
    return HADM


admissions_df = pd.read_csv('/Volumes/Passport/ADMISSIONS.csv')

def get_hadm_id_2(patient, date):
    num_id = patient[1:].lstrip('0')
    patient_adm_df = admissions_df[admissions_df['SUBJECT_ID'] == int(num_id) ]
    hadm_in_df = set(patient_adm_df['HADM_ID'])

    hadm_list = []

    for hadm_id in hadm_in_df:
        df = patient_adm_df[patient_adm_df['HADM_ID'] == hadm_id]
        start_str = df['ADMITTIME'].iloc[0]
        start_dt = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')

        end_str = df['DISCHTIME'].iloc[0]
        end_dt = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')

        hadm_list.append((hadm_id, start_dt, end_dt))
        LOS = (end_dt-start_dt).total_seconds()/3600
        admission_type = df['ADMISSION_TYPE'].iloc[0]

        date = date
        HADM = []
        for entry in hadm_list:
            check = is_time_between(entry[1], entry[2], date)
            if check == True:
                HADM = entry[0]
                return HADM, LOS, admission_type
            else:
                HADM.append(entry[0])

        HADM = 'NONE'
        return HADM, LOS, admission_type



def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def lead_list(leads):
    flat_list = []
    for sublist in leads:
        for item in sublist:
            flat_list.append(item)
    return flat_list

hadm_age_sex = pd.read_csv('PATIENT_INFO.csv')
path = '/Volumes/Passport/all_header_files/'
sub_dirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
patient_list = []
for sub_dir in sub_dirs:
    sub_dir_path = os.path.join(path, sub_dir)
    patients = [f for f in os.listdir(sub_dir_path) if os.path.isdir(os.path.join(sub_dir_path, f))]
    for patient in patients:
        patient_list.append(patient)

lead_table = pd.DataFrame(columns=['ID', 'HADM_ID', 'DATE', 'AGE', 'SEX', 'Admission Type', 'LOS (hours)', 'I', 'II', 'III', 'MCL', 'MCL1', 'V', 'AVR', 'AVF', 'AVL'])
i=0
for patient in patient_list:
    path_patient = os.path.join(path,patient[:3],patient)
    records = [f for f in os.listdir(path_patient) if os.path.isfile(os.path.join(path_patient, f))]
    regex_matched = re.compile('p[0-9-]*.hea')
    regex_date = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}')
    matched_record_files = list(filter(regex_matched.match, records))

    leads = []
    for record_file in matched_record_files:
        path_to_file = os.path.join(path_patient,record_file)
        layout_file_temp = pd.read_csv(path_to_file, header=None).iloc[1].values[0]
        layout_file_temp = patient + '/' + re.search(r'\d+', layout_file_temp).group() + '_layout'
        layout_file = '/Volumes/Elements/Database/' + layout_file_temp
        record_leads = layout_info(layout_file)
        if record_leads is None:
            continue
        record_leads = record_leads['Leads'].to_list()
        leads.append(record_leads)
        date_str = re.findall(regex_date, record_file)[0]
        date_dt = datetime.strptime(date_str, '%Y-%m-%d-%H-%M')
        hadm, LOS, admission_type = get_hadm_id_2(patient, date_dt)

        patient_id = patient[1:].lstrip('0')
        patient_info = hadm_age_sex[hadm_age_sex['SUBJECT_ID'] == int(patient_id)]
        sex = patient_info['SEX'].iloc[0]
        age = patient_info['AGE'].iloc[0]
        leads = lead_list(leads)



        append_dict = ({'ID':patient, 'HADM_ID':hadm, 'DATE':date_str[:10],
                        'AGE':age, 'SEX':sex, 'LOS (hours)':round(LOS), 'Admission Type':admission_type
                        })
        lead_table = lead_table.append(append_dict, ignore_index=True)

        arr = lead_table.columns._values

        for lead in leads:
            if lead in arr:
                index = (np.where(arr == lead)[0])[0]
                lead_table.iat[-1, index] = 1


    lead_table.to_csv('TABLE.csv', encoding='utf-8', index=False)

    i = i +1
    print(i)


#####
# MAKE DF OF HADMS THAT HAVE RECORDS - WILL BE USEFUL

#%%
flat_list = []
for sublist in leads:
    for item in sublist:
        flat_list.append(item)
set(flat_list)

from itertools import groupby
items = flat_list
results = {value: len(list(freq)) for value, freq in groupby(sorted(items))}

from matplotlib import pyplot as plt
ECG_leads = ['AVR', 'AVF', 'AVL', 'I', 'II', 'III', 'MCL', 'MCL1', 'V', 'V1']
dict_plot = {k:results[k] for k in ECG_leads if k in results}

x = list(dict_plot.keys())
y = list(dict_plot.values())

plt.bar(x,y)
plt.xlabel('Lead')
plt.title('Distribution')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.grid()
plt.show()



