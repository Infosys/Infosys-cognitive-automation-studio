'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import PyPDF2
import os


from abstract_bot import Bot

class PdfToText(Bot):
    def bot_init(self):
        pass

    def execute(self, executeContext):
        input_file = executeContext['inputFile']
        output_file_path = os.path.dirname(input_file)
        outputFile = '{0}\{1}'.format(output_file_path, "outputFile.txt")

        try:
            pdfFileObject = open(input_file, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
            pageObject = pdfReader.getPage(0)
            text = pageObject.extractText()
            f = open(outputFile, 'w', encoding='utf-8')
            f.writelines(text)
            f.close()
            return {"outputFile": outputFile}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    context = {}
    bot_obj = PdfToText()
    context = {'inputFile': r''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
