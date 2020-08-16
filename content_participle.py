''' 诗词正文分词 '''

# conda install -c conda-forge jieba
import jieba.posseg as pseg
import re
from collections import Counter
import json


################################################################
######### 使用jieba进行分词 ##########
# 输入待分词内容一段字符串 content
# 输出分词结果列表, word_list
def seg_poems_jieba(content):
    word_list = [w.word for w in pseg.cut(content) if w.flag[0] not in ['x','w']]
    return word_list    


######### 保存分词信息 ##########
db2_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db2.json'
with open(db2_file, 'r', encoding = 'utf-8') as file_obj:
	db2 = json.load(file_obj)

db3 = {}
for key, value in db2.items():
	content = value['content']
	seg_content_jieba = seg_poems_jieba(content)
	value['seg_content_jieba'] = seg_content_jieba
	db3[key] = value


db3_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db3.json'
with open(db3_file, 'w', encoding = 'utf-8') as file_obj:
	json.dump(db3, file_obj, ensure_ascii = False, indent = 4)
