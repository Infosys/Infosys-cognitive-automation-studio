'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol
from abstract_bot import Bot
import traceback
import sys
from socket import getfqdn

class CheckLastRebootTimeInWindowsServer(Bot):
   def bot_init(self):  
        pass
   def execute(self,executionContext):
        try:
            serverName =executionContext["serverName"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            rebootDateTime =""
            if  serverName == '':
                return ("Missing argument : serverName")
            if  userName == '':
                return ("Missing argument : userName")
            if  password == '':
                return ("Missing argument :password")
            serverName='http://'+ serverName +':5985/wsman'
            Session=Protocol(endpoint=serverName,transport='ntlm',username=userName, password=password,server_cert_validation='ignore')
            shell=Session.open_shell()
            remote = getfqdn(serverName[7:-11])
    
            sub = Session.run_command(shell,"systeminfo /s {}".format(remote))
            sub_out,sub_err,ret_code = Session.get_command_output(shell,sub)

            output = ''.join(str(sub_out))
            std_output=''
            for i in output:
                std_output+=i
            lines = std_output.split('\\r\\n')
            for line in lines:
                if 'System Boot Time:' in str(line):
                    line = str(line)
                    #retrieving date and time
                    date, time, ampm = line.split()[3:6]
                    date = date.replace(',', '')
                    date = date.replace('', '')
                    ampm = ampm.split("'")[0]
                    rebootDateTime = date+" "+time+" "+ ampm
            return {'OutputString': rebootDateTime}	
        except Exception as e:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          """
          exception handled here and above two line is generic exeption 
          """
          return {'Exception' : formatted_lines[-1]} 
       

if __name__ == '__main__':

    bot_obj = CheckLastRebootTimeInWindowsServer()
    # Enter Credentials
    context = {'serverName':'','userName':'','password':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)
