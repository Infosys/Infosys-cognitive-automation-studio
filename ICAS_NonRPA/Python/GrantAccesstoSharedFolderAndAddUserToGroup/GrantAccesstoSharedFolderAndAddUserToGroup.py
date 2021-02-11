'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import winrm
from winrm.protocol import Protocol
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot for adding user to group and granting shared folder access
class GrantAccesstoSharedFolderAndAddUserToGroup(Bot):

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

    def execute(self,executionContext):
        try:
            group = executionContext["group"] 
            user = executionContext["user"]
            shareName = executionContext["shareName"]
            permission = executionContext["permission"]
            varServerName = executeContext["varServerName"]
			varUserName = executeContext["varUserName"]
			varPassword = executeContext["varPassword"]
            if not varServerName:
				return {'Warning' : 'Missing varServerName'}
            if not varUserName:
				return {'Warning' : 'Missing varUserName'}
			if not varPassword:
				return {'Warning' : 'Missing varPassword'}  
            if not group:
                return {'Warning': 'group can not be empty'}
            if not user:
                return {'Warning': 'user can not be empty'}
            if not shareName:
                return {'Warning': 'shareName can not be empty'}
            if not permission:
                return {'Warning': 'permission can not be empty'}
            previous_status,previous_output = self.connectServer(r'winrm',str(varServerName),22,str(varUserName),str(varPassword))
			if previous_status != 'OK':
				return {'Validation Error' : 'Status failed'}
            previous_status,previous_output = self.executeServer(r'powershell "Add-ADGroupMember -Identity '+str(group)+ ' -Members ' + str(user) + r'"',str(varServerName),str(varUserName),str(varPassword))
            if previous_status != 'OK':
				return {'Validation Error' : 'Status failed'}
			else: 
                previous_status,previous_output = self.executeServer(r'powershell "Grant-SmbShareAccess -Name '+str(shareName)+ ' -AccountName ' + str(user) +' -AccessRight '+str(permission)+' -Force'+ r'"',str(varServerName),str(varUserName),str(varPassword))
                if previous_status != 'OK':
				    return {'Validation Error' : 'Status failed'}
			    else: 
                    return {'Status':'User has been added to the group and shared folder permission granted'}
        except Exception as e:
            return {'Exception' : str(e)} 

if __name__ == "__main__":
    context = {}
    bot_obj = GrantAccesstoSharedFolderAndAddUserToGroup()
    context = {'varServerName':'',varPassword':'','group':'','user':'','shareName':'','permission':''}
    #'permission' : 'Change' or 'Custom' or 'Full' or 'Read'
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)