'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
import netmiko
from getpass import getpass
from abstract_bot import Bot


#Bot to connect to a Network from a Linux Server

class ExecuteNetworkcmdsInLinux(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        cmdToExecute = executionContext["cmdToExecute"]
        configChange = executionContext["configChange"]
        connType = executionContext["connType"]
        hostName = executionContext["hostName"]
        remPort = executionContext["remPort"]
        userName = executionContext["userName"]
        passWord = executionContext["passWord"]

        network_type = connType.lower()
        
        #ret_status = varValidate('string','cmdToExecute',cmdToExecute)
       
        #ret_status = varValidate('string','configChange',configChange)
        
        try:
            network_connection = netmiko.ConnectHandler(device_type=network_type,ip=hostName,port=remPort,username=userName,password=passWord,secret=passWord)
            if network_type == '':
                print('No active network session','ERROR')
                            
            return_text = ''
            cmdToExecute = cmdToExecute.replace("\\'","'")
            
            if configChange == 'NO':
                if network_connection.check_config_mode():
                    network_connection.exit_config_mode()
            else:
                if not network_connection.check_config_mode():
                    network_connection.config_mode()
            return_text = network_connection.send_command(cmdToExecute)
            
            return_text = return_text.strip()
            print('Network command executed: '+str(cmdToExecute),'INFO')
            print(str(return_text))
            return {'Command Executed': return_text}
        except Exception as e:
            print('Network execution exception: '+str(e),'ERROR')
            return {'Command not Executed': str(e)}


if __name__ == "__main__":
    context = {}
    bot_obj = ExecuteNetworkcmdsInLinux()

    context = {'cmdToExecute':'',
                'configChange':'',
                'connType' : '',
                'hostName' : '',
                'remPort' : '',
                'userName' : '',
                'passWord' : ''
                
                }

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)     