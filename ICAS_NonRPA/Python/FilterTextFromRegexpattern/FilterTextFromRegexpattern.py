'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
import re
# Bot to filter the text using regex pattern
class FilterTextFromRegexpattern(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            inputText = executionContext["inputText"] #Input text
            regexPattern = executionContext["regexPattern"] #Regex pattern
            if regexPattern is None:
                return {'Missing Argument':'regexPattern'}
            if inputText is None:
                return {'Missing Argument':'inputText'}
            match = re.search(regexPattern,inputText) #Filtering the text using regex pattern
            return_text = match.group(0)
            return_text = return_text.strip()
            return {'Return' : return_text}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = FilterTextFromRegexpattern()
    context = {'inputText':'','regexPattern':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)