'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import csv
import re
import time
from collections import Counter
from datetime import datetime
import time


import json
import pandas as pd
from operator import itemgetter
from nltk.cluster.util import cosine_distance

from flask import Flask    
from flask_cors import CORS   
from flask_restful import  Api
from flask_restful import request

from abstract_bot import Bot

# app = Flask(__name__)
# api = Api(app)

class TextRank(Bot): 


    stopwords_english = None

    def bot_init(self):
        with open('D:\\28April\\bot-factory\\Microbots\\ML-AI\\TextRank\\data\\stopwords.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            list1 = list(reader)  
            self.stopwords_english = list1[0]
            readFile.close()


    def sentence_similarity(self, sent1, sent2, stopwords_english=None):
        if self.stopwords_english is None:
            self.stopwords_english = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))
        
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in self.stopwords_english:
                continue
            vector1[all_words.index(w)] += 1
            
        # build the vector for the second sentence
        for w in sent2:
            if w in self.stopwords_english:
                continue
            vector2[all_words.index(w)] += 1
        return 1 - cosine_distance(vector1, vector2)

    # @app.route('/api/text_rank/<int:num_related_sentences>/<float:match_percentage>')
    def text_rank(self, input_sentence, real_time_df, num_related_sentences, match_percentage):
        
        """ Implementation of text rank algorithm which 
            takes input a sentence and a dataframe of sentences
            and gives back the top num_related_sentences related
            sentences from the DataFrame

            in: input_sentence sentence from which similarity is matched
                real_time_df dataframe of real time sentences
                num_related_sentences number of related sentences
            
            out: top num_related_sentences similar sentences
        """
        #input_sentence = request.get_json('input_sentence')
        #real_time_df = request.get_json('real_time_df')

        weight = []
        num_sentences = len(real_time_df)    
        weight = [0] *(num_sentences)
        counter = 0
        column_name = real_time_df.columns[0]
        for i in range(num_sentences):  
            rel_weight = self.sentence_similarity(input_sentence.split(), real_time_df[column_name][i].split(),self.stopwords_english)
            if(rel_weight >= match_percentage):
                weight[i] = rel_weight
                counter += 1
            if(counter >= num_sentences):
                break

        weightDict = {}
        # print("Weights Inside Closed Tickets", weight)
        for index, item in enumerate(weight):
            if (item > 0):
                weightDict[index] = item

        if (weightDict):    
            sorted_weights = sorted(weightDict.items(), key=itemgetter(1))[::-1]
            ranked_sentence_indexes = [item[0] for item in sorted_weights]
            # print("Ranked Sentence Indexes Closed Tickets", ranked_sentence_indexes)
            
            # hardcoded value for related tickets 
            SELECTED_SENTENCES = sorted(ranked_sentence_indexes[:num_related_sentences])

            related_sentences = itemgetter(*SELECTED_SENTENCES)(real_time_df[column_name])

            if (not isinstance(related_sentences, tuple)):
                related_tickets = (related_sentences,)

            result_list = []
            results_matched = len(related_sentences)

            if (results_matched == 0):
                print("Sorry No matches found..." )
                return result_list
            else:
                print("Number of search results : %d" % (results_matched))
                result_list = list(related_sentences)
                return result_list

    # def main(csv_path, input_sentence, num_related_sentences, match_percentage=0.50):
    def execute(self, executeContext):
        csv_path = executeContext['csv_path']
        input_sentence = executeContext['input_sentence']
        num_related_sentences = int(executeContext['num_related_sentences'])
        match_percentage = float(executeContext['match_percentage'])
        print("csv path",type(match_percentage))
        real_time_df = pd.read_csv(csv_path)
        print("csv path",real_time_df)
        try:
            result_list = self.text_rank(input_sentence, real_time_df, num_related_sentences, match_percentage)

            print(result_list) 
            #jsList=''.join(result_list)

            #return 'success'
            if result_list is None:
                return {'result_list':'0'}
            else:
                return {'result_list':json.dumps(result_list)}
        except Exception as e:
            return {'Exception':str(e)}


# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = TextRank()

    # --input parameters--
    #context = {'csv_path':'D:\\28April\\bot-factory\\Microbots\\ML-AI\\TextRank\\data\\descriptions.csv', 'input_sentence':'(CI=SAP BW(Business Warehouse))Redwood PRD: Job Ended Not OK.', 'num_related_sentences':5, 'match_percentage':0.50}
    context = {'csv_path':'', 'input_sentence':'', 'num_related_sentences':'','match_percentage': ''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('response : ',output)
# if __name__ == '__main__':
#    app.run(host = '0.0.0.0', port=5002, debug=True)




    


