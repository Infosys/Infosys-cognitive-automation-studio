'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import xlrd
import json
from abstract_bot import Bot

class ConvertExcelToPandasDataframe(Bot):
    def bot_init(self):
        pass
    
    def execute(self, excecuteContext):
        try:
            inputFileName = excecuteContext['inputFileName']

            #csv to DataFrame
            def csv_to_df(src_file_path):
                df = pd.read_csv (src_file_path)
                df = df.to_json()
                print(df)
                return {'Output' : df}

            #xlsb to DataFrame
            def xlsb_to_df(src_file_path):
                df = pd.concat(pd.read_excel(src_file_path,engine = 'pyxlsb' ,sheet_name=None), ignore_index=True)
                df = df.to_json()
                print(df)
                return {'Output' : df}  
            
            #other formats to DataFrame
            def other_to_df(src_file_path):
                df = pd.concat(pd.read_excel(src_file_path, sheet_name=None), ignore_index=True)
                df = df.to_json()
                print(df)
                return {'Output' : df} 
            
            if inputFileName.endswith(".csv"):
                csv_to_df(inputFileName)
                return {'Status' : "Success"}
            elif inputFileName.endswith(".xlsb"):
                xlsb_to_df(inputFileName)
                return {'Status' : "Success"}

            elif (inputFileName.endswith(".xlsx") or inputFileName.endswith(".xls") or inputFileName.endswith(".xlsm")) or (inputFileName.endswith(".xlt") or inputFileName.endswith(".xltm")):
                other_to_df(inputFileName)
                return {'Status' : "Success"}      
            else:
                return {'Exception' : "Non Supported Format found"}

        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = ConvertExcelToPandasDataframe()

    context = {'inputFileName': ""}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)


