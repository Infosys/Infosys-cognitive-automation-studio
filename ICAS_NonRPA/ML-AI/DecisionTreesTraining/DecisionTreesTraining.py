'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:37:33 2019

@author: raajesh.rameshbabu
"""

# A sample micro bot for Decision trees algorithm

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from nltk.corpus import stopwords
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle
# api = Api(app)

'''
Dataset - Tf-IDF vectorizer
alpha - Algorithm parameter
model_file_name - pkl file name to be saved
target - one hot encoded predicted field
'''
# @app.route('/api/decision_trees_training', methods= ['POST'])
class DecisionTreesTraining(Bot):


    # def decision_trees_training(dataset,model_file_name,target,criterion='entropy'):   
    def execute(self, executeContext):
        # criterion = 'entropy'
        try:
           
            criterion = executeContext['criterion']
            input_data = executeContext['input_data'] 
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']
            random_state = executeContext['random_state']
           
            data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(data)

            #Comment the Two above lines and uncomment the below line for adding it to a worker bot.
            #data =pd.DataFrame(input_data)
            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)

            # # --reading dataset from given file path--
            # json_file = open(file_path, 'r')
            # dataset = json_file.read()
            
            dta = DecisionTreeClassifier(criterion = criterion, random_state = int(random_state))
            clf = dta.fit(X,target)
            #joblib.dump(clf,model_file_path/ model_file_name)
            return {'Decision Tree Training pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in DTA ",str(e))
        return 'failure'
    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True) 

if __name__ == '__main__':
    context = {}
    bot_obj = DecisionTreesTraining()

    # --input parameters--
    
    # context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv', 
    #            'pickle_file_path':'D:\\Bot_Factory\\testedbots\\tf_idf.pkl', 'model_file_path':'D:\\Bot_Factory\\testedbots\\',
    #            'model_file_name':'D:\\Bot_Factory\\testedbots\\decisiontreemodel.pkl','in_field_list':'in_field', 'pred_field':'Assignment_group',
    #             'criterion':'entropy','random_state':'42'}

    context = {'input_data':'', 
               'pickle_file_path':'', 'model_file_path':'',
               'model_file_name':'','in_field_list':'', 'pred_field':'',
                'criterion':'','random_state':''}

    resp = bot_obj.execute(context)
    print('response : ',resp)

