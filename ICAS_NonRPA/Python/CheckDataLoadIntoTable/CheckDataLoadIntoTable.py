'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pyodbc
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for data load check in SQL Server
class CheckDataLoadIntoTable(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            dbName = executeContext['dbName'] #DB Name
            dbUsername = executeContext['dbUsername'] #DB Username
            dbPassword = executeContext['dbPassword'] #DB Password
            dbHost = executeContext['dbHost'] #DB Host IP
            dbDriver = executeContext['dbDriver'] #DB Driver
            if not dbHost:
                return {'Warning': 'dbHost can not be empty'}
            if not dbDriver:
                return {'Warning': 'dbDriver can not be empty'}
            if not dbUsername:
                return {'Warning': 'dbUsername can not be empty'}
            if not dbPassword:
                return {'Warning': 'dbPassword can not be empty'}
            if not dbName:
                return {'Warning': 'dbName can not be empty'}

            conn = pyodbc.connect(driver=dbDriver, server=dbHost,  uid=dbUsername, pwd=dbPassword, database=dbName, trusted_connection='yes') #Method to connect to SQL Server
                        
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
        except Exception as e:
            return {'Exception': str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CheckDataLoadIntoTable()
    context = {'dbDriver' : '', 'dbHost' : '', 'dbUsername' : '', 'dbPassword' : '', 'dbName' : ''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)