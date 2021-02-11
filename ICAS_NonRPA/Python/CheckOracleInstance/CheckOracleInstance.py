'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import cx_Oracle
from abstract_bot import Bot

class CheckOracleInstance(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            serverName = executeContext['serverName']
            oracleUserName = executeContext['oracleUserName']
            oraclePortNo= executeContext['oraclePortNo']
            oraclePassword = executeContext['oraclePassword']
            oracleServiceName = executeContext['oracleServiceName']
            oracleInstanceName = executeContext['oracleInstanceName']
            dsn_tns = cx_Oracle.makedsn(serverName+'.ad.infosys.com', oraclePortNo, service_name=oracleServiceName)
            conn = cx_Oracle.connect(user=oracleUserName, password=oraclePassword, dsn=dsn_tns) 
            c = conn.cursor()
            instanceName=oracleInstanceName
            query= """SELECT INSTANCE_NAME,ACTIVE_STATE,STATUS from V$INSTANCE where INSTANCE_NAME= 
"""
            query= query+"'"+instanceName+"'"
            c.execute(query)
            list1 = list(c)
            if len(list1) > 0:
                status= list1[0][2]#[row[2] for row in c][0]
#                print("Instance Found with Status : ", status)
                return {'Output':"Instance Found with Status : "+status}
            elif len(list(c)) == 0:
                return {'Output':"Instance Not found"}
                
        except Exception as e:
                return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = CheckOracleInstance()
#    context = {'serverName' :'vimppnz01-05','oraclePassword':'manager','oracleUserName':'system','oracleServiceName':'XE','oraclePortNo':'1521','oracleInstanceName':'xe'}
    context = {'serverName' :'','oraclePassword':'','oracleUserName':'','oracleServiceName':'','oraclePortNo':'','oracleInstanceName':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
