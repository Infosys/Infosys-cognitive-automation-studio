'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20180306, by: rajesh.kella
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
from Ops_Conn import *
from abstract_bot import Bot
# ------------------------------------------------------------------------------------------
# Arguments: ["string","var_db_name"],["string","var_server_name"],["string","var_user_name"],["string","var_threshold_warning"],["password","var_password"]
# Check if backups were executed or not in DB2 DATABASE (need to check the regex pattern match)
# ------------------------------------------------------------------------------------------
class Database_db2_check_backup_failure(Bot):


	previous_status = None
	previous_output = None

	def bot_init(self)
		self.previous_status = ""
		self.previous_output = ""

		sys.path.append(r"./Dependencies")
		

	def execute(self, executeContext):
		self.previous_status,arg_dict = readArguments('Script expects arguments')
		if self.previous_status != 'OK':
			checkExit(1)
		if "var_db_name" in arg_dict:
			var_db_name = arg_dict["var_db_name"]
		else:
			printMsg('Missing argument: var_db_name','ERROR')
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
		if "var_threshold_warning" in arg_dict:
			var_threshold_warning = arg_dict["var_threshold_warning"]
		else:
			printMsg('Missing argument: var_threshold_warning','ERROR')
			checkExit(1)
		if "var_password" in arg_dict:
			var_password = arg_dict["var_password"]
		else:
			printMsg('Missing argument: var_password','ERROR')
			checkExit(1)
		self.previous_status,self.previous_output = connectDB(r'db2',str(var_db_name),str(var_server_name),1433,str(var_user_name),str(var_password))
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = executeDB(r'select 1 from sysibmadm.SNAPDB where LAST_BACKUP > current timestamp - '+str(var_threshold_warning)+r' days')
		if self.previous_status != 'OK':
			checkExit(1)
		printMsg('Return value: '+str(self.previous_output))
		if self.previous_output and re.search('1',str(self.previous_output),re.IGNORECASE):
			printMsg('IF condition matches','INFO')
			self.previous_status,self.previous_output = printMsg(r'Backup on DB '+str(var_db_name)+r' was completed successfully in the last '+str(var_threshold_warning)+r' days',r'IMP',r'NA')
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Exiting.','INFO')
			checkExit(0)
		else:
			printMsg('ELSE condition','INFO')
			self.previous_status,self.previous_output = printMsg(r'NO BACKUP in the last '+str(var_threshold_warning)+r' days',r'IMP',r'NA')
			if self.previous_status != 'OK':
				checkExit(1)
			printMsg('Aborting!','ERROR')
			checkExit(1)

# --for testing--
if __name__ == "__main__":
	context = {}
	db_obj = Database_db2_check_backup_failure()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)