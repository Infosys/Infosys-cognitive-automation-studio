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
#bot to connect to linux server
class ConnectToLinuxServer(Bot):
    
    def bot_init(self):
        pass
        
    def execute(self,executionContext):
        try:
            varServerName =executionContext["varServerName"]
            varUserName=executionContext["varUserName"]
            varPassword=executionContext["varPassword"]
            #condition to check values
            if varServerName is None:
                return ("Missing argument : varServerName")
            if varUserName is None:
                return ("Missing argument : varUserName")
            if  varPassword is None:
                return ("Missing argument :varPassword")
            #connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=varServerName,port=22,username=varUserName,password=varPassword)
            return {'Output':'connected to server'+str(ssh)}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 


if __name__ == "__main__":
    context = {}
    bot_obj = ConnectToLinuxServer()
    #variable to be passed as parameter
    context = {'varServerName':'','varUserName':'','varPassword':''}
    #function calling to connect to linux server and return object
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)     