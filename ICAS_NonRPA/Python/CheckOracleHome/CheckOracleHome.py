'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
import json
import wmi
from winrm import Protocol
from abstract_bot import Bot

#class for bot
class CheckOracleHome(Bot):
    #method to initialise 
    def bot_init(self):
        pass

    def getCmd_linux(self,serverName,userName,password,command):
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=serverName,port=22,username=userName,password=password)
        stdin,stdout,stderr=ssh.exec_command('source ~/.bash_profile;'+command, get_pty=False)
        value= stdout.readlines()#[0]
        if len(value)==0:
            return None
        elif value==['\n']:
            return None
        else:
            return value[0]
        ssh.close()
        return(value)
    
    def getENV_win(self,serverName,userName,password,envVar):
#        connection = wmi.WMI(serverName, user= userName,password= password)
#        utilizations = connection.Win32_Environment()  #environment variable class
#        value= [x.VariableValue for x in utilizations if x.Description.endswith(envVar)]
#        return value[0]
        varServerName='Http://'+serverName+':5985/wsman'
        Session=Protocol(endpoint=varServerName,transport='ntlm',username=userName,password=password,server_cert_validation='ignore')
        shell=Session.open_shell()
        
        command = Session.run_command(shell,"if defined "+envVar+" echo exists")
        sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
#        print(str(sub_out))
        
        if sub_out.decode("ASCII")[:-2]=="exists":   #if environment variable exists then get value .
            command = Session.run_command(shell,"echo %"+envVar+"%")
            sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
            directory_path= sub_out.decode("ASCII")[:-2]
#            print('if exist "'+directory_path+'\\bin" echo exists')
                        
            command = Session.run_command(shell,'if exist "'+directory_path+'" echo exists')
            sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
            
            if sub_out.decode("ASCII")[:-2]=="exists":  # check if env variable value exists as a directory
                command = Session.run_command(shell,'if exist "'+directory_path+'\\bin\\sqlplus" echo exists') 
                sub_out,sub_err,ret_code =Session.get_command_output(shell,command)
                
                if sub_out.decode("ASCII")[:-2]=="exists":  #check bin folder inside that exists.
#                    print("Bin directory exists inside", str(sub_out))
                    Session.cleanup_command(shell, command)
                    Session.close_shell(shell)
                    return("Success")
                else:
                    Session.cleanup_command(shell, command)
                    Session.close_shell(shell)
                    return("Invalid Oracle Home Directory (It is not an ORACLE_HOME directory)")
                    
            else:
                Session.cleanup_command(shell, command)
                Session.close_shell(shell)
                return("Invalid Oracle Home Directory (It is not a directory)")
                    
        else:
            Session.cleanup_command(shell, command)
            Session.close_shell(shell)
            return("ORACLE_HOME variable is not defined")                   
        


    def execute(self,executionContext):
        try:
            serverName =executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            os= executionContext['os']
#             command=executionContext['command']
            if serverName is None:
                return ("Missing argument : serverName")
            if userName is None:
                return ("Missing argument : userName")
            if  password is None:
                return ("Missing argument :password")
#             if  command is None:
#                 return ("Missing argument :Command")
            
            # connecting to server
            if os=="linux" or os=="unix":
                envVarValue= self.getCmd_linux(serverName,userName,password,'echo $'+"ORACLE_HOME")
                if envVarValue is not None:
                    Dir_exists= self.getCmd_linux(serverName,userName,password,'[ -d "'+ envVarValue[:-1] +'" ] && echo "exists"')
                    if Dir_exists[:-1]=="exists":
                        Dir_exists= self.getCmd_linux(serverName,userName,password,'[ -d "'+ envVarValue[:-1] +'/bin/sqlplus'+'" ] && echo "exists"')
                        if Dir_exists is not None:#[:-1]=="exists":
                            return {'Status':'Success'}
                        else:
                            return {'Status':"Invalid Oracle Home Directory (It is not an ORACLE_HOME directory)"}
                    else:
                        return {'Status':"Invalid Oracle Home Directory (It is not a directory)"}
                else:
                    return {'Status':"ORACLE_HOME variable is not defined"}
                
#                out= self.getENV_linux(serverName,userName,password,'KAFKA_HOME')            
#                return {'Status':'Valid Directory: '+out}
            elif os=="windows":
                out= self.getENV_win(serverName,userName,password,'ORACLE_HOME')
                print(out)
                if out=="Success":
                    return {'Status':'Success'}
                else:
                    return {'Status':out}
                
#             return {'Output':json.dumps(Output),'Status':'Success'}
            else:
                return {'Status':'Please enter valid OS as input :windows or linux'}
                
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckOracleHome()
    
    context = {'serverName':"",'userName':"",'password':"",'os':''}
#    context = {'serverName':"10.177.186.23",'userName':"ppcazureuser",'password':"",'os':'linux'}
#    context = {'serverName':"10.85.91.230",'userName':"vaddi.kumar01",'password':"Arusa7878#",'os':'windows'}
   
    bot_obj.bot_init()
    #Calling of execute function on linux server
    output = bot_obj.execute(context)
    print(output)