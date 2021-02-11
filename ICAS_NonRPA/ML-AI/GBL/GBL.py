'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#MicroBot for GBL Classifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib
from sklearn import tree
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from abstract_bot import Bot


# app = Flask(__name__)
# api = Api(app)

# @app.route('/api/GradientBoostingClassifier_training/<path:model_file_name>/<int:n_estimators>/<float:learning_rate><int:max_depth>/<int:random_state>', methods=['POST'])
class GBL(Bot):
    def bot_init(self):
        pass
    # def GradientBoostingClassifier_training(model_file_name,n_estimators=100,learning_rate=1.0,max_depth=1, random_state=0):
    def execute(self, executeContext):
        try:
            n_estimators = executeContext['n_estimators']
            learning_rate = executeContext['learning_rate']
            max_depth = executeContext['max_depth']
            random_state = executeContext['random_state']
            dataset_file_path = executeContext['dataset_file_path']
            target_file_path = executeContext['target_file_path']
            model_file_path = executeContext["model_file_path"]
            model_file_name = executeContext["model_file_name"]

            # --reading dataset from given file path--
            json_file = open(dataset_file_path, 'r')
            dataset = json_file.read()
            json_file = open(target_file_path, 'r')
            target = json_file.read()
            
            dataset= pd.read_json(dataset)
            target= pd.read_json(target)
            Target_encoder= LabelEncoder()
            Target_encoder.fit(target[0:])
            target.y= Target_encoder.transform(target[0:])
#            dataset = request.get_json('dataset')
#            target = request.get_json('target')           

            model= GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state)
            clf = model.fit(dataset,target[0:])           
            joblib.dump(clf,model_file_path +"\\"+ model_file_name +'.pkl')
            return {"status":"Success"}
        except Exception as e:
            print("Error occured in GBL ",str(e))
        return {"status":"Failure"}
    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)

if __name__ == '__main__':
    context = {'model_file_name':''}
    bot_obj = GBL()

    # --input parameters--
    #context = {'dataset_file_path':'D:\\Bot_Factory\\testedbots\\iris.json', 'target_file_path':'D:\\Bot_Factory\\testedbots\\iris_target.json', 'model_file_name':'GBL', 
    #"model_file_path":"D:\\Bot_Factory\\testedbots",'n_estimators':100, 'learning_rate':1.0, 'max_depth':1, 'random_state':0}

    context = {'dataset_file_path':'', 'target_file_path':'', 'model_file_name':'', 
    "model_file_path":"",'n_estimators':'', 'learning_rate':'', 'max_depth':'', 'random_state':''}

    resp = bot_obj.execute(context)
    print('response : ',resp)

