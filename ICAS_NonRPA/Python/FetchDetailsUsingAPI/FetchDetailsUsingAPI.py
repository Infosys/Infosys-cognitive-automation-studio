'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json
import requests
from abstract_bot import Bot
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Python Bot to fetch details using GET-API

class FetchDetailsUsingAPI(Bot):

	def bot_init(self):
		pass

	def execute(self, executeContext) :
		try:
			serverURL = executeContext['serverURL']
			if not serverURL:
				return {'validation error' : 'missing argument serverURL'}
			
			authUsername = executeContext['authUsername']
			if  not authUsername:
				return {'validation error' : 'missing argument authUsername'}
			
			authPassword = executeContext['authPassword']
			if not authPassword:
				return {'validation error' : 'missing argument authPassword'}
			
			maxRetryAttempt = executeContext['maxRetryAttempt']
			if not maxRetryAttempt:
				return {'validation error' : 'missing argument maxRetryAttempt'}
			
			maxRetryAttempt = int(maxRetryAttempt)
			auth_values = (authUsername, authPassword)

			retry_strategy = Retry(
					total = maxRetryAttempt,
					backoff_factor = 2,
					status_forcelist = [429, 500, 502, 503, 504],
					method_whitelist = ["HEAD", "GET", "PUT", "OPTIONS", "TRACE"]
								)
			adapter = HTTPAdapter(max_retries=retry_strategy)
			http = requests.Session()
			http.mount("https://", adapter)
			http.mount("http://", adapter)

			response = requests.get(serverURL,auth=auth_values)
			if response.status_code == 200:
				response = response.json()
				return {'status' : 'success', 'response':response}
			elif response.status_code != 200: 
					return {'status' : "failed", 'api_status_code' : response.status_code}		
		except Exception as e:
			return {'status' : "failed", 'error' : e}

  
if __name__ == '__main__':
	context = {}
	bot_obj = FetchDetailsUsingAPI()

	context =  {
				'serverURL' : '',
				'authUsername' : '',
				'authPassword' : '',
				'maxRetryAttempt' : '',
				
				}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)