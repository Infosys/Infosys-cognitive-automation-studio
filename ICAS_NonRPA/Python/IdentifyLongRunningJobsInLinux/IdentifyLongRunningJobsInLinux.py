'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
from datetime import datetime
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for long running processes in Linux
class IdentifyLongRunningJobsInLinux(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):
        try:
            varServerName = executionContext["varServerName"] #IP address of other remote server
            varUserName = executionContext["varUserName"] #Username
            varPassword = executionContext["varPassword"] #Password
            varTime = executionContext["varTime"] #Time
            if not varServerName:
                return {'Warning': 'varServerName can not be empty'}
            if not varUserName:
                return {'Warning': 'varUserName can not be empty'}
            if not varPassword:
                return {'Warning': 'varPassword can not be empty'}
            if not varTime:
                return {'Warning': 'varTime can not be empty'}
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=varServerName,port=22,username=varUserName,password=varPassword) #Connection with the remote server
            stdin,stdout,stderr = ssh.exec_command('ps -eo pid,comm,etime') #Execution of command
            outlines=stdout.readlines()
            out = outlines[0]
            outlines.remove(outlines[0])
            ol = []
            for i in outlines:
                h = i[-9:-7]
                m = i[-6:-4]
                s = i[-3:-1]
                if i[-9:-7] == '  ':
                    h ='00'
                if i[-6:-4] == '  ':
                    m ='00'
                if i[-3:-1] == '  ':
                    s ='00'
                et = h+':'+m+':'+s
                etf = datetime.strptime(et,'%H:%M:%S').time()
                itf = datetime.strptime(varTime,'%H:%M:%S').time()
                if (etf>itf):
                    ol.append(i)
            Output = ''.join(ol)
            Output = out + Output
            ssh.close()
            return {'Status': Output}
        except Exception as e:
            return {'Exception' : str(e)} 

if __name__ == "__main__":
    context = {}
    bot_obj = IdentifyLongRunningJobsInLinux()
    context = {'varServerName':'','varUserName':'','varPassword':'','varTime':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)