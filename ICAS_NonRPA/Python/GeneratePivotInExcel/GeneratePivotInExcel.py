'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
import matplotlib.pyplot as plt
 
class GeneratePivotInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:

            dataSheet = executeContext['dataSheet']
            index = executeContext['index']
            values = executeContext['values']
            aggFunc = executeContext['aggFunc']
            destination = executeContext['destination']

            if dataSheet is None:
                return {"Missing argument : dataSheet"}
            if index is None:
                return {"Missing argument : index"}    
            if values is None:
                return {"Missing argument : values"}
            if aggFunc is None:
                return {"Missing argument : aggFunc"}

            df =  pd.read_excel(dataSheet)
            
            table = pd.pivot_table(df,index=[index],
               values=[values],
               aggfunc=aggFunc,fill_value=0)
			
            table.to_excel(destination)
            return {'output' : 'Pivot table created'}
                       
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = GeneratePivotInExcel()
    context = {
           # 'dataSheet' : '',
            #'index' : '',
			#'values' : '',
            #'aggFunc' : '',
            #'destination' : '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   