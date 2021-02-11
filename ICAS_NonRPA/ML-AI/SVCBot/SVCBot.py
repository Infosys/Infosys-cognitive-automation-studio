'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# A sample micro bot for multinomial Naive bayes algorithm
from sklearn.svm import SVC
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
class SVCBot(Bot):

    # @app.route('/api/svc_training/<path:model_file_name>/<float: C>/<str:kernel>', methods= ['POST'])
    # def svc_training(model_file_name, C=1.0, kernel='rbf'):
    def execute(self, executeContext):
        try:
            model_file_name = executeContext['model_file_name'] 
            C=executeContext['C']
            kernel=executeContext['kernel']
            input_data = executeContext['input_data'] 
            #target_file_path = executeContext['target_file_path']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            #dataset_fp = executeContext['dataset_file_path']
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']

            data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(data)
            #data =pd.DataFrame(input_data)
            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)


            svc = SVC(C=float(C), kernel=kernel)
            clf = svc.fit(X,target)
            #joblib.dump(clf, model_file_path/ model_file_name)
            return {'SVC pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in LR ",str(e))
            return str(e)

# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = SVCBot()

    # --input parameters--
    context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv', 
                'pickle_file_path':'D:\\Bot_Factory\\testedbots\\tf_idf.pkl', 'model_file_path':'D:\\Bot_Factory\\testedbots\\',
                'model_file_name':'SVC.pkl', 'C':'1.0', 'kernel':'rbf','in_field_list':'in_field', 'pred_field':'Assignment_group'}

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)


# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True) 
