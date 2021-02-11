'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:46:48 2020

@author: vaddi.kumar01
"""


import numpy as np
import matplotlib.pyplot as plt
import json
import en_core_web_md
from collections import OrderedDict
import spacy
import pandas as pd
from abstract_bot import Bot

class NERUsingSpacy(Bot):
    def execute(self,executeContext):
        try:
            input_file_path = executeContext['input_file_path']
            textColumnName = executeContext['textColumnName']
            target_file_path = executeContext['target_file_path']
            
            def ner(string1):
                nlp = spacy.load("en_core_web_md")
                doc = nlp(string1)
                for ent in doc.ents:
                    return(ent.text+","+ ent.label_)
                    
            temp_df= pd.read_excel(input_file_path)
            temp_df['NamedEntities']= temp_df[textColumnName].apply(ner)
                    
                    # Saving The Named Entity Recognintion Model 
            temp_df.to_excel(target_file_path, index=False)
            return {'Output':'NER Updated'}
        except Exception as e:
            return {'Error Found': str(e)}
            
if __name__ == '__main__':
    context = {}
    bot_obj = NERUsingSpacy()

    # --input parameters--
    context = {'input_file_path':'', 
               'textColumnName':'description',
               'target_file_path':''}

#    context = {'input_file_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\NER_sample.xlsx', 
#               'textColumnName':'description',
#               'target_file_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\NER_spacy_output.xlsx'}

    resp = bot_obj.execute(context)
    print('response : ',resp)
