''' 诗人词云图 '''

import json 
from collections import Counter
from pyecharts import WordCloud 


# ######### 例 ##########  
# name =['中', '万能']
# value =[10000, 6181]

# wordcloud =WordCloud(width=1300, height=620)
# wordcloud.add("", name, value, word_size_range=[20, 100], shape='diamond')
# wordcloud.render('d.html')


# ######### 作图 ##########  
# # 词列表
# db_file = '/home/sufedc_nvidia_didi/Xu/poems/db/db3.json'
# with open(db_file, 'r', encoding='utf-8') as file_obj:
#     db = json.load(file_obj)
    

# author_wordCount = {}
# for value in db.values():
#     author = value['author'] + '@' + value['dynasty']
#     if author in author_wordCount:
#         author_wordCount[author] += value['seg_content_jieba'][:]
#     else:
#         author_wordCount[author] = value['seg_content_jieba'][:]


# author_wordCount_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_plotWordCloud/author_wordCount.json'
# with open(author_wordCount_file, 'w', encoding='utf-8') as file_obj:
#     author_wordCloud = json.dump(author_wordCloud, file_obj, ensure_ascii=False, indent=4)


# # 一个例子
# author_wordCount_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_plotWordCloud/author_wordCount.json'
# with open(author_wordCount_file, 'r', encoding='utf-8') as file_obj:
#     author_wordCloud = json.load(file_obj)

# wordCount = Counter(author_wordCount['李白@唐代'])
# words = []
# values = []
# for word, value in wordCount.items():
#     words.append(word)
#     values.append(value)

# sorted(wordCount.items(), key=lambda x: x[1], reverse=True)[100:120]

# wordCloud = WordCloud(width=1300, height=620)
# wordCloud.add('', words, values, word_size_range=[20, 100], shape='diamond')
# wordCloud.render('LiBai.html')


# # 批量作图
# count = 0
# for author in author_wordCount.keys():
# 	wordCount = Counter(author_wordCount[author])
# 	words = []
# 	values = []
# 	for word, value in wordCount.items():
# 		words.append(word)
# 		values.append(value)
# z
# 	wordCloud = WordCloud(width=1300, height=620)
# 	wordCloud.add('', words, values, word_size_range=[20, 100], shape='diamond')
# 	file_name = '/home/sufedc_nvidia_didi/Xu/poems/yanxin/result_plotWordCloud/{}.html'.format(author.encode('utf-8'))
# 	wordCloud.render(file_name)




######### 一个例子 ##########  
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import random


result = '一 二 三 四 一 二 三 四 像 首 歌 绿色 军营'
wc = WordCloud(
    font_path='STHeiti Medium.ttc',     #字体
    background_color='black',   	#背景颜色
    width=1000,
    height=600,
    max_font_size=50,            #字体大小
    min_font_size=10,
    #背景图片
    mask=plt.imread('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/cluster_similarity/background.jpg'),  
    max_words=1000
)


wc.generate(result)
wc.to_file('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_plotWordCloud/jielun.png')   


######### 作图 ##########  
author_wordCount_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/cluster_similarity/author_wordCount.json'
with open(author_wordCount_file, 'r', encoding='utf-8') as file_obj:
    author_wordCount = json.load(file_obj)


def random_color(word, font_size, position, orientation, font_path, random_state):
    s = 'hsl(%d, %d%%, %d%%)' % (h, random.randint(60, 80), random.randint(60, 80))
    return s

wordCloud = WordCloud(
	color_func = random_color,
    # 字体
    font_path = 'STHeiti Medium.ttc',
    width = 5000, height = 3000,
    max_font_size = 80,
    min_font_size = 10,
    #mode = 'RGBA',     
    # 背景图片
    #mask=plt.imread('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/cluster_similarity/background.png'),  
    mask=np.array(Image.open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/cluster_similarity/background_3.png')),  
    max_words=1000,
    random_state = 30
)


target_dir = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_plotWordCloud/'

#
author = '李白@唐代'
text = ''
for word in author_wordCloud[author]:
    text += word + ' '

wordCloud.generate(text)
wordCloud.to_file(target_dir + author + '词云图.png')


#
count = 1
for author in author_wordCount.keys():
    h = random.randint(0, 360)

    def random_color(word, font_size, position, orientation, font_path, random_state):
        s = 'hsl(%d, %d%%, %d%%)' % (h, random.randint(60, 80), random.randint(60, 80))
        return s

    wordCloud = WordCloud(
    	color_func = random_color,
     	background_color = 'white', 
        font_path = 'STHeiti Medium.ttc',
        width = 5000, height = 3000,
        max_font_size = 90,
        min_font_size = 10,
        mode = 'RGBA',     
        mask=np.array(Image.open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/cluster_similarity/background_3.jpg')),  
        max_words=1000,
        random_state = 30
    )

    text = ''
    for word in author_wordCloud[author]:
        text += word + ' '
    wordCloud.generate(text)
    wordCloud.to_file(target_dir + author + '词云图.png')
    print(count)
    count += 1
    
