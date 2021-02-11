'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json 
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from abstract_bot import Bot


# Python Bot to update request in SNOW using UPDATE API

class UpdateRequestInSNOWUsingAPI(Bot):

	def bot_init(self):
		pass

	def execute(self, executeContext) :
		try:
			snowServerURL = executeContext['snowServerURL']
			if not snowServerURL:
				return {'validation error' : 'missing argument snowServerURL'}

			requestSysID = executeContext['requestSysID']
			if not requestSysID:
				return {'validation error' : 'missing argument requestSysID'}
			
			
			snowUsername = executeContext['snowUsername']
			if  not snowUsername:
				return {'validation error' : 'missing argument snowUsername'}
			
			snowPassword = executeContext['snowPassword']
			if not snowPassword:
				return {'validation error' : 'missing argument snowPassword'}

			snowComment = executeContext['snowComment']
			if not snowComment:
				return {'validation error' : 'missing argument snowComment'}

			snowState = executeContext['snowState']
			if not snowState:
				return {'validation error' : 'missing argument snowState'}
			snowState = int(float(snowState))

			snowAssignedTo = executeContext['snowAssignedTo']
			if not snowAssignedTo:
				return {'validation error' : 'missing argument snowAssignedTo'}
			
			maxRetryAttempt = executeContext['maxRetryAttempt']
			if not maxRetryAttempt:
				return {'validation error' : 'missing argument maxRetryAttempt'}

			
			url = "{0}/{1}".format(snowServerURL,requestSysID)
			headers = {"Content-Type":"application/xml","Accept":"application/xml"}
			respone  = ''

			comments = '<comments>{0}</comments>'.format(snowComment)
			state = '<state>{0}</state>'.format(snowState)
			assignedTo = '<assigned_to>{0}</assigned_to>'.format(snowAssignedTo)
			allData = "<request><entry>"  + comments  +  state +  assignedTo + "</entry></request>"
			
			maxRetryAttempt = int(maxRetryAttempt)
			auth_values = (snowUsername, snowPassword)

			retry_strategy = Retry(
					total = maxRetryAttempt,
					backoff_factor = 2,
					status_forcelist = [429, 500, 502, 503, 504,401],
					method_whitelist = ["HEAD", "GET", "PUT", "OPTIONS", "TRACE"]
								)
			adapter = HTTPAdapter(max_retries=retry_strategy)
			http = requests.Session()
			http.mount("https://", adapter)
			http.mount("http://", adapter)

			response = requests.put(url, auth=(snowUsername, snowPassword), headers=headers, data=allData)
			if response.status_code == 200:
				return {'status' : 'success', 'api_status_code':response.status_code}
			elif response.status_code != 200: 
					return {'status' : "failed", 'api_status_code' : response.status_code}
		except Exception as e:
			return {'status' : "failed", 'error' : e}

  
if __name__ == '__main__':
	context = {}
	bot_obj = UpdateRequestInSNOWUsingAPI()

	context =  {
									
				
				'snowServerURL' : '',
				'snowUsername' : '',
				'snowPassword' : '',
				'snowComment' : ' ',
				'snowAssignedTo' : ' ',
				'snowState' : '',
				'requestSysID' : '',
				'maxRetryAttempt' : '',
				   															
				}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)