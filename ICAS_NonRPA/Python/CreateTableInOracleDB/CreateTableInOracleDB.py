'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import cx_Oracle  
from abstract_bot import Bot

class CreateTableInOracleDB(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext) :
        try: 
            
            dbUsername = executeContext['dbUsername']
            dbPassword = executeContext['dbPassword']
            dbHost = executeContext['dbHost']
            createQuery = executeContext['createQuery']
                        
            if dbUsername == '':
                return {'Exception' : 'missing argument dbUsername'}         
            if dbPassword == '':
                return {'Exception' : 'missing argument dbPassword'}
            if dbHost == '':
                return {'Exception' : 'missing argument dbHost'}         
            if createQuery == '':
                return {'Exception' : 'missing argument createQuery'}

            connString = '{0}/{1}@{2}'.format(dbUsername, dbPassword, dbHost)
            con = cx_Oracle.connect(connString)
            print("Successfully connected.")
            
            cursor = con.cursor()
            cursor.execute(createQuery)                      
            print("Table created successfully")
            
            con.close()
            return {'status' : 'success'}
        
        except cx_Oracle.DatabaseError as e: 
            return {'Exception' : str(e)}


if __name__ == '__main__':
    context = {}
    bot_obj = CreateTableInOracleDB()

    context =  {
                'dbUsername': '',           #enter the db username
                'dbPassword' : '',          #enter the db password
                'dbHost' : '',              #enter the db host
                'createQuery' : ''          #enter the create table query
                }
    '''
    #Sample input data
    context =  {
                'dbUsername': 'root', 
                'dbPassword' : 'secret',
                'dbHost' : 'localhost',
                'createQuery' : 'Create table employee (empno INT NOT NULL, empname varchar2 (20) NOT NULL, dept varchar2 (10), PRIMARY KEY(empno))'
                }
    '''
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)
