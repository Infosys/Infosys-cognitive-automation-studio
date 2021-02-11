'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#MicroBot for ANN Classifier
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

#from sklearn.externals import joblib
import joblib 
from keras import Sequential
from keras.layers import Dense

from sklearn.metrics import confusion_matrix
import pickle 
from abstract_bot import Bot
from keras.models import model_from_json

class ANN(Bot):
    
    def execute(self,executeContext):
        try:
            dataset_file_path = executeContext['dataset_file_path']
            model_file_name = executeContext['model_file_name']
            model_file_path = executeContext['model_file_path']
            batch_size = executeContext['batch_size']
            nb_epoch = executeContext['nb_epoch']

            # Read the dataset
            dataset = pd.read_csv(dataset_file_path)

            # dataset.head(2)
            # dataset.describe(include='all')
            # sns.pairplot(dataset, hue='Class')

            # creating input features and target variables
            X= dataset.iloc[:,0:8]
            y= dataset.iloc[:,8]

            #standardizing the input feature
            sc = StandardScaler()
            X = sc.fit_transform(X)
            
            # Creating training dataset and test dataset
            #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

            model = Sequential()
            #First Hidden Layer
            model.add(Dense(4, activation='relu', kernel_initializer='random_normal', input_dim=8))
            #Second  Hidden Layer
            model.add(Dense(4, activation='relu', kernel_initializer='random_normal'))
            #Output Layer
            model.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))

            #Compiling the neural network
            model.compile(optimizer ='adam',loss='binary_crossentropy', metrics =['accuracy'])

            #Fitting the data to the training dataset
            # model_file = model.fit(X_train,y_train, batch_size=batch_size, epochs=nb_epoch)
            model_file = model.fit(X, y, epochs=nb_epoch, batch_size=10, verbose=0)
            #Evaluate the Model
            scores = model.evaluate(X,y, verbose=0)
            print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))    

            # serialize model to JSON
            model_json = model.to_json()
            with open("model.json", "w") as json_file:
                json_file.write(model_json)
            # serialize weights to HDF5
            model.save_weights(model_file_path + '\\'+ model_file_name + ".h5")
            print("Saved model to disk")

            json_file = open('model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(model_file_path + '\\'+ model_file_name + ".h5")
            print("Loaded model from disk")
            
            # evaluate loaded model on test data
            loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
            score = loaded_model.evaluate(X, y, verbose=0)
            print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


           
            return {"status":"success"}
        except Exception as e:
            print(str(e))
            return {"status":'failure'}
        

# --for testing--
if __name__ == '__main__': 
    context = {}
    bot_obj = ANN()

    # --input parameters--
    # context = {'dataset_file_path':'D:\\Bot_Factory\\testedbots\\pima_indian_data.csv', 
    # 'model_file_name':'ANN_model_file',  
    # 'model_file_path':'D:\\Bot_Factory\\testedbots', 
    # 'batch_size':10, 'nb_epoch':100}

    context = {'dataset_file_path':'', 
    'model_file_name':'',  
    'model_file_path':'', 
    'batch_size':'', 'nb_epoch':''}
    
    # bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)