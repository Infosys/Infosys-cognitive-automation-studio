'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

#dependency to be installed before running 
#pip install paramiko run this command to install dependency

import paramiko
#from abstract_bot import Bot

class for bot
class PatchingOnUnix(Bot):
    #method to initialise 
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
        
            serverName=executionContext["serverName"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            origFile=executionContext["origFile"]
            modFile=executionContext["modFile"]

            if serverName=="":
                return{"Missing argument" : "serverName"}
            if userName=="":
                return{"Missing argument" : "userName"}
            if password=="":
                return{"Missing argument" : "password"}
            if origFile=="":
                return{"Missing argument" : "origFile"}
            if modFile=="":
                return {"Missing argument" : "modFile"}

            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            
            #creating a patch and then applying it
            stdin,stdout,stderr=ssh.exec_command('diff -u "'+origFile+'" "'+modFile+'" > patchfile.patch && patch "'+origFile+'" patchfile.patch')
            outlines=stdout.readlines()
            result=''.join(outlines)
            #print(result)
            error=''
            errOutlines=stderr.readline()
            error=''.join(errOutlines)
            #print(error)
            ssh.close()
            if error=='':
                return{'Status': 'Success'}
            else:
                return {'Exception': error}
            
        except Exception as e:
            return {'Exception':str(e)}
          

if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = PatchingOnUnix()
    #giving parameter as a dictinoary
    context = {'serverName':'',         #enter the IP address of the server to connect to
               'userName':'',           #enter the username        
               'password':'',           #enter the password
               'origFile':'',              #enter the name of original file
               'modFile':''}              #enter the name of updated file 
    '''
    #Sample Data
    context = {'serverName':'10.67.87.198',
               'userName':'admin',    
               'password':'secret',
               'origFile':'original.html',      #if file present in a specific dir, enter the name of the file along with that address
               'modFile':'updated.html'}
    '''
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)     