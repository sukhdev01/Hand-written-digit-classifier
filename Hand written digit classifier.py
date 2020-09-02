# -*- coding: utf-8 -*-
"""Hand written digit classifier.ipynb

Automatically generated by Colaboratory.

Import libraries and  our Data Set.
"""

import keras
import numpy as np
import pandas as pd
import random
from keras.datasets import fashion_mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from sklearn.metrics import confusion_matrix
from keras.activations import relu,softmax

#loading data
(train_X,train_Y), (test_X,test_Y) = fashion_mnist.load_data()

"""Data Preprocessing"""

# reshape dataset to have a single channel with 28x28 pixel size [for using conv2D]
# -1 for total length of the data
# 28x28 is size of the Image and 1 is channel.
train_X = train_X.reshape(-1, 28,28, 1)
test_X = test_X.reshape(-1, 28,28, 1)

train_X.shape

#convert from integers to Floats
train_X = train_X.astype('float32')
test_X = test_X.astype('float32')

#Normalize to 0-1  [as color combination 0-255]
train_X = train_X / 255.0
test_X = test_X / 255.0

# model cannot work with categorical data Directly (0-9 digits)
# Use Hot encoding to transfer this data into 0 & 1 using 10 digits (9 zeros,1 one)
train_Y_one_hot = to_categorical(train_Y)
test_Y_one_hot = to_categorical(test_Y)

"""Making Model using Keras Libraries"""

#Sequential groups a linear stack of layers
model = Sequential()

#to drop the unecessary data from the image matrix 
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))

# to pick the maximum element from the part of image pixel
model.add(MaxPooling2D((2, 2)))

#Flattern is used to convert it into 1D array for next layer Processing
model.add(Flatten())

# hidden fully connected layer (i.e.Dense) with 100 nodes and relu activation function
model.add(Dense(100, activation='relu'))

# to drop out data to remove overfitting
model.add(Dropout(0.3))

#final output fully connected layer (i.e. Dense) with 10 nides and Softmax activation function
model.add(Dense(10, activation='softmax'))

# compile model by adding to optimizer  with adam opt and loss function
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#fitting the data into model with 5 epochs 
model.fit(x= train_X , y = train_Y , epochs= 5)

"""Testing on few data"""

#slicing few data from 
test_xx = test_X[:30]
test_yy = test_Y[:30]

#prediction of classes on sample data by our model
predicted=model.predict_classes(test_xx,verbose=0)
print("predictoin and actual values for checking, is the model correct ?")
print("predicted:\t", predicted) #predicted values
print("Actual :\t",test_yy)    #Actual VAlues

"""computing TN, TP, FN, FP for confusion calculation 

Calculating Precision, Recall, F1 score, Sensitivity, Specificity and Accuracy.
"""

# predict probabilities for test set
yhat_probs = model.predict(test_X, verbose=0)

# predict crisp classes for test set
yhat_classes = model.predict_classes(test_X, verbose=0)

#forming confusion matrix formation for True (test_Y) and Predicted
conf_matrix=confusion_matrix(test_Y, yhat_classes)

#count for actual value true and prediction is true
TP = np.diag(conf_matrix)


#count for actual value false but prediction is true
FP = conf_matrix.sum(axis=0) - np.diag(conf_matrix)

#count for actual value true but prediction is false
FN = conf_matrix.sum(axis=1) - np.diag(conf_matrix)

#count for actual value false and prediction is false
TN = conf_matrix.sum() - (FP + FN + TP)
  
print("TP:",TP)
print("TN:",TN)
print("FP:",FP)
print("FN:",FN)

# Precision or positive predictive value
precision = TP/(TP+FP)

# Sensitivity, recall, hit rate or true positive rate
recall = sensitivity= TP/(TP+FN)

# Specificity or true negative rate
specificity = TN/(TN+FP) 

#f1_score 
F1_scores = 2 * ( (precision * recall) / (precision + recall) )

# Overall accuracy
acc= (TP+TN)/(TP+FP+FN+TN)

# to print in Matrix format making list of columns 
columns =[precision,specificity,F1_scores,acc,recall]

df=pd.DataFrame()

i=0 #adding column into data frame to print
for col in columns:
  df[i]=col
  i+=1

#printing dataFrame
df.columns=['precision','specificity','F1_scores','accuracy','recall=sensitivity']
df
