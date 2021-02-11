'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to compare data of 2 excel files
class ListDifferencesInExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            file1 = executionContext["file1"] #Path of the excel file1
            file2 = executionContext["file2"] #Path of the excel file2
            outputFile = executionContext["outputFile"] #Path of the output file with filename with .xlsx extension
            df = pd.read_excel(file2)
            index_col = df.columns[0]
            df1 = pd.read_excel(file1, index_col=index_col).fillna(0)
            df2 = pd.read_excel(file2, index_col=index_col).fillna(0)
            dfDiff = df2.copy()
            droppedRows = []
            newRows = []
            cols1 = df1.columns
            cols2 = df2.columns
            sharedCols = list(set(cols1).intersection(cols2))
            for row in dfDiff.index:
                if (row in df1.index) and (row in df2.index):
                    for col in sharedCols:
                        valueOld = df1.loc[row,col]
                        valueNew = df2.loc[row,col]
                        if valueOld==valueNew:
                            dfDiff.loc[row,col] = df2.loc[row,col]
                        else:
                            dfDiff.loc[row,col] = ('{}→{}').format(valueOld,valueNew)
                else:
                    newRows.append(row)
            for row in df1.index:
                if row not in df2.index:
                    droppedRows.append(row)
                    dfDiff = dfDiff.append(df1.loc[row,:])
            dfDiff = dfDiff.sort_index().fillna('')
            writer = pd.ExcelWriter(outputFile, engine='xlsxwriter')
            dfDiff.to_excel(writer, sheet_name='Difference', index=True)
            df1.to_excel(writer, sheet_name='file_1', index=True)
            df2.to_excel(writer, sheet_name='file_2', index=True)
            workbook  = writer.book
            worksheet = writer.sheets['Difference']
            worksheet.hide_gridlines(2)
            worksheet.set_default_row(15)
            greyFmt = workbook.add_format({'font_color': '#E0E0E0'})
            highlightFmt = workbook.add_format({'font_color': '#FF0000', 'bg_color':'#B1B3B3'})
            newFmt = workbook.add_format({'font_color': '#32CD32','bold':True})
            #Highlight changed cells
            worksheet.conditional_format('A1:ZZ1000', {'type': 'text',
                                                    'criteria': 'containing',
                                                    'value':'→',
                                                    'format': highlightFmt})
            #Highlight new/changed rows        
            for row in range(dfDiff.shape[0]):
                if row+1 in newRows:
                    worksheet.set_row(row+1, 15, newFmt)
                if row+1 in droppedRows:
                    worksheet.set_row(row+1, 15, greyFmt)
            writer.save()
            return {'Result': 'Success'}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = ListDifferencesInExcel()
    context = {'file1':'','file2':'','outputFile':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)