'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# A sample micro bot for LightGB
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from abstract_bot import Bot

# app = Flask(__name__)
# api = Api(app)

'''
Dataset - Tf-IDF vectorizer
alpha - Algorithm parameter
model_file_name - pkl file name to be saved
target - one hot encoded predicted field
X_test,y_test - from the train test split data
That is 'X_train, X_test, y_train, y_test = train_test_split(x_train, y, test_size = 0.2, random_state = 0)'
# '''
# @app.route('/api/LGB_training/<path:model_file_name>/<int:num_leaves>/<int:num_trees>/<str:objective>/<int:num_class>', methods=['POST'])
class LightGBM(Bot):


    # def LGB_training(model_file_name, num_leaves=31, num_trees=100, objective='multiclass',num_class=50}):
    def execute(self, executeContext) :
        try:
            num_leaves=executeContext['num_leaves']
            num_trees=executeContext['num_trees']
            objective=executeContext['objective']
            num_class=executeContext['num_class']
            model_file_name = executeContext['model_file_name']
            dataset_file_path = executeContext['dataset_file_path']
            target_file_path = executeContext['target_file_path']

            # --reading dataset from given file path--
            json_file = open(datset_file_path, 'r')
            dataset = json_file.read()
            json_file = open(target_file_path, 'r')
            target = json_file.read()

            # dataset = request.get_json('dataset')
            # target = request.get_json('target')

            params = {'num_leaves':num_leaves, 'num_trees':num_trees, 'objective':objective,'num_class': num_class}
            X_train, X_test, y_train, y_test = train_test_split(dataset,target,test_size = 0.2, random_state = 0)
            lgb_train = lgb.Dataset(X_train, y_train)
            lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)
            gbm = lgb.train(params,lgb_train,valid_sets=lgb_eval)
            joblib.dump(gbm,'models/'+ model_file_name)
            return "success"
        except Exception as e:
            print("Error occured in LGB ",str(e)) 
            return str(e)

    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = LightGBM()

    # --input parameters--
    context = {
        'dataset_file_path':'', 'target_file_path':'', 'model_file_name':'', 
        'num_leaves':31, 'num_trees':100, 'objective':'multiclass','num_class':50
        }

    resp = bot_obj.execute(context)
    print('response : ',resp)