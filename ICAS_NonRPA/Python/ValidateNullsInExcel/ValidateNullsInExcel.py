'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
 
class ValidateNullsInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:

            workBook = executeContext["workBook"]
            colName = executeContext["colName"]
            dest = executeContext["dest"]
            replaceWith = executeContext["replaceWith"]

            if workBook is None:
                return {"Missing argument : workBook"}
            if colName is None:
                return {"Missing argument : indcolNameex"}    
            if dest is None:
                return {"Missing argument : dest"}
            if replaceWith is None:
                return {"Missing argument : replaceWith"}


            workBook = pd.read_excel(workBook)
            nullColumns = workBook.columns[workBook.isnull().any()]
            nullChk = workBook.isnull().values.any()
            if(colName == ''):
                print('Invalid column name')

            if (colName == 'ALL'):
                if nullChk:
                    #print("Column {} contains null value".format(nullColumns))
                    print(workBook[workBook.isnull().any(axis=1)][nullColumns])
                    modified = workBook.fillna(replaceWith)
                    modified.to_excel(dest, index = False)

                else:
                    print('No null values')

            else:
                boolSeries = pd.isnull(workBook[colName]).values.any()
                nullColumn = workBook[colName].isnull().values
                if boolSeries:
                    print("Column {} contains null value".format(colName))
                    print(workBook[colName][nullColumn == True])
                    #modified = workBook[colName].fillna(replaceWith)
                    workBook[colName] = workBook[colName].fillna(replaceWith)
                    workBook.to_excel(dest, index = False)
                else:
                    print("Column {} contains no null value".format(colName))

            return {'output': 'Excel Null data validated'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = ValidateNullsInExcel()
    context = {
            'workBook' : '',
            'colName' : '',
            'dest' : '',
            'replaceWith' : '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   