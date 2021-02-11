'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import psycopg2
from abstract_bot import Bot

# Python bot to check if a table is available in Postgres DB


class CheckTableInDatabase(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            dbName = executeContext['dbName']
            dbUsername = executeContext['dbUsername']
            dbPassword = executeContext['dbPassword']
            tableName=executeContext['tableName']

            conn = psycopg2.connect(database=dbName, 
                                    user=dbUsername,
                                    password=dbPassword)
            print('connection created to postgres DB') 
                       
            cur = conn.cursor()
            cur.execute("SELECT * FROM information_schema.tables WHERE table_name ='"+tableName+"'")

            result=bool(cur.rowcount)
            cur = conn.close()
            if result==True:
                return {'output' : 'Table exists'}
            else:
                return {'output' : 'Table does not exists'}

        except Exception as e:
            return{'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CheckTableInDatabase()

    context = {'dbName':'',
               'dbUsername':'',
               'dbPassword':'',
               'tableName':''}
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
