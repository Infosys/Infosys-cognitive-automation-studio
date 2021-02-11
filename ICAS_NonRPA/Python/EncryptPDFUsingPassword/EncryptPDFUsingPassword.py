'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from PyPDF2 import PdfFileWriter, PdfFileReader
from abstract_bot import Bot


# Bot to encrypt PDF with password 

class EncryptPDFUsingPassword(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            inputPDF = executeContext['inputPDF']
            if not inputPDF:
                return {'Exception' : 'missing argument inputPDF'}

            outputDirPDF = executeContext['outputDirPDF']
            if not outputDirPDF:
                return {'Exception' : 'missing argument outputDirPDF'}

            outputPdfName = executeContext['outputPdfName']
            if not outputPdfName:
                return {'Exception' : 'missing argument outputPdfName'}

            outputDestinationPDF = outputDirPDF + "\\" + outputPdfName
            print (outputDestinationPDF)
            
            password = executeContext['password']
            if not password:
                return {'Exception' : 'missing argument password'}

            pdf_writer = PdfFileWriter()
            pdf_reader = PdfFileReader(inputPDF)

            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))

            pdf_writer.encrypt(user_pwd=password, owner_pwd=None, 
                            use_128bit=True)

            with open(outputDestinationPDF, 'wb') as fh:
                pdf_writer.write(fh)
            return {'status': 'success'}
        except Exception as e:
            return {'Exception' : str(e)}



if __name__ == '__main__':
    context = {}
    bot_obj = EncryptPDFUsingPassword()

    context =  {
                'inputPDF':'',
                'outputDirPDF':'',
                'outputPdfName':'',
                'password': ''

                # 'inputPDF':'D:\JAVATEST\output.pdf',
                # 'outputDirPDF':'D:\JAVATEST',
                # 'outputPdfName':'reportlab-encrypted.pdf',
                # 'password': 'password'
                }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)