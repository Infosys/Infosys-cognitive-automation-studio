'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#Dependency to be installed
from winrm import Protocol
from abstract_bot import Bot

class StopServiceInWindows(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
           
        serverName=executionContext['serverName']
        userName=executionContext['userName']
        password=executionContext['password']
        serviceName=executionContext['serviceName']

        if serverName is None:
            return("Missing argument : serverName")
        if userName is None:
            return("Missing argument : userName")
        if password is None:
            return("Missing argument : password")
        if serviceName is None:
            return("Missing argument : serviceName")

          
        try:     
            serverName='Http://'+serverName+':5985/wsman'
            session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            shell=session.open_shell()
            command = session.run_command(shell,"net stop "+serviceName )
            subOut,subErr,retCode =session.get_command_output(shell,command)
        
            session.cleanup_command(shell, command)
            session.close_shell(shell)
            return {'Output' : str(subOut)+str(subErr)}
        
        except Exception as e:
        	return{'Exception' : str(e)}
          

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = StopServiceInWindows()
    #Variable to be passed as argument
    #give server name as IP only
    context = {'serverName':'',
               'userName':'',
               'password':'',
               'serviceName':''  #enter the name of the service to be stopped
               }

   
    output = bot_obj.execute(context)
    print(output)     