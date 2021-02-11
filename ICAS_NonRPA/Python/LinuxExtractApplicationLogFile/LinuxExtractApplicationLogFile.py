'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import paramiko
from abstract_bot import Bot
class LinuxExtractApplicationLogFile(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        ServerName =executionContext["ServerName"]# Ip Address
        UserName=executionContext["UserName"]# User Name
        Password=executionContext["Password"]# Password
        NoOfLines=executionContext["NoOfLines"]# Last n lines as NoOfLines
        FilePath=executionContext["FilePath"]#File path of source file
        if ServerName == '':
            return ("Missing argument : ServerName")
        if UserName == '':
            return ("Missing argument : UserName")
        if  Password == '':
            return ("Missing argument :Password")
        if FilePath == '':
            return ("Missing argument : FilePath")
        if  NoOfLines == '':
            return ("Missing argument :NoOfLines")

        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ServerName,port=22,username=UserName,password=Password)
            print('Connection established')
            sftp_client=ssh.open_sftp()
            file=sftp_client.open(FilePath)  
            for line in (file.readlines()[-int(NoOfLines):]):
                print(line,end='')
            ssh.close()
            return{'Output':'Success'}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj =LinuxExtractApplicationLogFile()
	#Enter your Ip Address, UserName and Password and FilePath where filepath like: //home//ccdadmin//test1//test.txt
    context = {'ServerName':'','UserName':'','Password':'','FilePath':'','NoOfLines':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)
    
