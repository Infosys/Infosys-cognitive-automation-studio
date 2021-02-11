'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

from netmiko import ConnectHandler
from abstract_bot import Bot
class NetworkPacketTransferCheck(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        ServerName =executionContext["ServerName"]# Ip Address
        UserName=executionContext["UserName"]# User Name
        Password=executionContext["Password"]# Password

        if ServerName == '':
            return ("Missing argument : ServerName")
        if UserName == '':
            return ("Missing argument : UserName")
        if  Password == '':
            return ("Missing argument :Password")

        try:
            connection= ConnectHandler(device_type='cisco_ios',ip=ServerName, username=UserName, password=Password)
            Output=connection.send_command("show interface if_type")
            print(Output)
            connection.disconnect()
            return{'Output':'Success'}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = NetworkPacketTransferCheck()
	#Enter your Ip Address, UserName and Password 
    context = {'ServerName':'','UserName':'','Password':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)
    
