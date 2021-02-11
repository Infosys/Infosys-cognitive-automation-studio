'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import numpy as np
import spacy
from tqdm import tqdm
import re
import time
import pickle
pd.set_option('display.max_colwidth', 200)
import en_core_web_md
import tensorflow_hub as hub
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from abstract_bot import Bot

class ELMo(Bot):
    def execute(self, excecuteContext):
        try:
            train_file_path = excecuteContext['train_file_path']
            test_file_path= excecuteContext['test_file_path']
            Output_file_path = excecuteContext['Output_file_path']
            InputTextColumn = excecuteContext['InputTextColumn']
            TargetColumn = excecuteContext['TargetColumn']
        

            # read data
            train = pd.read_excel(train_file_path)
            test = pd.read_excel(test_file_path)

            # remove URL's from train and test
            train['clean_tweet'] = train[InputTextColumn].apply(lambda x: re.sub(r'http\S+', '', x))
            test['clean_tweet'] = test[InputTextColumn].apply(lambda x: re.sub(r'http\S+', '', x))

            punctuation = '!"#$%&()*+-/:;<=>?@[\\]^_`{|}~'
            train['clean_tweet'] = train['clean_tweet'].apply(lambda x: ''.join(ch for ch in x if ch not in set(punctuation)))
            test['clean_tweet'] = test['clean_tweet'].apply(lambda x: ''.join(ch for ch in x if ch not in set(punctuation)))

            # convert text to lowercase
            train['clean_tweet'] = train['clean_tweet'].str.lower()
            test['clean_tweet'] = test['clean_tweet'].str.lower()

            # remove numbers
            train['clean_tweet'] = train['clean_tweet'].str.replace("[0-9]", " ")
            test['clean_tweet'] = test['clean_tweet'].str.replace("[0-9]", " ")

            # remove whitespaces
            train['clean_tweet'] = train['clean_tweet'].apply(lambda x:' '.join(x.split()))
            test['clean_tweet'] = test['clean_tweet'].apply(lambda x: ' '.join(x.split()))


            # import spaCy's language model
            nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])

            # function to lemmatize text
            def lemmatization(texts):
                output = []
                for i in texts:
                    s = [token.lemma_ for token in nlp(i)]
                    output.append(' '.join(s))
                return output

            train['clean_tweet'] = lemmatization(train['clean_tweet'])
            test['clean_tweet'] = lemmatization(test['clean_tweet'])


            elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=True)
            # elmo= hub.Module('D:\\tfhub',trainable=True)

            def elmo_vectors(x):
              embeddings = elmo(x.tolist(), signature="default", as_dict=True)["elmo"]
            
              with tf.Session() as sess:
                sess.run(tf.global_variables_initializer())
                sess.run(tf.tables_initializer())
                # return average of ELMo features
                return sess.run(tf.reduce_mean(embeddings,1))


            list_train = [train[i:i+100] for i in range(0,train.shape[0],100)]
            list_test = [test[i:i+100] for i in range(0,test.shape[0],100)]


            # Extract ELMo embeddings for each 100 rows
            elmo_train = [elmo_vectors(x['clean_tweet']) for x in list_train]
            elmo_test = [elmo_vectors(x['clean_tweet']) for x in list_test]

            elmo_train_new = np.concatenate(elmo_train, axis = 0)
            elmo_test_new = np.concatenate(elmo_test, axis = 0)

            xtrain, xvalid, ytrain, yvalid = train_test_split(elmo_train_new, 
                                                  train[TargetColumn],  
                                                  random_state=42, 
                                                  test_size=0.2)

            clf = RandomForestClassifier(max_depth=None, random_state=0)
            clf.fit(xtrain, ytrain)
#print(clf.feature_importances_)
            preds_valid = clf.predict(xvalid)
            F1Score= f1_score(yvalid, preds_valid)
            preds_test = clf.predict(elmo_test_new) 
            sub = pd.DataFrame({str(InputTextColumn):test[InputTextColumn], 'label':preds_test})


            # write predictions to a CSV file
            sub.to_excel(Output_file_path, index=False)
            return {'output':'success','F1_Score': F1Score}
            
            
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = ELMo()

    # --input parameters--
    context = {'train_file_path':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\ELMO_train.xlsx",
                'test_file_path':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\ELMO_test.xlsx",
                'Output_file_path':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\Output_elmo.xlsx",
                'InputTextColumn':"tweet",
                'TargetColumn': "label"}

    resp = bot_obj.execute(context)
    print('response : ',resp)