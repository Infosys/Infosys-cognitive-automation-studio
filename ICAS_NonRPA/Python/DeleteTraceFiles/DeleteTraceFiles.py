'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
from abstract_bot import Bot
#class for bot
class DeleteTraceFiles(Bot):
    #method to initialise 
    def bot_init(self):
        pass
    #bot to delete trace files from a linux server
    def execute(self,executionContext):
        try:
            varServerName=executionContext["varServerName"]
            varUserName=executionContext["varUserName"] 
            varPassword=executionContext["varPassword"]
            varDrive=executionContext["varDrive"]
            if not varServerName:
                return {'Warning': 'varServerName can not be empty'}
            if not varUserName:
                return {'Warning': 'varUserName can not be empty'}
            if not varPassword:
                return {'Warning': 'varPassword can not be empty'}
            if not varDrive:
                return {'Warning': 'varDrive can not be empty'}
            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=varServerName,port=22,username=varUserName,password=varPassword)
            #executing command given in parameters to remove all the trc files from given drive
            stdin,stdout,stderr=ssh.exec_command('find '+varDrive+'/*.trc -mtime -1 -exec rm {} \;')
            outlines=stdout.readlines()
            Output=''.join(outlines)
            ssh.close()
            if Output == '':
                return {'Output':'Successfully deleted Trace Files'}
            else:
                return {'Output':'Not able to delete'}
        
        except Exception as e:
            return {'Exception': str(e)}

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = DeleteTraceFiles()
    #giving parameter as a dictinoary
    context = {'varServerName':'','varUserName':'','varPassword':'','varDrive':''}
    bot_obj.bot_init()
    #Calling of execute function using object of DeleteTraceFiles class
    output = bot_obj.execute(context)
    print(output)     