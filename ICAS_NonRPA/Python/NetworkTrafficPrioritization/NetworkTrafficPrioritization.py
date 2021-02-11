'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''


from files.abstract_bot import Bot
import telnetlib
server_timeout	= 60	# num of seconds for server connections timeouts like ssh etc.
telnet_interval	= 5		# num of seconds gap between telnet commands


# Prioritize traffic in WAN

class NetworkTrafficPrioritization(Bot):
    
    def bot_init(self):
        pass
        
		
    def execute(self,executionContext):
        # Arguments: {'user_name': 'String' , 'pass_word': 'String'}
        
        try:
            #previous_status,previous_output = connectServer(r'telnet',r'router01',23,r'router_user',r'NA')
            
            remote_connection = telnetlib.Telnet(r'router01',23,timeout=server_timeout)
            if executionContext['user_name'] != 'NA':
                td_out = remote_connection.read_until(b": ")
                remote_connection.write((str(executionContext['user_name'])+"\n").encode('ascii'))
                td_out = remote_connection.read_until(b": ")
                remote_connection.write((str(executionContext['pass_word'])+"\n").encode('ascii'))
            remote_connection.read_until(b"ops_auto_telnet",server_timeout)
			
            
            #previous_status,previous_output = executeServer(r'ip access-list extended acl-prec-af21')
            remote_connection.write((r'ip access-list extended acl-prec-af21'+"\n").encode('ascii'))
            return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
            return_text = return_text.strip()
			
            #previous_status,previous_output = executeServer(r'ip access-list extended acl-prec-2')
            remote_connection.write((r'ip access-list extended acl-prec-2'+"\n").encode('ascii'))
            return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
            return_text = return_text.strip()

            #previous_status,previous_output = executeServer(r'ip access-list extended acl-prec-3')
            remote_connection.write((r'ip access-list extended acl-prec-3'+"\n").encode('ascii'))
            return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
            return_text = return_text.strip()

            #previous_status,previous_output = executeServer(r'ip access-list extended acl-prec-af41')
            remote_connection.write((r'ip access-list extended acl-prec-af41'+"\n").encode('ascii'))
            return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
            return_text = return_text.strip()


            #previous_status,previous_output = executeServer(r'ip access-list extended acl-prec-4')
            remote_connection.write((r'ip access-list extended acl-prec-4'+"\n").encode('ascii'))
            return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
            return_text = return_text.strip()

            
            if return_text and return_text.search('ERROR',str(return_text),return_text.IGNORECASE):
                #print('IF condition matches','INFO')
                print('Aborting!','ERROR')
                return { 'output':'failure'}
            else:
                #printMsg('ELSE condition','INFO')
                #previous_status,previous_output = executeServer(r'show run int gi 0/0/0')
                remote_connection.write((r'show run int gi 0/0/0'+"\n").encode('ascii'))
                return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
                return_text = return_text.strip()

                #previous_status,previous_output = executeServer(r'show policy-map int gi 0/0/0')
                remote_connection.write((r'show policy-map int gi 0/0/0'+"\n").encode('ascii'))
                return_text = remote_connection.read_until(b"ops_auto_telnet",telnet_interval)
                return_text = return_text.strip()

                #printMsg('Return value: '+str(previous_output))
                if return_text and return_text.search('SUCCESS',str(return_text),return_text.IGNORECASE):
                    #print('IF condition matches','INFO')
                    #print('Exiting.','INFO')
                    return { 'output':'success'}
                else:
                    #printMsg('ELSE condition','INFO')
                    print('Aborting!','ERROR')
                    return { 'output':'failure'}
        except Exception as e:
            print('Aborting!', "ERROR: ", e)
            return { 'output':'failure'}

		
	
	

if __name__=="__main__":
    context={}
    bot_obj=NetworkTrafficPrioritization()
    
    context = {'user_name': '' , 'pass_word': ''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)	

