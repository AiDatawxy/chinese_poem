############################################################
''' 1 '''
from tkinter import *
from tkinter import scrolledtext
import os
import json
import pickle
from PIL import Image, ImageTk
import matplotlib 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from collections import Counter


os.chdir('C:/Users/yxzypx/Desktop/PoemPortrain')
os.getcwd()

############################################################
''' 2 数据准备 '''

# 诗人人物生平 李白
with open('data/author_desc.json', 'r', encoding='utf-8') as file_obj:
	author_desc = json.load(file_obj)

# 诗人足迹地名 李白
with open('data/author_locations.json', 'r', encoding='utf-8') as file_obj:
	author_locations = json.load(file_obj)

# 诗人词列表 李白@唐代
with open('data/author_wordCount.json', 'r', encoding='utf-8') as file_obj:
	author_wordCount = json.load(file_obj)

# 数据源
with open('data/db3.json', 'r', encoding='utf-8') as file_obj:
	db = json.load(file_obj)

# 诗人统计信息 
with open('data/sta_author3.json', 'r', encoding='utf-8') as file_obj:
	sta_author3 = json.load(file_obj)

# id2author
with open('data/id2author.json', 'r', encoding='utf-8') as file_obj:
	id2author = json.load(file_obj)

# author2id
with open('data/author2id.json', 'r', encoding='utf-8') as file_obj:
	author2id = json.load(file_obj)

# 降维后信息
embeddings_file_r = open('data/embeddings.bin', 'rb')
embeddings = pickle.load(embeddings_file_r)
embeddings_file_r.close()

# 距离矩阵 
emb_distances_file_r = open('data/emb_distances.bin', 'rb')
emb_distances = pickle.load(emb_distances_file_r)
emb_distances_file_r.close()

# 相似度矩阵
tag_similarities_file_r = open('data/tag_similarities.bin', 'rb')
tag_similarities = pickle.load(tag_similarities_file_r)
tag_similarities_file_r.close()

# 各朝代有哪些诗人，各诗人有哪些诗
dynasty_authors = {}
author_poems = {}
for value in db.values():
	if value['dynasty'] in dynasty_authors:
		if value['author'] not in dynasty_authors[value['dynasty']]:
			dynasty_authors[value['dynasty']].append(value['author'])
	else:
		dynasty_authors[value['dynasty']] = [value['author']]
	if value['author'] + '@' + value['dynasty'] in author_poems:
		author_poems[value['author'] + '@' + value['dynasty']].append(value['title'])
	else:
		author_poems[value['author'] + '@' + value['dynasty']] = [value['title']]

# 哪些诗人有足迹图
has_plotLocation = [file_name.split('.')[0].split('足迹图')[0] for file_name in os.listdir('result_plotLocation')]

# 获取距离及相似度的函数
def get_similarAuthors(author, num=10, emb_distances=emb_distances, tag_similarities=tag_similarities, id2author=id2author, author2id=author2id):
	target = author2id[author]
	author_num = len(id2author.keys())
	# 基于主题降维距离
	emb_result = []
	if target >= 0 and target < author_num - 1:
	    for col in range(len(emb_distances[target])):
	        emb_result.append({id2author[str(author_num - col - 1)]: emb_distances[target][col]})
	    for row in range(target - 1, -1, -1):
	        emb_result.append({id2author[str(row)]: emb_distances[row][author_num - target - 1]})
	elif target == author_num - 1:
	    for row in range(target):
	        emb_result.append({id2author[str(row)]: emb_distances[row][0]})
	emb_result = sorted(emb_result, key=lambda x: list(x.values())[0], reverse=False)
	# 基于标签调整余弦相似
	tag_result = []
	if target >= 0 and target < author_num - 1:
	    for col in range(len(tag_similarities[target])):
	        tag_result.append({id2author[str(author_num - col - 1)]: tag_similarities[target][col]})
	    for row in range(target - 1, -1, -1):
	        tag_result.append({id2author[str(row)]: tag_similarities[row][author_num - target - 1]})
	elif target == author_num - 1:
	    for row in range(target):
	        tag_result.append({id2author[(row)]: tag_similarities[row][0]})
	tag_result = sorted(tag_result, key=lambda x: list(x.values())[0], reverse=True)
	# 返回
	return emb_result[:num], tag_result[:num]


############################################################
''' 4 '''
class PoetPortrait:

	def __init__(self):

		self.window = Toplevel()
		self.window.title('诗人画像')
		self.window.geometry('1800x1000')
		self.frame_client = FrameSelect(self.window)
		self.frame_client.pack(side=LEFT, fill=Y)
		self.frame_server = Frame(self.window)
		self.frame_server.pack(side=LEFT, fill=Y)

		self.frame_serverBt = Frame(self.frame_server)
		self.frame_serverBt.pack()
		self.bt_authorSelf = Button(self.frame_serverBt, text='查看诗人', command=self.f_bt_authorSelf)
		self.bt_authorSelf.pack(side=LEFT)
		self.bt_auhthorRelated = Button(self.frame_serverBt, text='查看相关诗人', command=self.f_bt_authorRelated)
		self.bt_auhthorRelated.pack(side=LEFT)

		self.frame_show = FrameShow(self.frame_server)
		self.frame_show.pack()
		self.frame_similar = FrameSimilar(self.frame_server)

		self.window.mainloop()


	def f_bt_authorSelf(self):
		self.frame_similar.pack_forget()		
		self.frame_show.f_setDynasty(self.frame_client.f_getDynasty())
		self.frame_show.f_setAuthor(self.frame_client.f_getAuthor())
		self.frame_show.f_setPoem(self.frame_client.f_getPoem())	
		self.frame_show.f_showBasic()
		self.frame_show.f_showDesc()
		self.frame_show.f_showWord()
		self.frame_show.f_plotLocation()
		self.frame_show.f_plotWordCloud()
		self.frame_show.pack()


	def f_bt_authorRelated(self):
		self.frame_show.pack_forget()
		self.frame_similar.f_setDynasty(self.frame_client.f_getDynasty())
		self.frame_similar.f_setAuthor(self.frame_client.f_getAuthor())
		self.frame_similar.f_calculate()
		self.frame_similar.f_disAuthors()
		self.frame_similar.f_disTags()
		self.frame_similar.f_disWords()
		self.frame_similar.f_disPlot()
		self.frame_similar.f_simAuthors()
		self.frame_similar.f_simTags()
		self.frame_similar.f_simWords()
		self.frame_similar.f_simPlot()
		self.frame_similar.pack()


############################################################
''' 5 '''
PoetPortrait()


