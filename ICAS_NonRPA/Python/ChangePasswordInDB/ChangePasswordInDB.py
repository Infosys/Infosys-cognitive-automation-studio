'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''


import mysql.connector
from abstract_bot import Bot

# Python bot to change password of a user in MySQL DB

class ChangePasswordInDB(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            varUsername = executeContext['varUsername']
            varPassword = executeContext['varPassword']
            varHost = executeContext['varHost']
            modUsername=executeContext['modUsername']
            modHost=executeContext['modHost']
            modPassword=executeContext['modPassword']
            
            if varUsername =='':
                return{'Missing Argument':'varUsername'}
            if varPassword =='':
                return{'Missing Argument':'varPassword'}
            if varHost =='':
                return{'Missing Argument':'varHost'}
            if modUsername =='':
                return{'Missing Argument':'modUsername'}
            if modHost =='':
                return{'Missing Argument':'modHost'}
            if modPassword =='':
                return{'Missing Argument':'modPassword'}
            
            #establishing the connection
            conn = mysql.connector.connect(user=varUsername, password=varPassword, host=varHost)
            print('connection created to MySQL DB') 
                       
            cursor = conn.cursor()
            cursor.execute('Set Password For "'+modUsername+'"@"'+modHost+'" = "'+modPassword+'"')
            
            conn.close()
            return{'output':'Password changed successfully'}

        except Exception as e:
            return{'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = ChangePasswordInDB()

    context = {'varUsername':'',
               'varPassword':'',
               'varHost':'',
               'modUsername':'',
               'modHost':'',
               'modPassword':''}
    '''
    #Sample Data for input values
    context = {'varUsername':'root',
               'varPassword':'secret',
               'varHost':'127.1.1.1',
               'modUsername':'vikas',
               'modHost':'127.0.0.11',
               'modPassword':'secret@123'}}
    '''
    
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
