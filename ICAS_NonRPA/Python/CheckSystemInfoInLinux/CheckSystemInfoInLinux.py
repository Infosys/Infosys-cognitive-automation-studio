'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''


import paramiko
from abstract_bot import Bot
class CheckSystemInfoInLinux(Bot):
    
    def bot_init(self):
        pass
    
    def executeCpuUtilisation(self,executionContext):
        serverName =executionContext["serverName"]# Ip Address
        userName=executionContext["userName"]# User Name
        passWord=executionContext["passWord"]# passWord
        if serverName == '':
            return ("Missing argument : serverName")
        if userName == '':
            return ("Missing argument : userName")
        if  passWord == '':
            return ("Missing argument :passWord")

        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=passWord)
            stdin,stdout,stderr=ssh.exec_command("iostat")
            outlines=stdout.readlines()
            Output=''.join(outlines)
            ssh.close()
            return {"CpuOutput" : Output}
        except Exception as e:
            return {'Exception' : str(e)}

    def execute(self,executionContext):
        serverName =executionContext["serverName"]# Ip Address
        userName=executionContext["userName"]# User Name
        passWord=executionContext["passWord"]# passWord
        if serverName == '':
            return ("Missing argument : serverName")
        if userName == '':
            return ("Missing argument : userName")
        if  passWord == '':
            return ("Missing argument :passWord")

        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=passWord)
            stdin,stdout,stderr=ssh.exec_command("w")
            outlines=stdout.readlines()
            Output=''.join(outlines)
            ssh.close()
            CpuOutput=self.executeCpuUtilisation(executionContext)
            return {"LoggedOutput" : Output , "CpuOutput": CpuOutput}
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == "__main__":
    context = {}
    bot_obj =CheckSystemInfoInLinux()
	#Enter your Ip Address, userName and passWord
    context = {'serverName':'','userName':'','passWord':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)

