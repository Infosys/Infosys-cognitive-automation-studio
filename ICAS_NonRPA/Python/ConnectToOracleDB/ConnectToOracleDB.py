'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import cx_Oracle  
from abstract_bot import Bot


class ConnectToOracleDB(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext) :
        try: 
            dbUsername = executeContext['dbUsername']
            if not dbUsername:
                return {'Exception' : 'missing argument dbUsername'}
            
            dbPassword = executeContext['dbPassword']
            if not dbPassword:
                return {'Exception' : 'missing argument dbPassword'}

            dbHost = executeContext['dbHost']
            if not dbHost:
                return {'Exception' : 'missing argument dbHost'}

            connString = '{0}/{1}@{2}'.format(dbUsername, dbPassword, dbHost)
            con = cx_Oracle.connect(connString) 
            con.close()
            return {'status' : 'success'}
        except cx_Oracle.DatabaseError as e: 
            return {'Exception' : str(e)}


if __name__ == '__main__':
    context = {}
    bot_obj = ConnectToOracleDB()

    context =  {
                'dbUsername': '', 
                'dbPassword' : '',
                'dbHost' : '',
                
                }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)
  
