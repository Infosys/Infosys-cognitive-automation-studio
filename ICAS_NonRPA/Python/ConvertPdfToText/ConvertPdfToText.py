'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

class ConvertPdfToText(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            pdfFilePath = executeContext['pdfFilePath']
            textFilePath = executeContext['textFilePath']
            output = StringIO()
            manager = PDFResourceManager()
            converter = TextConverter(manager, output, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, converter)
            infile = open(pdfFilePath, 'rb')
            for page in PDFPage.get_pages(infile):
                interpreter.process_page(page)
            infile.close()
            converter.close()
            text = output.getvalue()
            output.close()
            filehandle = open(textFilePath, 'w')
            filehandle.write(text)
            filehandle.close()
            return {'Output':'Converted pdf to text successfully'}
                
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = ConvertPdfToText()
    #context = {'pdfFilePath' :'D:\Test\dumps6.pdf','textFilePath':'D:\Test\dumps6.txt'}
    context = {'pdfFilePath' :'','textFilePath':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
