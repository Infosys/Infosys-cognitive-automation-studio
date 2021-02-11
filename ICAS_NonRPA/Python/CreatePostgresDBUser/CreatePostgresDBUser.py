'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
from abstract_bot import Bot

# Python bot to create new user in Postgres database


class CreatePostgresDBUser(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']
            new_user_name = executeContext['new_user_name']
            new_user_password = executeContext['new_user_password']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )         
           
        except Exception as e:
            print("Error occured",str(e)) 
            return str(e)

        try:
            cur = conn.cursor()
            sqlSelect = "CREATE USER {0} with encrypted password '{1}'".format(new_user_name,
                                            new_user_password)
            cur.execute(sqlSelect)
            conn.commit()
            cur = conn.close()
            return {'output' : 'user created'}
        except Exception as e:
            return {'output' : 'user already exists'}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CreatePostgresDBUser()

    context = {
                'db_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'new_user_name' : '',
                'new_user_password' : ''
        }

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)