'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import groupby
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
# Python Bot to create charts based on updated BotCount excel
class GenerateChartsFromExcelData(Bot):

	def bot_init(self):
		pass

	def execute(self, executeContext) :
		try:
			filePath = executeContext['filePath']
			path = os.path.dirname(filePath)
			fullPath = path+'/GIT_BOT_CHARTS'
			isdir = os.path.isdir(fullPath)
			if isdir==False:
				os.mkdir(fullPath)
				
			def add_line(ax, xpos, ypos):
				line = plt.Line2D([xpos, xpos], [ypos + .1, ypos], transform=ax.transAxes, color='darkslategrey')
				line.set_clip_on(False)
				ax.add_line(line)

			def label_len(my_index,level):
				labels = my_index.get_level_values(level)
				return [(k, sum(1 for i in g)) for k,g in groupby(labels)]

			def label_group_bar_table(ax, df):
				ypos = -.1
				scale = 1./df.index.size
				for level in range(df.index.nlevels)[::-1]:
					pos = 0
					for label, rpos in label_len(df.index,level):
						lxpos = (pos + .5 * rpos)*scale
						ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes, rotation = 0)
						add_line(ax, pos*scale, ypos)
						pos += rpos
					add_line(ax, pos*scale , ypos)
					ypos -= .1

			def pieVal(pct,data):
				val=[]
				for i in data:
					val.append(i)
				absolute = int(pct/100.*np.sum(val))
				return "{:d}".format(absolute)

			#################
			## SL_Bot_Details
			#################
			plt.style.use('ggplot')
			df = pd.read_excel(filePath, sheet_name='SL_Bot_details') 
			df = df.replace(regex=['^ '], value='-')			
			dftable = df.pivot_table(index=['SL'],values=['BotName'],aggfunc='count',fill_value=0).reset_index().rename(columns={'BotName':'Bot Count'})
			dftable = dftable.groupby('SL')['Bot Count'].sum()
			fig = plt.figure()
			ax = fig.add_subplot(111)
			dftable.plot(kind='bar',ax=fig.gca(),figsize=(15,7))			
			labels = ['' for item in ax.get_xticklabels()]
			ax.set_xticklabels(labels)
			ax.set_xlabel('')
			label_group_bar_table(ax, dftable)
			fig.subplots_adjust(bottom=.1*dftable.index.nlevels)
			for i,v in enumerate(dftable):
				plt.text(i-.03,v-1,str(v),fontweight='bold',fontsize=12)
			plt.savefig(fullPath+'/SL_BotCount_Bar.png')
			plt.clf()
			
			fig = plt.figure()
			ax = fig.add_subplot(111)
			dftable.plot(kind='pie',autopct=lambda pct: pieVal(pct,dftable),ax=fig.gca(),figsize=(15,7),labeldistance=None)
			ax.legend(labels=dftable.index,loc='center left',bbox_to_anchor=(1,0,0.5,1))
			plt.savefig(fullPath+'/SL_BotCount_Pie.png')
			plt.clf()
			
			df = df.groupby(['Branch','SL','Technology'])['Tool'].count()
			fig = plt.figure()
			ax = fig.add_subplot(111)
			df.plot(kind='bar',ax=fig.gca(),figsize=(15,7))
			labels = ['' for item in ax.get_xticklabels()]
			ax.set_xticklabels(labels)
			ax.set_xlabel('')
			label_group_bar_table(ax, df)
			fig.subplots_adjust(bottom=.1*df.index.nlevels)
			for i,v in enumerate(df):
				plt.text(i-.03,v-1,str(v),fontweight='bold',fontsize=12)
			plt.savefig(fullPath+'/SL_Technology_Branch_Tool_Bar.png')
			plt.clf()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			df.plot(kind='pie',autopct=lambda pct: pieVal(pct,df),ax=fig.gca(),figsize=(15,7),labeldistance=None)
			ax.legend(labels=df.index,loc='center left',bbox_to_anchor=(1,0,0.5,1))
			ax.yaxis.set_label_coords(-0.15,0.5)
			plt.savefig(fullPath+'/SL_Technology_Branch_Tool_Pie.png')
			plt.clf()

			#################
			## Microbots
			#################
			df1 = pd.read_excel(filePath, sheet_name='Microbots_WorkerBots')
			df1 = df1.replace(regex=['^ '], value='-')
			dftable1 = df1.pivot_table(index=['Type'],values=['BotName'],aggfunc='count',fill_value=0).reset_index().rename(columns={'BotName':'Bot Count'}) 
			dftable1 = dftable1.groupby('Type')['Bot Count'].sum()
			fig = plt.figure()
			ax = fig.add_subplot(111)
			dftable1.plot(kind='bar',ax=fig.gca(),figsize=(15,7))			
			labels = ['' for item in ax.get_xticklabels()]
			ax.set_xticklabels(labels)
			ax.set_xlabel('')
			label_group_bar_table(ax, dftable1)
			fig.subplots_adjust(bottom=.1*dftable1.index.nlevels)
			for i,v in enumerate(dftable1):
				plt.text(i-.03,v-1,str(v),fontweight='bold',fontsize=12)
			plt.savefig(fullPath+'/Type_BotCount_Bar.png')
			plt.clf()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			dftable1.plot(kind='pie',autopct=lambda pct: pieVal(pct,dftable1),ax=fig.gca(),figsize=(15,7),labeldistance=None)
			ax.legend(labels=dftable1.index,loc='center left',bbox_to_anchor=(1,0,0.5,1))
			plt.savefig(fullPath+'/Type_BotCount_Pie.png')
			plt.clf()

			df1 = df1.groupby(['Type','Tool','Technology'])['BotName'].count()
			fig = plt.figure()
			ax = fig.add_subplot(111)
			df1.plot(kind='bar',ax=fig.gca(),figsize=(25,10))
			labels = ['' for item in ax.get_xticklabels()]
			ax.set_xticklabels(labels)
			ax.set_xlabel('')
			label_group_bar_table(ax, df1)
			fig.subplots_adjust(bottom=.1*df1.index.nlevels)
			for i,v in enumerate(df1):
				plt.text(i-.1,v+1,str(v),fontweight='bold',fontsize=12)
			plt.savefig(fullPath+'/BotType_Tool_Technology_Bar.png')
			plt.clf()

			fig = plt.figure()
			ax = fig.add_subplot(111)
			df1.plot(kind='pie',autopct=lambda pct: pieVal(pct,df1),ax=fig.gca(),figsize=(15,7),labeldistance=None)
			ax.legend(labels=df1.index,loc='center left',bbox_to_anchor=(1,0,0.5,1))
			ax.yaxis.set_label_coords(-0.15,0.5)
			plt.savefig(fullPath+'/BotType_Tool_Technology_Pie.png')
			plt.clf()

			return {'Status' : 'Success and new folder is created in the filePath directory.'}
		except Exception as e:
			return {'Exception' : str(e)}

  
if __name__ == '__main__':
	context = {}
	bot_obj = GenerateChartsFromExcelData()

	context =  {'filePath':''}
	bot_obj.bot_init()
	resp = bot_obj.execute(context)
	print('response : ',resp)