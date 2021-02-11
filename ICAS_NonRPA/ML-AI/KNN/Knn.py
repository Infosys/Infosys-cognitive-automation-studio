'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from sklearn.neighbors import KNeighborsClassifier
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


# @app.route('/api/KNeighborsClassifier_training/<path:model_file_name>/<int:n_neighbors>', methods=['POST'])
class Knn(Bot):
    # def KNeighborsClassifier_training(model_file_name,n_neighbors=5):
    def bot_init(self):
        pass
		
    def execute(self, executeContext):
        try:
            n_neighbors = executeContext['n_neighbors']
            #dataset_file_path = executeContext['dataset_file_path'] 
            #target_file_path = executeContext['target_file_path']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            input_data = executeContext['input_data']
            input_fields = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            model_file_name = executeContext['model_file_name']

            data = pd.read_csv(input_data,encoding='latin1')
            data =pd.DataFrame(data)
            list1 = list(data[input_fields])
            y = data[pred_field]
            target = y.factorize()[0]
            print("target ", target)


            tf_idf = joblib.load(pickle_file_path)
            X = tf_idf.transform(list1)

            # # --reading dataset from given file path--
            # json_file = open(dataset_file_path, 'r')
            # dataset = json_file.read()
            # json_file = open(target_file_path, 'r')
            # target = json_file.read()
            # # dataset = request.get_json('dataset')
            # # target = request.get_json('target')

            knn=KNeighborsClassifier(n_neighbors=int(n_neighbors))
            clf = knn.fit(X,target)
            joblib.dump(clf,model_file_path/ model_file_name)
            return {'KNN pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in KNN ",str(e))
    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)

if __name__ == '__main__':
    context = {}
    bot_obj = Knn()

    # --input parameters--
    # context = {'input_data':'D:\\real_time_usecase_bot\\files\\clean.csv', 
    #             'pickle_file_path':'D:\\real_time_usecase_bot\\files\\tf_idf.pkl', 'model_file_path':'D:\\real_time_usecase_bot\\files',
    #             'model_file_name':'Knn_model.pkl','in_field_list':'in_field', 'pred_field':'Assignment_group', 'n_neighbors':5}
    context = {'input_data':'', 
                'pickle_file_path':'', 'model_file_path':'',
                'model_file_name':'','in_field_list':'', 'pred_field':'', 'n_neighbors':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)