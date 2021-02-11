'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request
from abstract_bot import Bot

# app = Flask(__name__)
# api = Api(app)

# @app.route('/api/summarize_article/<str:text>', methods=['GET'])
class SummarizeArticle(Bot):


    # def summarize_article(text):
    def execute(self, executeContext):
        try:
            text = executeContext['text']
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LexRankSummarizer()
            summarize_document = summarizer(parser.document, 2)
            summary =''
            for sentence in summarize_document:
                summary += str(sentence)
            return summary
        except Exception as e:
            print('Exception : ',str(e))
            return str(e)

    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = SummarizeArticle()

    # --input parameters--
    context = {'text':''}

    resp = bot_obj.execute(context)
    print('response : ',resp)