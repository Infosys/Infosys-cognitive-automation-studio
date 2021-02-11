'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
import io
import os
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to create chart in excel
class GenerateMultireportsInExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        filePath = executionContext["filePath"] #Path of the excel file with .xlsx extension
        sheetName = executionContext["sheetName"] #Sheetname to be filtered

        try:
            filename = os.path.splitext(filePath)[0]+'_generated_reports.xlsx'
            wb = xlsxwriter.Workbook(filename)
            df = pd.read_excel(filePath, sheet_name = sheetName)
            indexCol = df.columns[0]
            df1 = pd.read_excel(filePath, sheet_name = sheetName, index_col = indexCol)
            df2 = pd.read_excel(filePath, sheet_name = sheetName, index_col = indexCol)
            df2.sort_values(by = indexCol, inplace = True)
            if len(list(df1)) > 1:
                if str(df1) == str(df2):
                    ws1 = wb.add_worksheet('Area Chart')
                    imagedataArea = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    areaChart = df1.loc[:,numCol].transpose()
                    plt.figure(figsize=(27,15))
                    plt.stackplot(areaChart.columns, areaChart, labels=list(areaChart.index))
                    plt.xticks(df[df.columns[0]],df[df.columns[0]])
                    plt.savefig(imagedataArea, format='png')
                    ws1.insert_image(0,0,'',{'image_data':imagedataArea})
                                
                    ws2 = wb.add_worksheet('Connected Scatter Plot')
                    imagedataScatter = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    df1.loc[:,numCol].plot.line(marker='o',figsize=(20,15))
                    plt.savefig(imagedataScatter, format='png')
                    ws2.insert_image(0,0,'',{'image_data':imagedataScatter})
                else:
                    ws1 = wb.add_worksheet('Scatter Plot')
                    imagedataScatter = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    pd.plotting.scatter_matrix(df1.loc[:,numCol], figsize=(20,18), diagonal='kde', s=99 )
                    plt.savefig(imagedataScatter, format='png')
                    ws1.insert_image(0,0,'',{'image_data':imagedataScatter})
            elif len(list(df1)) == 1:
                if str(df1) == str(df2):
                    ws1 = wb.add_worksheet('Box Plot')
                    imagedataBox = io.BytesIO()
                    col = list(df1.columns)
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):    
                            plt.boxplot(df1[i])
                            plt.savefig(imagedataBox, format='png')
                            ws1.insert_image(0,0,'',{'image_data':imagedataBox})
                        
                    ws2 = wb.add_worksheet('Line Chart')
                    imagedataLine = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    df1.loc[:,numCol].plot.line(figsize=(15,10))
                    plt.legend()
                    plt.savefig(imagedataLine, format='png')
                    ws2.insert_image(0,0,'',{'image_data':imagedataLine})
                    
                    ws3 = wb.add_worksheet('Area Chart')
                    imagedataArea = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    areaChart = df1.loc[:,numCol].transpose()
                    plt.figure(figsize=(27,15))
                    plt.stackplot(areaChart.columns, areaChart, labels=list(areaChart.index))
                    plt.xticks(df[df.columns[0]],df[df.columns[0]])
                    plt.savefig(imagedataArea, format='png')
                    ws3.insert_image(0,0,'',{'image_data':imagedataArea})
                else:
                    ws1 = wb.add_worksheet('Histogram')
                    imagedataHist = io.BytesIO()
                    col = list(df1.columns)
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            plt.hist(df1[i])
                            plt.savefig(imagedataHist, format='png')
                            ws1.insert_image(0,0,'',{'image_data':imagedataHist})
                    
                    ws2 = wb.add_worksheet('Density Plot')
                    imagedataDense = io.BytesIO()
                    col = list(df1.columns)
                    numCol = []
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            numCol.append(i)
                    df1.loc[:,numCol].plot.density()
                    plt.savefig(imagedataDense, format='png')
                    ws2.insert_image(0,0,'',{'image_data':imagedataDense})
                    
                    ws3 = wb.add_worksheet('Box Plot')
                    imagedataBox = io.BytesIO()
                    col = list(df1.columns)
                    for i in col:
                        if all(isinstance(x,(int,float)) for x in df[i]):
                            plt.boxplot(df1[i])
                            plt.savefig(imagedataBox, format='png')
                            ws3.insert_image(0,0,'',{'image_data':imagedataBox})
            wb.close()
            return {'Result': 'Success and new file is generated'}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = GenerateMultireportsInExcel()
    context = {'filePath':'','sheetName':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)