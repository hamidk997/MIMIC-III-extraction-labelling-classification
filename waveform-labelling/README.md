# Labelling interface
Our tailored Graphical User Interface enables rapid labelling of the extracted waveforms. 

This was developed using the python tkinter module, other dependencies are listed in the requirements.txt file

## Instructions for use

### Working directory
To use the GUI, we must provide the directory in which the image files are stored. This must be defined in the **path.py** file

We filter for files which have extensions in {'JPEG', 'BMP', 'PNG', 'GUI'} and load these in the next stage. 

### Labelling interface
With the path defined, running the **GUI.py** file loads the labelling interface. The screeshot below shows an example waveform being presented for labelling.

![Alt text](https://github.com/hamidk997/MIMIC-III-waveform-extraction/blob/master/GUI_demo.png?raw=true "Optional Title")
As the extracted waveforms images are all of the same dimensions, the window size does not need adjustment and we have smooth navigation experience.

#### Inputs
The user can select both a rhythm and noise classification for each image, default values are set to zero so any of these can be left blank.

We provide two ways of interacting with the interface:

**Mouse inputs:** By clicking on the radio buttons for classification and the arrow for navigation 

**Keyboard inputs:** By selecting the noise classification using the corresponding keyboard button and the rhythm classification using the following map:

| Rhythm | Labels              | Numeric Map |
|--------|---------------------|-------------|
| AF     |        q            |      0      |
| Sinus  |        w            |      1      |
| Other  |        e            |      2      |
| Sinus  |        r            |      3      |
| Discard|        t            |      4      |



#### Output

Open each navigation button press, the csv file - *'LABELS.csv'** is updated. This means that the labelling can stop at any stage and small subsets can be labelled in batches.

The submit button stops the interface and prints summary statistics of the labelling session to the terminal. 

The *'LABELS.csv'** os made up of 3 columns, as seen below.

The filename is of the format patient_id-recordfile-seconds_into_record, where recordfile is the record segment file from which the data was sourced and seconds_into_record is the number of seconds into this record from which we extracted data.



| Filename | Rhythm Classification (numeric)       |. Noise Classification
|----------|---------------------------------------|-----------------------
| filename1|        1            | 5
| filename2|        2            | 3
| filename3|        5            |  2
| filename4|        0            | 5
| filename5|        2            | 2
