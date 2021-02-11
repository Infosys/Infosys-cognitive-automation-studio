'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import pandas
import openpyxl
import xlrd
import win32com.client
from pandas import DataFrame
from rake_nltk import Rake
from nltk.corpus import stopwords 
from abstract_bot import Bot

class CreateSolutionRepoFromOutlook(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            searchKeyword=executionContext['searchKeyword']
            excelPath=executionContext['excelPath']
            
            if searchKeyword=="":
                return{"Missing argument": "searchKeyword"}
            if excelPath=="":
                return{"Missing argument": "excelPath"}
            
            #Triggering the Outlook application
            outlook=win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox=outlook.GetDefaultFolder(6) # 6 is used for the index of the folder
            msgBox=inbox.Items
            
            r=Rake()
                         
            for message in msgBox:
                subKeywords=[]
                bodyKeywords=[]
                if message.UnRead==True:
                    if searchKeyword.lower() in message.Subject.lower():
                        solnSub=message.Subject
                        
                        a=r.extract_keywords_from_text(solnSub)
                        b=r.get_ranked_phrases_with_scores()
                        
                        for key in b:
                          subKeywords.append(key[1])  
                        subjTopKeys=subKeywords[0:4]
                        
                        solnBody=message.Body
                        #print(solnBody)
                        a1=r.extract_keywords_from_text(solnBody)
                        b1=r.get_ranked_phrases_with_scores()
                        
                        for key1 in b1:
                            if key1[0]>1:
                                bodyKeywords.append(key1[1])
                        bodyTopKeys=bodyKeywords[0:4] 
                        
                   
                        msgSub=[solnSub]
                        msgBody=[solnBody]
                        subjKeys=[subjTopKeys]
                        bodyKeys=[bodyTopKeys]
                        
                        
                        df=DataFrame({'Subject':msgSub,'Body':msgBody,'Subject_Keys':subjKeys,'Body_Keys':bodyKeys}) 
						#Solution_Repository excel file contains 4 columns viz. Subject, Body, Subject_Keys, Body_Keys
						
                        dfExcel=pandas.read_excel(excelPath)
                        result=pandas.concat([dfExcel,df], ignore_index=True)
                        result.to_excel(excelPath, index=False)
                        message.Unread=False
                        #print("data added")
						
            return{"Result":"Successfully added to the Solution_Repository"}
        
        except Exception as e:
            return{"Exception":str(e)}

if __name__ == "__main__":
    context = {}
    bot_obj = CreateSolutionRepoFromOutlook()
	#write the path as "C:\\Users\\vikas.singh09\\Desktop\\Solution_Repository.xlsx"
    context = {"searchKeyword" : "", #enter keyword as "Solution"
               "excelPath": ""} #write the path to where the Solution_Repository excel file is located
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)