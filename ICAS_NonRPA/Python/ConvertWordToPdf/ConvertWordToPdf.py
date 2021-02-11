'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
import os
from abstract_bot import Bot
from docx2pdf import convert


# Python Bot to convert word document to PDF

class ConvertWordToPdf(Bot):

  
	def execute(self, executeContext) :
		try:
			docxFilePath = executeContext['docxFilePath']
			if  not docxFilePath:
				return {'validation error' : 'missing argument docxFilePath'}

			pdfDestinationPath = executeContext['pdfDestinationPath']
			if  not pdfDestinationPath:
				return {'validation error' : 'missing argument pdfDestinationPath'}

			pdfFileName = executeContext['pdfFileName']
			if  not pdfFileName:
				return {'validation error' : 'missing argument pdfFileName'}

			destination_path = '{0}\{1}'.format(pdfDestinationPath, pdfFileName)
			convert(docxFilePath, destination_path)
			return {'status': 'success'}
		except Exception as e:
			print("Error occured ",str(e)) 
			return {'Exception': str(e)}

	
if __name__ == '__main__':
	context = {}
	bot_obj = ConvertWordToPdf()

	context = {
				'docxFilePath': '',
				'pdfDestinationPath': '', 
				'pdfFileName' : ''  
			  
		}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)