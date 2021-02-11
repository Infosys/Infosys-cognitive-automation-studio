'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
import re
 
class ValidateExcelfieldsInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            workBook = executeContext["workBook"]
            colName = executeContext["colName"]
            cond = executeContext["cond"]

            if workBook is None:
                return {"Missing argument : workBook"}
            if colName is None:
                return {"Missing argument : colName"}    
            if cond is None:
                return {"Missing argument : cond"}

            workBook = pd.read_excel(workBook)

            res = [int(i) for i in cond.split() if i.isdigit()]
            inBetween = (workBook[colName] > res[0]) & (workBook[colName] < res[1])
            valChk = inBetween.values.all()

            if valChk:
                print('No anomalies found')
            else:
                result = workBook[colName][inBetween == False]
                result1 = pd.DataFrame(result)
                print('Invalid input is {}'.format(result1.to_string(index=False)))


            return {'output': 'Excel value validated'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = ValidateExcelfieldsInExcel()
    context = {
            'workBook' : '',
            'colName' : '',
            'cond' : '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   