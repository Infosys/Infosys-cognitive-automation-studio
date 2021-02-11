'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import json
#from abstract_bot import Bot

# Bot will convert the text data to array.
<<<<<<< HEAD
class TextToArray:
	
=======
class TextToArray(Bot):
>>>>>>> master
	def bot_init(self):
		pass
		
	
	def execute(self,executionContext):
		filepath=executionContext['filepath']
		filter=executionContext['de_limiter']

		print('delimiter is:',type(filter))
		print('delimiter is:',filter)
		
		if filepath is None:
			return ("Missing argument: filepath")
		if filter is None:
			return ("Missing argument : de_limiter")

		try:
			fileObject=open(filepath,"r")
			text=fileObject.read()
			#print(text)
			if filter == '\\n':
				return_list = text.splitlines()
			else:
				return_list = text.split(filter)
			#print(return_list)
			return{'return_list':return_list}

		except Exception as e:
			return {'Exception':str(e)}
<<<<<<< HEAD

=======
>>>>>>> master
		
	
	
if __name__=="__main__":
    context={}
    bot_obj=TextToArray()
    
<<<<<<< HEAD
    context = {'filepath':'D:/StringTest.txt','de_limiter':''}
	#context = {'filepath':'','de_limiter':''}
=======
    #context = {'filepath':'D:/StringTest.txt','de_limiter':'\s'}
	context = {'filepath':'','de_limiter':''}
>>>>>>> master
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)	

