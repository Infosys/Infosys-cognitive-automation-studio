'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# A sample micro bot for multinomial Naive bayes algorithm
from xgboost import XGBClassifier
from sklearn.externals import joblib
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle
# app = Flask(__name__)
# api = Api(app)

'''
Dataset - Tf-IDF vectorizer
alpha - Algorithm parameter
model_file_name - pkl file name to be saved
target - one hot encoded predicted field
'''
class XGBoostTraining(Bot):


    # @app.route('/api/xg_boost_training/<path:model_file_name>/<int:n_estimators>/<str: objective>', methods= ['POST'])
    # def xg_boost_training(model_file_name, n_estimators=1, objective='binary:logistic'):
    def execute(self, executeContext):
        try:
            n_estimators = executeContext['n_estimators']
            objective = executeContext['objective']
            input_data = executeContext['input_data'] 
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']

            #data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(input_data)
            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)

           
            # # --reading dataset from given file path--
            # json_file = open(dataset_fp, 'r')
            # dataset = json_file.read()
            # json_file = open(dataset_fp, 'r')
            # target = json_file.read()            
            # dataset = request.get_json('dataset')
            # target = request.get_json('target')

            xgb = XGBClassifier(n_estimators=int(n_estimators), objective=objective)
            clf = xgb.fit(X,target)
            #joblib.dump(clf,model_file_path/ model_file_name)
            return {'XGBoosttraining pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in LR ",str(e))
            return str(e)
        


# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = XGBoostTraining()

    # --input parameters--
    # context = {'input_data':'D:\\real_time_usecase_bot\\files\\clean.csv', 
    #             'pickle_file_path':'D:\\real_time_usecase_bot\\files\\tf_idf.pkl', 'model_file_path':'D:\\real_time_usecase_bot\\files',
    #             'model_file_name':'XGBoosttraining_model.pkl','in_field_list':'in_field', 'pred_field':'Assignment_group',
    #             'n_estimators':1, 'objective':'binary:logistic'}

    context = {'input_data':'', 
                'pickle_file_path':'', 'model_file_path':'',
                'model_file_name':'','in_field_list':'', 'pred_field':'',
                'n_estimators':'', 'objective':''}

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)
# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)