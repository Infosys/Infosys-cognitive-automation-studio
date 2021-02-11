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

# Bot is used to add a user to DL on a window server.

class ModifyOwnerDLInWindows(Bot):


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
			print ('Connect Server Error')
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
				return {'Exception' : str(std_err)}
			
			return_text = return_text.strip()
			print('Execute server connection OK: '+str(cmd_to_execute),'INFO')
			print(str(return_text))
			return 'OK',return_text
		except Exception as e:
			print('Execute server connection error: '+str(e),'ERROR')
			return {'Exception' : str(e)}

   
	def execute(self, executeContext):
	   
		varServerName = executeContext["varServerName"]
		if not varServerName:
			return {'validation error' : 'missing varServerName'}

		varUserName = executeContext["varUserName"]
		if not varUserName:
			return {'validation error' : 'missing varUserName'}

		varAdGroupName = executeContext["varAdGroupName"]
		if not varAdGroupName:
			return {'validation error' : 'missing varAdGroupName'}

		varAdUserName = executeContext["varAdUserName"]
		if not varAdUserName:
			return {'validation error' : 'missing varAdUserName'}

		varServerPassword = executeContext["varServerPassword"]
		if not varServerPassword:
			return {'validation error' : 'missing varServerPassword'}

		try:
			connect_status,connect_output = self.connectServer(r'winrm',str(varServerName),22,str(varUserName),str(varServerPassword))
			execute_status,execute_output = self.executeServer(r'powershell "get-adgroup -identity '+str(varAdGroupName)+r'"',str(varServerName),str(varUserName),str(varServerPassword))
			if connect_status =='OK' and execute_status =='OK':
				var_check = str(previous_output)
				print('Return value: '+str(previous_output))
				if var_check and re.search('True',str(var_check),re.IGNORECASE):
					print('IF condition matches','INFO')
					execute_status,execute_output = executeServer(r'powershell "set-adgroup -Identity '+str(varAdGroupName)+r' -managedby '+str(varAdUserName)+r'"')
					if execute_status == 'OK':
						execute_status,execute_output = print(r'Modified the user in DL',r'IMP',r'NA')
						return {'status' : 'success'}
				else:
					print('ELSE condition','INFO')
					previous_status,previous_output = print(r'User does not exist in AD ',r'IMP',r'NA')
					return {'status' : 'User does not exists in AD'}
			return {'execute_output':execute_output}
		except Exception as e:
			return {'Exception':str(e)}
	  

			
	
if __name__ == '__main__':
	context = {}
	output = {}
	obj_snow = ModifyOwnerDLInWindows()

	context = {
		
		'varServerName':'',
		'varUserName' : '',
		'varServerPassword' : '',
		'varAdUserName' : '',
		'varAdGroupName' : '',
		}

	obj_snow.bot_init()
	output = obj_snow.execute(context)
	print(output)
