'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import json
import traceback

from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class ConcatString(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):

        string1 = executionContext['str1']
        string2 = executionContext['str2']
        try:
            
            result = string1 + string2
            return {'Output': result }
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = ConcatString()

    context = {'str1':'','str2':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)