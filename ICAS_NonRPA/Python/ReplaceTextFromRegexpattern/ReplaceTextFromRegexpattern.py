'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
from abstract_bot import Bot
import traceback,sys

class ReplaceTextFromRegexpattern(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self, executeContext):
        inputText = executeContext["inputText"]
        regexPattern = executeContext["regexPattern"]
        replaceWithChar = executeContext["replaceWithChar"]
        	
        try:
        	return_text = inputText
        	if replaceWithChar == 'NA':
        		return_text = re.sub(regexPattern,'',return_text,re.M)
        	else:
        		return_text = re.sub(regexPattern,replaceWithChar,return_text,re.M)
        	return_text = return_text.strip()
        	print('Regex replace complete: '+str(regexPattern),'INFO')
        	return {'OutputString': return_text}	
        
        except Exception as e:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          """
          exception handled here and above two line is generic exeption 
          """
          return {'Exception' : formatted_lines[-1]} 
       

if __name__ == "__main__":
    context = {}
    bot_obj = ReplaceTextFromRegexpattern() # Instantiating the class object 
    #Passing input parameters in the context below.
    context =  {'inputText':'','regexPattern':'','replaceWithChar':''}  
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)