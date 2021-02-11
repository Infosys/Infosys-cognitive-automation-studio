'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:03:15 2019

@author: Bharath_Gogineni
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from flask_cors import CORS   #Currently 'cross_origin' Not Using
from flask_restful import  Api 
from abstract_bot import Bot

# app = Flask(__name__)
# api - Api(app)


# @app.route('/api/openCV/img_path/template_path/method,Choice', methods=['POST'])
"""
img_path - Path of the image in which we need to Search 
template_path - Template image which needs to be searched for
method( optional ) -Method of searching (available methods  - cv2.TM_CCOEFF (Default), cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED )
Choice(int) - enter '1'(Default) for drawing bounding box over matched image, enter 2  for Getting co-ordinates of template 

"""
class TemplateSearchML(Bot):
    def bot_init(self):
        pass

    # def main(img_path, template_path,method='cv2.TM_CCOEFF',Choice=1):
    def execute(self, executeContext):
        try:
            img_path = executeContext['img_path']
            template_path = executeContext['template_path']
            output_file_path= executeContext['output_file_path']

            img_rgb = cv2.imread(img_path)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template = cv2.imread(template_path,0)
            w, h = template.shape[::-1]
            
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            
            cv2.imwrite(output_file_path,img_rgb)
            return {'status':"Success new bot"}

        except Exception as e:
            print('Exception : ',str(e))
            return {'Exception' :str(e)}            
    # if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port=5002, debug=True)
if __name__ == '__main__':
    context = {}
    bot_obj = TemplateSearchML()

    # --input parameters--
    context = {'img_path':"", 'template_path':"",'output_file_path':""}
#    context = {'img_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\main_image.jpg', 'template_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\template_image.jpg','output_file_path':r'D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\AI ML Bots\output.png'}
    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)