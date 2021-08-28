# -*- coding: utf-8 -*-

from google.colab import drive
drive.mount('/content/drive')

!unzip -uq "/content/drive/My Drive/malaria.zip" -d "/content/drive/My Drive/disease"

#import shutil
#shutil.rmtree('/content/drive/My Drive/disease/malaria', ignore_errors=True)

import numpy as np 
import pandas as pd
import tensorflow as tf
import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
print(os.listdir("/content/drive/My Drive/disease/malaria"))

data=[]
labels=[]
Parasitized=os.listdir("/content/drive/My Drive/disease/malaria/Parasitized/")
for a in Parasitized:
    try:
        image=cv2.imread("/content/drive/My Drive/disease/malaria/Parasitized/"+a)
        image_from_array = Image.fromarray(image, 'RGB')
        size_image = image_from_array.resize((30, 30))
        data.append(np.array(size_image))
        labels.append(1)
    except AttributeError:
        print("")

Uninfected=os.listdir("/content/drive/My Drive/disease/malaria/Uninfected/")
for b in Uninfected:
    try:
        image=cv2.imread("/content/drive/My Drive/disease/malaria/Uninfected/"+b)
        image_from_array = Image.fromarray(image, 'RGB')
        size_image = image_from_array.resize((30, 30))
        data.append(np.array(size_image))
        labels.append(0)
    except AttributeError:
        print("")

Cells=np.array(data)
labels=np.array(labels)

s=np.arange(Cells.shape[0])
np.random.shuffle(s)
Cells=Cells[s]
labels=labels[s]

num_classes=len(np.unique(labels))
len_data=len(Cells)

(x_train,x_test)=Cells[(int)(0.1*len_data):],Cells[:(int)(0.1*len_data)]
x_train = x_train.astype('float32')/255 # As we are working on image data we are normalizing data by divinding 255.
x_test = x_test.astype('float32')/255

x_train.shape

(y_train,y_test)=labels[(int)(0.1*len_data):],labels[:(int)(0.1*len_data)]

def model_builder(hp):
  model = keras.Sequential()
  
  filters = hp.Int('filters', min_value = 32, max_value = 128, step = 16)
  kernel_size=hp.Choice('kernel_size', values=[3,5])
  model.add(keras.layers.Conv2D(filters,kernel_size, activation = 'relu', input_shape=(30, 30,3)))
  model.add(keras.layers.Conv2D(filters, kernel_size, activation = 'relu'))
  model.add(keras.layers.Flatten())
  model.add(keras.layers.Dense(units=hp.Int('unit', min_value = 32, max_value = 128, step = 16), activation='relu'))
  model.add(keras.layers.Dense(1, activation='sigmoid'))
  hp_learning_rate = hp.Choice('learning_rate', values = [1e-2, 1e-3, 1e-4]) 
  
  model.compile(optimizer = keras.optimizers.Adam(learning_rate = hp_learning_rate),
                loss='binary_crossentropy', 
                metrics = ['accuracy'])
  
  return model

!pip install keras.tuner

from tensorflow import keras
from kerastuner import RandomSearch
tuner_search=RandomSearch(model_builder,
                     objective = 'val_accuracy', 
                     max_trials = 5,
                     directory = 'malaria_output',
                     project_name = 'Malaria_Detection')

tuner_search.search(x_train, y_train, epochs=3, validation_split=0.1)

model=tuner_search.get_best_models(num_models=1)[0]
model.summary()

from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)

model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=50, initial_epoch=3, callbacks=[early_stop])

model.save('malariadisease.h5')
