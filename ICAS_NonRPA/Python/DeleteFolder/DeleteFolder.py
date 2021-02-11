'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20190723, by: akhil.krishna
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re, shutil
# from Ops_Conn import *
from abstract_bot import Bot


# ------------------------------------------------------------------------------------------
# Arguments: ["string","directory"]
# deletes a directory
# ------------------------------------------------------------------------------------------
class DeleteFolder(Bot):


	def bot_init(self):
		pass


	def execute(self, executeContext):
		# previous_status,arg_dict = readArguments('Script expects arguments')
		# if previous_status != 'OK':
		# 	checkExit(1)
		if "directory" in executeContext:
			directory = executeContext["directory"]
		else:
			return {'Missing argument': 'directory'}
		try:
			shutil.rmtree(directory)
			# response="Directory Removed "+directory

			return {'status' : 'success'}
		except Exception as e:
			return {'Exception' : str(e)}

  
if __name__ == '__main__':
	context = {}
	output = {}
	obj_snow = DeleteFolder()

	context = {'directory':'D:\\Dummy\\delete'}

    # print(dir(obj_snow))
	obj_snow.bot_init()
	output = obj_snow.execute(context)
	print(output)
    # write context to json