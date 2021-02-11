'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#MicroBot for Catboost Classifier
from catboost import CatBoostRegressor
from sklearn.externals import joblib
from sklearn import tree
from flask_cors import CORS
from flask import Flask, request
import pandas as pd

from abstract_bot import Bot

# app = Flask(__name__)
# cors = CORS(app)

# @app.route('/api/CatBoostRegressor_training/<dataset>/<model_file_name>/<target>', methods=['POST'])
class CatBoost(Bot):  
    # def CatBoostRegressor_training(dataset,model_file_name,target,iterations=50,depth=3,learning_rate=0.1,loss_function='RMSE'):
    def execute(self,executeContext):
        try:
            dataset_file_path = executeContext['dataset_file_path']
            target = executeContext['target']
            model_file_name = executeContext['model_file_name']
            iterations = executeContext['iterations']
            depth = executeContext['depth']
            learning_rate = executeContext['learning_rate']
            loss_function = executeContext['loss_function']

            # --reading dataset from given file path--
            json_file = open(dataset_file_path, 'r')
            dataset = json_file.read()
            json_file = open(target, 'r')
            target = json_file.read()
            
            dataset= pd.read_json(dataset)
            target= pd.read_json(target)
#            Target_encoder= LabelEncoder()
#            Target_encoder.fit(target[0:])
#            target.y= Target_encoder.transform(target[0:])

            model=CatBoostRegressor(iterations=iterations,depth=depth,learning_rate=learning_rate,loss_function=loss_function)
            clf = model.fit(dataset,target)
            joblib.dump(clf,model_file_name + '.pkl')
            return {'status':"Success"}
        except Exception as e:
            print("Error occured in Catboost ",str(e))
            return {'Exception':str(e)}

    # if __name__ == '__main__':
    #     print("Started the application...")
    #     app.run(host = '0.0.0.0', port=5002, debug=True)

# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = CatBoost()

    # --input parameters--
    context = {'dataset_file_path':'', 'model_file_name':'', 'target':'', 'iterations':50, 'depth':3, 'learning_rate':'', 'loss_function':''}    
#    context = {'dataset_file_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\iris_catboost.json', 'model_file_name':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\CatBoost', 'target':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\iris_catboost_target.json', 'iterations':50, 'depth':3, 'learning_rate':0.1, 'loss_function':'RMSE'}    
    
#    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)