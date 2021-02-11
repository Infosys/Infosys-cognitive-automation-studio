'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from googletrans import Translator
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to translate from one language to english
class CreateLanguageTranslatorBots(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        inputText = executionContext["inputText"] #Input text

        if not inputText:
            return {'Warning' : 'inputText can not be empty'}
        #To avoid exception error open port has to be configured first
        try:
            translator = Translator()  
            trans = translator.translate(inputText)
            result = trans.pronunciation
            return {'Result': result}
        except Exception as e:
            return {'Exception': str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = CreateLanguageTranslatorBots()
    context = {'inputText':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)