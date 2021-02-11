'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json
from abstract_bot import Bot
class ConvertJSONToString(Bot):
    def bot_init(self):  
        pass
    def execute(self,executionContext):
        filePath=executionContext["filePath"] #File Path
        if filePath == '':
            return ("Missing argument : filePath")
        try:
            with open(filePath) as f:
                data=json.load(f)
                #dataString=str(data)
                return { 'DataString' : data}
        except Exception as e:
            return {'Exception' : str(e)}

            
            
if __name__ == '__main__':
#Enter data path with syntax:  D:\Data/Data.json
    context={}
    bot_obj= ConvertJSONToString()
    context={'filePath':''}
    bot_obj.bot_init()
    DataString=bot_obj.execute(context)
    print("The JsonFile content converted to string is : " +str (DataString))

