'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import mysql.connector
from abstract_bot import Bot

# Python bot to setup a database


class SetupDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            varUsername = executeContext['varUsername']
            varPassword = executeContext['varPassword']
            varHost = executeContext['varHost']
            varDBName=executeContext['varDBName']
            
            if varUsername =='':
                return{'Missing Argument':'varUsername'}
            if varPassword =='':
                return{'Missing Argument':'varPassword'}
            if varHost =='':
                return{'Missing Argument':'varHost'}
            if varDBName =='':
                return{'Missing Argument':'varDBName'}
            
            #establishing the connection
            conn = mysql.connector.connect(user=varUsername, password=varPassword, host=varHost)
            print('connection created to MySQL DB') 
                       
            cursor = conn.cursor()
            cursor.execute("CREATE database "+varDBName)
            
            '''
            #To list all the databases present uncomment these lines
            print("List of databases: ")
            cursor.execute("SHOW DATABASES")
            print(cursor.fetchall())
            '''
            
            conn.close()
            return{'output':'Database created successfully'}

        except Exception as e:
            return{'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = SetupDB()

    context = {'varUsername':'',	#username for connecting to the MySQL server
               'varPassword':'',	#password for connecting to the MySQL server
               'varHost':'',		#host ip for connecting to the MySQL server
               'varDBName':''}		#name of the database that needs to be created
    '''
    #Sample Data for input values
    context = {'varUsername':'root',
               'varPassword':'secret',
               'varHost':'127.1.1.1',
               'varDBName':'testDB'}
    '''
    
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
