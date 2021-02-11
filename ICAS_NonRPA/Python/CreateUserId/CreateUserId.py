'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
import json
from abstract_bot import Bot

#class for bot
class CreateUserId(Bot):
    #method to initialise 
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
            serverName =executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            serviceAccountName=executionContext['serviceAccountName']
            if serverName is None:
                return ("Missing argument : serverName")
            if userName is None:
                return ("Missing argument : userName")
            if  password is None:
                return ("Missing argument :password")
            if  serviceAccountName is None:
                return ("Missing argument :serviceAccountName")
            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            #executing command given in parameters
            stdin,stdout,stderr=ssh.exec_command('sudo useradd {}'.format(serviceAccountName))
            outlines=stdout.readlines()
            Output=''.join(outlines)+'User Added Successfully'
            ssh.close()
            return {'Output':json.dumps(Output),'Status':'Success'}
        except Exception as e:
          return {'Exception' : str(e)}
 

if __name__ == "__main__":
    context = {}
    
    bot_obj = CreateUserId()
    
    context = {'serverName':'','userName':'','password':'','serviceAccountName':''}
    bot_obj.bot_init()
    #Calling of execute function on linux server
    output = bot_obj.execute(context)
    print(output)  
