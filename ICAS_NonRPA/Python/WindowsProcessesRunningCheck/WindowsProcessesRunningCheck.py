'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol
from abstract_bot import Bot
class WindowsProcessesRunningCheck(Bot):
   def bot_init(self):  
        pass
   def execute(self,executionContext):
        try:
            ServerName =executionContext["ServerName"]
            UserName=executionContext["UserName"]
            Password=executionContext["Password"]
            if  ServerName == '':
                return ("Missing argument : ServerName")
            if  UserName == '':
                return ("Missing argument : UserName")
            if  Password == '':
                return ("Missing argument :Password")
            ServerName='http://'+ ServerName +':5985/wsman'
            Session=Protocol(endpoint=ServerName,transport='ntlm',username=UserName, password=Password,server_cert_validation='ignore')
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
    bot_obj= WindowsProcessesRunningCheck()
    # Enter Credentials
    context = {"ServerName":"","UserName":"","Password":""}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)