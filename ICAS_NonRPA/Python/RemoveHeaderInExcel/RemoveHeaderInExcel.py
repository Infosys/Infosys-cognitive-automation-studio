'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import traceback
import sys
import pandas as pd
from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class RemoveHeaderInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executionContext):
        filePath = executionContext['filePath']
        destFilePath = executionContext['destFilePath']
        try:
            df = pd.read_excel(filePath)
            df.columns =['']*len(df.columns)
            df.to_excel(destFilePath)
            return {'result': 'Success'}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = RemoveHeaderInExcel()
#    context = {'filePath':'D:\Test\sample.xlsx','destFilePath':'D:\Test\sample_withoutHeader.xlsx'}
    context = {'filePath':'','destFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
