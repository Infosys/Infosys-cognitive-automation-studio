'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pyodbc 
from abstract_bot import Bot

class RunCommandsOnSQLServer(Bot):

     def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            DatabaseName = executeContext['DatabaseName']
            ServerName = executeContext['ServerName']
            Command= executeContext['Command']
            FilePath= executeContext['FilePath']
            if DatabaseName == '':
                return ("Missing argument : DatabaseName")
            if ServerName == '':
                return ("Missing argument : ServerName")
            if  Command == '':
                return ("Missing argument :Command")


            conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ServerName;'
                      'Database=DatabaseName;'
                      'Trusted_Connection=yes;')
            cursor = conn.cursor()
            cursor.execute(Command)
            for row in cursor:
                with open(file_output_path, 'a', newline='') as row:
                    output = csv.writer(row)
            return {'Output': 'Success'}
        except Exception as e:
            return{"Error occured :",str(e)) }

if __name__ == '__main__':
    context = {}
    bot_obj = RunCommandsOnSQLServer()
    context = {
                'DatabaseName' : "", 
                'ServerName' : "",
                'Command':"",
                'FilePath':""
        }
    bot_obj.bot_init()
    Output = bot_obj.execute(context)
    print(Output)