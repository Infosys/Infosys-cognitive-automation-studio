'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from sklearn.naive_bayes import MultinomialNB
import joblib
from flask import Flask    #Currently 'make_response' Not Using
from flask_cors import CORS   #Currently 'cross_origin' Not Using
from flask_restful import  Api 
from flask_restful import request
from abstract_bot import Bot
from pathlib import Path
import pandas as pd
import pickle


# app = Flask(__name__)
# api = Api(app)


# @app.route('/api/Vectorizer/<path:model_file_name>/<float: alpha_parameter>', methods=['POST'])
# def multinomial_nb_bot(data,input_fields,pred_field):
#     return MultiNomialNaiveBayesBot.multinomial_nb_training(model_file_name, alpha_parameter)

class MultiNomialNB(Bot):
    
    # '''
    # constructor
    # '''
    def bot_init(self):
        pass
    
    '''
    Dataset - Tf-IDF vectorizer
    alpha - Algorithm parameter
    model_file_name - pkl file name to be saved
    target - one hot encoded predicted field
    '''
    # @staticmethod
    # def multinomial_nb_training(model_file_name, alpha_parameter=1.0):
    def execute(self, executeContext):
        try:
            
            alpha_parameter = executeContext['alpha_parameter']
            input_data = executeContext['input_data'] 
            #target_file_path = executeContext['target_file_path']
            model_file_path = Path(executeContext['model_file_path'])
            pickle_file_path = executeContext['pickle_file_path'] 
            #dataset_fp = executeContext['dataset_file_path']
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
           

            mnb = MultinomialNB(alpha=float(alpha_parameter))
            clf = mnb.fit(X,target)
            #joblib.dump(clf,model_file_path/ model_file_name)
            return {'KMeans pickle':pickle.dump(clf,open(model_file_path/ model_file_name,'wb'))}
        except Exception as e:
            print("Error occured in MNB ",str(e)) 

# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = MultiNomialNB()

    # --input parameters--
    # context = {'input_data':'D:\\real_time_usecase_bot\\files\\clean.csv', 
    #             'pickle_file_path':'D:\\real_time_usecase_bot\\files\\tf_idf.pkl', 'model_file_path':'D:\\real_time_usecase_bot\\files',
    #             'model_file_name':'MultinomialNB_model.pkl','in_field_list':'in_field', 'pred_field':'Assignment_group', 'alpha_parameter':1.0}
    context = {'input_data':'', 
                'pickle_file_path':'', 'model_file_path':'',
                'model_file_name':'','in_field_list':'', 'pred_field':'', 'alpha_parameter':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)