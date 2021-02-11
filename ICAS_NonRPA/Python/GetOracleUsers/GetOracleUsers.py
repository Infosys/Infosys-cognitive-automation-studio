'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import cx_Oracle
from abstract_bot import Bot

class GetOracleUsers(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            serverName = executeContext['serverName']
            oracleUserName = executeContext['oracleUserName']
            oraclePortNo= executeContext['oraclePortNo']
            oraclePassword = executeContext['oraclePassword']
            oracleServiceName = executeContext['oracleServiceName']
#            dsn_tns = cx_Oracle.makedsn(serverName+'.ad.infosys.com', oraclePortNo, service_name=oracleServiceName) 
            dsn_tns = cx_Oracle.makedsn(serverName+'.ad.infosys.com', oraclePortNo, service_name=oracleServiceName)
            conn = cx_Oracle.connect(user=oracleUserName, password=oraclePassword, dsn=dsn_tns) 
            c = conn.cursor()
            query= """SELECT username FROM  dba_users where username IS NOT NULL"""
            c.execute(query)
            users = ",".join([row[0] for row in c])
            return {'Output':"Oracle users are "+ users}
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = GetOracleUsers()
#    context = {'serverName' :'vimppnz01-05','oraclePassword':'manager','oracleUserName':'system','oracleServiceName':'XE','oraclePortNo':'1521'}
    context = {'serverName' :'','oraclePassword':'','oracleUserName':'','oracleServiceName':'','oraclePortNo':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
