'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# A sample micro bot for multinomial Naive bayes algorithm
from sklearn.linear_model import LogisticRegression
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
# @app.route('/api/logistic_regression_training/<path:model_file_name>/<float: C>', methods= ['POST'])
class Logisticregression(Bot):


    # def logistic_regression_training(model_file_name, C=1.0):
    def execute(self, executeContext):
        try:
            C = executeContext['C']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            #dataset_fp = executeContext['dataset_file_path']
            input_data = executeContext['input_data']
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']

            input_data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(input_data)    

            #data =pd.DataFrame(input_data)
            print(data)
            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)

            print("beforepickle_load")
            tf_idf = pickle.load(open(pickle_file_path,'rb'))
            print('type of tf_idf is:',type(tf_idf))
            X = tf_idf.transform(list1)
            
            # --reading dataset from given file path--
            #json_file = open(dataset_file_path, 'r')
            #dataset = json_file.read()
            #json_file = open(target_file_path, 'r')
            #target = json_file.read()
            # dataset = request.get_json('dataset')
            # target = request.get_json('target')
        
            #lr = LogisticRegression()
            lr = LogisticRegression(C=float(C))
            print("afterLR")
            clf = lr.fit(X,target)
            #joblib.dump(clf,model_file_path/'LR_model.pkl')
            return {'tfidf_vectorizer': pickle.dump(clf,open(model_file_path / model_file_name,'wb'))}
            #return "success"
        except Exception as e:
            print("Error occured in LR ",str(e))
            return str(e)

# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = Logisticregression()

    # --input parameters--
    # context = {'input_data':'',
    #    'pickle_file_path':'', 
    #         'model_file_path':'', 'C':'','in_field_list':'', 'pred_field':'','model_file_name':""}

    context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv',
                'pickle_file_path':'D:\\Bot_Factory\\testedbots\\tf_idf.pkl', 
                'model_file_path':'D:\\Bot_Factory\\testedbots', 'C':'1.0','in_field_list':'in_field', 
                'pred_field':'Assignment_group','model_file_name':"LR_model.pkl"}


    resp = bot_obj.execute(context)
    #print('response : ',resp)