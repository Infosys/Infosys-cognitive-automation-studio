'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import paramiko

class CheckProcessMemoryOccupiedInLinux(Bot):
    def bot_init(self):
        pass
    def execute(self,executionContext):
        serverName=executionContext["serverName"]
        userName=executionContext["userName"]
        password=executionContext["password"]

        if serverName is None:
            return("Missing argument : serverName")
        if userName is None:
            return("Missing argument : userName")
        if password is None:
            return("Missing argument : password")

        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(serverName,22,userName,password)
            output=""
            stdin,stdout,stderr=ssh.exec_command('ps -o pid,cmd,%mem ax | sort -b -k3 -r | head -5')
            outlines=stdout.readlines()
            output=''.join(outlines)
            ssh.close()
            return {'output':output}

        except Exception as e:
            return {'Exception':str(e)}
      
 

if __name__=="__main__":
    context={}
    bot_obj=CheckProcessMemoryOccupiedInLinux()
    
   
    context = {'serverName':'','userName':'','password':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)