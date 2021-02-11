'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
import json
from abstract_bot import Bot

# Bot reads the location file and gives associated mail ids in the output
class CheckNetworkFileMailids(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        varLocation=executionContext["varLocation"]
        filePath=executionContext["filePath"]
        
        if varLocation is None:
            return ("Missing argument: varLocation")
        if filePath is None:
            return ("Missing argument: filePath")
        try:
            with open(filePath,'r') as file:
                r_text=file.read()
            r_text=r_text.strip()
            data_dict = json.dumps(r_text)
        except Exception as e:
            print('File Reading  exception: '+str(e),'ERROR')
            return {'Error while Reading a File ':str(e)}
        ###########existing IOPS way ####
        #considering file contains locations and respective 'to' email ids
        try:  
            if data_dict and re.search(varLocation,str(data_dict),re.IGNORECASE):   
                var_mail_ids = data_dict[varLocation]["to"]
                return {'output':var_mail_ids}    
            else:              
                return {'NORESULTS':'Not able to find any mail idsin the given file  path'}
        except Exception as e:
            return {'Error while searching for Location and mail ids ':str(e)}
        #-------------------------------------------
        ######## another  way to find mail ids  in txt fie ############
        # try:
        #     if r_text:
        #         lst = re.findall('\S+@\S+', r_text) 
        #         return {'mailIds from network file are ':lst}
        #     else:
        #         return {'Error':'empty file returned from network file'}

if __name__=="__main__":
    context={}
    bot_obj=CheckNetworkFileMailids()
    
    context = {'filePath':'','varLocation':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)