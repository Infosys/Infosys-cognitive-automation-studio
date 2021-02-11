'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot

class GeneratePollresponseFromExcel(Bot):
        #method to initialise 
    def bot_init(self):
        pass
    #bot to get GeneratePollresponseFromExcel
    def execute(self,executionContext):
        try:
            filePath=executionContext["filePath"]
            result=[]
            df=pd.read_excel(filePath)
            questions=df.columns.ravel()
            for i in range(3,len(questions)):
                output=df[questions[i]].value_counts(normalize='true')
                result.append(questions[i])
                result.append(output.to_string())
               
            return {'Output':result}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = GeneratePollresponseFromExcel()
    #giving parameter as a dictinoary
    context = {'filePath':''}
    bot_obj.bot_init()
    #Calling of execute function using object of Pollrsponses class
    output = bot_obj.execute(context)
    print(output)