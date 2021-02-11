'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import json
from abstract_bot import Bot

# Bot will convert the text data to array.
class ConvertTextToArray(Bot):
	def bot_init(self):
		pass
		
	
	def execute(self,executionContext):
		filePath=executionContext['filePath']
		filter=executionContext['deLimiter']

		print('deLimiter is:',type(filter))
		
		if filePath is None:
			return ("Missing argument: filePath")
		if filter is None:
			return ("Missing argument : deLimiter")

		try:
			fileObject=open(filePath,"r")
			text=fileObject.read()
			#print(text)
			if filter == '\\n':
				returnList = text.splitlines()
			else:
				returnList = text.split(filter)
			#print(returnList)
			return{'returnList':returnList}

		except Exception as e:
			return {'Exception':str(e)}
		
	
	
if __name__=="__main__":
    context={}
    bot_obj=ConvertTextToArray()
    
    context = {'filePath':'','deLimiter':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)	

