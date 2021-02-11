'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abc import ABC, abstractmethod 
import pysnow

import pymongo
from pymongo import MongoClient
import csv
import io
import pandas as pd
import json
from abstract_bot import Bot

class UploadResourceDetails(Bot):

    
    resourceDetails_tbl = None
    # datasets_tbl = None
    # teams_tbl = None

    def bot_init(self):
        print('Initializing things...')
        client = MongoClient('127.0.0.1',27017)
        db = client['INTENT']

        self.resourceDetails_tbl = db.TblResource
        # self.datasets_tbl = db.TblDataset
        # self.teams_tbl = db.TblTeams
    
    def execute(self,executionContext):
        new_dataset_flag = 0
        # customer_id = executionContext['customer_id']
        file_path = executionContext['file_path']
        # dataset_id = executionContext['dataset_id']
        # team_name = executionContext['team_name']

        #Newly adding the dataset
        # print(' Adding new dataset.')
        #getting max dataset id for the customer, so that new dataset id = old + 1
        # dataset_dict = self.datasets_tbl.find_one({"CustomerID" : customer_id, "DatasetID": {"$exists": True}},{'_id':0,"DatasetID":1,"DatasetName":1}, sort=[("DatasetID", -1)])
        # print('dataset dict ',dataset_dict)
        # if(dataset_dict):
        #     last_dataset_id = dataset_dict['DatasetID']
        #     dataset_name = dataset_dict['DatasetName']
        # else:
        #     last_dataset_id = 0
        #     dataset_name = executionContext['team_name']
        #     print('Adding dataset for very first team.')

        #     #New dataset id for the customer
        #     dataset_id = last_dataset_id + 1
            
        #     new_dataset_dict = {}
        #     new_dataset_dict["DatasetID"] = dataset_id
        #     new_dataset_dict["DatasetName"] = dataset_name
        #     new_dataset_dict["CustomerID"] =  customer_id
        #     new_dataset_flag = 1

        print('Trying to open the file from the given directory: ',file_path,'...')
        file = open(file_path, 'r')
    
        if not file:
            print("No file")
            return 'failure'
        elif(not file_path.lower().endswith(('.csv'))):
            print("Upload csv file.")
            return 'failure'
        #latin-1
        stream = io.StringIO(file.read(), newline=None)

        stream.seek(0)
        result = stream.read()
    
        #create list of dictionaries keyed by header row   k.lower()
        csv_dicts = [{k.lower(): v for k, v in row.items()} for row in csv.DictReader(result.splitlines(), \
            skipinitialspace=True)]
        # tmpdicts = csv_dicts
        # print(tmpdicts)
        #duplicate skip id not working properly... it iterating alternativly
        # for item in csv_dicts:
        #     item.update( {"CustomerID":customer_id})
        #     item.update( {"DatasetID":dataset_id})
        #     item.update( {"TrainingFlag":0})
            
        #Clease data before inserting into DB
        csv_df = pd.DataFrame(csv_dicts)
        # if('number' not in csv_df.columns):
        # print(' Please rename ticket_id/Incident_id column to "number".')
        # return 'failure'
        
        #remove spaces between the name of column
        csv_df.columns = ['_'.join(col.split(' ')) for col in csv_df.columns]
        #Remove duplicate columns if there any (Based on Incident number)
        # csv_df.drop_duplicates(subset ="number", keep = 'first', inplace = True)
        csv_df_cols = csv_df.columns
        
        if(len(set(csv_df_cols))<len(csv_df_cols)):
            print('Duplicate columns, please rename the duplicate column names..')
            return 'failure'
        
        json_str = csv_df.to_json(orient='records')
        json_data = json.loads(json_str)
        try:
            # print('Trying to insert records into resource_details_tbl...')
            for resource_doc in json_data:    
                self.resourceDetails_tbl.update_one({'email_id':resource_doc['email_id']},{'$set':resource_doc}, upsert=True)
            
            # if(new_dataset_flag):
            #     print('Trying to insert new dataset details into TblDataset, TblTeams...')
            #     self.datasets_tbl.insert_one(new_dataset_dict)
            #     self.teams_tbl.update_one({'CustomerID':customer_id, "TeamName":team_name}, {"$set": {"DatasetID":dataset_id}}, upsert=False)
                
            return {"resp":"success"}    
        except Exception as e:
            print(' Error : ',str(e))
            print(' Possible error: Data format in csv not matching with database constarints.(unique key & not null)')
            return {"resp":"Failure"} 
        return resp

if __name__ == '__main__':
    obj_application = UploadResourceDetails()
    # read data from json   
    context = {}
    #file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")
    # provide input for the execute method
    context = {
        "file_path":"",
        "customer_id":"","dataset_id":"","team_name":""
        }
    # context = {
    #     "file_path":"D:\\Bot_Factory\\Dummy\\Hershey_Resource.csv",
    #     "customer_id":"1","dataset_id":"1","team_name":"Infra team"
    #     }
    # #print(dir(obj_snow))
    obj_application.bot_init()
    resp = obj_application.execute(context)
    #write context to json
    print('-- status --:',resp)