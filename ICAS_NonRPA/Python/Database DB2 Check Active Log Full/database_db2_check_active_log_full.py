'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20181105, by: vinay.reddy
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
from Ops_Conn import *
from abstract_bot import Bot
# ------------------------------------------------------------------------------------------
# Arguments: ["string","var_user_name"],["string","var_server_name"],["string","var_db_name"],["password","var_password"]
# Checks db2 Activity Log Status
# ------------------------------------------------------------------------------------------
class Database_db2_check_active_log_full(Bot):


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
		if "var_user_name" in arg_dict:
			var_user_name = arg_dict["var_user_name"]
		else:
			printMsg('Missing argument: var_user_name','ERROR')
			checkExit(1)
		if "var_server_name" in arg_dict:
			var_server_name = arg_dict["var_server_name"]
		else:
			printMsg('Missing argument: var_server_name','ERROR')
			checkExit(1)
		if "var_db_name" in arg_dict:
			var_db_name = arg_dict["var_db_name"]
		else:
			printMsg('Missing argument: var_db_name','ERROR')
			checkExit(1)
		if "var_password" in arg_dict:
			var_password = arg_dict["var_password"]
		else:
			printMsg('Missing argument: var_password','ERROR')
			checkExit(1)
		self.previous_status,self.previous_output = connectServer(r'ssh',str(var_server_name),22,str(var_user_name),str(var_password))
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = executeServer(r'db2 get db cfg for '+str(var_db_name)+r' |grep LOGPRIMARY | awk -F"= " \\'{print $2}\\' |tail -1')
		if self.previous_status != 'OK':
			checkExit(1)
		var_logpri = self.previous_output
		self.previous_status,self.previous_output = executeServer(r'db2 get db cfg for '+str(var_db_name)+r' |grep LOGSECOND |awk -F"= " \\'{print $2}\\' |tail -1')
		if self.previous_status != 'OK':
			checkExit(1)
		var_logsec = self.previous_output
		self.previous_status,self.previous_output = executeServer(r'db2 get db cfg for '+str(var_db_name)+r' |grep "Path to log files" |awk -F"= " \\'{print $2}\\' |tail -1')
		if self.previous_status != 'OK':
			checkExit(1)
		var_logpath = self.previous_output
		self.previous_status,self.previous_output = executeServer(r'ls -l '+str(var_logpath)+r'*LOG |wc -l')
		if self.previous_status != 'OK':
			checkExit(1)
		var_logused = self.previous_output
		var_tmp_cal=var_logpri+(var_logsec/2)
		printMsg('Return value: '+str(self.previous_output))
		if var_logused and int(var_logused) < int(var_tmp_cal):
			printMsg('IF condition matches','INFO')
			self.previous_status,self.previous_output = printMsg(r'DB2 - The transaction log utilization is OK!',r'IMP',r'NA')
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Exiting.','INFO')
			checkExit(0)
		else:
			printMsg('ELSE condition','INFO')
			self.previous_status,self.previous_output = printMsg(r'NOK, Please check database transaction workload',r'IMP',r'NA')
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Aborting!','ERROR')
			checkExit(1)

# --for testing--
if __name__ == "__main__":
	context = {}
	db_obj = Database_db2_check_active_log_full()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)