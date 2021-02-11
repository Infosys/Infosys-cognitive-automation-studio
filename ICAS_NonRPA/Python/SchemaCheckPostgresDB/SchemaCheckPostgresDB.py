'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependencies to be installed before running
import psycopg2
from abstract_bot import Bot

# Python bot to check if a schema is available in PostgresDB

class SchemaCheckPostgresDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']
            var_schema_name = executeContext['var_schema_name']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )
                        
            cur = conn.cursor()
            print('connection created to postgres DB')
            
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name ='"+var_schema_name+"'")
            
            Result=bool(cur.rowcount)
        
            cur = conn.close()
            if Result==True:
                return {'output' : 'Schema exists'}
            else:
                return {'output' : 'Schema does not exists'}

        except Exception as e:
            print("Error occured",str(e)) 
            return str(e)

  
if __name__ == '__main__':
    context = {}
    bot_obj = SchemaCheckPostgresDB()

    context = {
                'db_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'var_schema_name':''
        }

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
