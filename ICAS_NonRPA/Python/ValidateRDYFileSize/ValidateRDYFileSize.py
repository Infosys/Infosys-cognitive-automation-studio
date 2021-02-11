'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
from abstract_bot import Bot

# Python bot to validate the size of each indice of .rdy file
# each record size must be of 172 Kbs


class ValidateRDYFileSize(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            
            filepath=executeContext['filepath']
            
            open_file = open(filepath,'r',encoding='utf-8')
            body = str(open_file.read()).splitlines()
            
            context = {}
            invalid_size_records = []
            n=1

            for item in body:
                if len(item) == 171 :                                       # memory allocation starts from 0 in python , so 171 (instead of 172)
                    n += 1
                    pass                                                    # No mail send
                else:
                    item_split = item.split()
                    invalid_size_records.append([n,item_split[0]])          # fetching invalid records
                    n += 1                                                    
            
            if len(invalid_size_records) > 0:
                context['invalid_size_records'] = invalid_size_records
                context['mail_status_code'] = '3'
                context['status'] = 'success'
            else:
               context['mail_status_code'] = '0'
               context['status'] = 'success'
            return context
             

        except Exception as e:
            print("Error occured",str(e)) 
            return {'status' :str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = ValidateRDYFileSize()

    context = {
                #'filepath' : 'D:/Bot_Factory/Dummy/ropinf.200617.050103.rdy'
                'filepath' : ''
        }

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)