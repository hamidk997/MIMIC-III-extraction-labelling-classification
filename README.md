# Structure

This repository contains the three stages of our project to build an arrhythmia classifier using the MIMIC-III database. 
These are:
- Waveform Extraction
- Waveform Labelling
- Classification

The stages can be run in succession or independetly of each other.

Below we present a summary of the objectives for these stages. 

## Waveform Extraction
To generate the waveforms, we use the [MIMIC-III Waveform Database](https://physionet.org/content/mimic3wdb/1.0/) - this is a very large database of raw data from the bedside monitors, with no labels. Our implementation allows for selective extraction of the waveforms from this database, using the nurse charts to provide tenetative labels as well as filtering according to demographics and ward. 

## Waveform Labelling
The waveforms extracted above were generated with tentative nurse labels from the same period, however to build a more reliable datbase, it it necessary to inspect the waveforms individually to ascertain the dominant rhythm. Our GUI allows for rapid labelling to create a training set which can then be used to build a database-specific classifier

## Classification
We present three different algorithms for classification of arrhythmia, these can be used for other ECG databases but are designed such that the outputs of the previous stage are fed directly in. Modifications may be required if using other data. 

## Environment set up
 ```
git clone git@github.com:hamidk997/mimic-iii-waveform-extraction.git
```

If you don't have `virtualenv`, install it with

```
pip install virtualenv
```

Make and activate a new Python 3.7 environment

```
virtualenv -p python3.7 mimic_env
source mimic_env/bin/activate
```
Install requirements - different requirements for each of the subfolders, so run the command below inside each of the subdirectories you wish to use
```
pip install -r requirements.txt
```
### System dependencies
System dependencies are [wfdb] (https://archive.physionet.org/physiotools/wfdb.shtml) which can be installed by following the instructions on hyperlink.

ImageMagick and Ghostscript are also required to produced the ECG plots. These can be installed using [homebrew](https://brew.sh) a package manager. Once homebrew is set up, the following instructions are to be run on the command line to install these dependencies. 

```
brew install imagemagick
brew install ghostscript
```
### Data

The MIMIC-III clinical data requires for permission to be granted before it can be used. This [link](https://mimic.physionet.org) leads to their webpage where researchers can request access and complete the recognized course in protecting human research participants that includes Health Insurance Portability and Accountability Act (HIPAA) requirements. The researcher must then sign a data use agreement which outlines appropriate data usage and security standards, and forbids efforts to identify individual patients. (https://physionet.org/content/mimiciii/1.4/)


