'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import subprocess
import traceback
import sys
import wmi
from abstract_bot import Bot

class PerformPatchingOnWindows(Bot):


    def bot_init(self):
        pass

    def execute(self, executeContext):
        path = executeContext['path']
        serverName = executeContext['serverName']
        userName = executeContext['userName']
        password = executeContext['password']
        logFilePath = executeContext['logFilePath']
       
        try:
            connection = wmi.WMI(serverName, user=userName, password=password)
            print("Connection established")
            process_startup = connection.Win32_ProcessStartup.new()
            process_startup.ShowWindow = 1
            
            for update in path:
                script='wusa '+update+' /quiet'+' /norestart'
                
                process_id, result = connection.Win32_Process.Create("cmd.exe /c  "+script+" > "+logFilePath)

                if result == 0:
                    return {'Output':'Patch Applied Sucessfully on '+update}
                else:
                    return {'Output':'Failed to apply Patch'}
                

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

           

if __name__ == "__main__":
    context = {}
    bot_obj = PerformPatchingOnWindows()
#path=['D:\934307\Windows6.0-KB934307-x86.msu','c:\Temp\windows10.0-kb4056887-x64.msu'],'logFilePath':'c:/users/harika.todupunoori/desktop/pythonScript.log'
    context = {'path':[],"serverName":"","userName":"",
               "password":"",'logFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
