# Background

We present a framework for selective extraction of waveforms according to nurse-labelled rhythm, electrocardiogram lead and demographic properties


## Data

The MIMIC-III clinical data requires for permission to be granted before it can be used. This [link](https://mimic.physionet.org) leads to their webpage where researchers can request access and complete the recognized course in protecting human research participants that includes Health Insurance Portability and Accountability Act (HIPAA) requirements. The researcher must then sign a data use agreement which outlines appropriate data usage and security standards, and forbids efforts to identify individual patients. (https://physionet.org/content/mimiciii/1.4/)


# Extraction pipeline

## Preliminary steps

To extract the waveform, we must first perform some preliminary steps to make the data more easier to work with.

### Splitting nurse chart data

The nurse recordings, necessary to perform the subsequent temporal matches comes in the form of a single, large csv file, over 30GB in size. To bypass download and further processing of this large file, we  query the cloud-based instance of the MIMIC-III database loaded onto Google BigQuery. Instructions on establishing access to this instance are provided on the following [link](https://mimic.physionet.org/tutorials/intro-to-mimic-iii-bq/). We only require the rows associated with the heart rhythm and therefore filter for the ITEMID codes associated with this.  The database was compiled over a long period, and the clinical information system used was replaced, therefore, in filtering for heart rhythms, we use both ITEMID codes 212 and 220048 (for CareVue and MetaVision respectively). This is implemented by the SQL query below which produces a significantly smaller file that contains just the information required.

``` sql
SELECT * FROM `physionet-data.mimiciii_clinical.chartevents`<br />
WHERE ITEMID = 212 OR ITEMID = 220048
```
To improve the speed of processing in subsequent steps, we split this file into patient specific csv| files, the split_by_patient.py python file provided in the repository runs the necessary code to build a directory comprised of per-patient csv files. 

The split_by_patient.py file takes two command line arguments:

``` console
split_by_patient.py --path_to_file_with_rhythm_rows --save_directory 
```
Where --path_to_file_with_rhythm_rows is the path to the csv file that is the output from running the SQL command above, and --save directory is the desired where the split csv files are to be saved.


### Downloading header files
The full waveform database is over 3TB, however most of the information we need in determining the useful segments are contained within the header files. We therefore need to download and process solely the header files in this preliminary stage. The information pertaining to the time, date and ECG leads used in the recordings are stored in the header files so it is necessary to download these in order to utilise this information. To excute this, we provide the download_header_files.py file which downloads all of the files with extension .hea from the server that hosts the The MIMIC-III Waveform Database Matched Subset. This is achieved using the rsync utility, using the command:

``` console
rsync -CaLvz -q --delete  --include='*.hea'    --include='*/' --exclude='*' --prune-empty-dirs 
``` 

The download_header_files.py takes a single command line argument: -- save_directory 

It outputs a nested set of directrories, with subdirectories for patient specific data. 

### Generate Patient Data table
To allow us to filter by patient demographics, we create this Patient Data table. Running the **create_patient_info.py** file in the misc folder generates a csv file with demographics for each hopsital admission. We chose to generate the demographics data for each hosptial rather than patient becauase there are instances where the same patient is admitted back to the ICU after many years. 

## Waveform extraction

We provide the interface shown below to extract waveforms.
![Alt text](https://github.com/hamidk997/MIMIC-III-waveform-extraction/blob/master/Waveform%20Extraction%20GUI.png?raw=true "Optional Title")


The sliders allow for the user to set the minimum and maximum age of patients from whom data are extracted. 
The dropdown menus allow for filters based on the sex of the patient and ward at admission.

Paths to the directories which store the data we generated in the preliminary sections can be set using the buttons which open the native file explorer, making it easier to identify the location and sparing the user from writing out the full path. We also require a save directory in which the generated csv and jpeg files will be stored.

Once these are set, the 'Set parameter values' commits these to a JSON file which can be accessed by main **build_database.py** script. 

This script can be executed by the GUI using the associated button.

Running this file generates two directories. A csv files folder which stores the raw data and a jpeg folder which stores the images. 
Corresponding files in these directories have the same filename but with different extension.

The filename is in the form:  patient - record_file - seconds_into_record

The seconds_into_record provides the location of the extracted period into the record which can be mapped into the date and time of recording. 

