'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Load libraries
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets
# Import train_test_split function
from sklearn.model_selection import train_test_split
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.svm import SVC
from flask_cors import CORS   #Currently 'cross_origin' Not Using
from flask_restful import  Api 
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle


# app = Flask(__name__)
# api - Api(app)



# @app.route('/api/adaboost_training/<int:alpha_parameter>/<path:model_file_name>/<int:target>', methods=['POST'])
# def adaboost_training(alpha_parameter,model_file_name,target):
#     return adaboost.adaboost_training(alpha_parameter,model_file_name,target)

class AdaBoost(Bot):
    # '''
    # constructor
    # '''
    # def __init__(self):
    #     pass
    
    # def adaboost_training(n_estimators=50,model_file_name,target):
    def execute(self,executeContext):
        try:
            n_estimators = executeContext['n_estimators']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            input_data = executeContext['input_data']
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']
            #base_estimator = executeContext['base_estimator']
            learning_rate = executeContext['learning_rate']

            data = pd.read_csv(input_data,encoding='latin1')

            data =pd.DataFrame(data)
            #data =pd.DataFrame(input_data)

            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)
            # # --reading json from given file path--
            # json_file = open(file_path, 'r')
            # dataset = json_file.read()
            # # dataset = request.get_json()       

            # Split dataset into training set and test set
            X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=0.3) # 70% training and 30% test
            svc=SVC(probability=True, kernel='linear')
            # Create adaboost classifer object
            abc = AdaBoostClassifier(base_estimator=svc,n_estimators=int(n_estimators),learning_rate=int(learning_rate))
            # Train Adaboost Classifer
            model = abc.fit(X_train, y_train)
            
            #Predict the response for test dataset
            y_pred = model.predict(X_test)
            #joblib.dump(model, model_file_path/ model_file_name) 
            # Model Accuracy, how often is the classifier correct?
            return {'AdaBoost pickle':pickle.dump(model,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in MNB ",str(e)) 

    
# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = AdaBoost()

    # --input parameters--
    # context = {'input_data':'D:\\real_time_usecase_bot\\files\\clean.csv', 'n_estimators':50, 'model_file_name':'AdaBoost_model.pkl',
    #             'pickle_file_path':'D:\\real_time_usecase_bot\\files\\tf_idf.pkl', 'model_file_path':'D:\\real_time_usecase_bot\\files',
    #             'in_field_list':'in_field', 'pred_field':'Assignment_group','learning_rate':1}
    context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv', 'n_estimators':'50', 'model_file_name':'AdaBoost_model.pkl',
                'pickle_file_path':'D:\\Bot_Factory\\testedbots\\tf_idf.pkl', 'model_file_path':'D:\\Bot_Factory\\testedbots\\',
                'in_field_list':'in_field', 'pred_field':'Assignment_group','learning_rate':'1'}

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)