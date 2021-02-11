'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import traceback
import sys
import pandas as pd
import datetime

from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class FormatDateInExcel(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
       # Itsm_Tool = executionContext['Itsm_Tool']
        filePath = executionContext['filePath']
        destFilePath = executionContext['destFilePath']
        dateFormat = executionContext['dateFormat']
        columns = executionContext['columns']
        columnsList= eval(columns)
#        print(columnsList,type(columnsList))
        try:
            df = pd.read_excel(filePath)
            for index, row in df.iterrows():
                for col in columnsList:
                    dt = row[col]
                    dtFormatted=pd.to_datetime(dt)
                    dtFormatted = datetime.datetime.strftime(dtFormatted, dateFormat)
#                    print(index,col,dtFormatted)
                    df.at[index,col] = dtFormatted
#            print(df)
            df.to_excel(destFilePath, index = False)
            return {'result': 'Success'}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

           

if __name__ == "__main__":
    context = {}
    bot_obj = FormatDateInExcel()
#    context = {'filePath':'D:\Test\sample.xlsx','dateFormat':'%Y-%m-%d %H:%M:%S','columns':'["DOB","DOJ"]','destFilePath':'D:\Test\sample_FormattedDate.xlsx'}
    context = {'filePath':'','dateFormat':'','columns':'','destFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
