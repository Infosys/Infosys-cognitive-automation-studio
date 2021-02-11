'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol
from abstract_bot import Bot
class CheckRunningProcesses(Bot):
   def bot_init(self):  
        pass
   def execute(self,executionContext):
        try:
            serverName =executionContext["serverName"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            if  serverName == '':
                return ("Missing argument : serverName")
            if  userName == '':
                return ("Missing argument : userName")
            if  password == '':
                return ("Missing argument :password")
            serverName='http://'+ serverName +':5985/wsman'
            Session=Protocol(endpoint=serverName,transport='ntlm',username=userName, password=password,server_cert_validation='ignore')
            shell=Session.open_shell()
            sub = Session.run_command(shell,"tasklist")
            sub_out,sub_err,ret_code = Session.get_command_output(shell,sub)
            a=''
            for i in str(sub_out):  
                a+=i
            x=a.split('\\r\\n')
            for i in x:
                print(i)
            return {'OutputString': "Success"}
        except Exception as e:
            return {'Exception' : str(e)}

 

if __name__ == '__main__':
    bot_obj= CheckRunningProcesses()
    # Enter Credentials
    context = {"serverName":"","userName":"","password":""}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)