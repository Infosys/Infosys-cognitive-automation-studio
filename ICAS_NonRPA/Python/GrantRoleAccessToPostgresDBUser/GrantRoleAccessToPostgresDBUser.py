'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
from abstract_bot import Bot

# Python bot to grant user privileges in Postgres database


class GrantRoleAccessToPostgresDBUser(Bot):

	def bot_init(self):
		pass
  
	def execute(self, executeContext) :
		try:
			dbName = executeContext['dbName']
			if not dbName:
				return {'validation' :  'Enter a valid database name'}

			dbUsername = executeContext['dbUsername']
			if not dbUsername:
				return {'validation' :  'Enter a valid database user name'}

			dbPassword = executeContext['dbPassword']
			if not dbPassword:
				return {'validation' :  'Enter a valid database password'}

			dbHost = executeContext['dbHost']
			if not dbHost:
				return {'validation' :  'Enter a valid database host'}

			port = executeContext['port']
			if not port:
				return {'validation' :  'Enter a valid database port'}
			
			userName = executeContext['userName']
			if not userName:
				return {'validation' :  'Enter a valid username to provide GRANT permissions'}

			conn = psycopg2.connect(database = dbName, 
							user = dbUsername, password = dbPassword, 
							host = dbHost, port = port
							)   
			print ("connection established")
		except Exception as e:
			print(str(e)) 
			return {'Exception' : str(e)}

		try:
			cur = conn.cursor()
			sqlSelect = "GRANT ALL PRIVILEGES ON DATABASE {0} TO {1};".format(dbName,
												userName)
			print (sqlSelect)
			cur.execute(sqlSelect)
			conn.commit()
			cur = conn.close()
			return {'status' : 'success'}
		except Exception as e: 
			return {'Exception' : str(e)}

  
if __name__ == '__main__':
	context = {}
	bot_obj = GrantRoleAccessToPostgresDBUser()

	context = {
			   
				'dbName' : "", 
				'dbUsername' : "", 
				'dbPassword' : "", 
				'dbHost' : "", 
				'port' : "",
				'userName' : '',
		
		}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)