'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import paramiko
import json
import wmi
from socket import *
from abstract_bot import Bot

# Check server RAM usage in Windows or Linux Server

class CheckServerRAMUsage(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):

        var_server_name=executionContext["var_server_name"]
        var_user_name=executionContext["var_user_name"]
        var_password=executionContext["var_password"]
        server_type=executionContext["server_type"]

        if var_server_name is None:
            return ("Missing argument: var_server_name")
        if var_user_name is None:
            return ("Missing argument : var_user_name")
        if var_password is None:
            return ("Missing arguement :var_password")
        if server_type is None:
            return ("Missing arguement :server_type")

        if server_type == 'linux':
            try:
                remote_connection = paramiko.SSHClient()
                remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                remote_connection.connect(var_server_name,22,var_user_name,var_password)
                print ('Linux Server connection established')
                sub_in, sub_out, sub_err = remote_connection.exec_command(r'free')
                sub_in.flush()
                sub_in.channel.shutdown_write()
                std_err = ''.join(err_line for err_line in sub_err)
                output = ''.join(out_line for out_line in sub_out)
                server_stats  = json.dumps(output)
                return {'output' : server_stats}
            except Exception as e:
                return {'Error while connecting to Linux server':str(e)}
        elif server_type == 'windows':
            try:
                connection = wmi.WMI(var_server_name, user = var_user_name, password = var_password)
                print ('Windows Server connection established')
                data = {}
                for i in connection.Win32_ComputerSystem():
                    data ['total_physical_memory_in_bytes'] = i.TotalPhysicalMemory
                for os in connection.Win32_OperatingSystem():
                    data ['free_physical_memory_in_bytes'] = os.FreePhysicalMemory   
                return {'output': data}
            except Exception as e:
                return {'Error while connecting to Windows server':str(e)}
        else:
            return {'Server Type is not valid'}
        

if __name__=="__main__":
    context={}
    bot_obj=CheckServerRAMUsage()
    
    context = {

                    'var_server_name':'',
                    'var_user_name':'',
                    'var_password':'',
                    'server_type':''
            }
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)