'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import os
import subprocess
import json 

class ExecutePowershellScript(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        try:
            folderName = executeContext['folderName']
            fileName=executeContext['fileName']
            inputs=executeContext['inputs']
            inputList= inputs.split('||')
            cmd="powershell.exe " +".\\"+fileName+" "
            for inp in inputList:
                cmd=cmd+inp+" "
			
            filepath=os.path.abspath(os.path.join(folderName,fileName))
            print(filepath)
            cmd="powershell.exe " +".\\"+fileName+" "+ inputs
            print("cmd========"+cmd)
            cmdChangeDir=os.chdir(folderName)
            print(os.listdir(cmdChangeDir))
            #include check for file
            os.system(cmd)
            out = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            stdout,stderr=out.communicate()
            print(stdout)
            result=json.dumps(stdout.decode("utf-8"))
            return {'status':'True'}

        except Exception as e:
            print("error")
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    output = {}
    obj = ExecutePowershellScript()

    # context = {'folderName' : "C:\\BotFactoryHome\\TestClone\\bot-factory\\Microbots\\PowerShell\\GetExecutionPolicy",'fileName' : "GetExecutionPolicy.ps1",'inputs' : "C:\\BotFactoryHome\\TestClone\\bot-factory\\Microbots\\PowerShell\\GetExecutionPolicy\\test.txt"}
    context = {'folderName' : "",'fileName' : "",'inputs' : ""}
    
    
    obj.bot_init()
    output = obj.execute(context)
    print(output)
    