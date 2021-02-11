'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import psycopg2
from abstract_bot import Bot

# Python bot to create new user in Postgres database


class CreateUserInPostgresDB(Bot):

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

			newUserName = executeContext['newUserName']
			if not newUserName:
				return {'validation' :  'Enter a valid name of new user to be created'}

			newUserPassword = executeContext['newUserPassword']
			if not newUserPassword:
				return {'validation' :  'Enter a valid password for new user'}

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
			sqlSelect = "CREATE USER {0} with encrypted password '{1}'".format(newUserName,
											newUserPassword)
			cur.execute(sqlSelect)
			conn.commit()
			cur = conn.close()
			return {'status' : 'success'}
		except Exception as e:
			print("User aleady exists") 
			return {'Exception' : str(e)}


  
if __name__ == '__main__':
	context = {}
	bot_obj = CreateUserInPostgresDB()

	context = {
				'dbName' : "", 
				'dbUsername' : "", 
				'dbPassword' : "", 
				'dbHost' : "", 
				'port' : "",
				'newUserName' : '',
				'newUserPassword' : ''
		}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)