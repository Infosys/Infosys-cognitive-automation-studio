'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependencies to be installed before running
import psycopg2
from abstract_bot import Bot

# Python bot to check if a table is available in Postgres DB


class TableCheckPostgresDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']
            var_table_name=executeContext['var_table_name']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )
            print('connection created to postgres DB')            
            cur = conn.cursor()
            cur.execute("SELECT * FROM information_schema.tables WHERE table_name ='"+var_table_name+"'")

            result=bool(cur.rowcount)
            cur = conn.close()
            if result==True:
                return {'output' : 'Table exists'}
            else:
                return {'output' : 'Table does not exists'}

        except Exception as e:
            print("Error occured",str(e)) 
            return str(e)

  
if __name__ == '__main__':
    context = {}
    bot_obj = TableCheckPostgresDB()

    context = {
                'db_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'var_table_name':""
        }

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
