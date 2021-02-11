'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from abstract_bot import Bot
#import json
# app = Flask(__name__)
# api = Api(app)

# @app.route('/api.clean_article/<path:doc_path>', methods=['GET'])
class CleanArticle(Bot):
    # def clean_article(doc_path):
    def execute(self, executeContext):
        try:
            file_path = executeContext['file_path']

            with open(file_path, 'r') as f:
                text = f.read()
            #Removing only the HTML tags from the article
            TAG_RE = re.compile(r'<[^>]+>')
            
            REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
            # BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
            text = TAG_RE.sub('', text)
            text = REPLACE_BY_SPACE_RE.sub(' ', text)
            text = re.sub(r'\n', " ", text)
            # text = REPLACE_BY_SPACE_RE.sub(' ', text)
            # text = BAD_SYMBOLS_RE.sub(' ', text)
            return {'output':text}
        except Exception as e:
            print('Exception : ',str(e))
            return 'failure'


# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)
# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = CleanArticle()

    # --input parameters--
    context = {''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)