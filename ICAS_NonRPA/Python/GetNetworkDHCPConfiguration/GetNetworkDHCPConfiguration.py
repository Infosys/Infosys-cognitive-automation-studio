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

# Bot will check the Network DHCP Configuration
class GetNetworkDHCPConfiguration(Bot):
    networkConnection=''
    def bot_init(self):
        pass
    def execute(self,executionContext):
        
        userName=executionContext["userName"]
        password=executionContext["password"]
      
             
        def connectNetwork(connType,hostName,remPort,enableMode='NO',userName='NA',password='NA'):
            networkType = connType.lower()
            deviceName = hostName.lower()
            networkConnection = netmiko.ConnectHandler(device_type=networkType,ip=hostName,port=remPort,
                                                        username=userName,password=password,secret=password)
            if enableMode != 'NO':
                networkConnection.enable()
            print('Network connection made: '+str(hostName))
       
        def executeNetwork(cmdToExecute,configChange='NO'):
            networkConnection = netmiko.ConnectHandler(device_type=r'cisco_ios',ip=r'device01',port=22,
                                                        username=executionContext['userName'],
                                                        password=executionContext['password'],
                                                        secret=executionContext['password'])

            return_text = ''
            cmdToExecute = cmdToExecute.replace("\\'","'")
            if configChange == 'NO':
                if networkConnection.check_config_mode():
                    networkConnection.exit_config_mode()
            else:
                if not networkConnection.check_config_mode():
                    networkConnection.config_mode()
            return_text = networkConnection.send_command(cmdToExecute)
            
            return_text = return_text.strip()
            print('Network command executed: '+str(cmdToExecute))
            return return_text
        try:
            #connecting to network 
            connectNetwork(r'cisco_ios',r'device01',22,r'NO',r'userName',r'password')
        except Exception as e:
            print('Network connection exception: '+str(e))
            return {'output':'Error while connecting to network: '+str(e)}
        try:
            #executing network all the commands 
            #once all are successfully run DHCP Pool configuration is Success
            temp1=executeNetwork(r'ip dhcp excluded-address 192.168.101.254',r'YES')
            if temp1:
                temp2=executeNetwork(r'ip dhcp ping packets 3',r'YES')
            if temp2:
               temp3= executeNetwork(r'ip dhcp ping timeout 1000',r'YES')
            if temp3:
                temp4=executeNetwork(r'ip dhcp pool VOICE-LAN-Pool',r'YES')
            if temp4:
                temp5=executeNetwork(r'import all',r'YES')
            if temp5:
                temp6=executeNetwork(r'network 192.168.101.0 255.255.255.0',r'YES')
            if temp6:
                temp7=executeNetwork(r'default-router 192.168.101.254',r'YES')
            if temp7:
                temp8=executeNetwork(r'dns-server 8.8.8.8 4.4.4.4',r'YES')
            if temp8:
                temp9=executeNetwork(r'option 42 ip 192.168.101.254',r'YES')
            if temp9:
                temp10=executeNetwork(r'option 150 ip 10.10.10.10 10.10.11.10',r'YES')
            if temp10:
                temp11=executeNetwork(r'option 66 ascii dms.xyzbusiness.abc.com',r'YES')
            if temp11:
                temp12=executeNetwork(r'option 160 ascii http://poldms.xyzbusiness.abc.com/dms/bootstrap',r'YES')
            if temp13:
                temp13=executeNetwork(r'lease 7',r'YES')
            if temp14:
                temp_out= executeNetwork(r'show run | include dhcp',r'NO')
            if temp_out and re.search('dhcp',str(temp_out),re.IGNORECASE):
                return {'output':'SUCCESS:-DHCP pool config done'}
            else:
                return {'output':'FAILURE:-DHCP pool config error'}

        except Exception as e:
            return {'output':'Error while executing network dhcp commands: '+str(e)}

if __name__=="__main__":
    context={}
    bot_obj=GetNetworkDHCPConfiguration()
    
    context = {'userName':'','password':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)