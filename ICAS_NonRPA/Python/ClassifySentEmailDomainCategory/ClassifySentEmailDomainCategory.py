'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from abstract_bot import Bot

class ClassifySentEmailDomainCategory(Bot):
    def bot_init_(self):
        pass

    def execute(self, executionContext):
        try:
            domain = executionContext['domain']
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            sent = outlook.GetDefaultFolder(5)
            smessages = sent.Items
            recipients = []
            for sm in smessages:
                if sm.Class == 43:
                    #print(sm.To)
                    if sm.To not in recipients:
                        recipients.append(sm.To)
                        finalList = recipients
            #print(finalList)
            finalList = str(finalList)
            finalList1 = finalList.replace(';', ',')
            finalList2 = finalList1.replace("'","") 

            res = finalList2.strip('][').split(', ')

            res1 = set(res)

            if domain == "internal":
                c=0
                for int in res1:
                    if ("@" not in int):
                        c=c+1
                        #print(int)        
                print('Total Internal Domain sender count:',c)
                return {'Status': 'success'}
            else:
                count=0 
                for ext in res1:
                    if ("@" in ext):
                        count=count+1
            print('Total External Domain sender count:',count)           
            return {'Status': 'success'}
                 
        except Exception as e:
            return {'Exception': str(e)}

if __name__ == '__main__':

    context = {}
    obj_snow = ClassifySentEmailDomainCategory()
    context = {
            'domain' : '',
                } 
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)