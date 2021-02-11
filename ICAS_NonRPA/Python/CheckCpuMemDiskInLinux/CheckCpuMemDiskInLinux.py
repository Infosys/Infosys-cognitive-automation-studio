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
class CheckCpuMemDiskInLinux(Bot):
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
          
            stdin,stdout,stderr=ssh.exec_command('cat /proc/meminfo | grep MemFree')
            outlines=stdout.readlines()
            freeMemory=''.join(outlines)
            #print (freeMemory)  #prints the free memory space in kB
            
            stdin,stdout,stderr=ssh.exec_command('top -bn1 | grep load')
            outlines=stdout.readlines()
            cpuLoad=''.join(outlines)
            #print ('CpuLoad: '+cpuLoad) #prints the Cpu Load stats 
            
            stdin,stdout,stderr=ssh.exec_command('df --output=source,avail -h /')
            outlines=stdout.readlines()
            diskAvail=''.join(outlines)
            #print (diskAvail) #prints the available disk size in Gb
            
            finalStats=freeMemory+'CpuLoad: '+cpuLoad+'DiskUsage: '+diskAvail
         
            ssh.close()
            return {'Output':finalStats}

        except Exception as e:
            return {'Exception':str(e)}
          

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = CheckCpuMemDiskInLinux()
    #giving parameter as a dictinoary
    context = {'serverName':'',
               'userName':'',
               'password':''
               }
              
    bot_obj.bot_init()

    output = bot_obj.execute(context)
    print(output)     