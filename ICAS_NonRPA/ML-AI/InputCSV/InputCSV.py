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
class InputCSV(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            file_path = executionContext['csv_path']

            data = pd.read_csv(file_path,encoding='latin-1')
            data1 = data.to_json(orient='records')
            return {'data1':json.loads(data1)}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = InputCSV()

    context = {'csv_path':'C:\\Users\\Supriya_Mahto\\Desktop\\TestOutput\\AIMLFiles\\Samplefile.csv'}
    #context = {'csv_path':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)