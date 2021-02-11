'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20180330, by: vinay.reddy
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
from Ops_Conn import *
from abstract_bot import Bot 
# ------------------------------------------------------------------------------------------
# Arguments: ["string","var_server_name"],["string","var_user_name"],["password","var_password"]
# Check if db2 instance(s) running fine 
# ------------------------------------------------------------------------------------------
class Database_db2_instance_running_status(Bot):


	previous_status = None
	previous_output = None

	def bot_init(self):
		self.previous_status = ''
		self.previous_output = 	''

		sys.path.append(r"./Dependencies")


	def execute(self,executeContext):
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
		self.previous_status,self.previous_output = connectServer(r'ssh',str(var_server_name),22,str(var_user_name),str(var_password))
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = executeServer(r'ps -ef | awk \'BEGIN {QTDE=0} {if ($8 ~ /db2sysc/) {QTDE=QTDE+1}}END {print QTDE}\'')
		if self.previous_status != 'OK':
			checkExit(1)
		var_db2sysc = self.previous_output
		printMsg('Return value: '+str(self.previous_output))
		if var_db2sysc and int(var_db2sysc) == 0:
			printMsg('IF condition matches','INFO')
			self.previous_status,self.previous_output = printMsg(r'No instances are running',r'IMP',r'NA')
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Exiting.','INFO')
			checkExit(0)
		else:
			printMsg('ELSE condition','INFO')
			var_db2sysc_real=int(var_db2sysc[0])
			printMsg('Return value: '+str(self.previous_output))
			if var_db2sysc_real and int(var_db2sysc_real) >= 1:
				printMsg('IF condition matches','INFO')
				self.previous_status,self.previous_output = printMsg(r''+str(var_no_instances)+r' instance(s) running properly',r'IMP',r'NA')
				if self.previous_status != 'OK':
					checkExit(1)
				printMsg('Exiting.','INFO')
				checkExit(0)
			else:
				printMsg('ELSE condition','INFO')
				self.previous_status,self.previous_output = printMsg(r'No instances are running',r'IMP',r'NA')
				if self.previous_status != 'OK':
					checkExit(1)
				printMsg('Aborting!','ERROR')
				checkExit(1)

		return 'success'


# --for testing--
if __name__ == "__main__":
	context = {}
	db_obj = Database_db2_instance_running_status()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)