'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
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
class AddDiskSpaceInLinux(Bot):
    #method to initialise 
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
        
            serverName=executionContext["serverName"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            partitionName=executionContext["partitionName"]
            partitionSize=executionContext["partitionSize"]

            if serverName=="":
                return{"Missing argument" : "serverName"}
            if userName=="":
                return{"Missing argument" : "userName"}
            if password=="":
                return{"Missing argument" : "password"}
            if partitionName=="":
                return{"Missing argument" : "partitionName"}
            if partitionSize=="":
                return {"Missing argument" : "partitionSize"}

            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            
            if partitionSize.lower()=="max":
                stdin,stdout,stderr=ssh.exec_command('sudo resize2fs "'+partitionName+'"')
                outlines=stdout.readlines()
                result=''.join(outlines)
                #print(result)
                ssh.close()
                return {'Status': 'Success'}
            else:
                stdin,stdout,stderr=ssh.exec_command('sudo resize2fs "'+partitionName+'" "'+partitionSize+'"')
                outlines=stdout.readlines()
                result=''.join(outlines)
                #print(result)
                ssh.close()
                return {'Status': 'Success'}
                        
        except Exception as e:
            return {'Exception':str(e)}
          

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = AddDiskSpaceInLinux()
    #giving parameter as a dictinoary
    context = {'serverName':'',         #enter the IP address of the server to connect to
               'userName':'',           #enter the username        
               'password':'',           #enter the password
               'partitionName':'',      #enter the name of partition.
               'partitionSize':''}      #enter the size of partition which is required. Either enter as 'max' or specify the value required.
                                        #size should be in whole numbers like 25G, or 50M. For sizes like 25.4 GB, enter 25400M
    '''
    #Sample Data
    context = {'serverName':'10.67.87.198',
               'userName':'admin',    
               'password':'secret',
               'partitionName':'/dev/sda1',
               'partitionSize':'20G'}
    '''
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)     