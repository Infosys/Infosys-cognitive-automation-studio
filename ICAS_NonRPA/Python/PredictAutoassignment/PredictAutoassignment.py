'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pysnow
import json
import requests

import urllib.request # python 3.6

class PredictAutoassignment(Bot):

    def bot_init(self):
        pass
		
    
    def _CALL(self,accesToken, url, incJsonTxt, method_type='PUT', media_type=""):
        print("_CALL : "+str(method_type)+" : "+str(url))
#        print(incJsonTxt)
        
        try:
            if incJsonTxt!="":
                incJson =  json.loads(incJsonTxt)
                print(incJson)
            
            headers = {}    
            headers['Content-Type'] = 'application/json'
            headers['Authorization'] = accesToken #self.token
            if media_type != "":
                headers['X-Nia-Media-Type'] =  media_type
            
            print(headers)
          
            request = urllib.request.Request(url, data=incJsonTxt.encode('utf8'), headers=headers, method=method_type )
            resp = urllib.request.urlopen(request)
#            print(resp)
            
            return resp
            
        except Exception as e:
           print(e)
            
    
    def execute(self, executeContext):

        try:
            output = {'PredictedValue': []}
            records = executeContext['incidentDetails']
            threshholdConfidence=executeContext['threshholdConfidence']
            api = executeContext['api']
            accessToken = executeContext['accessToken']
            jsonrecord = json.loads(records)

            for record in jsonrecord:
               
                incidentId=str(record['incidentId'])
                reportedBy=str(record['openedBy'])
                reportedAt=str(record['openedAt'])
                priority=str(record['priority'])
                descriptionRT=str(record['shortDesc'])
                
            
#                url = api
#            
#                assignJsonTxtdata={'incident_id': incidentId, 'created_at': reportedAt,
#                    'description': descriptionRT, 'application': 'BotFactory','discussions': [
#                {"discussion_id": 0, "created_at": reportedAt ,
#                "content_type": "string", "content": "string"}]}
#                assignJsonTxtdata= json.dumps(assignJsonTxtdata)
#                con = self._CALL(accessToken,url, incJsonTxt= assignJsonTxtdata, method_type='POST')
#                strResp = con.read() #.decode("utf-8") 
#                self.log(strResp)
#                assigneeJson =  json.loads(strResp.read())
#                cfscore = strResp["incident"]["Confidence_Score"]
                cfscore = 0.9
                if cfscore < float(threshholdConfidence):
               
                    comments='Expected confidence score is less than Predicted score'
                    incidentInfo = {"incident_id":incidentId, "comments": comments,"assignee_name": '','cfscore':cfscore} # adding above hardcoded value
                else:
#                    assigneeName= assigneeJson["classification"]["label"]
                    assigneeName = "David Dan"
                    incidentInfo = {"incident_id":incidentId, "assignee_name": assigneeName,"comments":'','cfscore':cfscore} # adding above hardcoded value
#                assigneeName= assigneeJson["classification"]["label"]
#                assigneeName = "David Dan"
                
#                incidentInfo = {"incident_id":incidentId, "assignee_name": assigneeName} # adding above hardcoded value
                output['PredictedValue'].append((incidentInfo))
                finalOutput = json.dumps(output)
                
            return {'PredictedFields':finalOutput}
            
        except Exception as e:
            
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictAutoassignment()
#    context = {'incidentDetails' :'','api':'http://vimphyz03-01:8084/model/assignmentcfscore','accessToken':''}
    context = {'incidentDetails' :'','api':'','accessToken':'','threshholdConfidence':''} # incident details is the output of fetchsnow and api is the url to predict the category
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
