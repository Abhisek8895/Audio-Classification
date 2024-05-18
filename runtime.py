import tensorflow as tf
import os
import librosa
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from pydub import AudioSegment
import IPython.display as ipd
import sys
import subprocess
# Reconfigure the standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')


# Load the model
model = load_model('audio_classification.keras')


y = ['dog_bark', 'children_playing', 'car_horn', 'air_conditioner',
       'street_music', 'gun_shot', 'siren', 'engine_idling', 'jackhammer',
       'drilling']


# Label Encoder
labelencoder=LabelEncoder()
y=to_categorical(labelencoder.fit_transform(y))


def converter_mp3(filename):
    src = filename
    dst = "audios/sample.wav"

    sound = AudioSegment.from_mp3(src)
    sound.export(dst,format="wav")
    return dst

def converter_ogg(filename):
    src = filename
    dst = "audios/sample.wav"
    try:
        subprocess.run(['ffmpeg', '-i', src, dst])
    except Exception as e:
        print("The error is",e)
    # print("ogg converted")
    return dst

def predictData(filename):
    # print(filename)
    
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast') 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    # print(mfccs_scaled_features)
    mfccs_scaled_features=mfccs_scaled_features.reshape(1,-1)
    predicted_label=model.predict(mfccs_scaled_features)
    # Get the index of the maximum value (class with highest probability)
    predicted_index = np.argmax(predicted_label, axis=-1)
    # Use this index with inverse_transform
    prediction_class = labelencoder.inverse_transform(predicted_index) 
    return prediction_class


def main_function(audio_file):
    file=""
    filename=temp_file=audio_file

    basename, extension = os.path.splitext(temp_file)
    if(extension == ".mp3"):
        file=converter_mp3(filename)    
    # print(file)
        result = predictData(file)
    # print(result[0])
        return result[0]
    elif(extension == ".ogg"):
        file=converter_ogg(filename)    
    # print(file)
        result = predictData(file)
    # print(result[0])
        return result[0]
    else:
        result = predictData(filename)
        return result[0]