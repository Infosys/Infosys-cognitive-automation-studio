'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# importing the required modules
import sys
import traceback
import PyPDF2
import os


from abstract_bot import Bot

class AddWatermark(Bot):
    def bot_init(self):
        pass

    def execute(self, executionContext):

        try:
            input_file = executionContext['inputFile']
            output_file_path = os.path.dirname(input_file)
            output_file = '{0}\{1}'.format(output_file_path, "outputFile.pdf")
            watermark_file = executionContext['watermarkFile']

            if os.path.isfile(input_file):
                text = open(input_file, 'r')
            else:
                return {"Failure": "File does not exist"}

            # creating a pdf File object of original pdf
            inputPdfFileObj = open(input_file, 'rb')
            # creating a pdf Reader object for input file
            inputPdfReader = PyPDF2.PdfFileReader(inputPdfFileObj)

            # creating a pdf File object of original pdf
            wmPdfFileObj = open(watermark_file, 'rb')
            # creating a pdf Reader object for watermark file
            wmPdfReader = PyPDF2.PdfFileReader(wmPdfFileObj)

            # accessing first page
            pdf_page = inputPdfReader.getPage(0)
            watermark_page = wmPdfReader.getPage(0)

            # merging the pages
            pdf_page.mergePage(watermark_page)

            # Save the output file
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addPage(pdf_page)

            newPdfFileObj = open(output_file, 'wb')
            pdfWriter.write(newPdfFileObj)

            # closing the original pdf file object
            inputPdfFileObj.close()
            newPdfFileObj.close()
            wmPdfFileObj.close()
            return {'outputFile': output_file}

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'result': formatted_lines[-1]}


if __name__ == "__main__":
    context = {}
    bot_obj = AddWatermark()
    context = {'inputFile': r'',
               'watermarkFile': r''
               }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
