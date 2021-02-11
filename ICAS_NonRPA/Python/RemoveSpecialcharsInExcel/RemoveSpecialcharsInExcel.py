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
class RemoveSpecialcharsInExcel(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        filePath = executionContext['filePath']
        specialChars = executionContext['specialChars']
        destFilePath = executionContext['destFilePath']
        try:
            df = pd.read_excel(filePath)
            for index, row in df.iterrows():
                for col in df:
                     for spclChar in specialChars:
                         if spclChar in str(df.at[index,col]):
                             val = str(df.at[index,col]).replace(spclChar, " ")
                             df.at[index,col] = val
                             df.to_excel(destFilePath, index = False)

            return {'result': 'Success'}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 
           

if __name__ == "__main__":
    context = {}
    bot_obj = RemoveSpecialcharsInExcel()
#    context = {'filePath':'D:\Test\sampleOld.xlsx','specialChars':[",", "#","\n","\\"],'destFilePath':'D:\Test\sample_SpecialCharRemoved.xlsx'}
    context = {'filePath':'','specialChars':[],'destFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
