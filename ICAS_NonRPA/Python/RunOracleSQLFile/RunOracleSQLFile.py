'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol

from abstract_bot import Bot

class RunOracleSQLFile(Bot):
    
    def bot_init_(self):
        pass
    
    def execute(self,executeContext):
        try:
           
            serverName = executeContext['serverName']
            userName = executeContext['userName']
            password = executeContext['password']
            dbUsername = executeContext['dbUsername']
            dbPassword = executeContext['dbPassword']
            dbName = executeContext['dbName']
            filePath = executeContext['filePath']

    
            serverName='Http://'+serverName+':5985/wsman'
            session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            shell=session.open_shell()


            
            command = session.run_command(shell,f"echo exit |sqlplus {dbUsername}/{dbPassword}@{dbName} @{filePath}" )
            
            subOut,subErr,retCode =session.get_command_output(shell,command)
            session.cleanup_command(shell, command)
            session.close_shell(shell)
            
            a=''
            for i in str(subOut):  
                a+=i
            x=a.split('\\r\\n')
        
            for i in x:
                print(i)
            
            return{'Status':'Success'}
        
        except Exception as e:
        	return{'Exception':str(e)}
          

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = RunOracleSQLFile()
    
    context = {'serverName' :'','userName':'','password':'',
               'dbUsername':'','dbPassword':'','dbName':'','filePath':''}
    
    
    '''context = {'serverName' :'vimppnz01-05','userName':'moosashah.syed','password':'pass',
               'dbUsername':'system','dbPassword':'manager','dbName':'xe','filePath':'C:\\Users\\moosashah.syed\\desktop\\new.sql'}'''

    

    
    output = bot_obj.execute(context)
    print(output)     


  