'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pyodbc 
from abstract_bot import Bot

class PerformSQLPatchingReportOnDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext):
        try:
            databaseName = executeContext['databaseName']
            serverName = executeContext['serverName']
            userName= executeContext['userName']
            password= executeContext['password']
            if databaseName == '':
                return ("Missing argument : databaseName")
            if serverName == '':
                return ("Missing argument : serverName")

            if  userName == '':
                return ("Missing argument :userName")
            if  password == '':
                return ("Missing argument :password")
            conn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                      host=serverName,
                      database=databaseName,
                      trusted_connection='yes',user=userName, password=password)
            cursor = conn.cursor()
            cursor.execute('SELECT @@VERSION')
            for row in cursor:
                print(row)
            return {'Output': 'Success'}
        except Exception as e:
            return{"Exception ":str(e) }

if __name__ == '__main__':
    context = {}
    bot_obj = PerformSQLPatchingReportOnDB()
	# Required SQL Server on desktop
    context = {
                'databaseName' : "", 
                'serverName' : "",
                'userName':"",
                'password':""
        }
    bot_obj.bot_init()
    Output = bot_obj.execute(context)
    print(Output)