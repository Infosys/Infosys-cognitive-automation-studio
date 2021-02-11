'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
import shutil
from abstract_bot import Bot

# Python Bot to copy file from one location to other

class CopyFileToDestination(Bot):

    def execute(self, executeContext) :
        try:
            source = executeContext['source_file_path']
            destination = executeContext['destination_path']
            newPath = shutil.copy(source, destination)
            print("Path of copied file : ", newPath)
            return {"output" : "File copied"}
        except Exception as e:
            print("Error occured ",str(e)) 
            return str(e)

  
if __name__ == '__main__':
    context = {}
    bot_obj = CopyFileToDestination()
    context = {
                'source_file_path': r'', 
                'destination_path' : r''
                # 'source_file_path': r'D:\eebc.txt', 
                # 'destination_path' : r'\\ad.infosys.com\blr\KEc\GDLY\IMPBLT01\Users\Vikram Chauhan'

        }
    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)
 
