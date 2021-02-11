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
import xlrd
from abstract_bot import Bot
    
class UploadRoster(Bot):


    roaster_tbl = None
    # datasets_tbl = None
    # teams_tbl = None
    # resource_details_tbl = None
    # applicationDetails_tbl = None

    def bot_init(self):
        print('Initializing things...')
        client = MongoClient('127.0.0.1',27017)
        db = client['INTENT']

        self.roaster_tbl = db.TblRoaster
        # self.datasets_tbl = db.TblDataset
        # self.teams_tbl = db.TblTeams
        # self.resource_details_tbl = db.TblResource
        # self.applicationDetails_tbl = db.TblApplication
    
    # overriding abstract method 
    def execute(self,executionContext): 
        customer_id = executionContext['customer_id']
        file_path = executionContext['file_path']
        dataset_id = executionContext['dataset_id']
        # dataset_id = executionContext['dataset_id']
        # team_name = executionContext['team_name']

        #print('type of file: ',type(file))
        # dataset_ = self.teams_tbl.find_one({"CustomerID": customer_id,"TeamName":team_name},{"DatasetID":1,"_id":0})
        # if(dataset_):
        #     #Dataset exist for the team
        #     print('Getting old dataset details.')
        #     dataset_id = dataset_["DatasetID"]
        # else:
        #     #Newly adding the dataset
        #     print('Adding new dataset.')
        #     #getting max dataset id for the customer, so that new dataset id = old + 1
        #     dataset_dict = self.datasets_tbl.find_one({"CustomerID" : customer_id, "DatasetID": {"$exists": True}},{'_id':0,"DatasetID":1,"DatasetName":1}, sort=[("DatasetID", -1)])
        #     if(dataset_dict):
        #         last_dataset_id = dataset_dict['DatasetID']
        #         dataset_name=dataset_dict['DatasetName']
        #     else:
        #         last_dataset_id = 0
        #         dataset_name=team_name
        #         print('Adding dataset for very first team.')
    
        #     #New dataset id for the customer
        #     dataset_id = last_dataset_id + 1
            
        #     new_dataset_dict = {}
        #     new_dataset_dict["DatasetID"] = dataset_id
        #     new_dataset_dict["DatasetName"] = dataset_name
        #     new_dataset_dict["CustomerID"] =  customer_id
            
        #     self.datasets_tbl.insert_one(new_dataset_dict)

        
      
        try:

            if(not file_path.lower().endswith(('.xlsx'))):
                print('Uploded file is not excel, insert excel file to continue')
                

            #--fetching data from excel sheet--
            wb=xlrd.open_workbook(file_path)

            if not wb:
                print('No file')
                
            
            #    --Validationsss--
            no_of_sheets=len(wb.sheet_names())
            resource_lst=[]
            app_lst=[]
            # email_lst=[]
            # assignment_lst=[]
            # ignored_lst=[]
            # -- for validation --
            # print('Trying to get documents from "resource_details_tbl", "applicationDetails_tbl"')
            # resource_lst=list(self.resource_details_tbl.find({'CustomerID':customer_id,'DatasetID':dataset_id},{'_id':0,'email_id':1}))
            # app_lst=list(self.applicationDetails_tbl.find({'CustomerID':customer_id,'DatasetID':dataset_id},{'_id':0,'assignment_group':1}))
            
            # if(len(resource_lst)!=0 or len(app_lst)!=0):
     
            # for resource_doc in resource_lst:
            #     email_lst.append(resource_doc['email_id'])
            # for app_doc in app_lst:
            #     assignment_lst.append(app_doc['assignment_group'])
            
            for index in range(1,no_of_sheets-1):
                sheet=wb.sheet_by_index(index)
                #--Variables--
                document={}
                rows=sheet.nrows
                cols=sheet.ncols
                assignment_group=sheet.cell_value(1,2)
                month=sheet.cell_value(1,15)
                segment_1=sheet.cell_value(2,2)
                segment_2=sheet.cell_value(2,14)
                app_name=sheet.cell_value(2,26)

                #--Program logic--
                for row in range(6,rows):#--Iterate through the rows of excel--
                    email_id=sheet.cell_value(row,0)

                    # if(email_id in email_lst and assignment_group in assignment_lst): -- validation --

                    for col in range(1,cols):#--Iterate through the columns of excel--
                        shift=sheet.cell_value(row,col)
                        
                        if(shift in ['F','M','N','O','S','G']):
                            day=sheet.cell_value(5,col)
                            document['email_id']=email_id
                            # document['assignment_group']=assignment_group
                            document['segment_1']=segment_1
                            document['segment_2']=segment_2
                            document['application_name']=app_name
                            document['shift']=shift
                            document['CustomerID'] = customer_id
                            document['DatasetID'] = dataset_id
                            document['availability']=True
                            day_tomorrow=str(int(day)+1)
                            
                            if(len(day)==1):
                                day='0'+day
                            if(len(day_tomorrow)==1):
                                day_tomorrow='0'+day_tomorrow
                            
                            date=month+'-'+day+' T'
                            date_tomorrow=month+'-'+day_tomorrow+' T'
                            
                            if(shift in ['M','O']):
                                document['support_type']='on-call'
                            else:
                                document['support_type']='online'
                            
                            if(shift=='G'):
                                start_date=date+'08:00:00'
                                document['start_date']=start_date
                                end_date=date+'18:00:00'
                                document['end_date']=end_date
                            elif(shift=='O'):
                                start_date=date+'00:00:00'
                                document['start_date']=start_date
                                end_date=date+'24:00:00'
                                document['end_date']=end_date
                            elif(shift=='S'):
                                start_date=date+'14:00:00'
                                document['start_date']=start_date
                                end_date=date+'23:00:00'
                                document['end_date']=end_date 
                            elif(shift in ['F','M']):
                                start_date=date+'06:00:00'
                                document['start_date']=start_date
                                end_date=date+'14:00:00'
                                document['end_date']=end_date
                            elif(shift=='N'):
                                #--date from today night to tommorrow morning--
                                start_date=date+'21:00:00'
                                document['start_date']=start_date
                                end_date=date_tomorrow+'06:00:00'
                                document['end_date']=end_date
                
                            self.roaster_tbl.update_one({
                                            'CustomerID':customer_id,
                                            'DatasetID':dataset_id,
                                            'email_id':email_id,
                                            'start_date':start_date,
                                            'end_date':end_date,
                                            'assignment_group':assignment_group
                                    },{
                                            '$set':document
                                    }, upsert=True)            
                            document={}
                    # else: -- validation else --
                    #     ignored_lst.append(email_id)
            # else:
            #     print('Could not get documents from either "resource_details_tbl" or from "applicationDetails_tbl" for cutomer id: ',customer_id,', dataset id: ',dataset_id)                
        except Exception as e:
            print('Error: ',str(e))
            return {'Exception':str(e)}
             	
        return {"resp":'success'}

if __name__ == '__main__':
    obj_application = UploadRoster()
    # read data from json   
    context = {}
    #file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")
    # provide input for the execute method
    #C:\\Users\\atul.kumar31\\Desktop\\Hershey_roaster_excel_2020_april.xlsx
    context = {
        "file_path":"","customer_id":"","dataset_id":"","team_name":""
        }

    # context = {
    #     "file_path":"D:\\Bot_Factory\\Dummy\\Hershey_roaster_excel_2020_april.xlsx",
    #     "customer_id":"1","dataset_id":"1","team_name":"Infra team"
    #     }
    #print(dir(obj_snow))
    obj_application.bot_init()
    resp = obj_application.execute(context)
    #write context to json
    print('-- status --:',resp)