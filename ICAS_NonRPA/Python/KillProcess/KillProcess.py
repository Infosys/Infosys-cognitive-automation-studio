'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:07:00 2020

@author: anuj.gupta03
"""

#pid 
#Dependency to be installed
import sys
import traceback
from winrm import Protocol
from abstract_bot import Bot
class KillProcess(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:    
            var_server_name=executionContext['var_server_name']
            var_user_name=executionContext['var_user_name']
            var_password=executionContext['var_password']
            process_name=executionContext['process_name']
            
            
            if var_server_name is None:
                return ("Missing Arguments: Server Name")
            if var_user_name is None:
                return ("Missing Arguments: user Name")
            if var_password is None:
                return ("Missing Arguments: password")
            if process_name is None:
                return ("Missing Arguments: process_name")
            
    
            var_server_name='Http://'+var_server_name+':5985/wsman'
            Session=Protocol(
                    endpoint=var_server_name,
                    transport='ntlm',
                    username=var_user_name,
                    password=var_password,
                    server_cert_validation='ignore'
                    )
            shell=Session.open_shell()
            command = Session.run_command(shell,"taskkill /f /im  "+process_name )
            sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
        
            Session.cleanup_command(shell, command)
            Session.close_shell(shell)
            Output={'Output':str(sub_out)+str(sub_err)}
            return Output
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = KillProcess()
    #Variable to be passed as argument
    #give server name as IP only
    context = {'var_server_name':'',
               'var_user_name':'',
               'var_password':'',
               'process_name':'' #chrome.exe
               }

   
    output = bot_obj.execute(context)
    print(output)     