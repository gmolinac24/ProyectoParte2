# -*- coding: utf-8 -*-
"""RedesNeuronales2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fjEnxvyAZHnPfzzjVP_M7eGGYOYqetVi
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from google.colab import files

# Subir archivos .sav
uploaded = files.upload()

!pip install pyreadstat
import pyreadstat

# Cargar archivos .sav
a_2018, meta1 = pyreadstat.read_sav("2018.sav")
a_2019, meta2 = pyreadstat.read_sav("2019.sav")
a_2020, meta3 = pyreadstat.read_sav("2020.sav")
a_2021, meta4 = pyreadstat.read_sav("2021.sav")
a_2022, meta4 = pyreadstat.read_sav("2022.sav")

# Visualizar los primeros registros
print(a_2018.head())

# Concatenar filas
d_total = pd.concat([a_2018,a_2019,a_2020,a_2021, a_2022], ignore_index=True)

# Verificar resultado
print(d_total.head())

#Convirtiendo CAUFIN a factor
d_total['Cat_caufin'] = d_total['CAUFIN'].astype('category')
# Convert 'Cat_caufin' to numerical using one-hot encoding
d_total = pd.get_dummies(d_total, columns=['Cat_caufin'])
print(d_total)

import pandas as pd
# Ver el número de filas
print("Número de filas:", len(d_total))

# Ver el número de columnas
print("Número de columnas:", len(d_total.columns))

# Método alternativo que muestra ambos a la vez
print("Forma del dataset (filas, columnas):", d_total.shape)

#Aleatoriedad
d_total = d_total.sample(frac = 1, random_state = 42).reset_index(drop=True)

#Selección de la data
X = d_total[['SEXO','DIASESTANCIA','EDAD']]
y = d_total['PPERTENENCIA']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size = 0.2, random_state = 42)

X_train = X_train.replace(' ', np.nan).dropna().astype('float32')
y_train = y_train[X_train.index].astype('float32')

X_test = X_test.replace(' ', np.nan).dropna().astype('float32')
y_test = y_test[X_test.index].astype('float32')

#Densidad de las capas, relu: función de activación de la capa (cambia valores negativos a positivos), introduce no linealidades
#sigmoid salida que representa la probabilidad de pertenencia a una de las clases
model = Sequential()
model.add(Dense(8, input_dim = 3, activation = 'relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss ='binary_crossentropy', optimizer ='adam', metrics =['accuracy'])

#Entrenamiento
model.fit(X_train, y_train, epochs = 50, batch_size = 200, validation_data=(X_test, y_test))

loss, acc = model.evaluate(X_test, y_test)
print(acc*100)