'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#Dependency to be installed
from winrm import Protocol
from abstract_bot import Bot

class AddDiskSpaceInWindows(Bot):
    
    def bot_init_(self):
        pass
    #method for main logic execution
    def execute(self,executionContext):
        try:
           
            serverName=executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            driveName=executionContext['driveName']
            driveSize=executionContext['driveSize']

            if serverName=="":
                return{"Missing argument" : "serverName"}
            if userName=="":
                return{"Missing argument" : "userName"}
            if password=="":
                return{"Missing argument" : "password"}
            if driveName=="":
                return{"Missing argument" : "driveName"}
            if driveSize=="":
                return{"Missing argument" : "driveSize"}
          
    
            serverName='Http://'+serverName+':5985/wsman'
            session=Protocol(
                    endpoint=serverName,
                    transport='ntlm',
                    username=userName,
                    password=password,
                    server_cert_validation='ignore'
                    )
            
            if driveSize.lower()=="max":
                shell=session.open_shell()
                command = session.run_command(shell,'Powershell.exe \
                                              $size=Get-PartitionSupportedSize -DriveLetter "'+driveName+'";\
                                              Resize-Partition -DriveLetter "'+driveName+'" -Size $size.SizeMax ')
                subOut,subErr,retCode =session.get_command_output(shell,command)
                #print(str(subOut), str(subErr), str(retCode))
        
                session.cleanup_command(shell, command)
                session.close_shell(shell)
                return {'Output' : 'Success'}
            
            else:
                shell=session.open_shell()
                command = session.run_command(shell,'Powershell.exe \
                                              Resize-Partition -DriveLetter "'+driveName+'" -Size "'+driveSize+'"')
                subOut,subErr,retCode =session.get_command_output(shell,command)
                #print(str(subOut), str(subErr), str(retCode))
        
                session.cleanup_command(shell, command)
                session.close_shell(shell)
                return {'Output' : 'Success'}
        
        except Exception as e:
            return{'Exception' : str(e)}
          

      
        
if __name__ == "__main__":
    context = {}
    bot_obj = AddDiskSpaceInWindows()
    #Variable to be passed as argument 
    context = {'serverName':'',     #enter the IP address to connect to
               'userName':'',       #enter the username
               'password':'',       #enter the password
               'driveName':'',      #enter the driveName such as 'C', 'D'.
               'driveSize':''       #enter the new size required for the disk such as '50 GB'
               }
    '''    
    #Sample Data
    context = {'serverName':'10.85.90.200',        
               'userName':'admin',        
               'password':'secret',        
               'driveName':'C',        
               'driveSize':'20 GB'        
               }
    '''

   
    output = bot_obj.execute(context)
    print(output)     