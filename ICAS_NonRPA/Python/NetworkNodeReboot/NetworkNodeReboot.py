'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
from abstract_bot import Bot
import re
import netmiko
import telnetlib
#import environ
import fernet
import sqlite3
import inspect
import subprocess
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
                            

server_timeout	= 60
telnet_interval	= 5
team_names	= [	]

ruba_reps	= {}
home_path	= r"D:\\" # Absolute path where the tool is installed
auto_rep	= home_path+r"/REP"
app_rep		= auto_rep+r"/Apps"
ruba_rep	= app_rep+r"/RubA"
ruba_db		= ruba_rep+r"/RubA.db"
auto_work 	= auto_rep+r"/Work"
auto_vault	= auto_rep+r"/vault.ini"



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
	

auto_db= auto_rep+r"/users.db"

bin_paths	= {
	r".yml" : [r"/usr/local/bin/ansible-playbook",r"--vault-password-file",auto_vault],
	r".sh"	: [r"/usr/bin/sh"],
	r".ps1"	: [r"C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",r"-ExecutionPolicy",r"ByPass",r"-File"],
	#r".pl"	: [r""],
	#r".py"	: [r"/usr/local/bin/python3"]
	r".py"	: [r"C:/Python37/python.exe"]
    }
	
log_level = 1

auto_temp 	= auto_work+r"/temp"


# This script will login to device by ssh and then telnet, it will fetch output and send email to specified email.
# Arguments: ["string","var_host"],["string","var_location"],["string","var_command"],["password","var_password"]



class NetworkNodeReboot(Bot):
    
    def bot_init(self):
        pass
    
    def userTeam():
        import inspect
        stack_list = inspect.stack()
        user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
        print('User team: '+str(user_team),'INFO')
        if user_team in team_names:
            return user_team
        else:
            return 'NOK'
    

        
		
    def execute(self,executionContext):
        # Arguments: ["string","var_host"],["string","var_location"],["string","var_command"],["password","var_password"]
        try:
            if "var_host" in executionContext:
                var_host = executionContext["var_host"]
            else:
                print('Missing argument: var_host','ERROR')
                return { 'output':'failure'}
            if "var_location" in executionContext:
                var_location = executionContext["var_location"]
            else:
                print('Missing argument: var_location','ERROR')
                return { 'output':'failure'}
            if "var_command" in executionContext:
                var_command = executionContext["var_command"]
            else:
                print('Missing argument: var_command','ERROR')
                return { 'output':'failure'}
            if "var_password" in executionContext:
                var_password = executionContext["var_password"]
            else:
                print('Missing argument: var_password','ERROR')
                return { 'output':'failure'}
            #previous_status,previous_output = connectNetwork(r'cisco_ios',str(var_host),22,r'sxkomaku',str(var_password),r'undefined')
            try:
                network_connection = netmiko.ConnectHandler(device_type=r'cisco_ios',ip=str(var_host),port=22,username=r'sxkomaku',password=str(var_password),secret=str(var_password))
                # Not sure below about enable method is to exexute or not
		        #network_connection.enable()
                previous_status,previous_output =  'OK','Network connection made: '+str(var_host)
            except Exception as e:
    		        print('Network connection exception: '+str(e),'ERROR')
            previous_status,previous_output = 'NOK',str(e)          
            
            
            if previous_output and re.search('"NOK"',str(previous_output),re.IGNORECASE):
                print('IF condition matches','INFO')
                #previous_status,previous_output = connectServer(r'telnet',str(var_host),23,r'sxkomaku',str(var_password))
                user_name = r'sxkomaku'
                remote_connection = telnetlib.Telnet(str(var_host).lower(),23,timeout=server_timeout)
                if user_name != 'NA':
                    td_out = remote_connection.read_until(b": ")
                    remote_connection.write((user_name+"\n").encode('ascii'))
                    td_out = remote_connection.read_until(b"password: ")
                    remote_connection.write((str(var_password)+"\n").encode('ascii'))
                td_out = remote_connection.read_until(b"ops_auto_telnet",server_timeout)
                

                #revious_output = executeServer(str(var_command))
                remote_connection.write((str(var_command)+"\n").encode('ascii'))
                return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
                return_text = return_text.strip()

                
                var_comm_out = return_text
                #previous_status,previous_output = runScript(r'Network_File_MailIds.py',r'sequential',{"var_location":"'+str(var_location)+r'"},r'NA',r'NA')
                
                try:
                    return_text = ""
                    user_team = userTeam()
                    stack_list = inspect.stack()
                    user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                    print('User team: '+str(user_team),'INFO')
                    if user_team in team_names:
                        user_team =  user_team
                    else:
                        user_team = 'NOK'
                    job_args = {"var_location":"'+str(var_location)+r'"}
                    job_path = os.path.join(ruba_reps[user_team]['script'],r'Network_File_MailIds.py')
                    if not os.path.exists(job_path):
                        print('Script does not exist: '+str(job_path),'ERROR')
                        return { 'output':'failure'}
                    
                    if user_name != 'NA':
                        if pass_word == 'NA': 
                            #ret_status, pass_word = getLogins(user_name)
                            return_text = 'NOK'
                            user_team = userTeam()
                            stack_list = inspect.stack()
                            user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                            print('User team: '+str(user_team),'INFO')
                            if user_team in team_names:
                                pass
                            else:
                                user_team =  'NOK'
                            if os.path.exists(auto_db):
                                db = sqlite3.connect(auto_db)
                                db_cursor = db.execute("select access_key from user_list where user_team='"+user_team+"' and user_group='saccount' and user_name=lower('"+str(user_name)+"')")
                                sql_out = db_cursor.fetchone()
                                db.close()
                            else:
                                print('Database not found: '+str(ruba_reps[user_team]['db']),'ERROR')
                                ret_status, pass_word = 'NOK',return_text
                            
                            if not sql_out:
                                print('Logins not configured: '+str(user_name),'WARN')
                                ret_status, pass_word = 'NOK',return_text
                            return_text = fernet.decryptString(sql_out[0])
                            print('Logins retrieved: '+str(user_name),'INFO')
                            ret_status, pass_word = 'OK',return_text

                            if ret_status != 'OK':
                                print('NOK','Logins not found')
                                return { 'output':'failure'}
                        job_args['user_name'] = user_name
                        job_args['pass_word'] = pass_word
                    
                    fname,extn = os.path.splitext(job_path)
                    if extn not in bin_paths:
                        print('Invalid script type: '+str(extn),'ERROR')
                        #return 'NOK','Invalid script type ERROR: '+str(extn)
                        return { 'output':'failure'}
                    
                    script_exe = bin_paths[extn][:]
                    script_exe.append(job_path)
                    print("Script to run: "+str(script_exe))
                    if extn == '.yml':
                        script_exe.extend([r'-i',ruba_reps[user_team]['hosts']])
                        script_exe.extend([r'-e','@'+ruba_reps[user_team]['vars']])
                        if log_level > 1:
                            script_exe.append(r'-vvv')
                        script_exe.append(r'-e')
                    script_exe.append(json.dumps(job_args))
                    
                    sub = subprocess.Popen(script_exe,cwd=auto_temp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
                    sub_out, sub_err = sub.communicate()
                    
                    return_text = str(sub_out).strip()
                    return_list = return_text.splitlines()
                    return_text = '\n'.join(ret_line for ret_line in return_list if '   IMP: ' in ret_line or ' ERROR: ' in ret_line)
                    sub_err = sub_err.strip()
                    
                    if sub_err:
                        return_text += str(sub_err)
                        if 'NoCertificateRetrievedWarning' not in return_text:
                            #print('Execution error: '+str(return_text),'ERROR')
                            previous_status,previous_output = 'NOK','Execution error: '+str(return_text)
                    if sub.returncode != 0 or ' ERROR: ' in return_text:
                        #print('Execution failed: '+str(return_text),'ERROR')
                        previous_status,previous_output = 'NOK','Execution failed: '+str(return_text)
                    
                    #print('Script executed: '+str(job_name),'INFO')
                    #print(return_text)
                    previous_status,previous_output = 'OK',return_text
                except Exception as e:
                    print('Script execution exception: '+str(e),'ERROR')
                    previous_status,previous_output = 'NOK',str(e)
                
                #previous_status,previous_output = sendMail(str(var_comm_out),r'iops_auto@testexc.com',str(previous_output).split(','),r''+str(var_host)+r' - Info',r'mail.testexc.com',25,r'plain',r'NA',r'NA')
                try:
                    if pass_word == 'NA' and user_name != 'NA':
                        ret_status, pass_word = getLogins(user_name)
                        return_text = 'NOK'
                        user_team = userTeam()
                        stack_list = inspect.stack()
                        user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                        print('User team: '+str(user_team),'INFO')
                        if user_team in team_names:
                            pass
                        else:
                            user_team =  'NOK'
                        if os.path.exists(auto_db):
                            db = sqlite3.connect(auto_db)
                            db_cursor = db.execute("select access_key from user_list where user_team='"+user_team+"' and user_group='saccount' and user_name=lower('"+str(user_name)+"')")
                            sql_out = db_cursor.fetchone()
                            db.close()
                        else:
                            print('Database not found: '+str(ruba_reps[user_team]['db']),'ERROR')
                            ret_status, pass_word = 'NOK',return_text
                        
                        if not sql_out:
                            print('Logins not configured: '+str(user_name),'WARN')
                            ret_status, pass_word = 'NOK',return_text
                        return_text = fernet.decryptString(sql_out[0])
                        print('Logins retrieved: '+str(user_name),'INFO')
                        ret_status, pass_word = 'OK',return_text
                        if ret_status != 'OK':
                            return 'NOK','Logins not found'
                    
                    mail_content = 'From: '+r'iops_auto@testexc.com'+'\nTo: '+str(previous_output).split(',')+'\nSubject: '+r''+str(var_host)+r' - Info'+'\n\n'+str(var_comm_out)
                    
                    mail = smtplib.SMTP(r'mail.testexc.com',port=25)
                    if user_name != 'NA':
                        mail.ehlo()
                        mail.starttls()
                        mail.login(user_name,pass_word)
                    mail.sendmail(r'iops_auto@testexc.com',str(previous_output).split(','),mail_content)
                    mail.quit()
                    print('Mail sent to: '+str(previous_output).split(','),'INFO')
                    #return 'OK',str(previous_output).split(',')
                except Exception as e:
                    #print('Send mail exception: '+str(e),'ERROR')
                    #return 'NOK',str(e)
                    return { 'output':'failure'}

                print('Exiting.','INFO')
                return { 'output':'success'}
                
            else:
                print('ELSE condition','INFO')
                #revious_status,previous_output = executeNetwork(str(var_command),r'NO')
                if network_connection.check_config_mode():
                    network_connection.exit_config_mode()
                return_text = network_connection.send_command(str(var_command))
                return_text = return_text.strip()

                var_comm_out = return_text
                #previous_status,previous_output = runScript(r'Network_File_MailIds.py',r'sequential',{"var_location":"'+str(var_location)+r'"},r'NA',r'NA')
                
                try:
                    return_text = ""
                    user_team = userTeam()
                    stack_list = inspect.stack()
                    user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                    print('User team: '+str(user_team),'INFO')
                    if user_team in team_names:
                        user_team =  user_team
                    else:
                        user_team = 'NOK'
                    job_args = {"var_location":"'+str(var_location)+r'"}
                    job_path = os.path.join(ruba_reps[user_team]['script'],r'Network_File_MailIds.py')
                    if not os.path.exists(job_path):
                        print('Script does not exist: '+str(job_path),'ERROR')
                        return { 'output':'failure'}
                    
                    if user_name != 'NA':
                        if pass_word == 'NA': 
                            #ret_status, pass_word = getLogins(user_name)
                            return_text = 'NOK'
                            user_team = userTeam()
                            stack_list = inspect.stack()
                            user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                            print('User team: '+str(user_team),'INFO')
                            if user_team in team_names:
                                pass
                            else:
                                user_team =  'NOK'
                            if os.path.exists(auto_db):
                                db = sqlite3.connect(auto_db)
                                db_cursor = db.execute("select access_key from user_list where user_team='"+user_team+"' and user_group='saccount' and user_name=lower('"+str(user_name)+"')")
                                sql_out = db_cursor.fetchone()
                                db.close()
                            else:
                                print('Database not found: '+str(ruba_reps[user_team]['db']),'ERROR')
                                ret_status, pass_word = 'NOK',return_text
                            
                            if not sql_out:
                                print('Logins not configured: '+str(user_name),'WARN')
                                ret_status, pass_word = 'NOK',return_text
                            return_text = fernet.decryptString(sql_out[0])
                            print('Logins retrieved: '+str(user_name),'INFO')
                            ret_status, pass_word = 'OK',return_text

                            if ret_status != 'OK':
                                print('NOK','Logins not found')
                                return { 'output':'failure'}
                        job_args['user_name'] = user_name
                        job_args['pass_word'] = pass_word
                    
                    fname,extn = os.path.splitext(job_path)
                    if extn not in bin_paths:
                        print('Invalid script type: '+str(extn),'ERROR')
                        #return 'NOK','Invalid script type ERROR: '+str(extn)
                        return { 'output':'failure'}
                    
                    script_exe = bin_paths[extn][:]
                    script_exe.append(job_path)
                    print("Script to run: "+str(script_exe))
                    if extn == '.yml':
                        script_exe.extend([r'-i',ruba_reps[user_team]['hosts']])
                        script_exe.extend([r'-e','@'+ruba_reps[user_team]['vars']])
                        if log_level > 1:
                            script_exe.append(r'-vvv')
                        script_exe.append(r'-e')
                    script_exe.append(json.dumps(job_args))
                    
                    sub = subprocess.Popen(script_exe,cwd=auto_temp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
                    sub_out, sub_err = sub.communicate()
                    
                    return_text = str(sub_out).strip()
                    return_list = return_text.splitlines()
                    return_text = '\n'.join(ret_line for ret_line in return_list if '   IMP: ' in ret_line or ' ERROR: ' in ret_line)
                    sub_err = sub_err.strip()
                    
                    if sub_err:
                        return_text += str(sub_err)
                        if 'NoCertificateRetrievedWarning' not in return_text:
                            #print('Execution error: '+str(return_text),'ERROR')
                            previous_status,previous_output = 'NOK','Execution error: '+str(return_text)
                    if sub.returncode != 0 or ' ERROR: ' in return_text:
                        #print('Execution failed: '+str(return_text),'ERROR')
                        previous_status,previous_output = 'NOK','Execution failed: '+str(return_text)
                    
                    #print('Script executed: '+str(job_name),'INFO')
                    #print(return_text)
                    previous_status,previous_output = 'OK',return_text
                except Exception as e:
                    print('Script execution exception: '+str(e),'ERROR')
                    previous_status,previous_output = 'NOK',str(e)
                
                #previous_status,previous_output = sendMail(str(var_comm_out),r'iops_auto@testexc.com',str(previous_output).split(','),r''+str(var_host)+r' - Info',r'mail.testexc.com',25,r'plain',r'NA',r'NA')
                try:
                    if pass_word == 'NA' and user_name != 'NA':
                        ret_status, pass_word = getLogins(user_name)
                        return_text = 'NOK'
                        user_team = userTeam()
                        stack_list = inspect.stack()
                        user_team = "".join(instack[1].replace('\\','/').split('/')[-3] for instack in stack_list if 'Scripts' in instack[1])
                        print('User team: '+str(user_team),'INFO')
                        if user_team in team_names:
                            pass
                        else:
                            user_team =  'NOK'
                        if os.path.exists(auto_db):
                            db = sqlite3.connect(auto_db)
                            db_cursor = db.execute("select access_key from user_list where user_team='"+user_team+"' and user_group='saccount' and user_name=lower('"+str(user_name)+"')")
                            sql_out = db_cursor.fetchone()
                            db.close()
                        else:
                            print('Database not found: '+str(ruba_reps[user_team]['db']),'ERROR')
                            ret_status, pass_word = 'NOK',return_text
                        
                        if not sql_out:
                            print('Logins not configured: '+str(user_name),'WARN')
                            ret_status, pass_word = 'NOK',return_text
                        return_text = fernet.decryptString(sql_out[0])
                        print('Logins retrieved: '+str(user_name),'INFO')
                        ret_status, pass_word = 'OK',return_text
                        if ret_status != 'OK':
                            return 'NOK','Logins not found'
                    
                    mail_content = 'From: '+r'iops_auto@testexc.com'+'\nTo: '+str(previous_output).split(',')+'\nSubject: '+r''+str(var_host)+r' - Info'+'\n\n'+str(var_comm_out)
                    
                    mail = smtplib.SMTP(r'mail.testexc.com',port=25)
                    if user_name != 'NA':
                        mail.ehlo()
                        mail.starttls()
                        mail.login(user_name,pass_word)
                    mail.sendmail(r'iops_auto@testexc.com',str(previous_output).split(','),mail_content)
                    mail.quit()
                    print('Mail sent to: '+str(previous_output).split(','),'INFO')
                    #return 'OK',str(previous_output).split(',')
                except Exception as e:
                    #print('Send mail exception: '+str(e),'ERROR')
                    #return 'NOK',str(e)
                    return { 'output':'failure'}

                print('Exiting.','INFO')
                return { 'output':'success'}

            
        except Exception as e:
            print('Aborting!', "ERROR: ", e)
            return { 'output':'failure'}

		
	
	

if __name__=="__main__":
    context={}
    bot_obj=NetworkNodeReboot()
    
    context = {'var_host':'' ,'var_location': '' , 'var_command': '', 'var_password':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)	

