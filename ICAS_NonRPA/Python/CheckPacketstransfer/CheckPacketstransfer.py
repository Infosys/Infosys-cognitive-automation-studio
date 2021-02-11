'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

from netmiko import ConnectHandler
from abstract_bot import Bot
class CheckPacketstransfer(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        serverName =executionContext["serverName"]# Ip Address
        userName=executionContext["userName"]# User Name
        password=executionContext["password"]# Password

        if serverName == '':
            return ("Missing argument : serverName")
        if userName == '':
            return ("Missing argument : userName")
        if  password == '':
            return ("Missing argument :password")

        try:
            connection= ConnectHandler(device_type='cisco_ios',ip=serverName, username=userName, password=password)
            Output=connection.send_command("show interface if_type")
            print(Output)
            connection.disconnect()
            return{'Output':'Success'}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckPacketstransfer()
	#Enter your Ip Address, UserName and Password 
    context = {'serverName':'','userName':'','password':''}
    bot_obj.bot_init()
    OutputString=bot_obj.execute(context)
    print(OutputString)
    
