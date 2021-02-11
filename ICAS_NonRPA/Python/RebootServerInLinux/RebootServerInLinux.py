'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependency to be installed before running 
#pip install paramiko run this command to install dependency
import paramiko

from abstract_bot import Bot
#class for bot
class RebootServerInLinux(Bot):
    #method to initialise 
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        
        serverName =executionContext["serverName"]
        userName=executionContext["userName"]
        password=executionContext["password"]

        if serverName is None:
            return("Missing argument : serverName")
        if userName is None:
            return("Missing argument : userName")
        if password is None:
            return("Missing argument : password")

        try:              
            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            
            stdin,stdout,stderr=ssh.exec_command('echo "'+password+'" | sudo -S reboot')
            outlines=stdout.readlines()
            result=''.join(outlines)
            if result=='':
                output='Reboot Successful'
            ssh.close()
            return {'Status': output}
        
        except Exception as e:
        	return {'Exception':str(e)}
          

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = RebootServerInLinux()
    #giving parameter as a dictinoary
    context = {'serverName':'','userName':'','password':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)     