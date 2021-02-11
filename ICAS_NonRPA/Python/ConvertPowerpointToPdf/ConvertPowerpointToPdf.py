'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client
from abstract_bot import Bot
# Python Bot to convert pptx document to PDF

class ConvertPowerpointToPdf(Bot):

	def execute(self, executeContext) :
		try:
			pptxFilePath = executeContext['pptxFilePath']
			if  not pptxFilePath:
				return {'validation error' : 'missing argument pptxFilePath'}
			
			pdfDestinationPath = executeContext['pdfDestinationPath']
			if  not pdfDestinationPath:
				return {'validation error' : 'missing argument pdfDestinationPath'}

			pdfFileName = executeContext['pdfFileName']
			if  not pdfFileName:
				return {'validation error' : 'missing argument pdfFileName'}
			
			destination_path = '{0}\{1}'.format(pdfDestinationPath, pdfFileName)
			print(f'Converting {pptxFilePath} to {destination_path}')
			powerpoint = win32com.client.Dispatch("Powerpoint.Application")
			pdf = powerpoint.Presentations.Open(pptxFilePath, WithWindow=False)
			pdf.SaveAs(destination_path, 32)
			pdf.Close()
			powerpoint.Quit()
			return {'status': 'success'}
		except Exception as e:
			return {'Exception': str(e)}

  
if __name__ == '__main__':
	context = {}
	bot_obj = ConvertPowerpointToPdf()

	context = {
				'pptxFilePath': '',
				'pdfDestinationPath': '', 
				'pdfFileName' : '' 
				
				
		}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)