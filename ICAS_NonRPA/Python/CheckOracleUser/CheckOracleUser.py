'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import cx_Oracle
from abstract_bot import Bot

#class for bot
class CheckOracleUser(Bot):
    #method to initialise 
    def bot_init(self):
        pass

    def execute(self,executionContext):
        try:
            serverName = executionContext['serverName']
            oracleUserName = executionContext['oracleUserName']
            oraclePortNo= executionContext['oraclePortNo']
            oraclePassword = executionContext['oraclePassword']
            oracleServiceName = executionContext['oracleServiceName']
            oracleCheckUser= executionContext['oracleCheckUser']

            if serverName is None:
                return ("Missing argument : serverName")
            if oracleUserName is None:
                return ("Missing argument : oracleUserName")
            if  oraclePassword is None:
                return ("Missing argument :oraclePassword")
            if  oraclePortNo is None:
                return ("Missing argument :oraclePortNo")
            if  oracleCheckUser is None:
                return ("Missing argument :oracleCheckUser")
            if  oracleServiceName is None:
                return ("Missing argument :oracleServiceName")

            dsn_tns = cx_Oracle.makedsn(serverName, oraclePortNo, service_name=oracleServiceName) # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
            conn = cx_Oracle.connect(user=oracleUserName, password=oraclePassword, dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
            c = conn.cursor()
            query= """SELECT username,machine,logon_time,STATUS FROM  v$session where STATUS ='ACTIVE' and username= """
            query= query+"'"+oracleCheckUser+"'"
            c.execute(query)
            if len(list(c)) > 0:
                return {'Status':'User found'}
            else:
#                print("User Not found")
                return {'Status':'User Not found'}
                
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckOracleUser()
    

    context = {'serverName' :'','oracleUserName':'','oraclePassword':'','oracleServiceName':'','oraclePortNo':'','oracleCheckUser':''}
#    context = {'serverName' :'vimppnz01-05.ad.infosys.com','oracleUserName':'system','oraclePassword':'manager','oracleServiceName':'xe','oraclePortNo':'1521','oracleCheckUser':'SYSTEM'}
    bot_obj.bot_init()
    #Calling of execute function on linux server
    output = bot_obj.execute(context)
    print(output)