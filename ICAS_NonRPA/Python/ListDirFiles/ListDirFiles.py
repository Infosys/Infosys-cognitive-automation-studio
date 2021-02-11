'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
from files.abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class ListDirFiles(Bot):


    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            file_path = executeContext['file_path']

            lst = os.listdir(file_path)
            lst.sort()
            return {'files':lst}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = ListDirFiles()

    context = {'file_path':'C:\\Users\\mansi.saini\\Desktop\\Target'}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)