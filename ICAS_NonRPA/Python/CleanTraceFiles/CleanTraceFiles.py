'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependency to be installed before running 
#pip install paramiko run this command to install dependency
import paramiko
import sys
import traceback
from abstract_bot import Bot
#class for bot
class CleanTraceFiles(Bot):
    #method to initialise 
    def bot_init(self):
        pass
    #bot to delete trace files from a linux server
    def execute(self,executionContext):
        try:
            Var_server_name =executionContext["Var_server_name"]
            Var_user_name=executionContext["Var_user_name"]
            Var_password=executionContext["Var_password"]
            Var_drive=executionContext["Var_drive"]
            if Var_server_name is None:
                return ("Missing argument : Var_server_name")
            if Var_user_name is None:
                return ("Missing argument : Var_user_name")
            if  Var_password is None:
                return ("Missing argument :Var_password")
            if  Var_drive is None:
                return ("Missing argument :Var_drive")
            
            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=Var_server_name,port=22,username=Var_user_name,password=Var_password)
            #executing command given in parameters to remove all the trc files from given drive
            stdin,stdout,stderr=ssh.exec_command('find '+Var_drive+'/*.trc -mtime -1 -exec rm {} \;')
            outlines=stdout.readlines()
            Output=''.join(outlines)
            ssh.close()
            if Output is '':
                return {'Output':'Successfully deleted Trace Files'}
            else:
                return {'Output':'not able to delete'}
            
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = CleanTraceFiles()
    #giving parameter as a dictinoary
    context = {'Var_server_name':'','Var_user_name':'','Var_password':'','Var_drive':''}
    bot_obj.bot_init()
    #Calling of execute function using object of linux server uptime class
    output = bot_obj.execute(context)
    print(output)     