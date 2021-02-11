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
class CheckServerUptimeInLinux(Bot):
    #method to initialise 
    def bot_init(self):
        pass
    #bot to get linux server uptime
    def execute(self,executionContext):
        serverName =executionContext["serverName"]
        
        userName=executionContext["userName"]
        passWord=executionContext["passWord"]
        command=executionContext["command"]
        if serverName is None:
            return ("Missing argument : serverName")
        if userName is None:
            return ("Missing argument : userName")
        if  passWord is None:
            return ("Missing argument :passWord")
        if  command is None:
            return ("Missing argument :Command")
	
        try:

            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=passWord)
            #executing command given in parameters
            stdin,stdout,stderr=ssh.exec_command(command)
            outLines=stdout.readlines()
            Output=''.join(outLines)
            ssh.close()
            return {'Uptime:':Output}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formattedLines = traceback.format_exc().splitlines()
          return {'Error' : formattedLines[-1]} 

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = CheckServerUptimeInLinux()
    #giving parameter as a dictinoary
    context = {'serverName':'','userName':'','passWord':'','command':''}
    bot_obj.bot_init()
    #Calling of execute function using object of linux server uptime class
    Output = bot_obj.execute(context)
    print(Output)     