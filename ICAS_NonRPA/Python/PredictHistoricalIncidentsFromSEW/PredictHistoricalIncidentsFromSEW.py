'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import json
import urllib.request # python 3.6

class PredictHistoricalIncidentsFromSEW(Bot):

    def bot_init(self):
        pass
                                
    
    def _CALL(self,accesToken, url, incJsonTxt="", method_type='PUT', media_type=""):
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

#        incidentDetails = executeContext['incidentDetails']
#        output = {'similarIncidents': []}
        try:
            accessToken = executeContext['accessToken']
            serverName = executeContext['serverName']
            sewIncidentIdList = executeContext['sewIncidentIdList']
            print(".............",sewIncidentIdList,",,,,,,,,,,",type(sewIncidentIdList))
            catJson = json.loads(sewIncidentIdList)
            incidentList = catJson["SewIdDetails"]
            
            for record in incidentList:
                incidentId=str(record['incident_id'])
                sewId=str(record['sew_id'])
                reportedBy=str(record['reportedBy'])
                reportedAt=str(record['reportedAt'])
                priority=str(record['priority'])
                descriptionRT=str(record['descriptionRT'])
#                url = "http://"+serverName+":8084/model/enrichment/incidents/"+sewId+"/sources/incident-history-source"
#                list = []
#                con = self._CALL(accessToken,url,method_type='GET')
#                strResp = con.read() #.decode("utf-8") 
#                similarIncidentsJson =  json.loads(strResp.read())
#                list.append(similarIncidentsJson)  
                list=["INC1111","INC2222"]
                
            finalOutput = json.dumps(list)          
            return {'similarIncidents':finalOutput}
            
        except Exception as e:
            
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictHistoricalIncidentsFromSEW()
    context = {'serverName':'','accessToken':'','sewIncidentIdList':''} # enrichedIncident is the output of addSewIncident file
      #Pick similar incidents based on category matching.  
#    context = {'incidentDetails' :'','api':'http://vimphyz03-01:8084/model/enrichment/incidents/{incident_id}/sources/incident-history-source','accessToken':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
