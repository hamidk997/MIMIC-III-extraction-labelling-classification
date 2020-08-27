from tkinter import *
import json
from tkinter import filedialog
import os

def check():
    min_age = Minimum_Age.get()
    max_age = Maximum_Age.get()
    num_waveforms = int(Num_Waveforms.get())
    rhythm_class = rhythm_selection.get()
    ECG_lead = lead_selection.get()
    sex = sex_selection.get()
    data = {}
    data['min_age'] = min_age
    data['max_age'] = max_age
    data['sex'] = sex
    data['savedir'] = save_dir
    data['path'] = header_files_directory
    data['clinical_path'] = clinical_dir

    data['NumberWaveforms'] = num_waveforms
    data['rhythm_class'] = rhythm_class
    data['ECG_lead'] = ECG_lead
    writeToJSONFile(data)

    print(data)

window = Tk()
window.geometry('640x380')
window.title('Configurations')


#%% Labels


demographics_title = Label(window, text="Demographics:", font = "Helvetica 16 bold underline")
parameters_properties = Label(window, text="Waveform Parameters:", font = "Helvetica 16 bold underline")
set_paths = Label(window, text="Set Paths:", font = "Helvetica 16 bold underline")

min_age = Label(window, text="Age (lower bound):")
max_age = Label(window, text="Age (upper bound):")
sex = Label(window, text="Sex:")
ward = Label(window, text = 'Ward:')
rhythm = Label(window, text = 'Rhythm:')
num_waveforms = Label(window, text = 'Number of waveforms:')
lead = Label(window, text = 'ECG lead:')





#%% Inputs


""" Entry """
Num_Waveforms = Entry(window, width =12)

""" Sliders """
Minimum_Age = Scale(window, from_ = 0, to=120, orient = HORIZONTAL)
Maximum_Age = Scale(window, from_ = 0, to=120, orient = HORIZONTAL)

"""Drop-down menus"""
sex_options = ['M',
               'F',
               'All']
sex_selection = StringVar()
sex_selection.set('All')
sex_dropdown_menu = OptionMenu(window,sex_selection,*sex_options)
sex_dropdown_menu.config(width = 12)
sex_dropdown_menu.pack()

rhythm_options = ['AF',
               'SINUS',
               'OTHER']

rhythm_selection = StringVar()
rhythm_selection.set('AF')
rhythm_dropdown_menu = OptionMenu(window,rhythm_selection,*rhythm_options)
rhythm_dropdown_menu.config(width = 12)
rhythm_dropdown_menu.pack()

lead_options = ['I',
               'II',
               'III',
                'AVF']
lead_selection = StringVar()
lead_selection.set('I')
lead_dropdown_menu = OptionMenu(window,lead_selection,*lead_options)
lead_dropdown_menu.config(width = 12)
lead_dropdown_menu.pack()

ward_options= ['CCU',
               'MICU',
               'TSICU',
                'NCU']
ward_selection = StringVar()
ward_selection.set('MICU')
ward_dropdown_menu = OptionMenu(window,ward_selection,*ward_options)
ward_dropdown_menu.config(width = 12)
ward_dropdown_menu.pack()


def build_database():
    os.system('python3 build_database.py')

def get_header_dir():
    global header_files_directory
    header_files_directory = filedialog.askdirectory()
    print(header_files_directory)

def reform_pickle():
    print(rhythm_selection)
    print('Selecting new waveform pool')

def get_save_dir():
    global save_dir
    save_dir = filedialog.askdirectory()
    print(save_dir)

def get_clinical_dir():
    global clinical_dir
    clinical_dir = filedialog.askdirectory()
    print(clinical_dir)

SET = Button(window,text="Set Parameter Values", command = check, width = 24)
Randomise = Button(window,text="Re-randomise selections", command = reform_pickle)
RUN_BUILD = Button(window,text="Run build_database.py", command = build_database, width = 24)


PATH_TO_HEADER_FILES = Button(window,text="Select path to header files", command = get_header_dir, bg='blue', fg='white')

PATH_TO_SAVE_DIR = Button(window,text="Select path of save directory ", command = get_save_dir)

PATH_TO_CLINICAL_DIR = Button(window,text="Select path of clinical data", command = get_clinical_dir)


def writeToJSONFile(data):
    with open('config.json', 'w') as fp:
        json.dump(data, fp)


path = './'


# Labels
demographics_title.grid(row=0, column = 0,  sticky = 'W')
min_age.grid(row=2, column=0),
max_age.grid(row=3, column=0)
sex.grid(row=5, column=0)
ward.grid(row=6,column=0)

parameters_properties.grid(row=8, column =0, sticky = 'W')
rhythm.grid(row=9, column= 0)
num_waveforms.grid(row=11, column=0)
lead.grid(row=10, column=0)

Minimum_Age.grid(row=2, column=1)
Maximum_Age.grid(row=3, column=1)
PATH_TO_HEADER_FILES.grid(row=2, column=3, sticky ='W')
PATH_TO_SAVE_DIR.grid(row=4, column=3, sticky ='W')
PATH_TO_CLINICAL_DIR.grid(row=3, column=3, sticky ='W')

SET.grid(row=12, column=3)
RUN_BUILD.grid(row =13, column=3)
Randomise.grid(row=12, column=1)

Num_Waveforms.grid(row=11, column=1)

sex_dropdown_menu.grid(row=5, column=1)
ward_dropdown_menu.grid(row=6, column = 1)

rhythm_dropdown_menu.grid(row=9, column = 1)
lead_dropdown_menu.grid(row=10, column = 1)




window.grid_rowconfigure(7, minsize=30)  # Here
#window.grid_rowconfigure(12, minsize=80)  # Here

window.grid_columnconfigure(2,minsize=70)

mainloop()