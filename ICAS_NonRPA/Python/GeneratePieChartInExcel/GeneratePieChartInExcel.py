'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
import matplotlib.pyplot as plt
 
class GeneratePieChartInExcel(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            dataSheet = executeContext['dataSheet']
            destination = executeContext['destination']

            if dataSheet is None:
                return {"Missing argument : dataSheet"}
            if destination is None:
                return {"Missing argument : destination"} 

            df =  pd.read_excel(dataSheet)
            
            x=df.iloc[:,0]
            y=df.iloc[:,1]

            plt.pie(y, labels=x,autopct='%1.1f%%')
            plt.savefig(destination)
            return {'output': 'pie chart created'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = GeneratePieChartInExcel()
    context = {
            'dataSheet': '', 
            'destination': '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   