'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pandas as pd
import matplotlib.pyplot as plt
from docx import Document

class ConvertTabledataToChartInWord(Bot):

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

            document = Document(dataSheet)
            tables = []
            for index,table in enumerate(document.tables):
                df = [['' for i in range(len(table.columns))] for j in range(len(table.rows))]
                for i, row in enumerate(table.rows):
                    for j, cell in enumerate(row.cells):
                        df[i][j] = cell.text 
   
            df1=pd.DataFrame(df) 
            x=df1.iloc[1:,0]
            y=df1.iloc[1:,1]

            plt.pie(y, labels=x,autopct='%1.1f%%')
            plt.savefig(destination)
            return {'output': 'pie chart created'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    obj_snow = ConvertTabledataToChartInWord()
    context = {
            'dataSheet': '', 
            'destination': '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   