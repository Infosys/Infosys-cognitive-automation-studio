'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
from abstract_bot import Bot

# Python bot to connect Postgres DB


class ConnectPostgresDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )
                        
            cur = conn.cursor()
  
            cur = conn.close()
            return {'output' : 'connection created to postgres DB'}

        except Exception as e:
            print("Error occured",str(e)) 
            return {'output' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = ConnectPostgresDB()

    context = {
                'db_name' : "bot-factory", 
                'db_username' : "postgres", 
                'db_password' : "infy", 
                'db_host' : "127.0.0.1", 
                'port' : "5432"
        }
    

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)