'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import barcode
from barcode.writer import ImageWriter
from abstract_bot import Bot


class CreateBarcodeFromText(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext) :
        try:
            data = executeContext['data']
            if not data:
                return {'Exception' : 'missing argument data'}
            
            imageFileDir = executeContext['imageFileDir']
            if not imageFileDir:
                return {'Exception' : 'missing argument imageFileDir'}

            fileName = executeContext['fileName']
            if not fileName:
                return {'Exception' : 'missing argument fileName'}
            fileName = fileName.split(".", 1)[0]
            
            ean = barcode.get('ean13', data, writer=ImageWriter())
            imageFilePath =  imageFileDir +  '/' +  fileName
            filename = ean.save(imageFilePath)           
            return {'status' : 'success'}
        except Exception as e:
            return {'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CreateBarcodeFromText()

    context =  {
                'data' : '',
                'imageFileDir' : '',
                'fileName' : ''
                }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)


