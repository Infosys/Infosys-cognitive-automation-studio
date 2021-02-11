'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import wmi

class RemoteExecuteScriptInWindows(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            serverName = executeContext['serverName']
            userName = executeContext['userName']
            password = executeContext['password']
            scriptFilePath = executeContext['scriptFilePath']
            logFilePath = executeContext['logFilePath']
            connection = wmi.WMI(serverName, user=userName, password=password)
            print("Connection established")
            process_startup = connection.Win32_ProcessStartup.new()
            process_startup.ShowWindow = 1
            process_id, result = connection.Win32_Process.Create("cmd.exe /c  "+scriptFilePath+" > "+logFilePath)
            if result == 0:
                return {'Output':'Executed the file Sucessfully'}
            else:
                return {'Output':'Failed to Execute'}
      
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = RemoteExecuteScriptInWindows()
    #context = {'serverName' :'vimppnz02-01','userName':'itlinfosys\harika.todupunoori','password':'','scriptFilePath':'c:/users/harika.todupunoori/desktop/apple.bat','logFilePath':'c:/users/harika.todupunoori/desktop/pythonScript.log'}
    context = {'serverName' :'','userName':'','password':'','scriptFilePath':'','logFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
