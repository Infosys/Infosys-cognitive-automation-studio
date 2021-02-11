'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import winrm
from winrm.protocol import Protocol
from abstract_bot import Bot

class CreateServiceIdInAD(Bot):


	def bot_init(self):
		pass

	def get_remote_connection (self, varServerName, varPassword, varUserName):
		try:
			winrm_http = 'http'
			winrm_type = 'ntlm'
			rem_port= 22

			remote_connection = Protocol(
				endpoint=winrm_http+r'://'+varServerName+':'+str(rem_port)+'/wsman',
				transport=winrm_type,
				username=varUserName,
				password=varPassword,
				server_cert_validation='ignore')
			return remote_connection
		except Exception as e:
			print ('Remote connection Error')
			return {'Exception' : str(e)}

	def connectServer(self,conn_type,server_name,rem_port,user_name='NA',pass_word='NA'):
		try:
			remote_connection = self.get_remote_connection(server_name, pass_word, user_name)
			print('Connect Server OK: '+str(server_name),'INFO')
			return 'OK','Connect Server OK: '+str(server_name)
		except Exception as e:
			print ('connect Server Error')
			return {'Exception' : str(e)}

	def executeServer(self,cmd_to_execute, varServerName, varUserName, varPassword):
		print (cmd_to_execute, varServerName, varPassword, varUserName)
		try:
			return_text = ''
			cmd_to_execute = cmd_to_execute.replace("\\'","'")
			
			remote_connection = self.get_remote_connection(varServerName, varPassword, varUserName)
			shell_id = remote_connection.open_shell()
			sub = remote_connection.run_command(shell_id,cmd_to_execute)
			sub_out, sub_err, ret_code = remote_connection.get_command_output(shell_id,sub)
			remote_connection.cleanup_command(shell_id,sub)
			std_err = sub_err.decode("utf-8",errors='ignore')
			return_text = sub_out.decode("utf-8",errors='ignore')
			
			std_err = std_err.strip()
			if std_err:
				print('Execute server connection error: '+str(std_err),'ERROR')
				return {'validation error' : str(std_err)}
			
			return_text = return_text.strip()
			print('Execute server connection OK: '+str(cmd_to_execute),'INFO')
			print(str(return_text))
			return 'OK',return_text
		except Exception as e:
			print ('Execute Server  Error')
			return {'Exception' : str(e)}

   
	def execute(self, executeContext):
		try:
			varServerName = executeContext["varServerName"]
			if not varServerName:
				return {'validation error' : 'missing varServerName'}

			varUserName = executeContext["varUserName"]
			if not varUserName:
				return {'validation error' : 'missing varUserName'}

			serviceAccount = executeContext["serviceAccount"]
			if not serviceAccount:
				return {'validation error' : 'missing serviceAccount'}

			dnsHostName = executeContext["dnsHostName"]
			if not dnsHostName:
				return {'validation error' : 'missing dnsHostName'}

			varPassword = executeContext["varPassword"]
			if not varPassword:
				return {'validation error' : 'missing varPassword'}

			previous_status,previous_output = self.connectServer(r'winrm',str(varServerName),22,str(varUserName),str(varPassword))
			if previous_status != 'OK':
				return {'validation error' : 'status failed'}
			previous_status,previous_output = self.executeServer(r'powershell "new-adserviceaccount -name '+str(serviceAccount)+ ' -dnshostname ' + str(dnsHostName) + r'"',str(varServerName),str(varUserName),str(varPassword))

			if previous_status != 'OK':
				return {'validation error' : 'status failed'}
			else:
				return {'status' : 'success'}

		except Exception as e:
			return {'Exception' : str(e)}
		
	
	
if __name__ == '__main__':
	context = {}
	obj_snow = CreateServiceIdInAD()

	context = {
		'varServerName':'',
		'varUserName' : '',
		'varPassword' : '',
        'serviceAccount' : '',
		'dnsHostName' : '',
		}

	obj_snow.bot_init()
	output = obj_snow.execute(context)
	print(output)
