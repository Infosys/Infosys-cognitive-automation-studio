'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol
from abstract_bot import Bot

class BackupPostgresDB(Bot):
    
    def bot_init_(self):
        pass
    
    def execute(self,executeContext):
        try:
           
            serverName = executeContext['serverName']
            userName = executeContext['userName']
            password = executeContext['password']
            databaseName = executeContext['databaseName']
            postgresPassword = executeContext['postgresPassword']
            sqlFilePath=executeContext['sqlFilePath']
            databaseUser = executeContext['databaseUser']

    
            serverName='Http://'+serverName+':5985/wsman'
            session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            shell=session.open_shell()

            backUpCmd = f'''set "PGPASSWORD={postgresPassword}" & pg_dump -U '''+databaseUser+" -d "+databaseName+" > "+sqlFilePath
            command = session.run_command(shell,backUpCmd )
            
            subOut,subErr,retCode =session.get_command_output(shell,command)
            session.cleanup_command(shell, command)
            session.close_shell(shell)
            print(str(subOut)+str(subErr))
            
            return{'Status':f'Backup done successfully for Database : "{databaseName}"'}
        
        except Exception as e:
        	return{'Exception':str(e)}
          

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = BackupPostgresDB()
    
    context = {'serverName' :'','userName':'','password':'','databaseUser':'',
               'databaseName':'','postgresPassword':'','sqlFilePath':''}
    

    
    output = bot_obj.execute(context)
    print(output)     


  