'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

# This Bot merges multiple PDFs in a folder into one PDF.
# Input Parameters: path of the PDF files that are to be merged,
#                   full path of the final output PDF file


class MergeMultiplePDFs(Bot):

    def bot_init(self):
        pass

    # execute method with main functionality
    def execute(self,executeContext):
        try:
            pdfpath = executeContext['inputPDFPath']
            mergepdf = executeContext['outputPDFPath']
            mergepdfpath = os.path.dirname(mergepdf)

            if pdfpath == '' or mergepdfpath == '':
                return {'Exception': 'Please provide input and/or output path correctly'}
            else:
                mergefiles = []
                if os.path.exists(pdfpath) and os.path.exists(mergepdfpath):
                    for pdf in os.listdir(pdfpath):
                        if pdf.endswith(".pdf"):
                            mergefiles.append(pdf)
                else:
                    return {'Exception': 'input path does not exist'}

                pdfmerger = PdfFileMerger()
                for eachfile in mergefiles:
                    pdffullpath = pdfpath + "\\" + eachfile
                    with open(pdffullpath,"rb") as pdfobj:
                        pdfmerger.append(PdfFileReader(pdfobj))

                pdfmerger.write(mergepdf)
                pdfmerger.close()
                return {'status': 'Merged all PDF files successfully'}

        except Exception as e:
            print("Exception ",str(e))

if __name__ == '__main__':
    output = {}
    #context = {'inputPDFPath':'C:\\Users\\aishwarya_padhi\\Downloads\\folder\\mergepdf',
    #           'outputPDFPath':'C:\\Users\\aishwarya_padhi\\Downloads\\folder\\mergepdf\\finalPDF2.pdf'}
    context = {'inputPDFPath':'', 'outputPDFPath':''}
    obj = MergeMultiplePDFs()
    obj.bot_init()
    output = obj.execute(context)







