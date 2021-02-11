'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import sys, re, os
import paramiko
import telnetlib
from winrm.protocol import Protocol
from abstract_bot import Bot

class AddUserInWindowsAD(Bot):


    def bot_init(self):
        pass

    def executeServer(self,cmd_to_execute):
        try:
            return_text = ''
            cmd_to_execute = cmd_to_execute.replace("\\'","'")
            
            remote_connection = Protocol(
                            endpoint=winrm_http+r'://'+serverName+':'+
                            str(rem_port)+'/wsman',transport=winrm_type,
                            username=userName,password=var_server_password,
                            server_cert_validation='ignore')
            shell_id = remote_connection.open_shell()

            sub = remote_connection.run_command(shell_id,cmd_to_execute)
            sub_out, sub_err, ret_code = remote_connection.get_command_output(shell_id,sub)
            remote_connection.cleanup_command(shell_id,sub)
            std_err = sub_err.decode("utf-8",errors='ignore')
            return_text = sub_out.decode("utf-8",errors='ignore')
            
            std_err = std_err.strip()
            if std_err:
                print('Remote execution error: '+str(std_err),'ERROR')
                return 'NOK','Remote execution error: '+str(std_err)
            
            return_text = return_text.strip()
            print('Remote command executed: '+str(cmd_to_execute),'INFO')
            print(str(return_text))
            return 'OK',return_text
        except Exception as e:
            print('Remote execution exception: '+str(e),'ERROR')
            return 'NOK',str(e)

    def connectServer(self,conn_type,server_name,rem_port,user_name='NA',pass_word='NA'):
        winrm_http = 'http'
        winrm_type = 'ntlm'

        try:
            remote_connection = Protocol(
                            endpoint=winrm_http+r'://'+server_name+':'+
                            str(rem_port)+'/wsman',transport=winrm_type,
                            username=user_name,password=pass_word,
                            server_cert_validation='ignore')
            shell_id = remote_connection.open_shell()
            print('Remote connection made: '+str(server_name),'INFO')
            return 'OK','Remote connection made: '+str(server_name)
        except Exception as e:
            print('Remote connection exception: '+str(e),'ERROR')
            return 'NOK',str(e)
   
    def execute(self, executeContext):
        try:
            serverName = executeContext["serverName"]
            userName = executeContext["userName"]
            password = executeContext["password"]
            adGroupName = executeContext["adGroupName"]
    
            previous_status,previous_output = self.connectServer(r'winrm',str(serverName),22,str(userName),str(password))
            if previous_status != 'OK':
                 return ("Status Failed")
            previous_status,previous_output = self.executeServer(r'powershell "get-adgroup -identity '+str(adGroupName)+r'"')
            if previous_status != 'OK':
                return ("Status Failed")
            var_check = str(previous_output)
            print('Return value: '+str(previous_output))
            if var_check and re.search('False',str(var_check),re.IGNORECASE):
                print('IF condition matches','INFO')
                previous_status,previous_output = self.executeServer(r'powershell "New-adgroup -Name '+str(adGroupName)+r' -GroupScope DomainLocal -GroupCategory Distribution"')
                if previous_status != 'OK':
                	return ("Status Failed")
                previous_status,previous_output = print(r'Created DL and Added users ',r'IMP',r'NA')
                if previous_status != 'OK':
                    return ("Status Failed")
                print('Exiting.','INFO')
            else:
                print('ELSE condition','INFO')
                previous_status,previous_output =print(r'DL Group already exist',r'IMP',r'NA')
                if previous_status != 'OK':
                    return ("Status Failed")
        except Exception as e:
            print('Aborting!','ERROR')
            return 'NOK',str(e)
            
        
        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = AddUserInWindowsAD()

    context = {
        'serverName':'',
        'userName' : '',
		'password' : '',
		'adGroupName':''
        }

    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
