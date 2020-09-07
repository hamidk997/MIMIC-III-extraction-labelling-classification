# Classification

To demonstrate how this data may be used, we provide a simple CNN-based classifier built using keras. This is a very simple model which is sufficient for the purpose of this demo however we envisage that our pipeline would work effectively with very deep networks such as the one proposed in [Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network](https://www.nature.com/articles/s41591-018-0268-3) because we make it possible to label large volumes of waveforms in a manner that was not previously feasible using this database (which is the largest of its kind)


## Inputs
When the waveforms are labelled the **dataframe.csv** in which the labels are stored is saved in the **base directory** - the user defined directory in which the  **JPEG** and **CSV** subdirectories are created. As we will be using this file which includes the labels and the **CSV** directory, where the raw data for each waveform is saved, we must define the path to the **base directory**. This is to be entered in the parameters section at the top of the **train.py** file.


## Implementation
We produce a simple 8 stage Conv1D Sequential keras model which we use to train and test a classifier.

Firstly, waveforms which were labelled as "Discard" and those which were not labelled at all are removed.

For the remaining waveforms we read and extract the raw data, before storing them in an (mxn) array, where m is the number of waveforms and n is the number of samples (which is 3750 for our 30 second waveforms). The labels are also extracted from the **dataframe.csv** file are passed through a one-hot encoder which produces a (nx4) array where each row is a waveform and its associated label has the value **1**, with the others **0**.


The training/validation data is formed, using a stratified selection and validation size of 20% and these are used to compile the keras model.

The parameters are preset as seen in the file but it will necessary to change them depending on your database size.

