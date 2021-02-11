'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys
import subprocess
import os
from abstract_bot import Bot

class ExecutePythonFile(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        try:
            folderPath = executeContext['folderPath']
            fileName = executeContext['fileName']
            script_path=os.path.join(folderPath,fileName) 
            #print(script_path)

            if not os.path.exists(script_path):
                raise Exception('File not found')
            else:
                subprocess.call([sys.executable, script_path])
                print(sys.executable)

            return {'status':'success'}
        except Exception as e:
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    output = {}
    obj = ExecutePythonFile()

    context = {'folderPath' : '' , 'fileName' : '' }


    obj.bot_init()
    output = obj.execute(context)
    print(output)
