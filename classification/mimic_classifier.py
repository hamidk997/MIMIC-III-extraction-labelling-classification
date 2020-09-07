from keras.callbacks import ModelCheckpoint
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, LSTM, Conv1D, \
    GlobalAveragePooling1D, MaxPooling1D
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import os
from sklearn.model_selection import train_test_split

np.random.seed(97)
NUM_CLASSES = 4  # Total number of classes
INPUT_LENGTH = 3750
base_path = '/Volumes/Passport/MALE-0-49/'


def extract_waveform_and_rhythms(base_path):
    path_to_labels = os.path.join(base_path, 'dataframe.csv')

    df = pd.read_csv(path_to_labels)
    df = df[df.iloc[:,1] != 5] # Remove discard
    df = df[df.iloc[:,1] != 0] # Remove unlabelled

    waveforms = list(df.iloc[:,0])
    rhythm_labels = list(df.iloc[:,1])

    size = len(waveforms)
    print('Total training size is ', size)

    return waveforms, rhythm_labels


def create_data_array(waveforms):
    path_to_data = os.path.join(base_path, 'CSV')

    size = len(waveforms)
    X = np.zeros((size, INPUT_LENGTH))

    for i in range(len(waveforms)):
        data = pd.read_csv(os.path.join(path_to_data, waveforms[i]) + '.csv', skiprows=[0]).iloc[:,1].values
        X[i,:] = data

    # NORMALISING AND MEETING KERAS REQUIREMENT
    X = (X - X.mean()) / (X.std())
    X = np.expand_dims(X, axis=2)

    return X


def create_encoded_labels(rhythm_labels):

    values = np.array(rhythm_labels)
    label_encoder = LabelEncoder()
    one_hot_encoder = OneHotEncoder(sparse=False)
    rhythm_encoded_decimal = label_encoder.fit_transform(values)
    temp = rhythm_encoded_decimal.reshape(len(rhythm_encoded_decimal),1)
    y = one_hot_encoder.fit_transform(temp)

    return y


def create_model():
    model = Sequential()
    model.add(Conv1D(128, 55, activation='relu', input_shape=(INPUT_LENGTH, 1)))
    model.add(MaxPooling1D(10))
    model.add(Dropout(0.5))
    model.add(Conv1D(128, 25, activation='relu'))
    model.add(MaxPooling1D(5))
    model.add(Dropout(0.5))
    model.add(Conv1D(128, 10, activation='relu'))
    model.add(MaxPooling1D(5))
    model.add(Dropout(0.5))
    model.add(Conv1D(128, 5, activation='relu'))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(256, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(NUM_CLASSES, kernel_initializer='normal', activation='softmax'))
    return model


if __name__ == '__main__':
    waveforms, labels =  extract_waveform_and_rhythms(base_path)
    X = create_data_array(waveforms)
    y = create_encoded_labels(labels)

    train_size = 0.8  # Size of training set in percentage
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size= 1-train_size, stratify=y)

    model = create_model()
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    checkpointer = ModelCheckpoint('classifier_model.hdf5', monitor='val_acc', verbose=1, save_best_only=True)

    model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=100, epochs=20, verbose=1, shuffle=True,
                 callbacks=[checkpointer])

    predictions = model.predict(X_val)

    model.save_weights("model.h5")
    print("Saved model (weights only)")
