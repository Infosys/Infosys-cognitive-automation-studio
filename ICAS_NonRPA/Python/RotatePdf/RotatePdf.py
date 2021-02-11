'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# importing the required modules
import PyPDF2
import os


from abstract_bot import Bot

class RotatePdf(Bot):
    def bot_init(self):
        pass

    def execute(self, executionContext):

        try:
            input_file = executionContext['inputFile']

            output_file_path = os.path.dirname(input_file)
            output_file = '{0}\{1}'.format(output_file_path, "outputFile.pdf")
            rotation = executionContext['rotation']

            if os.path.isfile(input_file):
                text = open(input_file, 'r')
            else:
                return {"result": "File does not exist"}

            # creating a pdf File object of original pdf
            pdfFileObj = open(input_file, 'rb')

            # creating a pdf Reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # creating a pdf writer object for new pdf
            pdfWriter = PyPDF2.PdfFileWriter()

            # rotating each page
            for page in range(pdfReader.numPages):
                # creating rotated page object
                pageObj = pdfReader.getPage(page)
                pageObj.rotateClockwise(int(rotation.strip() or 0))

                # adding rotated page object to pdf writer
                pdfWriter.addPage(pageObj)

            # new pdf file object
            newFile = open(output_file, 'wb')

            # writing rotated pages to new file
            pdfWriter.write(newFile)

            # closing the original pdf file object
            pdfFileObj.close()

            # closing the new pdf file object
            newFile.close()
            return {'outputFile': output_file}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    context = {}
    bot_obj = RotatePdf()
    context = {'inputFile': r'',
               'rotation': ''
               }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
