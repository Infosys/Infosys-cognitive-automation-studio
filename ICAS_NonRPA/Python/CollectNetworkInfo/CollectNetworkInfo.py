'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
from abstract_bot import Bot
import netmiko
import inspect



# Arguments: ["string","varUserName"],["string","varCommand"],["password","var_pass"]
# Scripts SSHs to devices and collecting output of show commands and saving into text files
class CollectNetworkInfo(Bot):
    
    def bot_init(self):
        pass
        
		
    def execute(self,executionContext):
        try:
            varServerName = executionContext["varServerName"] #IP address of other remote server
            varUserName = executionContext["varUserName"] #Username
            varPassword = executionContext["varPassword"] #Password
            varCommand = executionContext["varCommand"] #Command
            if varServerName is None:
                return {'Missing Argument':'varServerName'}
            if varUserName is None:
                return {'Missing Argument':'varUserName'}
            if varPassword is None:
                return {'Missing Argument':'varPassword'}
            if varCommand is None:
                return {'Missing Argument':'varCommand'}
            #previous_status,previous_output = readFile(r'network_ssh_devices.txt')
            file_path = r'network_ssh_devices.txt'
            return_text = ''
            team_names	= [	r"window"]
            home_path	= r"D:\iOps\iOps_Auto-master"
            auto_rep	= home_path+r"/REP"
            app_rep		= auto_rep+r"/Apps"
            ruba_rep	= app_rep+r"/RubA"
            ruba_reps	= {}
            for team_name in team_names:
                ruba_reps[team_name] = {
                        r"home"		: ruba_rep+r"/"+team_name,
                        r"script"	: ruba_rep+r"/"+team_name+r"/Scripts",
                        r"flow" 	: ruba_rep+r"/"+team_name+r"/Flows",
                        r"rule"		: ruba_rep+r"/"+team_name+r"/Rules",
                        r"file" 	: ruba_rep+r"/"+team_name+r"/Files",
                        r"log"		: ruba_rep+r"/"+team_name+r"/Logs",
                        r"hosts"	: ruba_rep+r"/"+team_name+r"/Files/hosts.ini",
                        r"vars"		: ruba_rep+r"/"+team_name+r"/Files/variables.yml"
                        }
            if "\\" not in file_path and "/" not in file_path:
                #user_team = userTeam()
                stack_list = inspect.stack()
                user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                print('User team: '+str(user_team),'INFO')
                if user_team in team_names:
                    pass
                else:
                    user_team = 'NOK'
                file_path = os.path.join(ruba_reps[user_team]['file'],file_path)			
            if not os.path.exists(file_path):
                print('Invalid path: '+str(file_path),'ERROR')
                return { 'output':'failure'}
            
            with open(file_path,'r') as file:
                return_text = file.read()
            return_text = return_text.strip()

            #previous_status,previous_output = textToArray(str(previous_output),r'\n')
            de_limiter = r'\n'
            if de_limiter == '\\n':
                return_list = return_text.splitlines()
            else:
                return_list = return_text.split(de_limiter)
            return_text = ",".join(return_list)

            var_devices = return_text
            for var_foreach in str(var_devices).split(','):
                #print('Loop: '+str(previous_output),'INFO')
                #previous_status,previous_output = connectNetwork(r'cisco_ios',str(previous_output),22,str(varUserName),str(var_pass),r'undefined')
                network_connection = netmiko.ConnectHandler(device_type=r'cisco_ios',ip=varServerName,port=22,username=varUserName,password=varPassword,secret=varPassword)
		
                 # Not sure below about enable method is to exexute or not
		        #network_connection.enable()
                
                #previous_status,previous_output = executeNetwork(str(varCommand),r'NO')
                if network_connection.check_config_mode():
                    network_connection.exit_config_mode()
                return_text = network_connection.send_command(varCommand)
                return_text = return_text.strip()

                #previous_status,previous_output = writeFile(str(previous_output),r'/tmp/network_files/'+str(var_foreach)+r'.txt')
                file_path = r'/tmp/network_files/'+str(var_foreach)+r'.txt'
                if "\\" not in file_path and "/" not in file_path:
                    #user_team = userTeam()
                    stack_list = inspect.stack()
                    user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                    print('User team: '+str(user_team),'INFO')
                    if user_team in team_names:
                        pass
                    else:
                        user_team = 'NOK'
                    file_path = os.path.join(ruba_reps[user_team]['file'],file_path)	
                
                with open(file_path,'a') as file:
                    file.write(str(return_text)+'\n')
                
            return { 'output':"success"}

                       
        except Exception as e:
            print('Exception : ' + str(e))
            return { 'Exception':'failure'}

		
	
	

if __name__=="__main__":
    context={}
    bot_obj=CollectNetworkInfo()
    
    context = {'varServerName': '','varUserName': '','varCommand': '' , 'varPassword': ''}
    #Arguments: ["string","varServerName"],["string","varUserName"],["string","varCommand"],["password","var_pass"]
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)	