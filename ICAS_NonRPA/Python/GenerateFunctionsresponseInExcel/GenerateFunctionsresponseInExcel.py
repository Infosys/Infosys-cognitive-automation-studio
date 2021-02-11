'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import sys
import traceback
from abstract_bot import Bot

class GenerateFunctionsresponseInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            filePath = executeContext["filePath"]
            functionName = executeContext["functionName"]
            column1 = executeContext["column1"]
            column2 = executeContext["column2"]
            destFilePath = executeContext["destFilePath"]

            df = pd.read_excel(filePath)
            if functionName== 'Sum':
                df[functionName]=df[column1]+df[column2]
            elif functionName== 'Subtract':
                df[functionName]=df[column1]-df[column2]
            elif functionName== 'Multilpy': 
                df[functionName]=df[column1]*df[column2]
            elif functionName== 'Divide':
                df[functionName]=df[column1]/df[column2]
            elif functionName== 'Average':
                df[functionName]=(df[column1]+df[column2])/2
            elif functionName== 'Modulus':
                df[functionName]=(df[column1]%df[column2])
#            writer = ExcelWriter(dest)
            df.to_excel(destFilePath, index = False)
#            writer.save()

            return {'Output': 'Success'}
        
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

        
if __name__ == '__main__':
    context = {}
    output = {}
    bot_obj = GenerateFunctionsresponseInExcel()
#    context = {'filePath' : 'D:\Test\\number.xlsx','functionName' : 'Modulus','column1' : 'number1','column2' : 'number2','destFilePath' : 'D:\Test\\result.xlsx'}
    # functionName can be Sum,Subtract,Multiply,Divide,Average,Modulus
    context = {'filePath' : '','functionName' : '','column1' : '','column2' : '','destFilePath' : ''} 
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
