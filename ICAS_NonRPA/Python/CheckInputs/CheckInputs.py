'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import pandas as pd
from abstract_bot import Bot
import json

# -- bot for fetching file names from given directory and for sorting the names --
class CheckInputs(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            value1 = executionContext['value1']
            value2 = executionContext['value2']
            value3 = executionContext['value3']
            value4 = executionContext['value4']
            value5 = executionContext['value5']
            

            
            return {'data1':json.dumps(value1),'data2':json.dumps(value2),'data3':json.dumps(value3),
                            'data1':json.dumps(value4),'data1':json.loads(value5)}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = CheckInputs()

    #context = {'csv_path':'D:\\Testing_bots\\Local testing\\sample_data.csv'}
    context = {'value1':'','value2':'','value3':'','value4':'','value5':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)