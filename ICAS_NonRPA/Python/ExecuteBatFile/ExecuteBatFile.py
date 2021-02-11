'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys
import subprocess
import os
from abstract_bot import Bot

class ExecuteBatFile(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        try:
            fileLocation = executeContext['fileLocation']
            #print(script_path)

            if not os.path.exists(fileLocation):
                raise Exception('File not found')
            else:
                subprocess.call([fileLocation])
                print(sys.executable)

            return {'status':'success'}
        except Exception as e:
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    output = {}
    obj = ExecuteBatFile()

    #context = {'fileLocation' : 'D:/1Jun/sample.bat' }
	context = {'fileLocation' : '' }


    obj.bot_init()
    output = obj.execute(context)
    print(output)
