'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
 
class ValidateDatatypeInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            workBook = executeContext["workBook"]
            colName = executeContext["colName"]
            expDtype = executeContext["expDtype"]
            dest = executeContext["dest"]

            if workBook is None:
                return {"Missing argument : workBook"}
            if colName is None:
                return {"Missing argument : colName"}    
            if expDtype is None:
                return {"Missing argument : expDtype"}
            if dest is None:
                return {"Missing argument : dest"}

            workBook = pd.read_excel(workBook)
            curDtype = workBook[colName].dtypes

            print("curDtype :", curDtype)
            print("expDtype :", expDtype)

            if (curDtype != expDtype):
                workBook[colName] = workBook[colName].astype(expDtype)
                workBook.to_excel(dest, index = False)   
            else:
                print('No change in datatype needed') 

            return {'output': 'Excel value validated'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = ValidateDatatypeInExcel()
    context = {
            'workBook' : '',
            'colName' : '',
            'expDtype' : '',
            'dest' : '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   