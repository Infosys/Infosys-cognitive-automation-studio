'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

#Dependency to be installed
from winrm import Protocol
from abstract_bot import Bot

class InstallDriverOnDB(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:
           
            serverName=executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']

            if serverName=="":
                return{"Missing argument":"serverName"}
            if userName=="":
                return{"Missing argument":"userName"}
            if password=="":
                return{"Missing argument":"password"}

    
            serverName='Http://'+serverName+':5985/wsman'
            session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            shell=session.open_shell()

            command=session.run_command(shell,"pip install mysql-connector-python")
            #For running this code on Infy network uncomment the below line and comment the above above line
            #command = session.run_command(shell,"pip install --user mysql-connector-python -i http://infynp.ad.infosys.com/repository/pypi-all/simple --trusted-host infynp.ad.infosys.com" )
            
            subOut,subErr,retCode =session.get_command_output(shell,command)
            session.cleanup_command(shell, command)
            session.close_shell(shell)
            print(str(subOut)+str(subErr))
            
            return{'Status':'Success'}
        
        except Exception as e:
        	return{'Exception':str(e)}
          

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = InstallDriverOnDB()
    
    context = {'serverName':'',     #enter the IP address of the remote windows server to connect to
               'userName':'',       #enter the username for the windows server
               'password':''        #enter the password for the windows server
               }
    '''
    #Sample data for input arguments
    context = {'serverName':'10.138.22.220',     
               'userName':'root', 
               'password':'secret' 
               }
    '''
    
    output = bot_obj.execute(context)
    print(output)     


  