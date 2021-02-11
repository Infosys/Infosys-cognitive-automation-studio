'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os      
import win32com.client
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to convert powerpoint file to jpg
class ConvertPowerpointToJpg(Bot):

    def bot_init(self):
        pass

    def execute(self, executionContext):  
        try:
            filePath = executionContext["filePath"] #Path of the powerpoint file
            outputFile = os.path.splitext(filePath)[0]
            powerpoint = win32com.client.Dispatch('Powerpoint.Application') #Create powerpoint object
            jpg = powerpoint.Presentations.Open(filePath, WithWindow = False)
            jpg.SaveAs(outputFile, 17)
            jpg.close()
            powerpoint.Quit()
            return {'Result': 'Success'}
        except Exception as e:
            return {'Exception' : str(e)} 

if __name__ == "__main__":
    context = {}
    bot_obj = ConvertPowerpointToJpg()
    context = {'filePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)