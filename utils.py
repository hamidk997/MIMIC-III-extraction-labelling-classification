from datetime import datetime
from datetime import timedelta
import pandas as pd
import pickle
import os
import re

def read_file(path):
    top_header = pd.read_csv(path, header=None, nrows=1).iloc[:,0]
    temp = ' '.join(top_header[0].split())
    temp = pd.Series(temp)
    top_header = temp.apply(lambda x: pd.Series(str(x).split(" ")))

    top_columns = ['Filename', 'Number of signals', 'Sampling rate', 'Samples', 'Time', 'Date']
    top_header.dropna(axis='columns')
    top_header.columns = top_columns


    datetime_string = top_header['Date'][0] + ' ' + top_header['Time'][0]
    start_datetime = datetime.strptime(datetime_string, '%d/%m/%Y %H:%M:%S.%f')
    samples = int(top_header['Samples'][0])
    sampling_rate = int((top_header['Sampling rate'][0]))
    seconds_to_add = samples/sampling_rate
    end_datetime = start_datetime + timedelta(0,seconds_to_add)

    return [start_datetime, end_datetime, samples]


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True
    else:
        return False


def get_record_file(args, dict_input, id, entry):

    dict_rhythm_and_waveform_times = dict_input

    # Sample
    # get choice date time
    num_id = id.strip('p')
    num_id = num_id.lstrip('0')
    patient_dict = dict_rhythm_and_waveform_times[str(num_id)]
    if len(patient_dict) == 0:
        return (None, None)
    choice = dict_rhythm_and_waveform_times[str(num_id)][entry]
    # get associated record
    p_id = str(id).zfill(6)

    path_to_data = os.path.join(args.path, p_id)
    records = [f for f in os.listdir(path_to_data) if os.path.isfile(os.path.join(path_to_data, f))]
    regex_for_record = re.compile('p.*[0-9].hea')
    reversed_record_files = sorted(list(filter(regex_for_record.match, records)), reverse = True)
    reversed_record_files_datetime = sorted([datetime.strptime(choice[-20:-4], '%Y-%m-%d-%H-%M') for choice in reversed_record_files], reverse=True)

    for i in range(len(reversed_record_files)):
        if choice >= reversed_record_files_datetime[i]:
            script_input = p_id + '/' + reversed_record_files[i][:-4]
            return script_input, choice

    return (None, None)

def check_channel_empty(path, start, channel):
    f = open("check_empty", "w")
    command = """rdsamp -r %s -c -H -f %s -t %s -v -pd -s %s >samples.csv""" % (path,start,(start +30),channel)
    f.write(command)
    f.close()
    os.system('chmod 755 check_empty')
    os.system('./check_empty')


def save_csv_signal(args, path, record, start, channel):
    f = open("check_empty", "w")
    command = """rdsamp -r %s -c -H -f %s -t %s -v -pd -s %s >%s.csv""" % (path,start,(start +30),channel, (('{}/CSV/').format(args.savedir) + record + '_' +str(start)))
    f.write(command)
    f.close()
    os.system('chmod 755 check_empty')
    os.system('./check_empty')


def save_jpeg_images(args, record, start, channel):
    f = open("command", "w")

    input = ("""pschart -a "" -c "" -C -E -G -CG 1 .5 .5 -Cs 0 0 0 -H -l -r -P 300x150 -m 20 20 5 5 -M -n 0 \
    -s '%d' \
    -S 4 2 -t 25 -T "" -v 10 -w 0.5\
     script\
       >chart.ps
    sudo convert -density 400x400 chart.ps """ % channel \
             + '%s' + '.jpg') % (
                    (('{}/JPEG/').format(args.savedir) + record + '_' +str(start)))
    f.write(input)

    f.close()
    os.system('chmod 755 command')
    os.system('./command')


def header_info (path):
    header = pd.read_csv(path+'.hea', header=None, skiprows=[0]).iloc[:,0]
    header = header.apply(lambda x: pd.Series(str(x).split(" ")))
    if header.shape[1] > 9:
        header = header.iloc[:, : 9]

    header_columns = ['File', 'Storage format', 'Unit', 'Resolution', 'Offset', 'First Sample Value', 'Checksums', 'Block Field Size', 'Leads']
    header.columns = header_columns

    return header

def layout_info (path):
    header = pd.read_csv(path+'.hea', header=None, skiprows=[0]).iloc[:,0]
    header = header.apply(lambda x: pd.Series(str(x).split(" ")))
    if header.shape[1] > 9:
        header = header.iloc[:, : 9]
    header_columns = ['~', 'units', '~', '~', '~', '~', '~', '~','Leads']
    header.columns = header_columns

    return header
