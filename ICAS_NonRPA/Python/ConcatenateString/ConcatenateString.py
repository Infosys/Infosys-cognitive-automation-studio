'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
from abstract_bot import Bot

# -- bot for concatenation of 2 strings --
class ConcatenateString(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
           str1 = executionContext['value1']
           str2 = executionContext['value2']
           result = str1 + ' ' + str2
           return {'result' : result}
        except Exception as e:
            return {'Exception' : str(e)}
          

if __name__ == "__main__":
    context = {}
    bot_obj = ConcatenateString()
    context = {'value1':'','value2':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)