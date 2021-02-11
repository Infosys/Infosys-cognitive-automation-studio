'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# A micro bot for K-Means clustering algorithm

from sklearn.cluster import KMeans
from sklearn.externals import joblib

from flask_cors import CORS
from flask import Flask, request
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle

# app = Flask(__name__)
# cors = CORS(app)

'''
Dataset - Tf-IDF vectorizer
n_clusters - Algorithm parameter(numerical non-decimal)
model_file_name - pkl file name to be saved
'''

# @app.route('/kmeans', methods=['GET', 'POST'])
class Kmeans(Bot):


    # def kmeans_clustering_training(dataset,n_clusters=7,model_file_name):
    def execute(self, executeContext):
        try:
            n_clusters = executeContext['n_clusters']
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
            # # dataset = request.form.get('dataset')

            # n_clusters = request.form.get('n_clusters')
            # model_file_name = request.form.get('model_file_name')
            
            modelkmeans = KMeans(n_clusters=int(n_clusters))
            clf = modelkmeans.fit(X)
            #joblib.dump(clf,model_file_path/ model_file_name)
            return {'KMeans pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in KMeans: ",str(e))
            return str(e)
        


# if __name__ == '__main__':
#     print("Started the application...")
#     app.run(debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = Kmeans()

    # --input parameters--
    # context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv', 
    #             'pickle_file_path':'D:\\Bot_Factory\\testedbots\\files\\tf_idf.pkl', 'model_file_path':'D:\\Bot_Factory\\testedbots\\files',
    #             'model_file_name':'Kmeans_model.pkl','in_field_list':'in_field', 'pred_field':'Assignment_group', 'n_clusters':7}
    context = {'input_data':'', 
                'pickle_file_path':'', 'model_file_path':'',
                'model_file_name':'','in_field_list':'', 'pred_field':'', 'n_clusters':''}

    resp = bot_obj.execute(context)
    #print('response : ',resp)