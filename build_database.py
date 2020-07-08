import random
import numpy as np
from utils import *
from preprocessing import *
import argparse
import os.path


def rhythm_and_waveform_times(rhythm):
    rhythm_and_waveform = {}
    start_end_times = {}

    for k, v in dict_rhythms.items():
        rhythms = [l for l in v]
        list_with_AF_and_waveform = []

        if rhythm == 'AF':
            rhythm_annotations = ['Atrial Fib', 'AF (Atrial Fibrillation)']
            rhythm_present = common_member(rhythms, rhythm_annotations)

        elif rhythm == 'SINUS':
            rhythm_annotations = ['Normal Sinus', 'Sinus Tachy', 'ST (Sinus Tachycardia)',
                                  'Sinus Brady', 'Sinus Arrhythmia', 'SR (Sinus Rhythm)']
            rhythm_present = common_member(rhythms, rhythm_annotations)

        elif rhythm == 'OTHER':
            rhythm_annotations = ['Atrial Fib', 'AF (Atrial Fibrillation)', 'Normal Sinus', 'Sinus Tachy',
                      'ST (Sinus Tachycardia)', 'Sinus Brady', 'Sinus Arrhythmia', 'SR (Sinus Rhythm)']
            rhythm_present = not(common_member(rhythms, rhythm_annotations))





        if rhythm_present:
            print('RHYTHM PRESENT')
            path_to_file = '../merged/' + k + '.csv'
            if os.path.exists(path_to_file):
                df = pd.read_csv('../merged/' + k + '.csv')
                heart_rhythm_df = df[(df['ITEMID'] == 212) | (df['ITEMID'] == 220048)]
                if len(heart_rhythm_df) == 0:
                    continue

                if rhythm != 'OTHER':
                    selected_rhythm_df = heart_rhythm_df[
                    (heart_rhythm_df['VALUE'].isin(rhythm_annotations))]
                else:
                    selected_rhythm_df = heart_rhythm_df[~(heart_rhythm_df['VALUE'].isin(rhythm_annotations))]





                selected_rhythm_date_time = selected_rhythm_df['CHARTTIME'].tolist()

                # find waveform_record
                # number_records_on_day
                id = 'p' + k.zfill(6)
                regex_for_record = re.compile('p.*[0-9].hea')
                path_to_data = '../Database/' + id + '/'

                if os.path.exists(path_to_data):
                    records = [f for f in os.listdir(path_to_data) if os.path.isfile(os.path.join(path_to_data, f))]
                    record_files = list(filter(regex_for_record.match, records))

                    start_list = []
                    end_list = []
                    for record_file in record_files:
                        (start, end, samples) = read_file(path_to_data + record_file)
                        start_list.append(start)
                        end_list.append(end)

                        start_end_times[k] = (start_list, end_list)

                selected_rhythm_times = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in selected_rhythm_date_time]
                candidate_times = []

                if k in start_end_times.keys():
                    start = start_end_times[k][0]
                    end = start_end_times[k][1]
                    for item in range(len(start)):
                        for time in selected_rhythm_times:
                            if start[item] < time < end[item]:
                                candidate_times.append(time)
                                list_with_AF_and_waveform.append(str(time))
                                rhythm_and_waveform[k] = list_with_AF_and_waveform

        print(k)

    # SAVE PICKLE
    save_pickle_path = './{}.pickle'.format(rhythm)
    with open(save_pickle_path, 'wb') as handle:
        pickle.dump(rhythm_and_waveform, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return rhythm_and_waveform

def select_timestamps(rhythm):
    patient_choices = {}

    for id, candidates in dict_rhythm_and_waveform_times.items():
        number_of_charted_rhythms = len(candidates)
        choices = []

        if number_of_charted_rhythms < 10:
            selected = 0
            while selected < 10:
                for candidate in candidates:
                    candidate = datetime.strptime(candidate, '%Y-%m-%d %H:%M:%S')
                    time_delta = random.uniform(-20, 0)
                    candidate_ = candidate - timedelta(minutes=time_delta)
                    choices.append(candidate_)
                    selected += 1

            choices = choices[:10]

        else:
            idx = list(np.round(np.linspace(0, len(candidates) - 1, 10)).astype(int))
            selected_candidates = [candidates[i] for i in idx]
            for candidate in selected_candidates:
                candidate = datetime.strptime(candidate, '%Y-%m-%d %H:%M:%S')
                time_delta = random.uniform(-20, 0)
                candidate_ = candidate - timedelta(minutes=time_delta)
                choices.append(candidate_)

        choices = choices[:10]

        patient_choices[id] = choices

    # OVERLAPPING RECORDS - DELETE - TOO HARD TO FIND CORRECT RECORD FOR PATIENT - REVERSING AND COMING BACK DOESNT WORK
    delete_list = ['1158']

    for item in delete_list:
        if item in patient_choices.keys():
            del patient_choices[item]


    save_pickle_path = './{}_choices.pickle'.format(rhythm)
    with open(save_pickle_path, 'wb') as handle:
        pickle.dump(patient_choices, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return patient_choices

def produce_waveforms():
    patients = [f for f in os.listdir(args.path)
                if os.path.isdir(os.path.join(args.path, f)) and f.startswith('p')]

    problematic_records = ['p001004', 'p001158']
    patients = [patient for patient in patients if patient not in problematic_records]

    i = 0
    keys = ['p' + key.zfill(6) for key in choices.keys()]
    patient_count = 0
    for patient in patients:
        if patient[0] == 'p' and (patient in keys):
            num_id = patient.strip('p').lstrip('0')
            ########################################################
            ##### Either - find time it is supposed to be AF) ######
            ########################################################
            success_check = 0
            for entry in range(30):
                print('ENTRY', entry)
                if success_check == 1:
                    break

                if entry >= len(choices[num_id]):
                    break

                path, choice = get_record_file(args, choices, patient, entry)
                global_path = os.path.join(args.path, path)
                if path == None:
                    continue
                print('PATIENT', patient)
                print('RECORD', path)
                print('Selected Period = ', choice)
                start_time, end_time, samples = read_file(global_path + '.hea')
                print('        START: ', start_time)
                print('Selected Time: ', choice)
                seconds_into_record = (choice - start_time).total_seconds()
                print(seconds_into_record)

                if seconds_into_record < 0:
                    print('NO WAVEFORM AT THIS TIME ')
                    break

                if path is not None:
                    i = i + 1
                    f = open("script", "w")
                    write_command = """%s %s-%s""" % (path, seconds_into_record, seconds_into_record + 30)
                    f.write(write_command)
                    f.close()

                    record_file_regex = re.compile('[^\/]+$')  # Regex for everything after last slash
                    record_file = re.findall(record_file_regex, path)[0]
                    print(record_file, i)

                    ##########
                    # find subrecord file

                    segment_records = pd.read_csv(global_path + '.hea', header=None, skiprows=2)
                    layout_file = pd.read_csv(global_path + '.hea', header=None).iloc[1].values[0]
                    layout_file = os.path.join(args.path,patient,re.search(r'\d+', layout_file).group()+'_layout')

                    record_leads = layout_info(layout_file)['Leads']
                    segment_records = segment_records.apply(preprocess_split_names_gaps_samples)
                    segment_records['Record'], segment_records['Samples'] = segment_records[0].str.split(' ', 1).str

                    # Dealing with fail case
                    if segment_records['Record'].iloc[-1] == '#':
                        segment_records = segment_records[:-1]

                    segment_records['Cumulative samples'] = segment_records['Samples'].astype(int).cumsum()
                    samples = seconds_into_record * 125

                    # check which record is the first which is less than samples
                    cumsum_list = segment_records['Cumulative samples'].to_list()
                    start_sample = []
                    for cumsum_item in (cumsum_list):
                        if cumsum_item > samples:
                            start_sample = cumsum_item
                            break

                    if (start_sample) == []:
                        continue
                    segment_file = \
                    segment_records[segment_records['Cumulative samples'] == start_sample]['Record'].values[0]

                    # open segment file header

                    # If it's during one of the breaks, move on
                    if segment_file == '~':
                        continue

                    segment_path = os.path.join(args.path, patient, segment_file)
                    header = header_info(segment_path)

                    leads_in_segment = header['Leads'].to_list()

                    lead = 'II'
                    channel = 0  # default placeholder
                    if lead in record_leads.values:
                        channel = record_leads[record_leads == lead].index[0]
                    else:
                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                        print(' LEAD NOT PRESENT IN RECORD, SKIPPING')
                        print('~~~~~~                                                                  SKIPPING')

                        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

                        break

                    if os.path.exists('samples.csv'):
                        os.system('rm samples.csv')


                    os.chdir(args.path)
                    print(os.getcwd())

                    if os.path.exists(args.savedir) == False:
                        os.makedirs(('{}/CSV/').format(args.savedir), exist_ok=True)
                        os.makedirs(('{}/JPEG/').format(args.savedir), exist_ok=True)



                    print('Checking channel: ', channel)
                    check_channel_empty(path, seconds_into_record, channel)
                    df = pd.read_csv(os.path.join(args.path, 'samples.csv'), header=None)
                    if df.iloc[:, 1][3] == '-':
                       print('~~~~~~')
                       print('Lead does not exist at this time, skipping')
                       print('~~~~~~                                                                  SKIPPING')
                       print('################################################################################')

                       continue

                    print('#####', channel)

                    ############
                    save_csv_signal(args, path, record_file, seconds_into_record, channel)
                    save_jpeg_images(args, record_file, seconds_into_record, channel)
                    print('WRITING FILE')
                    success_check += 1

                    print('################################################################################')

    return patients

def filter_patient_ids():
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to waveform data")
    parser.add_argument("rhythm_class", help="desired rhythm class")
    parser.add_argument("savedir", help="directory to be saved to")

    args = parser.parse_args()

    # List of patients for which we have waveform data, leading 'p' and leading zeros removed from patient ids
    patient_ids = get_patient_ids(args.path)
  #  patient_ids = filter_patient_ids()

    # Create dictionary of rhythms present for each patient, as per the nurse charted data
    if os.path.isfile('./dict_rhythms.pickle'):
        with open('./dict_rhythms.pickle', 'rb') as handle:
            dict_rhythms = pickle.load(handle)
    else:
        dict_rhythms = build_dict_rhythms(patient_ids)

    # Create dictionary to indicate start and end times of each instance of the rhythm class, as per the nurse charted data
    if os.path.isfile(('./{}.pickle').format(args.rhythm_class)):
        with open(('./{}.pickle').format(args.rhythm_class), 'rb') as handle:
            dict_rhythm_and_waveform_times = pickle.load(handle)
    else:
        dict_rhythm_and_waveform_times = rhythm_and_waveform_times(args.rhythm_class)

    # Select random periods from these timestamps
    choices = select_timestamps(args.rhythm_class)

    # Produce waveforms for these choices
    test = produce_waveforms()





