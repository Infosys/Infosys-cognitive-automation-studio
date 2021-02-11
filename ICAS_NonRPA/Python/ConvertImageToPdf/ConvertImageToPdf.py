'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from PIL import Image
from abstract_bot import Bot

class ConvertImageToPdf(Bot):

 

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            image = executeContext['image']
            pdfName = executeContext['pdfName']
            
            image1 = Image.open(image)
            im1 = image1.convert('RGB')
            im1.save(pdfName)
                
            return {'Output':'Success'}
        except Exception as e:
             return {'Exception':str(e)}
   

 

if __name__ == '__main__':

 

    context = {}
    bot_obj = ConvertImageToPdf()
    
    context = {'pdfName' :'','image':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)