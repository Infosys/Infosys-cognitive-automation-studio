'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Spyder Editor

#created by Anuj.gupta03
"""
import paramiko
from abstract_bot import Bot

class CheckDiskspaceInLinux(Bot):
    def bot_init(self):
        pass
    def execute(self,executionContext):
        serverName=executionContext["serverName"]
        userName=executionContext["userName"]
        passWord=executionContext["passWord"]
        port=executionContext["port"]
        partitionName=executionContext["partitionName"]
        
        if serverName is None:
            return ("Missing argument: serverName")
        if userName is None:
            return ("Missing argument : userName")
        if passWord is None:
            return ("Missing argument :passWord")
        if port is None:
            return ("Missing argument :port")
            
  
        try:
            #Making connection with remote linux server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(serverName,port,userName,passWord)
            print("connection established")
    
            #Execution Command
            stdin,stdout,stderr=ssh.exec_command('df --output=source,avail -h '+partitionName)
            #stdin,stdout,stderr=ssh.exec_command('df -k /opt')
            outlines=stdout.readlines()
            output=''.join(outlines)
            print(output)
            #return {output}
            return {'DiskSpaceInGB' : output }
            
        except Exception as e:
            return {'Error occured ': str(e)}

if __name__=="__main__":
    context={}
    bot_obj=CheckDiskspaceInLinux()
    
    context = {'serverName':'','userName':'','passWord':'','port':'','partitionName':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)