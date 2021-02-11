'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#Microbot for dbscan algorithm
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from flask_cors import CORS
from flask import Flask, request
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle
'''
Dataset - Tf-IDF vectorizer
n_clusters - Algorithm parameter(numerical non-decimal)
model_file_name - pkl file name to be saved
'''
# app = Flask(__name__)
# api = Api(app)

# @app.route('/api/dbscan_training/',methods=['put','POST'])
# def dbscan_training(csv_path):
#     return dbscanTraining.dbscan_training(csv_path)

class DBScan(Bot):

    # @staticmethod
    # def dbscan_training(eps=0.5,min_samples=5,random_state=111):
    def execute(self, executeContext):
        try:
            eps = executeContext['eps']
            min_samples = executeContext['min_samples']
            #random_state1 = executeContext['random_state']
            #dataset_file_path = executeContext['dataset_file_path'] 
            #target_file_path = executeContext['target_file_path']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            input_data   = executeContext['input_data']
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']
           
            data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(data)
            
            #please comment the two lines above and uncomment below one line of code to make it work as a worker bot Flow
            #data =pd.DataFrame(input_data)

            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)

            dbscan = DBSCAN(eps=float(eps), min_samples=int(min_samples))
            clf = dbscan.fit(X)
            #joblib.dump(clf,model_file_path/ model_file_name)            
            return {'DBSCAN pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in DBSCAN",str(e))
            return 'failure'
        return 'success'

# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)

if __name__ == '__main__':
    context = {}
    bot_obj = DBScan()

    # --input parameters--
    # context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv',  'model_file_name':'dbscan_model.pkl',
    #             'pickle_file_path':'D:\\Bot_Factory\\testedbots\\tf_idf.pkl', 'model_file_path':'D:\\Bot_Factory\\testedbots\\',
    #              'eps':0.5, 'min_samples':5, 'in_field_list':'in_field', 'pred_field':'Assignment_group'}
    context = {'input_data':'',  'model_file_name':'',
                'pickle_file_path':'', 'model_file_path':'',
                 'eps':'', 'min_samples':'', 'in_field_list':'', 'pred_field':''}
    resp = bot_obj.execute(context)
    print('response : ',resp)
