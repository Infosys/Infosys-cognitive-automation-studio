'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import paramiko
from abstract_bot import Bot
class ExtractApplicationLogs(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        serverName =executionContext["serverName"]# Ip Address
        userName=executionContext["userName"]# User Name
        password=executionContext["password"]# Password
        noOfLines=executionContext["noOfLines"]# Last n lines as NoOfLines
        filePath=executionContext["filePath"]#File path of source file
        if serverName == '':
            return ("Missing argument : serverName")
        if userName == '':
            return ("Missing argument : userName")
        if  password == '':
            return ("Missing argument :password")
        if filePath == '':
            return ("Missing argument : filePath")
        if  noOfLines == '':
            return ("Missing argument :noOfLines")

        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            print('Connection established')
            sftp_client=ssh.open_sftp()
            file=sftp_client.open(filePath)  
            for line in (file.readlines()[-int(noOfLines):]):
                print(line,end='')
            ssh.close()
            return{'Output':'Success'}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj =ExtractApplicationLogs()
	#Enter your Ip Address, UserName and Password and FilePath where filepath like: //home//ccdadmin//test1//test.txt
    context = {'serverName':'','userName':'','password':'','filePath':'','noOfLines':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)
    
