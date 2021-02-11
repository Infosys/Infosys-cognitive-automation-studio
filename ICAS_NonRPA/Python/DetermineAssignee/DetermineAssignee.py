'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abc import ABC, abstractmethod 
import pysnow
import pymongo
from pymongo import MongoClient
from datetime import datetime,date
import numpy as np
from files.abstract_bot import Bot
    
    
class DetermineAssignee(Bot):


    applicationDetails_tbl = None
    roaster_tbl = None
    resource_details_tbl = None
    rt_tickets_tbl = None
    predicted_tickets_tbl = None
    assign_grp_lst = []

    def bot_init(self):
        client = MongoClient('127.0.0.1',27017)
        db = client['INTENT']

        self.applicationDetails_tbl = db.TblApplication
        self.roaster_tbl = db.TblRoaster
        self.resource_details_tbl = db.TblResource
        self.rt_tickets_tbl = db.TblIncidentRT
        self.predicted_tickets_tbl = db.TblPredictedData
    

    def getRoasterList(self, assign_grp):
        # app_name='.*'
        roaster_lst = []
        
        #--code to get today's date edited today--
        print('Trying to get todays date and time...')
        date1 = date.today()
        time1 = datetime.now().time()
        today= str(date1)+' T'+str(format(time1.hour,'02d'))+':'+str(format(time1.minute,'02d'))+':'+str(format(time1.second,'02d'))

        print('Trying to get documents from "roaster_tbl" for today: ',today,'...')
        roaster_lst=list(self.roaster_tbl.aggregate([
                {
                    '$match':{
                                '$and':[
                                        {'start_date':{'$lte':today}},
                                        {'end_date':{'$gte':today}}
                                ],'availability':True, 'assignment_group':assign_grp
    #                            ,'CustomerID':customer_id,
    #                            'DatasetID':dataset_id
                    }
                },{
                    '$lookup':{
                                'from': "TblResource",
                                'localField': "email_id",
                                'foreignField': "email_id",
                                'as': "resource_name"
                    }        
                },{
                    '$project':{
                                '_id':0,'resource_name.resource_name':1,'shift':1,'support_type':1,'email_id':1
                    }        
                }
                    
            ]))
        
        if(len(roaster_lst)==0):
            print('Could not get documents from "roaster_tbl"')
    
        return roaster_lst


    def getAppWeightage(self, assignment_group):
        print('In "getAppWeightage" method, Trying to fetch details from "TblApplication" for assignment grp: ',assignment_group,'...')
        app_doc=self.applicationDetails_tbl.find_one({'assignment_group': assignment_group},{'_id':0,'app_weightage':1})
        if(app_doc):
            app_weightage = app_doc['app_weightage']
        else:
            app_weightage = 0
            print('No document for assignment grp :',assignment_group,' , returning 0 as "app_weightage"')
        return app_weightage 

    
    def find_assignees(self, assignment_group,incidentCount):
        print(': in "find_assignees" method, assign grp: ',assignment_group,' , incident count: ',incidentCount)
        try:
            resource_name_lst = []
            roaster_lst = []
            resource_lst = []
            assignments = []

            print('Trying to call "getAppWeightage" method of "ApplicationMasterData"...')
            app_weightage = float(self.getAppWeightage(assignment_group))
            print('Trying to call "getRoasterList" method of "ApplicationMasterData"...')
            roaster_lst = self.getRoasterList(assignment_group)
            
            if(roaster_lst):
                for roaster_doc in roaster_lst:
                    resource_name_lst.append(roaster_doc['resource_name'][0]['resource_name'])
                print('Trying to fetch documents from "resource_details_tbl"...')
                resource_lst=list(self.resource_details_tbl.find({
                            'resource_name':{
                                    '$in':resource_name_lst
                            }},{
                                    '_id':0,
                                    'resource_name':1,
                                    'res_bandwidth':1
                            }))
        
                    #------------------------------------
                if(resource_lst):
                    for resource_doc in resource_lst:
                        tickets_assigned=0
                        workload = 0.0
                        incident_lst= list(self.rt_tickets_tbl.find({"assigned_to":resource_doc['resource_name']},{'workload':1,"_id":0}))
                        for incident_doc in incident_lst:
                            tickets_assigned=tickets_assigned+1
                            workload = workload + float(incident_doc["workload"])
            
                                    
                        resource_doc['current_workload']= workload
                        resource_doc['tickets_assigned']=tickets_assigned
#                        workload= 0.0
                        #------------------------------------
                    for res in resource_lst:
                        availability_threshold_value = int(res['res_bandwidth'])/50
                        # availability_threshold_value = int(res['res_bandwidth'])/100
                        res['availableBandwidth'] = availability_threshold_value- res['current_workload'] 
                        res['incidents']=[]
                    i = 0
                    assigned = True
                    assignments = []
                    while i < incidentCount and assigned:
                        assigned = False
                        #--finding resource which is having more bandwidth--
                        res_hvg_mr_bandwidth=resource_lst[0]
                        for res in resource_lst:
                            if(res_hvg_mr_bandwidth['availableBandwidth']<res['availableBandwidth']):
                                res_hvg_mr_bandwidth=res
        
                        res=res_hvg_mr_bandwidth
        #                for res in resource_lst:
                        if i>=incidentCount:
                            break
                        if(res['availableBandwidth'] > app_weightage):
                            res['availableBandwidth'] = res['availableBandwidth'] - app_weightage
                            try:
                                assignments.append(res)
        #                       res['incidents'].append(i)
                            except Exception as e:
                                print("ex : 460",e)
                            i= i+1
                            assigned= True
                    
                    if(i!=incidentCount):
                        print('some of the assignment group cannot be assigned with assignee becoz, all resources having maximum bandwidth')
                    else:
                        print('all tickets are assigned with assignees!')
                else:
                    print('Could not get documents from "resource_details_tbl"')
            else:
                print('Could not get documents from "getRoasterList"')
        except Exception as e:
            print(str(e))
    
        return assignments


    def find_assigneesForAssignmentGroups(self):
        counts = dict()
        #Finding the resource name by iteration 
        for ag in self.assign_grp_lst:
            if ag not in counts :
                counts[ag] = 1
            else:
                counts[ag] = counts[ag] + 1
        assignees = ['']*len(self.assign_grp_lst)

        #print("Inside assignee groups.2"+ str(self.possible_assignee_for_assignment))
        try:
            print('calling find_assignees function for each assignmnet group')
            for ag in counts.keys():
                res = self.find_assignees(ag, counts[ag])
                if(res):
                    j = 0
                    for k in range(0 , len(self.assign_grp_lst)):
                        if self.assign_grp_lst[k] == ag:
                            assignees[k] = res[j]['resource_name']
                            j= j+1
                            if(j==len(res)):
                                j=0
                else:
                    print('empty assignees list for assign grp: ',ag)
        except Exception as e:
            print(str(e))
        return np.array(assignees)


    # overriding abstract method 
    def execute(self,executionContext):
        print('Trying to fetch details from rt_tickets_table')
        assign_grp_lst = []
        rt_tckts_lst = list(self.rt_tickets_tbl.find({},{'_id':0,'assignment_group':1,'number':1}))
        
        for rt_tckts_doc in rt_tckts_lst:
            assign_grp_lst.append(rt_tckts_doc['assignment_group'])

        # print('-----',assign_grp_lst)
        self.assign_grp_lst = assign_grp_lst
        assignees = self.find_assigneesForAssignmentGroups()
        print('Trying to update predicted_tickets_tbl with assignee details...')
        index = 0
        self.predicted_tickets_tbl.delete_many({})
        for rt_tckts_doc in rt_tckts_lst:
            self.predicted_tickets_tbl.insert_one({'number':rt_tckts_doc['number'],'assignment_group':rt_tckts_doc['assignment_group'],'predicted_assigned_to':assignees[index]})
            index = index + 1
        # for pred_doc in predicted_tckts_lst:
        #     self.predicted_tickets_tbl.update_one({'number':pred_doc['number']},{'$set':{'predicted_assigned_to':assignees[index]}},upsert=True)
        #     index = index + 1
        return 'success'

if __name__ == '__main__':
    obj_snow = DetermineAssignee()
    # read data from json
    context = {}
    #file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")

    # context = {}
    #print(dir(obj_snow))
    obj_snow.bot_init()
    resp = obj_snow.execute(context)
    #write context to json
    print('-- status -- : ',resp)