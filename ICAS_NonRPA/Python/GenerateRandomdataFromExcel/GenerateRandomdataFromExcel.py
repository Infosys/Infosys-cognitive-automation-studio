'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to generate sample test and train data for AI/ML models
class GenerateRandomdataFromExcel(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            filePath = executionContext["filePath"] #Path of the excel file with .xlsx extension
            splitPercentage = executionContext["splitPercentage"] #Percentage for the training data from the whole data
            outputFile = executionContext['outputFile'] #Path of the output file with filename with .xlsx extension
            if int(splitPercentage)>0 and int(splitPercentage)<100:
                dataFrame = pd.read_excel(filePath)
                testPercent = 1-(int(splitPercentage)/100)
                dataTrain, dataTest = train_test_split(dataFrame, test_size = testPercent, random_state = 99)
                writer = pd.ExcelWriter(outputFile, engine = 'xlsxwriter')
                dataTrain.to_excel(writer, sheet_name = 'Training Data')
                dataTest.to_excel(writer, sheet_name = 'Test Data')
                writer.save()
                return {'Result': 'Success and new file created'}
            else:
                return {'Warning': 'Provide splitPercentage between 0 to 100'}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = GenerateRandomdataFromExcel()
    context = {'filePath':'','splitPercentage':'','outputFile':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)