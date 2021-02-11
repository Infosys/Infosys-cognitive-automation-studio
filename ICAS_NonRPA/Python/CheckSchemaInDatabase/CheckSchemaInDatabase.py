'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import psycopg2
from abstract_bot import Bot

# Python bot to check if a schema is available in PostgresDB

class CheckSchemaInDatabase(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            dbName = executeContext['dbName']
            dbUsername = executeContext['dbUsername']
            dbPassword = executeContext['dbPassword']
            schemaName = executeContext['schemaName']

            conn = psycopg2.connect(database=dbName,
                                    user=dbUsername,
                                    password=dbPassword)
                       
            cur = conn.cursor()
            print('connection created to postgres DB')
            
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name ='"+schemaName+"'")
            
            result=bool(cur.rowcount)
        
            cur = conn.close()
            if result==True:
                return {'output' : 'Schema exists'}
            else:
                return {'output' : 'Schema does not exists'}

        except Exception as e:
            return{'Exception':str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CheckSchemaInDatabase()

    context = {
                'dbName' : "", 
                'dbUsername' : "",
                'dbPassword' : "", 
                'schemaName':''
                }

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
