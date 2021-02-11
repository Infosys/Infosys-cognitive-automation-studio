'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#Default libraries
import re

#Other ibraries
import pandas as pd
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from nltk.corpus import stopwords
from abstract_bot import Bot
from pathlib import Path
import json

stopWords = set(stopwords.words('english'))



# app = Flask(__name__)
# api = Api(app)


# @app.route('/api/clean_data', methods= ['POST'])


    # def clean_data():
"""Cleaning a DataFrame & encoding the target field
    input:
            Json Data: {"csv_path": path where data to be cleaned is stored},
                        {"in_field_list": list of input fields},
                        {"pred_field": field to be predicted}
    output:
        clean dataframe with column in_field and category_id
"""
class PreProcessing(Bot):

    stopWords = None

    def bot_init(self):
        self.stopWords = set(stopwords.words('english'))
    
    def execute(self,executeContext):
        try:
            #file_path = executeContext['file_path']

            # input_data = request.get_json()
            input_data = executeContext['input_data']
            in_field_list = executeContext['in_field_list']
            pred_field = executeContext['pred_field']
            in_field = executeContext['in_field']
            out_put = Path(executeContext['output_path'])
            output_file_name = executeContext['output_file_name']
             
            #following two lines are for local testing without worker bot framework
            data = pd.read_csv(input_data,encoding='latin-1')
            data = pd.DataFrame(data)
            
            #uncomment the below line and comment the above two lines if you need to execute in worker bot framework.
            #data = pd.DataFrame(input_data)

            input_df = pd.DataFrame()
            input_df['in_field'] = data[in_field_list[0]]
            print('input_df',input_df['in_field'])
            if(len(in_field_list)>1):
                for field in in_field_list:
                    if(input_df[field] is None):
                        input_df[field] = ""
                    input_df['in_field'] += input_df[field] + ' --~||~-- '

            training_df = pd.DataFrame()
            training_df['in_field'] = input_df['in_field']
            training_df[pred_field] = data[pred_field]

            print('Number of columns before cleaning: %d.' % (training_df.shape[0]))
            training_df = training_df[(training_df['in_field']!="")]
            training_df = training_df[(training_df[pred_field]!="")]
            training_df = training_df.dropna(how='any', axis=0)  # IMP step
            print('Number of columns after cleaning: %d.' % (training_df.shape[0]))

            training_df['category_id'] = training_df[pred_field].factorize()[0]
            

            print("Inside line break method")
            for i, row in training_df.iterrows():
                row[in_field] = re.sub(r'\n', " ", row[in_field])
                row[in_field] = re.sub("[^_a-zA-Z]", " ", row[in_field])
                #-------------------
                row[in_field] = row[in_field].split()
                row[in_field] = [word for word in row[in_field] if not word in set(stopWords)]
                row[in_field] = " ".join(sorted(set(row[in_field]),key=row[in_field].index))
                #-------------------
                training_df[in_field][i] = row[in_field].lower()
            
            #training_df.to_csv(r'D:\Bot Factory\ML BOTS git\bot-factory\Outputfiles\cleaned_data.csv')
            training_df.to_csv(out_put / output_file_name)
            training_df.to_csv(out_put / output_file_name)
            training_df1 = training_df.to_json(orient='records')
            lst_pred_fields = list(training_df['Assignment_group'].unique())
            
            print('lst_pred_fields are:',lst_pred_fields)

            return {'training_df1':json.loads(training_df1),'lst_pred_fields':json.dumps(lst_pred_fields)}
            
        except Exception as e:
            print('Exception in python file : ',str(e))
            return str(e)
    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)

if __name__ == '__main__':
    context = {}
    bot_obj = PreProcessing()

    # --input parameters--
    # context = {'input_data':[{
    #                 'Number': 'INC0212875',
    #                 'Assigned to': 'Neha Purohit',
    #                 'Assignment_group': 'Commercial',
    #                 'Description': 'Sales Force Database Extract' },{'Number': 'INC0212876',
    #                 'Assigned to': 'Neha Purohit',
    #                 'Assignment_group': 'Commercial',
    #                 'Description': 'testing ' },{'Number': 'INC0212876',
    #                 'Assigned to': 'Neha Purohit',
    #                 'Assignment_group': 'Corporate',
    #                 'Description': 'testing ' }],
    #                 'in_field_list':['Description'], 'pred_field':'Assignment_group', 'in_field':'in_field',
    #                'output_path':"D:\\real_time_usecase_bot\\files",'output_file_name':'clean.csv'}

    # context = {'input_data':"D:\\Bot_Factory\\testedbots\\hershey_traindata.csv", 
    # 'in_field_list':['Description'], 'pred_field':'Assignment_group', 'in_field':'in_field',"output_path":"D:\\Bot_Factory\\testedbots","output_file_name":"clean.csv"}

    context = {'input_data':"", 
    'in_field_list':"", 'pred_field':'', 'in_field':'',
    "output_path":"","output_file_name":""}
        
    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)