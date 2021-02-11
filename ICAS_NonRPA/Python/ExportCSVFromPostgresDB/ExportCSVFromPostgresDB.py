'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
import csv
from abstract_bot import Bot

# Creates csv file from records inside specified PostgresDB table


class ExportCSVFromPostgresDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            filepath=executeContext['filepath']
            filename=executeContext['filename']
            db_name = executeContext['db_name']
            db_username = executeContext['db_username']
            db_password = executeContext['db_password']
            db_host = executeContext['db_host']
            port = executeContext['port']
            table_name = executeContext['table_name']

            conn = psycopg2.connect(database = db_name, 
                            user = db_username, password = db_password, 
                            host = db_host, port = port
                            )
                        
            cursor = conn.cursor()

            sqlSelect = "SELECT * FROM {0}".format(table_name)
            cursor.execute(sqlSelect)
            results = cursor.fetchall()

            # Extract the table headers.
            headers = [i[0] for i in cursor.description]

            csvFile = csv.writer(open(filepath + filename, 'w', newline=''),
                                delimiter=',', lineterminator='\r\n',
                                quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)
            
            conn.close()
            return {'output' : 'Data export successful'}
        except Exception as e:
            print("Error occured",str(e)) 
            return {'Exception':str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = ExportCSVFromPostgresDB()

    context = {
                'db_name' : "", 
                'table_name' : "", 
                'db_username' : "", 
                'db_password' : "", 
                'db_host' : "", 
                'port' : "",
                'filepath' : '',
                'filename' : ''
        }

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)