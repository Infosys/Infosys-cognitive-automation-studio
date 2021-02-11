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
    
class UploadApplicationCsv(Bot):

    
    applicationDetails_tbl = None
    # datasets_tbl = None
    # teams_tbl = None

    def bot_init(self):
        print('Initializing things...')
        client = MongoClient('127.0.0.1',27017)
        db = client['INTENT']

        self.applicationDetails_tbl = db.TblApplication
        # self.datasets_tbl = db.TblDataset
        # self.teams_tbl = db.TblTeams
    
    def execute(self,executionContext):
        # new_dataset_flag = 0
        # customer_id = executionContext['customer_id']
        file_path = executionContext['file_path']
        # dataset_id = executionContext['dataset_id']
        # team_name = executionContext['team_name']

        
        
        try:
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
            csv_df = pd.DataFrame(csv_dicts)

            csv_df.columns = ['_'.join(col.split(' ')) for col in csv_df.columns]
            #Remove duplicate columns if there any (Based on Incident number)
            # csv_df.drop_duplicates(subset ="number", keep = 'first', inplace = True)
            csv_df_cols = csv_df.columns
            
            if(len(set(csv_df_cols))<len(csv_df_cols)):
                print('Duplicate columns, please rename the duplicate column names..')
                return 'failure'
            
            json_str = csv_df.to_json(orient='records')
            json_data = json.loads(json_str)
            # print('Trying to insert records into application_details_tbl...')
            for app_doc in json_data:    
                self.applicationDetails_tbl.update_one({'assignment_group':app_doc['assignment_group']},{'$set':app_doc}, upsert=True)
            
            # if(new_dataset_flag):
            #     # print('Trying to insert new dataset details into TblDataset, TblTeams...')
            #     self.datasets_tbl.insert_one(new_dataset_dict)
            #     self.teams_tbl.update_one({'CustomerID':customer_id, "TeamName":team_name}, {"$set": {"DatasetID":dataset_id}}, upsert=False)
                
            return {'resp':'success'}    
        except Exception as e:
            print(' Error : ',str(e))
            print(' Possible error: Data format in csv not matching with database constarints.(unique key & not null)')
            return {'Exception':str(e)}    
        

if __name__ == '__main__':
    obj_application = UploadApplicationCsv()
    # read data from json   
    context = {}
    #file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")
    # provide input for the execute method
    context = {
        "file_path":""
        
        }
    # context = {
    #     "file_path":"C:\\Users\\atul.kumar31\\Desktop\\Hershey_Application.csv",
    #     "customer_id":"1","dataset_id":"1","team_name":"Infra team"
    #     }
    # #print(dir(obj_snow))
    obj_application.bot_init()
    resp = obj_application.execute(context)
    #write context to json
    print('-- status --:',resp)
