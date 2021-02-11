'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20180329, by: rajesh.kella
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
from Ops_Conn import *
from abstract_bot import Bot
# ------------------------------------------------------------------------------------------
# Arguments: ["string","var_db_name"],["string","var_server_name"],["string","var_user_name"],["password","var_password"]
# Script to check when will a SQL login password expire?
# ------------------------------------------------------------------------------------------
class Database_sql_when_password_expires(Bot):


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
		if "var_password" in arg_dict:
			var_password = arg_dict["var_password"]
		else:
			printMsg('Missing argument: var_password','ERROR')
			checkExit(1)
		self.previous_status,self.previous_output = connectDB(r'mssql',str(var_db_name),str(var_server_name),1433,str(var_server_name),str(var_password))
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = executeDB(r'SELECT SL.name AS LoginName,LOGINPROPERTY (SL.name, "PasswordLastSetTime") AS PasswordLastSetTime,LOGINPROPERTY (SL.name, "DaysUntilExpiration") AS DaysUntilExpiration,DATEADD(dd, CONVERT(int, LOGINPROPERTY (SL.name, "DaysUntilExpiration")),CONVERT(datetime, LOGINPROPERTY (SL.name, "PasswordLastSetTime"))) AS PasswordExpiration,SL.is_policy_checked AS IsPolicyChecked,LOGINPROPERTY (SL.name, "IsExpired") AS IsExpired,LOGINPROPERTY (SL.name, "IsMustChange") AS IsMustChange,LOGINPROPERTY (SL.name, "IsLocked") AS IsLocked,LOGINPROPERTY (SL.name, "LockoutTime") AS LockoutTime,LOGINPROPERTY (SL.name, "BadPasswordCount") AS BadPasswordCount,LOGINPROPERTY (SL.name, "BadPasswordTime") AS BadPasswordTime,LOGINPROPERTY (SL.name, "HistoryLength") AS HistoryLength FROM sys.sql_logins AS SL WHERE is_expiration_checked = 1 ORDER BY LOGINPROPERTY (SL.name, "PasswordLastSetTime") DESC')
		if self.previous_status != 'OK':
			checkExit(1)
		self.previous_status,self.previous_output = printMsg(str(self.previous_output),r'IMP',r'NA')
		if self.previous_status != 'OK':
			checkExit(1)
		printMsg('Exiting.','INFO')
		checkExit(0)

		return 'success'


if __name__ == "__main__":
	context = {}
	db_obj = Database_sql_when_password_expires()

	db_obj.bot_init()
	resp = db_obj.execute(context)

	print('response : ',resp)