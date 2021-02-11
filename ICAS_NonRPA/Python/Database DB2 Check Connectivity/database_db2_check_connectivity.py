'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20180320, by: rajesh.kella
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
from Ops_Conn import *
from abstract_bot import Bot
# ------------------------------------------------------------------------------------------
# Arguments: ["string","var_server_name"],["string","var_user_name"],["password","var_password"],["string","file_name"]
# Check if all databases are connectable
# ------------------------------------------------------------------------------------------
class Database_db2_check_connectivity(Bot):


	previous_status = None
	previous_output = None

	def bot_init(self):
		self.previous_status = ''
		self.previous_output = 	''

		sys.path.append(r"./Dependencies")
		

	def exeecute(self,executeContext):
		self.previous_status,arg_dict = readArguments('Script expects arguments')
		if self.previous_status != 'OK':
			checkExit(1)
		if "var_server_name" in arg_dict:
			var_server_name = arg_dict["var_server_name"]
		else:
			printMsg('Missing argument: var_server_name','ERROR')
			checkExit(1)
		if "var_user_name" in arg_dict:
			var_user_name = arg_dict["var_user_name"]
		else:
			printMsg('Missing argument: var_user_name','ERROR')
			checkExit(1)
		if "var_password" in arg_dict:
			var_password = arg_dict["var_password"]
		else:
			printMsg('Missing argument: var_password','ERROR')
			checkExit(1)
		if "file_name" in arg_dict:
			file_name = arg_dict["file_name"]
		else:
			printMsg('Missing argument: file_name','ERROR')
			checkExit(1)
		self.previous_status,self.previous_output = readFile(file_name)
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = textToArray(str(self.previous_output),r'\n')
		if self.previous_status != 'OK':
			checkExit(1)
		printMsg('For each loop','INFO')
		for var_foreach in str(self.previous_output).split(','):
			self.previous_output = var_foreach
			printMsg('Loop: '+str(self.previous_output),'INFO')
			self.previous_status,self.previous_output = connectDB(r'oracle',str(self.previous_output),str(var_server_name),1433,str(var_user_name),str(var_password))
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Return value: '+str(self.previous_output))
			if self.previous_output and re.search('OK',str(self.previous_output)):
				printMsg('IF condition matches','INFO')
				self.previous_status,self.previous_output = printMsg(str(self.previous_output),r'IMP',r'NA')
				if self.previous_status != 'OK':
					checkExit(1)
			else:
				printMsg('ELSE condition','INFO')
				self.previous_status,self.previous_output = printMsg(str(self.previous_output),r'IMP',r'NA')
				if self.previous_status != 'OK':
					checkExit(1)
		printMsg('Exiting.','INFO')
		checkExit(0)

		return 'success'


# --for testing--
if __name__ == "__main__":
	context = {}
	db_obj = Database_db2_check_connectivity()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)