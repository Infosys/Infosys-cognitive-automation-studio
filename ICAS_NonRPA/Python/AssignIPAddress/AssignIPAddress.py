'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import wmi
from abstract_bot import Bot

#Bot to assign new IP address to a windows server

class AssignIPAddress(Bot):
    
    def bot_init(self):
        pass

        
    def execute(self,executionContext):
        try:
        
            oldIPAddress = executionContext['oldIPAddress']
            userName = executionContext['userName']
            passWord = executionContext['passWord']
        
            newIPAddress=executionContext['newIPAddress']
            newSubnetmask=executionContext['newSubnetmask']
            newGateway=executionContext['newGateway']
            
            if oldIPAddress=='':
                return{'Missing Argument':'oldIPAddress'}
            if userName=='':
                return{'Missing Argument':'userName'}
            if passWord=='':
                return{'Missing Argument':'passWord'}
            if newIPAddress=='':
                return{'Missing Argument':'newIPAddress'}
            if newSubnetmask=='':
                return{'Missing Argument':'newSubnetmask'}
            if newGateway=='':
                return{'Missing Argument':'newGateway'}

            print('Establishing connection to {0}'.format(oldIPAddress))
            print('userName: {0}'.format(userName))
            connection = wmi.WMI(oldIPAddress, user=userName, password=passWord)  #to connect with a remote server
            print('Connection established')
            
            nic_configs = connection.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            #print(nic_configs)
                       
            nic = nic_configs[0]  # First network adaptor

            # Setting the new values for IP address, subnetmask and default gateway
            nic.EnableStatic(IPAddress=[newIPAddress],SubnetMask=[newSubnetmask])
            nic.SetGateways(DefaultIPGateway=[newGateway])
            
            return{'Status':'Success'}
           
        except Exception as e:
            return {'Exception' : str(e)}
    

if __name__ == "__main__":
    context = {}
    bot_obj = AssignIPAddress()

    context = {'oldIPAddress':'',
                'userName':'',
                'passWord':'',
                'newIPAddress':u'',             # New IP address, subnetmask and gateway values should be unicode objects
                'newSubnetmask':u'',
                'newGateway':u''
                }
    '''
    # Sample Values for input variables
    
    context = {'oldIPAddress':'10.85.54.210',
                'userName':'admin',
                'passWord':'secret',
                'newIPAddress':u'10.85.65.144',
                'newSubnetmask':u'255.255.0',
                'newGateway':u'10.85.65.1'
                }
    '''

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)  
