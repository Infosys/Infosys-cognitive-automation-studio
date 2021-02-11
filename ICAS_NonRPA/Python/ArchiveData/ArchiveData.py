'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from winrm import Protocol
from abstract_bot import Bot
class ArchiveData(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:    
            varServerName=executionContext['varServerName']
            varUserName=executionContext['varUserName']
            varPassword=executionContext['varPassword']
            varDriveName=executionContext['varDriveName']
            varDays=executionContext["varDays"]    
            if not varServerName:
                return {'Warning': 'varServerName can not be empty'}
            if not varUserName:
                return {'Warning': 'varUserName can not be empty'}
            if not varPassword:
                return {'Warning': 'varPassword can not be empty'}
            if not varDriveName:
                return {'Warning': 'varDriveName can not be empty'}
            if not varDays:
                return {'Warning': 'varDays can not be empty'}
            
            #connecting to window server 
            varServerName='Http://'+varServerName+':5985/wsman'
            Session=Protocol(
                    endpoint=varServerName,
                    transport='ntlm',
                    username=varUserName,
                    password=varPassword,
                    server_cert_validation='ignore'
                    )
            shell=Session.open_shell()
            #running command to delete files older than provided days
            command = Session.run_command(shell,'ForFiles /p '+varDriveName+' /s /d '+varDays+' /c "cmd /c del @file"')
            subOut,subErr,retCode =Session.get_command_output(shell,command)
            Session.cleanup_command(shell, command)
            Session.close_shell(shell)
            if retCode == 1:
                return {'Output': str(subErr)[1:]}
            else:
                return {'Output':'Success'}
           
        except Exception as e:
            return {'Exception': str(e)} 

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = ArchiveData()
    #Variable to be passed as argument
    #give server name as IP only
    #drive name where files to be deleted with the time period as in how old files to be deleted in days
    # put -before days to delete files before 10 days  put + before days to delete file older than 10 days 
    context = {'varServerName':'','varUserName':'','varPassword':'','varDriveName':r'','varDays':''}
    output = bot_obj.execute(context)
    print(output)     