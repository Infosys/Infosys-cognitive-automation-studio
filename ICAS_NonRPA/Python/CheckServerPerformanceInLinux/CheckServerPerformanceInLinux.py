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
from abstract_bot import Bot


#Bot will Check the Server Performance
class CheckServerPerformanceInLinux(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):

        try:
            varServerName=executionContext["varServerName"]
			if not varServerName:
				return {'validation' :  'Enter a valid IP Address'}
			
			varUserName=executionContext["varUserName"]
			if not varServerName:
				return {'validation' :  'Enter a valid user name'}
			
			varPassword=executionContext["varPassword"]
			if not varPassword:
				return {'validation' :  'Enter a valid password'}
			
			statsToKnow=executionContext["statsToKnow"]
			if not statsToKnow:
				return {'validation' :  'Enter a valid stats to know command'}

            remote_connection = paramiko.SSHClient()
            remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote_connection.connect(varServerName,22,varUserName,varPassword)
            print ("Server connected")
        except Exception as e:
            return {'Exception':str(e)}

        try:

            stats_cmds =  ['vmstat', 'iostat', 'netstat', 'sar']
            if statsToKnow not in stats_cmds:
                return {'validation' :  'Enter a valid linux command to check performance'}
            if(statsToKnow=='vmstat'):
                sub_in, sub_out, sub_err = remote_connection.exec_command(r'vmstat')   
            if(statsToKnow=='iostat'):
                sub_in, sub_out, sub_err = remote_connection.exec_command(r'iostat')
            if(statsToKnow=='netstat'):
                sub_in, sub_out, sub_err = remote_connection.exec_command(r'netstat')
            if(statsToKnow=='sar'):
                sub_in, sub_out, sub_err = remote_connection.exec_command(r'sar')
            sub_in.flush()
            sub_in.channel.shutdown_write()
            std_err = ''.join(err_line for err_line in sub_err)
            output = ''.join(out_line for out_line in sub_out)
            # outlines=stdout.readlines()
            # output=''.join(outlines)
            server_stats  = json.dumps(output)
            return {'server_performance' : server_stats}
        except Exception as e:
            return {'Exception':str(e)}


if __name__=="__main__":
    context={}
    bot_obj=CheckServerPerformanceInLinux()
    
    context = {
            'varServerName':'',
            'varUserName':'',
            'varPassword':'',
            'statsToKnow':''
            }
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)