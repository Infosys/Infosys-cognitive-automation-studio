'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import netmiko
import paramiko
from abstract_bot import Bot

# Bot to connect to a Network from a Linux Server


class ConnectToNetworkFromLinux(Bot):
	
	def bot_init(self):
		pass

	def connectNetwork(self, conn_type,host_name,rem_port,enable_mode='NO',
									user_name='NA',pass_word='NA'):
		try:
			ssh_connection = netmiko.ConnectHandler(
										device_type=conn_type,
										ip=host_name,port=rem_port,username=user_name,
										password=pass_word,secret=pass_word
										)

			# enter enable mode
			ssh_connection.enable()

			# close SSH connection
			ssh_connection.disconnect()
			
			print('Network connection made: '+str(host_name),'INFO')
			return 'OK','Network connection made: '+str(host_name)
		except Exception as e:
			print('Network connection exception: '+str(e),'ERROR')
			return {'Exception' : str(e)}
	
	def execute(self,executionContext):
		try:
			linuxServerName =executionContext["linuxServerName"]
			linuxUserName=executionContext["linuxUserName"]
			linuxPassword=executionContext["linuxPassword"]

			networkIP =executionContext["networkIP"]
			networkUserName=executionContext["networkUserName"]
			networkPassword=executionContext["networkPassword"]
		
		
			ssh=paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(hostname=linuxServerName,
						username=linuxUserName,
						password=linuxPassword,
						port=22
					)
			print ('linux ssh connection done')
		except Exception as e:
			return {'Exception' : str(e)}

		try:
			net_connect = self.connectNetwork('cisco_ios',networkIP,22,r'NO',
						networkUserName,networkPassword)  
			if not ValueError:
				return {'status' :  'success'}
			else:
				return {'Exception' : 'Error in Network connection'}
		except Exception as e:
			return {'Exception' : str(e)}


if __name__ == "__main__":
	context = {}
	bot_obj = ConnectToNetworkFromLinux()

	context = {
				'linuxServerName':'',
				'linuxUserName':'',
				'linuxPassword':'',

				'networkIP' : '',
				'networkUserName': '',
				'networkPassword' : ''
				}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print(output)     