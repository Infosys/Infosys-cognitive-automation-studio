'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import pandas as pd
from flask import Flask ,request   #Currently 'make_response' Not Using
from flask_cors import CORS   #Currently 'cross_origin' Not Using
from flask_restful import  Api 
import re
from nltk.corpus import stopwords
from abstract_bot import Bot
from pathlib import Path
from sklearn.externals import joblib
import pickle
import json

stopWords = set(stopwords.words('english'))

# app = Flask(__name__)
# api = Api(app)

# @app.route('/api/Vectorizer/',methods=['POST'])
# def vectorizer_bot():
#     return VectorizerBot.vectorizer()

class TFIDFVectorizer(Bot):
# class VectorizerBot():
    '''
    constructor
    '''
    # def __init__(self):
    #     pass
    

    ##data -- cleaned dataset 
    ##input_fields - input fields
    ##pred_field - predicted feild
    # @staticmethod
    # def vectorizer():
    def execute(self, executeContext):
        try:
            #dataset_fp = executeContext['dataset_fp']
            input_data = executeContext['input_data']
            input_fields = executeContext['input_fields']
            pred_field = executeContext['pred_field']
            out_put = Path(executeContext['output_path'])
            output_file_name = executeContext['output_file_name']
            
            
            #data = pd.DataFrame(input_data)
            
            #comment the 2 lines below and uncomment the code above to make it work in worker bot scenario 
            data = pd.read_csv(input_data)
            data = pd.DataFrame(data)

            list1 = list(data[input_fields])
            y = list(data[pred_field])
            print('y is :',y)

            tfIdf_vec = TfidfVectorizer()
            print('type of tfIdf_vec',type(tfIdf_vec))
            tfidf_vectorizer= tfIdf_vec.fit_transform(list1)
            print('type of tfidf_vectorizer',type(tfidf_vectorizer))
            #print('tfidf_vectorizer is',tfidf_vectorizer)
            #tfidf_vectorizer1 = pickle.dump(tfidf_vectorizer).to_json()
            #joblib.dump(tfIdf_vec, out_put / output_file_name)
            #pickle.dump(tfidf_vectorizer,open(out_put / output_file_name,'wb'))

            return {'tfidf_vectorizer':pickle.dump(tfIdf_vec,open(out_put / output_file_name,'wb')),'y':json.dumps(y)}
        except Exception as e:
            print('Exception : ',str(e))
            return str(e)


# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = TFIDFVectorizer()

    #--input parameters--

    # context = {'input_data':'D:\\Bot_Factory\\testedbots\\clean.csv', 'input_fields':'in_field', 'pred_field':'Assignment_group',
    #            'output_path':"D:\\Bot_Factory\\testedbots\\",'output_file_name':'tf_idf.pkl'}

    context = {'input_data':'', 'input_fields':'', 'pred_field':'',
               'output_path':"",'output_file_name':''}

   
    bot_obj.bot_init()
    resp, target = bot_obj.execute(context)
    #print('response : ',resp)
    #print("target", target)

# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)
