'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import googletrans
import xlsxwriter
import pandas as pd
from googletrans import Translator
class ConvertLanguageFromExcel(Bot):
    def bot_init(self):
        pass
    def execute(self,executionContext):
        try:
            translator=Translator()
            work=executionContext['type']
            work=work.lower()
            filePath=executionContext['filePath']
            convertTo=executionContext['convertTo']
            convertTo=convertTo.lower()
            inputColumn=executionContext['columnToTranslate']
            outputFile=executionContext['outputFile']                       
            if(work=='find'):
                
                workbook=xlsxwriter.Workbook(outputFile)
                worksheet=workbook.add_worksheet()
                worksheet.write(0,0,'Inputs')
                worksheet.write(0,1,'Language Types')
                df=pd.read_excel(filePath)
                row=1
                col=0
                intput=df[inputColumn]
                for i in intput:
                    lang=translator.detect(i)
                    worksheet.write(row,col,i)
                    worksheet.write(row,col+1,googletrans.LANGUAGES[lang.lang])
                    row+=1
                workbook.close()
                return {"Output":"OutputofType file is created successfully"}
            elif(work=='translate'):
                workbook=xlsxwriter.Workbook(outputFile)
                worksheet=workbook.add_worksheet()
                worksheet.write(0,0,'Inputs')
                worksheet.write(0,1,'Language Translation')
                df=pd.read_excel(filePath)
                intput=df[inputColumn]
                
                dicts=dict(googletrans.LANGUAGES)
                
                for key,value in dicts.items():
                    if(value==convertTo):
                        convert=key
                row=1
                col=0    
                for sentence  in intput:
                    lang=translator.detect(sentence)
                    translated=translator.translate(sentence,src=lang.lang,dest=convertTo)
                    worksheet.write(0,0,'Inputs')
                    worksheet.write(0,1,'Translation to '+convertTo)
                    worksheet.write(row,col,sentence)
                    worksheet.write(row,col+1,translated.text)
                    row+=1
                workbook.close()
                return {"Output":"OutputofTranslation file is created successfully"}
            else:
                return {'Exception':'Wrong type is inserted'}
                    
        except Exception as e:
            return {'Exception' : str(e)}
        
        
        
        
        
if __name__ == "__main__":
    context = {}
    #class object creation
    bot_obj = ConvertLanguageFromExcel()
    #giving parameter as a dictionary
    context = {'filePath':'','type':'','convertTo':'','columnToTranslate':'','outputFile':''}
    bot_obj.bot_init()
   
    output = bot_obj.execute(context)
    print(output)