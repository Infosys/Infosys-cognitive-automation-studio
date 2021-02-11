'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
from abstract_bot import Bot
#class for bot
class PerformMountCleanup(Bot):
    #method to initialise 
    def bot_init(self):
        pass
    #bot for linux server Mounted drive clean up if reached certain threshold
    def execute(self,executionContext):
        try:
            varServerName =executionContext["varServerName"]
            varUserName=executionContext["varUserName"]
            varPassword=executionContext["varPassword"]
            threshold =executionContext["threshold"]
            mountedDrive=executionContext["mountedDrive"]
            if not varServerName:
                return {'Warning': 'varServerName can not be empty'}
            if not varUserName:
                return {'Warning': 'varUserName can not be empty'}
            if not varPassword:
                return {'Warning': 'varPassword can not be empty'}
            if not threshold:
                return {'Warning': 'threshold can not be empty'}
            if not mountedDrive:
                return {'Warning': 'mountedDrive can not be empty'}
            test=[]
            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=varServerName,port=22,username=varUserName,password=varPassword)
            #executing command given in parameters
            stdin,stdout,stderr=ssh.exec_command("df "+mountedDrive+" | awk '{ print $5}'")
            outlines=stdout.readlines()
            Output=''.join(outlines)
            for i in Output.split("\n"):
                test.append(i)
            #Checking for theshold
            if(test[1]>=threshold+'%'):
                stdins,stdouts,stderrs=ssh.exec_command("rm -rf "+mountedDrive+"/* ")
                Outline=stderrs.readlines()
                Outputs=''.join(Outline)
                if Outputs == '':
                    Outputs='Success Mounted drive cleaned up'
            ssh.close()
            return {'Output':Outputs}
        except Exception as e:
            return {'Exception': str(e)}
          

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = PerformMountCleanup()
    #giving parameter as a dictinoary
    context = {'varServerName':'','varUserName':'','varPassword':'','threshold':'','mountedDrive':''}
    bot_obj.bot_init()
    #Calling of execute function using object of PerformMountCleanup class
    output = bot_obj.execute(context)
    print(output)     