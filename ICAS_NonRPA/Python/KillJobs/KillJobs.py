'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys
import traceback
from winrm import Protocol
from abstract_bot import Bot

class KillJobs(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:    
            serverName=executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            processName=executionContext['processName']
            
            
            if serverName is None:
                return ("Missing Arguments: Server Name")
            if userName is None:
                return ("Missing Arguments: user Name")
            if password is None:
                return ("Missing Arguments: password")
            if processName is None:
                return ("Missing Arguments: processName")
            
    
            serverName='Http://'+serverName+':5985/wsman'
            Session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            shell=Session.open_shell()
            command = Session.run_command(shell,"taskkill /f /im  "+processName )
            sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
        
            Session.cleanup_command(shell, command)
            Session.close_shell(shell)
            Output={'Output':str(sub_out)+str(sub_err)}
            return Output
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Exception' : formatted_lines[-1]} 

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = KillJobs()
    #Variable to be passed as argument
    #give server name as IP only
    context = {'serverName':'',
               'userName':'',
               'password':'',
               'processName':'' #chrome.exe
               }

   
    output = bot_obj.execute(context)
    print(output)     