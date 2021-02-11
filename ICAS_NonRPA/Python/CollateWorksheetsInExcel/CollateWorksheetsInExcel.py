'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import pandas
import openpyxl
from abstract_bot import Bot

class CollateWorksheetsInExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            inputExcelPath=executionContext['inputExcelPath']
            outputExcelPath=executionContext['outputExcelPath']
            
            if inputExcelPath=="":
                return{"Missing argument": "inputExcelPath"}
            if outputExcelPath=="":
                return{"Missing argument": "outputExcelPath"}
                
            df=pandas.read_excel(inputExcelPath, None)
            allDf=[]
            for key in df.keys():
                allDf.append(df[key])
            dataConcatenated=pandas.concat(allDf,axis=0,ignore_index=True,sort=False)
            writer=pandas.ExcelWriter(outputExcelPath)
            dataConcatenated.to_excel(writer,sheet_name='Collated',index=False)
            writer.save()
            return{'Output':'Collated the worksheets successfully'}
        except Exception as e:
            return{'Exception':str(e)}

if __name__ == "__main__":
    context = {}
    bot_obj = CollateWorksheetsInExcel()
	#path to be provided as "C:\\Users\\vikas.singh09\\Desktop\\Test_Excel2.xlsx"
    context = {"inputExcelPath" : "", #write the path to the input excel file
               "outputExcelPath": ""} #write the path to the new excel file which will contain the single collated worksheet.
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)