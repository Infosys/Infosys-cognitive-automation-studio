'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

#Dependency to be installed
import sys
import traceback
from winrm import Protocol
from abstract_bot import Bot
class CheckAccessrightsInWindowsFolder(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:    
            varServerName=executionContext['varServerName']
            varUserName=executionContext['varUserName']
            varPassword=executionContext['varPassword']
            varDriveName=executionContext['varDriveName']
            
            if varServerName is None:
                return ("Missing Arguments: Server Name")
            if varUserName is None:
                return ("Missing Arguments: user Name")
            if varPassword is None:
                return ("Missing Arguments: password")
            if varDriveName is None:
                return ("Missing Arguments: drive Name")
            
    
            varServerName='Http://'+varServerName+':5985/wsman'
            Session=Protocol(
                    endpoint=varServerName,
                    transport='ntlm',
                    username=varUserName,
                    password=varPassword,
                    server_cert_validation='ignore'
                    )
            shell=Session.open_shell()
            command = Session.run_command(shell,"icacls "+varDriveName )
            sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
            Session.cleanup_command(shell, command)
            Session.close_shell(shell)
            return {'Rights to':str(sub_out)}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Exception' : formatted_lines[-1]} 

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckAccessrightsInWindowsFolder()
    #Variable to be passed as argument
    #give server name as IP only
    context = {'varServerName':'','varUserName':'','varPassword':'','varDriveName':r''}

   
    output = bot_obj.execute(context)
    print(output)     