'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from docx2csv import extract
import docx
import os
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to change word file into excel
class ConvertWordDataToExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            filePath = executionContext["filePath"] #Path of the word file
            doc = docx.Document(filePath)
            extract(filename=filePath, format="xlsx", singlefile=True)
            data=[]
            for paragraph in doc.paragraphs:
                data.append(paragraph.text)
            outputFile = os.path.splitext(filePath)[0]+'.xlsx'
            dfs = pd.read_excel(outputFile, sheet_name = None)
            dfPara = pd.DataFrame(data)
            dfPara.columns = [''] * len(dfPara.columns) 
            dfs['Sheet'] = dfPara
            writer = pd.ExcelWriter(outputFile, engine='xlsxwriter')
            for sheet in dfs.keys():
                dfs[sheet].to_excel(writer, sheet_name = sheet, index = False)
            writer.save()
            return {'Result': 'Success and .xlsx format file created with same name in the same path'}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = ConvertWordDataToExcel()
    context = {'filePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)