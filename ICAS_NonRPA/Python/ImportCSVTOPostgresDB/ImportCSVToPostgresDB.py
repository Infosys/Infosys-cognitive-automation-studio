'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
import csv
from abstract_bot import Bot

# Inserts csv records to specified table of Postgres DB


class ImportCSVToPostgresDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            table_name = executeContext['table_name']
            port = executeContext['port']
            column_count = executeContext['column_count']
            filepath=executeContext['filepath']


            # creating values for INSERT query using column_count
            values_str = '%s'
            if int(column_count) < 1:
                pass
            else:
                for i in range(1,int(column_count)):
                    values_str = values_str + ',%s'


            sql_dialect = """
                                INSERT INTO {0} VALUES ({1})                 
                         """.format (table_name,values_str)


            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )
                        
            cur = conn.cursor()
            
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader)                            # Skip the header row.
                for row in reader:                    
                    cur.execute(sql_dialect,row)
                conn.commit()
            
            cur = conn.close()
            return {'output' : 'Data import successful'}
           
        except Exception as e:
            print("Error occured",str(e)) 
            return{'Exception': str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = ImportCSVToPostgresDB()

    context = { 
                'db_name' : "", 
                'table_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'column_count' : "",
                'filepath' : ''
        }

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)