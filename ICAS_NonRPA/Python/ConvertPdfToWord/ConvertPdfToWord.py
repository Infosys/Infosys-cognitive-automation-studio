'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import win32com.client

class ConvertPdfToWord(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            pdfFilePath = executeContext['pdfFilePath']
            wordFilePath = executeContext['wordFilePath']
            word = win32com.client.Dispatch("Word.Application")
            word.visible = 0
            wb = word.Documents.Open(pdfFilePath)
            wb.SaveAs2(wordFilePath, FileFormat=16) # file format for docx
            wb.Close()
            word.Quit()
            return {'Output':'Converted pdf to word successfully'}
                
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = ConvertPdfToWord()
#    context = {'pdfFilePath' :'D:\sample\saledeed.pdf','wordFilePath':'D:\sample\sa.docx'}
    context = {'pdfFilePath' :'','wordFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)