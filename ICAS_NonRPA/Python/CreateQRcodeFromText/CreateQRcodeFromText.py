'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import qrcode
from abstract_bot import Bot

class CreateQRcodeFromText(Bot):

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
            qr = qrcode.QRCode(
                    version = 1,box_size = 10,border = 4,
                    error_correction = qrcode.constants.ERROR_CORRECT_H,
                    )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            imageFilePath =  imageFileDir +  '/' +  fileName + '.jpg'
            img.save(imageFilePath)        
            return {'status' : 'success'}
        except Exception as e:
            return {'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = CreateQRcodeFromText()

    context =  { 
                'data' : '',
                'imageFileDir' : '',
                'fileName' : ''
                }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)


