'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pysnow
import sys
import traceback
from datetime import timedelta,datetime
import pandas as pd
from abstract_bot import Bot

class GetSLAViolatedTicketsFromSNOW(Bot):

    def bot_init(self):
        pass
    
    def execute(self, executeContext):
        try:
            instanceId = executeContext['instanceId']
            userName = executeContext['userName']
            password = executeContext['password']
            slaTime = executeContext['slaTime']
            priority = executeContext['priority']
            destFilePath = executeContext['destFilePath']
#            if slaTime is None:
#                return ("Missing Arguments: slaTime")
                
            conn = pysnow.Client(instance=instanceId, user=userName, password=password)
            qb = (
                    pysnow.QueryBuilder()
                    .field('state').equals('1')
                )
            incident = conn.resource(api_path='/table/incident')
            result = incident.get(query=qb,stream=True)
            slaViolatedList= []
            nonViolatedList = []
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nowDate = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
            writer = pd.ExcelWriter(destFilePath, engine = 'xlsxwriter')
          
            for record in result.all():
#                 print(record['number'],record['priority'])
                 if priority.casefold()  == "all":
                     openDate = datetime.strptime(record['opened_at'], '%Y-%m-%d %H:%M:%S')
                     diffDate = nowDate - openDate
#                     print("-------------",openDate,"--------",str(diffDate),"-------",slaTime)
                     if (timedelta(hours= int(slaTime)) < diffDate):
                            incidentInfo = [record['number'],record['priority'],str(diffDate)]
                            slaViolatedList.append(incidentInfo)
                     else:
                            breachTime = timedelta(hours= int(slaTime))-diffDate
                            print(breachTime)
                            incidentInfo = [record['number'],record['priority'],str(breachTime)]
                            nonViolatedList.append(incidentInfo)
                        
                 else:
                     if(str(record['priority']) == priority):
                        openDate = datetime.strptime(record['opened_at'], '%Y-%m-%d %H:%M:%S')
                        diffDate = nowDate - openDate
#                        print("-------------",openDate,"--------",str(diffDate),"-------",slaTime)
                        if (timedelta(hours= int(slaTime)) < diffDate):
                            breachTime = diffDate - timedelta(hours= int(slaTime))
#                            print(breachTime)
                            incidentInfo = [record['number'],record['priority'],str(breachTime)]
                            slaViolatedList.append(incidentInfo)
                        else:
                            breachTime = timedelta(hours= int(slaTime))-diffDate
                            print(breachTime)
                            incidentInfo = [record['number'],record['priority'],str(breachTime)]
                            nonViolatedList.append(incidentInfo)
                        
            slaViolatedDf = pd.DataFrame(slaViolatedList, columns=['Incident_Number','Priority','BreachTime(in hrs)'])
            slaViolatedDf.to_excel(writer, sheet_name = 'Violated Incidents')
            slaNonViolatedDf = pd.DataFrame(nonViolatedList, columns=['Incident_Number','Priority','will Breach(in hrs)'])
            slaNonViolatedDf.to_excel(writer, sheet_name = 'Non Violated Incidents')
            writer.save()
            return {'output':'SLA violated incidents are'+str(slaViolatedList)}
            
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

if __name__ == '__main__':
    context = {}
    bot_obj = GetSLAViolatedTicketsFromSNOW()    
#    context = {'instanceId' : 'dev82133','userName' : 'admin','password' : 's','slaTime':'105','priority':'ALL','destFilePath':'D:\Sla.xlsx'}
    context = {'instanceId' : '','userName' : '','password' : '','slaTime':'','priority':'','destFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
   
    
