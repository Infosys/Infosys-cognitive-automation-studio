'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
from abstract_bot import Bot
import netmiko

# Network bandwidth configuration

class ConfigNetworkBandwidth(Bot):
    
    def bot_init(self):
        pass
        
        
    def execute(self,executionContext):
        # Arguments: ["string","bandwidthSize"]
        
        try:
            if "bandwidthSize" in executionContext:
                bandwidthSize = executionContext["bandwidthSize"]
            else:
                print('Missing argument: bandwidthSize','ERROR')
                return 'failure'
            
            
            network_connection = netmiko.ConnectHandler(device_type=r'cisco_ios',ip=r'device01',port=22,username=executionContext['userName'],password=executionContext['passWord'],secret=executionContext['passWord'])
        
            # Not sure below about enable method is to exexute or not
            #network_connection.enable()
        


            #previous_status,previous_output = executeNetwork(r'policy-map Shaping',r'YES')
            if not network_connection.check_config_mode():
                network_connection.config_mode()
            return_text = network_connection.send_command(r'policy-map Shaping')
            return_text = return_text.strip()
            
            #previous_status,previous_output = executeNetwork(r'description *** Shaping***',r'YES')
            if not network_connection.check_config_mode():
                network_connection.config_mode()
            return_text = network_connection.send_command(r'description *** Shaping***')
            return_text = return_text.strip()
            
            
            #previous_status,previous_output = executeNetwork(r'class class-default',r'YES')
            if not network_connection.check_config_mode():
                network_connection.config_mode()
            return_text = network_connection.send_command(r'class class-default')
            return_text = return_text.strip()

            #previous_status,previous_output = executeNetwork(r'shape average 2000000',r'YES')
            if not network_connection.check_config_mode():
                network_connection.config_mode()
            return_text = network_connection.send_command(r'shape average 2000000')
            return_text = return_text.strip()

            #previous_status,previous_output = executeNetwork(r'Show policy-map shaping',r'NO')
            if network_connection.check_config_mode():
                network_connection.exit_config_mode()
            return_text = network_connection.send_command(r'Show policy-map shaping')
            return_text = return_text.strip()


            if return_text and re.search('shape average 2000000',str(return_text),re.IGNORECASE):
                print('IF condition matches','INFO')
                #previous_status,previous_output = executeNetwork(r'interface GigabitEthernet0/0',r'YES')
                if not network_connection.check_config_mode():
                    network_connection.config_mode()
                return_text = network_connection.send_command(r'interface GigabitEthernet0/0')
                return_text = return_text.strip()

                #previous_status,previous_output = executeNetwork(r'bandwidth '+str(bandwidthSize)+r'',r'YES')
                if not network_connection.check_config_mode():
                    network_connection.config_mode()
                return_text = network_connection.send_command(r'bandwidth '+str(bandwidthSize)+r'')
                return_text = return_text.strip()

                #previous_status,previous_output = executeNetwork(r'service-policy output Shaping',r'YES')
                if not network_connection.check_config_mode():
                    network_connection.config_mode()
                return_text = network_connection.send_command(r'service-policy output Shaping')
                return_text = return_text.strip()

                #previous_status,previous_output = executeNetwork(r'show run int gi 0/0',r'NO')
                if network_connection.check_config_mode():
                    network_connection.exit_config_mode()
                return_text = network_connection.send_command(r'show run int gi 0/0')
                return_text = return_text.strip()

                
                if return_text and re.search('bandwidth 2048',str(return_text),re.IGNORECASE):
                    print('IF condition matches','INFO')
                    print('Exiting.','INFO:', 'Bandwidth config successful')
                    return { 'output':"success"}
                else:
                    printMsg('ELSE condition','INFO')
                    print('Aborting!','ERROR:', 'Bandwidth config failed')
                    return { 'output':'failure'}
            else:
                print('ELSE condition','INFO')
                print('Aborting!','ERROR:', 'Policy mapping shaping failed')
                return { 'output':'failure'}
        except Exception as e:
            print('Aborting!', "ERROR: ", e)
            return { 'output':'failure'}

        
    
    

if __name__=="__main__":
    context={}
    bot_obj=ConfigNetworkBandwidth()
    
    context = {'bandwidthSize': '','userName': '' , 'passWord': ''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)    

