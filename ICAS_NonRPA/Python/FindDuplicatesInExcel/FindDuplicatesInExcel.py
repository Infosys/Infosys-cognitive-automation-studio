'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to to find duplicate values in an excel file
class FindDuplicatesInExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            filePath = executionContext["filePath"] #Path of Excel file with .xlsx extension 
            filterColumn = executionContext["filterColumn"] #Give any column name from the file if headerPresent is 'Yes' else if headerPresent is 'No' give input as number starting from 0
            outputFile = executionContext['outputFile'] #Path of the output file with filename with .xlsx extension
            headerPresent= executionContext["headerPresent"] #If header is present in the file then 'Yes' else 'No'
            sheetName = executionContext["sheetName"] #Sheet name present in the file
            if headerPresent.lower()=='yes':
                dataFrame = pd.read_excel(filePath, sheet_name = sheetName)
                dataColumnDuplicate = dataFrame[dataFrame[filterColumn].duplicated(keep = False)]
                dataRowDuplicate = dataFrame[dataFrame.duplicated(keep = False)]
                dataColumnFiltered = dataFrame.drop_duplicates(subset = filterColumn)
                dataRowFiltered = dataFrame.drop_duplicates()
                writer = pd.ExcelWriter(outputFile, engine = 'xlsxwriter')
                dataColumnDuplicate.to_excel(writer, sheet_name = 'Duplicate Column Data')
                dataRowDuplicate.to_excel(writer, sheet_name = 'Duplicate Row Data')
                dataColumnFiltered.to_excel(writer, sheet_name = 'Filtered Column Data')
                dataRowFiltered.to_excel(writer, sheet_name = 'Filtered Row Data')
                writer.save()
                return {'Result': 'Success and output file created'}
            elif headerPresent.lower()=='no':
                dataFrame = pd.read_excel(filePath, sheet_name = sheetName, header = None)
                dataColumnDuplicate = dataFrame[dataFrame[int(filterColumn)].duplicated(keep = False)]
                dataRowDuplicate = dataFrame[dataFrame.duplicated(keep = False)]
                dataColumnFiltered = dataFrame.drop_duplicates(subset = int(filterColumn))
                dataRowFiltered = dataFrame.drop_duplicates()
                writer = pd.ExcelWriter(outputFile, engine = 'xlsxwriter')
                dataColumnDuplicate.to_excel(writer, sheet_name = 'Duplicate Column Data')
                dataRowDuplicate.to_excel(writer, sheet_name = 'Duplicate Row Data')
                dataColumnFiltered.to_excel(writer, sheet_name = 'Filtered Column Data')
                dataRowFiltered.to_excel(writer, sheet_name = 'Filtered Row Data')
                writer.save()
                return {'Result': 'Success and output file created'}
            else:
                return {'Warning': 'Give headerPresent as either "Yes" or "No"'}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = FindDuplicatesInExcel()
    context = {'filePath':'','sheetName':'','headerPresent':'','filterColumn':'','outputFile':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)