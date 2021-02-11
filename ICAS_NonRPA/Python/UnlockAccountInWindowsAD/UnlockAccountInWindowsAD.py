'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys
import re
import os
import winrm
from winrm.protocol import Protocol
from abstract_bot import Bot

# Bot is used to unlock user account from AD on a windows server.

class UnlockAccountInWindowsAD(Bot):


	def bot_init(self):
		pass

	def get_remote_connection (self, varServerName, varServerPassword, varUserName):
		try:
			winrm_http = 'http'
			winrm_type = 'ntlm'
			rem_port= 22

			remote_connection = Protocol(
				endpoint=winrm_http+r'://'+varServerName+':'+str(rem_port)+'/wsman',
				transport=winrm_type,
				username=varUserName,
				password=varServerPassword,
				server_cert_validation='ignore')
			return remote_connection
		except:
			print ('Remote connection Error')
			return {'Exception' : str(e)}

	def connectServer(self,conn_type,server_name,rem_port,user_name='NA',pass_word='NA'):
		try:
			remote_connection = self.get_remote_connection(server_name, pass_word, user_name)
			print('Connect Server OK: '+str(server_name),'INFO')
			return 'OK','Connect Server OK: '+str(server_name)
		except Exception as e:
			print ('connect server  Error')
			return {'Exception' : str(e)}

	def executeServer(self,cmd_to_execute, varServerName, varServerPassword, varUserName):
		print (cmd_to_execute, varServerName, varServerPassword, varUserName)
		try:
			return_text = ''
			cmd_to_execute = cmd_to_execute.replace("\\'","'")
			
			remote_connection = self.get_remote_connection(varServerName, varServerPassword, varUserName)
			shell_id = remote_connection.open_shell()
			sub = remote_connection.run_command(shell_id,cmd_to_execute)
			sub_out, sub_err, ret_code = remote_connection.get_command_output(shell_id,sub)
			remote_connection.cleanup_command(shell_id,sub)
			std_err = sub_err.decode("utf-8",errors='ignore')
			return_text = sub_out.decode("utf-8",errors='ignore')
			
			std_err = std_err.strip()
			if std_err:
				print('Execute server connection error: '+str(std_err),'ERROR')
				return 'NOK','Execute server connection error: '+str(std_err)
			
			return_text = return_text.strip()
			print('Execute server connection OK: '+str(cmd_to_execute),'INFO')
			print(str(return_text))
			return 'OK',return_text
		except Exception as e:
			print ('Execute Server Error')
			return {'Exception' : str(e)}

   
	def execute(self, executeContext):
		try:
			varServerName = executeContext["varServerName"]
			varUserName = executeContext["varUserName"]
			varServerPassword = executeContext["varServerPassword"]
			varAdUserName = executeContext["varAdUserName"]

			previous_status,previous_output = self.connectServer(r'winrm',str(varServerName),
													22,str(varUserName),str(varServerPassword))
			if previous_status != 'OK':
				return ("Status Failed")
			previous_status,previous_output = self.executeServer(r'powershell "Get-ADUser '+
										str(varAdUserName)+r' -Properties LockedOut | Select-Object LockedOut"',
											varServerName, varServerPassword, varUserName)
			if previous_status != 'OK':
				return ("Status Failed")
			var_check_ad_user = str(previous_output)
			print('Return value: '+str(previous_output))
			if var_check_ad_user and re.search('True',str(var_check_ad_user),re.IGNORECASE):
				print('IF condition matches')
				previous_status,previous_output = self.executeServer(r'powershell "Unlock-ADAccount -Identity '+
									str(varAdUserName)+r'"',  varServerName, varServerPassword, varUserName)
				if previous_status != 'OK':
					return ("Status Failed")
				previous_status,previous_output = print(r'User Account is Unlocked')
				if previous_status != 'OK':
					return ("Status Failed")
				print('Exiting INFO ')
				return {'status' : 'success'}
			else:
				print('ELSE condition','INFO')
				previous_status,previous_output = print(r'User Account is active')
				if previous_status != 'OK':
					checkExit(1)
				print('Aborting with error')
				return ("Status Failed")
		except Exception as e:
			print("Error occured",str(e)) 
			return {'Exception' : str(e)}

	
if __name__ == '__main__':
	context = {}
	output = {}
	obj_snow = UnlockAccountInWindowsAD()

	context = {
		'varServerName':'',
		'varUserName' : '',
		'varServerPassword' : '',
		'varAdUserName' : '',
		}

	obj_snow.bot_init()
	output = obj_snow.execute(context)
	print(output)
