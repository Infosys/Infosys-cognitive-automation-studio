'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abc import ABC, abstractmethod 
import pysnow

import pymongo
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import time
import configparser
import pandas as pd
from pathlib import Path
from sklearn.externals import joblib
import re
import spacy
import psycopg2
from config import Config
import io
import pickle
import json
from abstract_bot import Bot

class Predict(Bot):
    conn = None
    # rt_tickets_tbl = None
    users_tbl = None
    whitelisted_word_tbl = None
    assign_enable_tbl = None
    customer_tbl = None
    datasets_tbl = None
    # predicted_tickets_tbl = None
    teams_tbl = None
    itsm_details_tbl = None
    training_tickets_tbl = None
    configuration_values_tbl = None
    mapping_tbl = None
    rt_tickets_BotFactory_tbl = None
    predicted_tickets_BotFactory_tbl = None

    def bot_init(self):
        client = MongoClient('127.0.0.1',27017)
        db = client['INTENT']

        # self.conn = psycopg2.connect(dbname='bindb', user='postgres', password='infy@1234')

        # self.rt_tickets_tbl = db.TblIncidentRT
        self.users_tbl = db.TblUsers
        self.whitelisted_word_tbl = db.TblWhitelistedWordDetails
        self.assign_enable_tbl = db.TblAssignmentEnableStatus
        self.customer_tbl = db.TblCustomer
        self.datasets_tbl = db.TblDataset
        # self.predicted_tickets_tbl = db.TblPredictedData
        self.teams_tbl = db.TblTeam
        self.itsm_details_tbl = db.TblITSMDetails
        self.training_tickets_tbl = db.TblTraining
        self.configuration_values_tbl = db.TblConfigurationValues
        self.mapping_tbl = db.TblITSMFieldMapping
        self.rt_tickets_BotFactory_tbl = db.TblRTTicketsBotFactory
        self.predicted_tickets_BotFactory_tbl = db.TblPredTicketsBotFactory


    
    def get_mapping_details(self, customer_id):
        itsm_details = self.itsm_details_tbl.find_one({}, {"_id":0, "ITSMToolName":1})
        itsm_tool_name = itsm_details['ITSMToolName']
        field_mapping = self.mapping_tbl.find_one({"CustomerID":customer_id, "Source_ITSM_Name": itsm_tool_name}, {"_id":0})
        return field_mapping


    def cleaningInputFields(self, df, in_field):
        # print("Inside line break method")
        for index, row in df.iterrows():
            row[in_field] = re.sub(r'\n', " ", row[in_field])
            row[in_field] = re.sub("[^_a-zA-Z]", " ", row[in_field])
            df[in_field][index] = row[in_field].lower()
        return df
    
    def execute(self, executionContext):
        try:
            conf_score = []
            pred_field_confidance = {}
            input_data = executionContext['input_data']
            cust_name = executionContext['cust_name']
            dataset_name = executionContext['dataset_name']
            pred_field = executionContext['pred_field']
            algoName = executionContext['algorithm_name']
            #description = executionContext['description']
            result=[]

            model_file_path = executionContext['model_file_path']
            vocab_file_path = executionContext['vocab_file_path']
            
            print('type of input data is ',type(input_data))
            input_df = pd.DataFrame({'description':input_data})
            #input_df['description'] = input_data
            #input_df = pd.DataFrame([{'description':input_data}])
            # final_predictions[input_field_list[0]] = ticket[input_field_list[0]]
            # for input_field_ in input_field_list[1:]:
            #     final_predictions[input_field_] = ticket[input_field_]
            #     input_df[input_field_] = pd.DataFrame([{input_field_:ticket[input_field_]}])
            input_df['in_field'] = ''
            # for field in input_field_list:
            #     if(input_df[field] is None):
            #         input_df[field] = ""
            input_df['in_field'] += input_df['description'] + ' --~||~-- '
            input_df1 = pd.DataFrame()
            input_df1['in_field'] = input_df['in_field']
            
            # logging.info(input_df1.iloc[0]['in_field'])
            in_field = 'in_field'
            input_df1 = input_df1[pd.notnull(input_df1[in_field])]
            print('input df1',input_df1)
            
            training_tkt_df = self.cleaningInputFields(input_df1,in_field)

            input_df_list = input_df1['in_field'].tolist()
            descr_df = [str(x) for x in input_df_list]
            found_white_lst_wrd=False
            input_descr=descr_df[0]

            pred_output_result = []
            
            #vocab_path = vocab_file_path + '/' + cust_name + "__" + dataset_name + '__' + "in_field" + "__" + pred_field + "__" + "Approved" + "__" +"Vocabulary.pkl"
            #model_path = model_file_path + '/' + cust_name + "__" + dataset_name + '__' + algoName + "__" + pred_field + "__" + "Approved" + "__" +"Model.pkl"
            vocab_path = vocab_file_path
            model_path = model_file_path
            vocab_file = Path(vocab_path)
            model_file = Path(model_path)
            
            # vocab_binary = self.get_pkl_file(vocab_name)
            # model_binary = self.get_pkl_file(model_name)
            
            if vocab_file != None:
                tfidf = pickle.load(open(vocab_file,'rb'))
            else:
                print("Vocabulary file not found for pred_field.. please train algo, save the choices & try again.")
                # continue

            if model_file != None:
                fittedModel = pickle.load(open(model_file,'rb'))
            else:
                print("ML Model file not found for pred_field field.. please train algo, save the choices & try again.")
                # continue
            
            #print('descr_df is',tfidf.transform(descr_df))
            pred_output_result = fittedModel.predict(tfidf.transform(descr_df).toarray()).tolist()
            #pred_output_result = fittedModel.predict(descr_df.toarray())
            print('pred_output_result is',pred_output_result)

            # id_to_labels = self.datasets_tbl.find_one({'CustomerID':customer_id, "DatasetID": dataset_id},{"_id":0,"IdToLabels":1})
            # if(id_to_labels):
            #     id_to_labels_dict = id_to_labels["IdToLabels"]
            #     inside_id_to_label = id_to_labels_dict[str(pred_field)]
            # else:
                # logging.info('%s: De-map data not found for %s field.'%(RestService.timestamp(),pred_field))
            inside_id_to_label = {         
                "0" : "Commercial",
                "1" : "Corporate",
                "2" : "Digital"
                        
            }
        
            
            print('type is pred_output_result',type(pred_output_result))
            #predicted_label = inside_id_to_label[str(pred_output_result)]
            if(len(pred_output_result)>1):
                pred_val =[]
                for val in pred_output_result:
                    predicted_label = inside_id_to_label[str(val)]
                    #print('this is predicted label',predicted_label)
                    pred_val.append(predicted_label)
                    #print('pred field outside loop',predicted_label)
                    pred_field_confidance[pred_field] = predicted_label
                    pred_field_confidance['prediction_by'] = 'algorithm'
                    confidence_score = float("{0:.2f}".format(max(fittedModel.predict_proba(tfidf.transform(descr_df).toarray())[0])))
                    pred_field_confidance['ConfidenceScore'] = confidence_score  
                    #print('pred_field_confidance',pred_field_confidance)    
                    #for key,val in pred_field_confidance.items():
                    #    conf_score.append({key,':',val})
                    #    conf_score.append(val['prediction_by'])  
                    #    conf_score.append(val['ConfidenceScore'])         
                    conf_score.append(pred_field_confidance.copy())
                    # #print('type of conf',type(pred_field_confidance))
                    #print('conf_score is',conf_score)
                for i in conf_score:
                    print(i["Assignment group"])
                    result.append(i["Assignment group"])        
            return{"Result": json.dumps(result)}
            
            #return {"Result":"success"}
        except Exception as e:
            print("Error occured in Predict ",str(e))


if __name__ == '__main__':
    bot_obj = Predict()
    # read data from json
    context = {}
    # file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")


    # context = {'cust_name':'AMD', 
    # 'dataset_name':'App Team', 
    # 'pred_field':'Assignment group' ,
    # 'input_data':['User unable to to enter time into monday','User getting blank white screen when attempting to access mdm.hersheys.com','Sales Force Database Extract'],
    # 'algorithm_name':'LogisticRegression', 
    # 'vocab_file_path':"D:\\Bot_Factory\\testedbots\\tf_idf.pkl", 
    # 'model_file_path':"D:\\Bot_Factory\\testedbots\\Randomforeset_model.pkl"}
     
    context = {'cust_name':'', 
    'dataset_name':'', 
    'pred_field':'' ,
    'input_data':'',
    'algorithm_name':'', 
    'vocab_file_path':"", 
    'model_file_path':""}


    bot_obj.bot_init()
    response = bot_obj.execute(context)

    print(response)
