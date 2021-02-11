'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pysnow
import json

class OverrideTicketsInITSM(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        instance1 = executeContext['instance']
        user1 = executeContext['user']
        password1 = executeContext['password']
        predictedDetails = executeContext['predictedDetails']
        predict = executeContext['predict']
        threshholdConfidence=executeContext['threshholdConfidence']
        
        catJson = json.loads(predictedDetails)
        
#        categoryDetails= {"PredCategory": [{"incident_id": "INC0000039", "category_name": "Database"}, {"incident_id": "INC0009009", "category_name": "Database"}, {"incident_id": "INC0010005", "category_name": "Database"}, {"incident_id": "INC0000059", "category_name": "Database"}, {"incident_id": "INC0000058", "category_name": "Database"}, {"incident_id": "INC0010111", "category_name": "Database"}]}
        incidentList = catJson["PredictedValue"]

        try:
            c = pysnow.Client(instance= instance1, user=user1 , password=password1)
        
            # Define a resource, here we'll use the incident table API
            incident = c.resource(api_path='/table/incident')

            for record in incidentList:
                incidentId=str(record['incident_id'])
                if predict=='Category':
                    cfscore=record['cfscore']
                    if float(threshholdConfidence) < cfscore:
                        categoryName=str(record['category_name'])
#                print(incidentId,"...............",categoryName)
                        update_query={'category':categoryName,"number":incidentId}
                        update = update_query
                        updated_record = incident.update(query={'number': incidentId}, payload=update)
                    else:
                        comments=str(record['comments'])
                        update_query={'work_notes':comments,"number":incidentId}
                        update = update_query
                        updated_record = incident.update(query={'number': incidentId}, payload=update)
                    
                elif predict=='Assignee':
                    cfscore=record['cfscore']
                    if float(threshholdConfidence) < cfscore:
                        assignee=str(record['assignee_name'])
#                print(incidentId,"...............",categoryName)
                        update_query={'assigned_to':assignee,"number":incidentId}
                        update = update_query
                        updated_record = incident.update(query={'number': incidentId}, payload=update)
                    else:
                        comments=str(record['comments'])
                        update_query={'work_notes':comments,"number":incidentId}
                        update = update_query
                        updated_record = incident.update(query={'number': incidentId}, payload=update)
                    
#                print(incidentId,"...............",categoryName)
                    
                
                    
            return{'Updated_Status': "SUCCESS"}
           
        except Exception as e:
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    obj_snow = OverrideTicketsInITSM()

    context = {'instance' : "", "user" : "", "password" : "",
        "predictedDetails":"","predict":"","threshholdConfidence":''}

    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
