'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import seaborn as sns
# Standard plotly imports
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
#from files.abstract_bot import Bot
from abstract_bot import Bot
import json

class interactiveVisualization(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            file_path = executionContext['csv_path']
            outputfile_path = executionContext['outputfile_path']
            X = executionContext['X']
            Y = executionContext['Y']
            hover_data = executionContext['hover_data']
            color_param = executionContext['color_param']
            label = executionContext['label']
            height = executionContext['height']
            

            data = pd.read_csv(file_path,encoding='latin-1')
            #data1 = data.to_json(orient='records')


            fig = px.bar(data, x=X, y=Y,
                hover_data=hover_data, color=color_param,
                labels=label, height=int(height))

            fig.show()

            print(type(fig))

            pio.write_html(fig, file= outputfile_path + 'index.html', auto_open=False)
            return {"status":"success"}
            #return {'data1':json.loads(data1)}
        
        
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == "__main__":
    context = {}
    bot_obj = interactiveVisualization()

    
    # context = {'csv_path':'D:\\Bot_Factory\\usecases\\FTTC_Feb_data.csv', 
    #             "X":"Date","Y":"RFT%","hover_data":['Completed_Order', 'Total_Order'],"color_param":"Completed_Order",
    #             "label":{'RFT Percent':'Percentage Of Completed Orders','Date':'Hourly'},"height":400,
    #            'outputfile_path':'D:\\Bot_Factory\\usecases\\'}
    context = {'csv_path':'', "X":"","Y":"","hover_data":"","color_param":"","label":"","height":"",'outputfile_path':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)