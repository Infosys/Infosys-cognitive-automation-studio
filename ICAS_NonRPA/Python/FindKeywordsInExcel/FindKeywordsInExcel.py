'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for search function in excel
class FindKeywordsInExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            filePath = executionContext["filePath"] #Path of the excel file in .xlsx format
            search = executionContext["search"] #Keyword to be searched
            sheetNameSearch = executionContext["sheetNameSearch"] #Sheet name in which searching has to be done
            df = pd.read_excel(filePath, sheet_name = sheetNameSearch)
            dfs = pd.read_excel(filePath, sheet_name = None)         
            for data in list(df):
                dfSearch = df[df[data].apply(str).str.contains(search) | df[data].apply(str).str.match(search)]
                if 'Empty DataFrame' not in str(dfSearch):
                    dfs['Search List'] = dfSearch
            writer = pd.ExcelWriter(filePath, engine = 'xlsxwriter')
            for sheet in dfs.keys():
                dfs[sheet].to_excel(writer, sheet_name = sheet, index = False)
            writer.save()
            return {'Result': 'Success and list of rows copied to new sheet in the same file'}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = FindKeywordsInExcel()
    context = {'filePath':'', 'search':'', 'sheetNameSearch':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)