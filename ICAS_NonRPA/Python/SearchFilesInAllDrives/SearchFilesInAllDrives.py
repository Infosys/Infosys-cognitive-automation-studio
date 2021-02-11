'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import os
import re
import win32api

class SearchFilesInAllDrives(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            fileName = executeContext['fileName']
            location = " "
            rex = re.compile(fileName)
            for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
                for root,dirs,files in os.walk(drive):
                    for i in range(len(files)):
                        result = rex.search(files[i])
                        if result:
                            loc = os.path.join(root, files[i])
                            if i>0:
                                location += ", "
                            location += loc
                            
            if location == " ":
                return {'Output':"No such file found"}
            else:
                return {'Output':"File is found at: " +location}
                
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = SearchFilesInAllDrives()
#    context = {'fileName' :'dum.docx'}
    context = {'fileName' :''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
