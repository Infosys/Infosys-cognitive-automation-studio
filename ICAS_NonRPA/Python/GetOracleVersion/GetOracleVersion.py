'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import cx_Oracle
from abstract_bot import Bot

class GetOracleVersion(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            serverName = executeContext['serverName']
            oracleUserName = executeContext['oracleUserName']
            oraclePortNo= executeContext['oraclePortNo']
            oraclePassword = executeContext['oraclePassword']
            oracleServiceName = executeContext['oracleServiceName']
            dsn_tns = cx_Oracle.makedsn(serverName+'.ad.infosys.com', oraclePortNo, service_name=oracleServiceName)
            conn = cx_Oracle.connect(user=oracleUserName, password=oraclePassword, dsn=dsn_tns) 
            c = conn.cursor()
            query= """select * from v$version"""
            c.execute(query)
            version= ",".join([x[0] for x in list(c)])
            return {'Output':"Oracle version is... "+ version}   
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = GetOracleVersion()
#    context = {'serverName' :'vimppnz01-05','oraclePassword':'manager','oracleUserName':'system','oracleServiceName':'xe','oraclePortNo':'1521'}
    context = {'serverName' :'','oracleUserName':'','oraclePassword':'','oracleServiceName':'','oraclePortNo':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
