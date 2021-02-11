'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 18:44:03 2020

@author: anuj.gupta03
"""

import sys, re, os
import paramiko
import telnetlib
from winrm.protocol import Protocol
from abstract_bot import Bot

class ResetPasswordInWindowsAD(Bot):


    def bot_init(self):
        pass

    def executeServer(self,cmd_to_execute):
        try:
            return_text = ''
            cmd_to_execute = cmd_to_execute.replace("\\'","'")
            
            remote_connection = Protocol(
                            endpoint=winrm_http+r'://'+serverName+':'+
                            str(rem_port)+'/wsman',transport=winrm_type,
                            username=userName,password=varPassword,
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

    def connectServer(self,conn_type,serverName,rem_port,userName='NA',varPassword='NA'):
        winrm_http = 'http'
        winrm_type = 'ntlm'

        try:
            remote_connection = Protocol(
                            endpoint=winrm_http+r'://'+serverName+':'+
                            str(rem_port)+'/wsman',transport=winrm_type,
                            username=userName,password=varPassword,
                            server_cert_validation='ignore')
            shell_id = remote_connection.open_shell()
            print('Remote connection made: '+str(serverName),'INFO')
            return 'OK','Remote connection made: '+str(serverName)
        except Exception as e:
            print('Remote connection exception: '+str(e),'ERROR')
            return 'NOK',str(e)
        
    def execute(self, executeContext):
        try:
            serverName = executeContext["serverName"]
            userName = executeContext["userName"]
            varPassword = executeContext["varPassword"]
            varAdUserName = executeContext["varAdUserName"]
            varAdPassword=executeContext["varAdPassword"]
        
            previous_status,previous_output = self.connectServer(r'winrm',str(serverName),22,str(userName),str(varPassword))
		
		
            if previous_status != 'OK':
                return ("Status Failed")
        
        
            previous_status,previous_output = self.executeServer(r'powershell "Get-ADUser '+str(varAdUserName)+r'"')
		
            if previous_status != 'OK':
                return ("Status Failed")
		
            var_check_ad_user = str(previous_output)
		
            print('Return value: '+str(previous_output))
		
            if var_check_ad_user and re.search('True',str(var_check_ad_user),re.IGNORECASE):
			
                print('IF condition matches','INFO')
            
                previous_status,previous_output = executeServer(r'powershell "Set-adaccountpassword '+str(varAdUserName)+r' -reset -newpassword (ConvertTo-SecureString -AsPlainText '+str(varAdPassword)+r' -Force)"')
                if previous_status != 'OK':
                    return ("Status Failed")
                previous_status,previous_output = executeServer(r'powershell "Set-aduser '+str(varAdUserName)+r' -changepasswordatlogon $true"')
                if previous_status != 'OK':
                
		
                    return ("Status Failed")
                previous_status,previous_output = print(r'Password Resetted Sucessfully',r'IMP',r'NA')
                if previous_status != 'OK':
                    return ("Status Failed")
                
                
            else:
                print('ELSE condition','INFO')
                previous_status,previous_output = print(r'User is not present in AD group',r'ERROR',r'NA')
                if previous_status != 'OK':
                    return ("Status Failed")
                print('Aborting!','ERROR')
                return ("Status Failed")
        except Exception as e:
            print("Error occured",str(e)) 
            return str(e)

       
        
        
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = ResetPasswordInWindowsAD()

    context = {
        'serverName':'',
        'userName' : '',		
        'varPassword' : '',
        'varAdUserName':'',
		'varAdPassword':''

        }

    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
                
		
	
	
            
            
            
            
            
            
            
            
            
            