'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client as win32
from abstract_bot import Bot


class ConvertExcelSheetToImage(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            xlsxFilePath = executeContext['xlsxFilePath']
            if not xlsxFilePath:
                return {'validation error': 'missing argument xlsxFilePath'}

            imgDestinationPath = executeContext['imgDestinationPath']
            if not imgDestinationPath:
                return {'validation error': 'missing argument imgDestinationPath'}

            imgFileName = executeContext['imgFileName']
            if not imgFileName:
                return {'validation error': 'missing argument imgFileName'}

            imgSheetName = executeContext['imgSheetName']
            if not imgSheetName:
                return {'validation error': 'missing argument imgSheetName'}

            imgSheetSelection = executeContext['imgSheetSelection']
            if not imgSheetSelection:
                return {'validation error': 'missing argument imgSheetSelection'}

            destinationPath = '{0}\{1}'.format(imgDestinationPath, imgFileName)
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            wb = excel.Workbooks.Open(xlsxFilePath)
            xl_range = wb.Sheets(imgSheetName).Range(imgSheetSelection)
            excel.ActiveWorkbook.Sheets.Add(After=excel.ActiveWorkbook.Sheets(3)).Name = imgSheetName+"_temp"
            cht = excel.ActiveSheet.ChartObjects().Add(0, 0, xl_range.Width, xl_range.Height)
            xl_range.CopyPicture()
            cht.Chart.Paste()
            cht.Chart.Export(destinationPath, 'png')
            cht.Delete()
            excel.DisplayAlerts = False
            excel.ActiveSheet.Delete()
            excel.ActiveWorkbook.Close(SaveChanges=1)

            return {'status': 'success'}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    context = {}
    bot_obj = ConvertExcelSheetToImage()

    context = {
        'xlsxFilePath': '',
        'imgDestinationPath': '',
        'imgFileName': "",
        'imgSheetName': "",
        'imgSheetSelection': ''

    }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ', output)



