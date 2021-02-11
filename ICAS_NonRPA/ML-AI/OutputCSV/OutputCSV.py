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
from pathlib import Path

# -- bot for fetching file names from given directory and for sorting the names --
class OutputCSV(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            
            output_path = Path(executionContext['output_file_path'])
            output_name = executionContext['output_file_name']
            input_data = request.get_json()
            
            df = pd.DataFrame.from_dict(input_data, orient='columns')
            
            df.to_csv( output_path / output_name )

            return df
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = OutputCSV()

    #context = {'csv_path':'D:\\Testing_bots\\Micro Bots\\PreProcessingBot\\sample_data.csv'}
    context = {'output_file_path':'','output_file_name':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    #print(output)