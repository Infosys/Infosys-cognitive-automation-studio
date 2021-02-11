'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pyodbc
from datetime import datetime
from datetime import timedelta
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for long running processes in SQL Server
class IdentifyLongRunningJobsInSQL(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            dbName = executeContext['dbName'] #DB Name
            dbUsername = executeContext['dbUsername'] #DB Username
            dbPassword = executeContext['dbPassword'] #DB Password
            dbHost = executeContext['dbHost'] #DB Host IP
            dbDriver = executeContext['dbDriver'] #DB Driver
            varTime = executeContext["varTime"] #Time
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
            if not varTime:
                return {'Warning': 'varTime can not be empty'}

            conn = pyodbc.connect(driver=dbDriver, server=dbHost,  uid=dbUsername, pwd=dbPassword, database=dbName, trusted_connection='yes') #Method to connect to SQL Server
                        
            cur = conn.cursor()
            cur.execute('''SELECT  creation_time 
                        ,last_execution_time
                        , total_worker_time
                        , total_elapsed_time
                        , total_elapsed_time / execution_count avg_elapsed_time
                        ,SUBSTRING(st.text, (qs.statement_start_offset/2) + 1,
                                   ((CASE statement_end_offset
                                     WHEN -1 THEN DATALENGTH(st.text)
                                     ELSE qs.statement_end_offset END
                                     - qs.statement_start_offset)/2) + 1) AS statement_text
                        FROM sys.dm_exec_query_stats AS qs
                        CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
                        ORDER BY total_elapsed_time / execution_count DESC;''') #Long running jobs query
            
            ol=[]
            for row in cur:
                conversion = str(timedelta(microseconds=row[3])).split('.')[0]
                etf = datetime.strptime(conversion,'%H:%M:%S').time()
                itf = datetime.strptime(varTime,'%H:%M:%S').time()
                if (etf>itf):
                    ol.append(str(row))
            Output = ','.join(ol)
            cur = conn.close()
            return {'Status' : Output}
        except Exception as e:
            return {'Exception' : str(e)} 

  
if __name__ == '__main__':
    context = {}
    bot_obj = IdentifyLongRunningJobsInSQL()
    context = {'dbDriver' : '', 'dbHost' : '', 'dbUsername' : '', 'dbPassword' : '', 'dbName' : '', 'varTime':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)