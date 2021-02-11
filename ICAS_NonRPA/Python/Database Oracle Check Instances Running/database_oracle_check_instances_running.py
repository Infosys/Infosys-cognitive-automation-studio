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
# Arguments: ["string","var_server_name"],["string","var_user_name"],["password","var_user_password"]
# check oracle database running status(checks number of instances running)
# ------------------------------------------------------------------------------------------
class Database_oracle_check_instances_running(Bot):


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
		if "var_user_password" in arg_dict:
			var_user_password = arg_dict["var_user_password"]
		else:
			printMsg('Missing argument: var_user_password','ERROR')
			checkExit(1)
		self.previous_status,self.previous_output = connectServer(r'ssh',str(var_server_name),22,str(var_user_name),str(var_user_password))
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = executeServer(r'ps -ef|grep "ora"|grep "pmon"|grep -v "grep"|wc -l')
		if self.previous_status != 'OK':
			checkExit(1)
		var_no_instances = self.previous_output
		var_no_instances = int(var_no_instances)
		printMsg('Return value: '+str(self.previous_output))
		if var_no_instances and int(var_no_instances) >= 1:
			printMsg('IF condition matches','INFO')
			self.previous_status,self.previous_output = printMsg(r''+str(var_no_instances)+r' instance(s) are running',r'IMP',r'NA')
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
	db_obj = Database_oracle_check_instances_running()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)