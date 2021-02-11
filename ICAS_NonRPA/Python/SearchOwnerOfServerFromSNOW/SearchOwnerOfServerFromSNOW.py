'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import requests
from abstract_bot import Bot

class SearchOwnerOfServerFromSNOW(Bot):
    def bot_init(self):
        pass
    
    def execute(self, excecuteContext):
        try:
            instance= excecuteContext['instance']
            userName = excecuteContext['userName']
            password = excecuteContext['password'] 
            
            if not userName:
                return{'Missing Argument':'userName'}
            if not password:
                return{'Missing Argument':'password'}

            url = 'https://'+instance+'.service-now.com/api/now/table/cmdb_ci'
            headers = {"Accept":"application/json"} 
            response = requests.get(url, auth=(userName, password), headers=headers)

            storage_server= [x for x in response.json()['result'] if x["sys_class_name"]=="cmdb_ci_storage_server"]
            user_value_id= storage_server[0]['assigned_to']['value']
#            storage_server= [x for x in response.json()['result'] if x["name"]=="TestServer"]
#            user_value_id= storage_server[0]['assigned_to']['value']
            print("Node 1", user_value_id)
           
            url = 'https://'+instance+'.service-now.com/api/now/table/sys_user'
            response = requests.get(url, auth=(userName, password), headers=headers )
            users_data= response.json()
            user_email_id= [x['email'] for x in users_data['result'] if x["sys_id"]==user_value_id]
            
            output= {'output': user_email_id}
            return output
            
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = SearchOwnerOfServerFromSNOW()

    context = {'instance':'',
            'userName': '',
		       'password': ''}

    resp = bot_obj.execute(context)
    print('response : ',resp)


