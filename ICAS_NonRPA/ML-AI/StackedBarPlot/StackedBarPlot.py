'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import plotly.io as pio
import matplotlib.pyplot as plt
from abstract_bot import Bot
import json

class StackedBarPlot(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            file_path = executionContext['csv_path']
            outputfile_path = executionContext['outputfile_path']
            stack1 = executionContext['stack1']
            stack2 = executionContext['stack2']
            stack3 = executionContext['stack3']

            medals = pd.read_csv(file_path,index_col=0)
            
            fig, ax = plt.subplots()
            ax.bar(medals.index, medals[stack1],label=stack1)
            ax.bar(medals.index, medals[stack2], bottom=medals[stack1],label=stack2)
            ax.bar(medals.index, medals[stack3],bottom=medals[stack1] + medals[stack2], label=stack3)
            ax.set_xticklabels(medals.index, rotation=90)
            ax.set_ylabel("Number of medals")
            ax.legend()
            #plt.show()
            
            fig.savefig(outputfile_path+"medal_png",dpi=200)
            #pio.write_html(fig, file= outputfile_path + 'medals.html', auto_open=True)
            return {"status":"success"}
            #return {'data1':json.loads(data1)}
        
        
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == "__main__":
    context = {}
    bot_obj = StackedBarPlot()

    context = {'csv_path':'D:\\Bot_Factory\\Docs\dataset for visualization\\dummymedalssheet.csv',
                "stack1":"Gold","stack2":"Silver","stack3":"Bronze",
                'outputfile_path':'D:\\Bot_Factory\\usecases\\'}
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)