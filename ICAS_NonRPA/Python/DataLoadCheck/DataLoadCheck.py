'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys
import traceback
import pyodbc
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for data load check in SQL Server
class DataLoadCheck(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name'] #DB Name
            db_username = executeContext['db_username'] #DB Username
            db_password = executeContext['db_password'] #DB Password
            db_host = executeContext['db_host'] #DB Host IP
            db_driver = executeContext['db_driver'] #DB Driver

            if db_name == '':
                return ("Missing argument : db_name")
            if db_username == '':
                return ("Missing argument : db_username")
            if db_password == '':
                return ("Missing argument : db_password")
            if db_host == '':
                return ("Missing argument : db_host")
            if db_driver == '':
                return ("Missing argument : db_driver")
    
            conn = pyodbc.connect(driver=db_driver, host=db_host, database=db_name, trusted_connection='yes', user=db_username, password=db_password) #Method to connect to SQL Server
                        
            cur = conn.cursor()
            cur.execute('''SELECT 
                        T.NAME AS 'TABLE NAME',
                        P.[ROWS] AS 'NO OF ROWS'
                        FROM SYS.TABLES T 
                        INNER JOIN  SYS.PARTITIONS P ON T.OBJECT_ID=P.OBJECT_ID;''') #Data load check query
            
            ol=[]
            for row in cur:
                ol.append(str(row))
            Output = ','.join(ol)
            cur = conn.close()
            return {'Status' : Output}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Error' : formatted_lines[-1]}

  
if __name__ == '__main__':
    context = {}
    bot_obj = DataLoadCheck()
    context = {'db_name' : '', 'db_username' : '', 'db_password' : '', 'db_host' : '', 'db_driver' : ''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)