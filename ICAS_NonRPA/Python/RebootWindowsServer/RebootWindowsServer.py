'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
import wmi
from socket import *
#Bot to reboot a windows server
class RebootWindowsServer(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            varServerName = executionContext["varServerName"] #IP address of other remote server
            varUserName = executionContext["varUserName"] #Username
            varPassword = executionContext["varPassword"] #Password
            if varServerName is None:
                return {'Missing Argument':'varServerName'}
            if varUserName is None:
                return {'Missing Argument':'varUserName'}
            if varPassword is None:
                return {'Missing Argument':'varPassword'}
            print('Establishing connection to {0}'.format(varServerName))
            print('Username: {0}'.format(varUserName))
            connection = wmi.WMI(varServerName, user = varUserName, password = varPassword) #Connection with the remote server
            print('Connection established')
            remote_machine = (getfqdn(varServerName)) #Method to get the name of the server using IP
            #Process to reboot the server
            os = wmi.WMI(computer = remote_machine,privileges=["RemoteShutdown"])
            server = os.Win32_OperatingSystem (Primary=1)[0]
            server.Reboot()
            restart = wmi.WMI (varServerName, user = varUserName, password = varPassword)
            if restart!=None:
                result = remote_machine + ' has been successfully rebooted.'
            return {'Result' : result}
        except wmi.x_wmi as e:
            print('Your Username and Password of '+getfqdn(varServerName)+' are wrong or remote access is not enabled or remote server is not active.')
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = RebootWindowsServer()
    context = {'varServerName':'','varUserName':'','varPassword':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)