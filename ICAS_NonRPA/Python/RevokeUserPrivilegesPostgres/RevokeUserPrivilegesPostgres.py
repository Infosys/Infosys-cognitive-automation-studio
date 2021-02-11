'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
from abstract_bot import Bot

# Python bot to revoke user privileges in Postgres database


class RevokeUserPrivilegesPostgres(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']
            user_name = executeContext['user_name']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )         
           
        except Exception as e:
            print("Error occured",str(e)) 
            return str(e)

        try:
            cur = conn.cursor()
            sqlSelect = "REVOKE ALL PRIVILEGES ON DATABASE {0} FROM {1};".format(db_name,user_name)
            print (sqlSelect)
            cur.execute(sqlSelect)
            conn.commit()
            cur = conn.close()
            return {'output' : 'action performed'}
        except Exception as e:
            return {'ERROR occured' : e}

  
if __name__ == '__main__':
    context = {}
    bot_obj = RevokeUserPrivilegesPostgres()

    context = {
               
                'db_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'user_name' : '',
               
        }

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)