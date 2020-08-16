from gensim.models import AuthorTopicModel
from gensim import corpora
from sklearn.manifold import TSNE
import matplotlib
import matplotlib.pyplot as plt
import json
import pickle

db3_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db3.json'
with open(db3_file, 'r', encoding = 'utf-8') as file_obj:
    db = json.load(file_obj)


########## gensim.corpora ##########
a = [['一', '一', '二'], ['一', '二', '三']]
b = ['一','一','三','四','四']
my_dictionary = corpora.Dictionary(a)

str(my_dictionary)       # 词列表 []
my_dictionary.dfs        # 词字典 {词id: 出现多少次}
print(dict(my_dictionary.items()))
my_dictionary.id2token   # 词字典 {词id: 词}
my_dictionary.token2id   # 词字典 {词: 词id}
my_dictionary.num_pos    # 所有词数
my_dictionary.num_nnz    # 不重复(篇章内不重复)词的个数之和
my_dictionary.num_docs   # 文档数

# result 为b文章转换得到的词袋，[(单词id, 词频)]
result, missing = my_dictionary.doc2bow(b, allow_update=False, return_missing=True)
print(result)
print(missing)

# bow 信息
for id, freq in result:
    print(id, ' ', my_dictionary.id2token[id], freq)
    
# 过滤文档词频大于 no_below, 小于 no_above * num_docs 的词
my_dictionary.filter_extremes(no_below=1, no_above=0.5, keep_n=10)    



######### 构造训练语料 ##########
''' 训练词袋和字典 '''

# 词袋模型 author2doc, docs
# author2doc = {诗人a: [诗人a的诗词在docs中的位置], 诗人b: [诗人b的诗词在docs中的位置], ...}
# docs = [[诗词0的分词], [诗词1的分词], ...]
author2doc = {}
docs = []

index = 0
for value in db.values():
	# 向 author2doc 添加
	author = value['author'] + '@' + value['dynasty']
	if author not in author2doc:
		author2doc[author] = [index]
	else:
		author2doc[author].append(index)
	# 向 docs 添加
	docs.append(value['seg_content_jieba'])
	index += 1


# 构建词典
dictionary = corpora.Dictionary(docs)
print(str(dictionary))
dictionary.dfs
print(dict(dictionary.items()))
dictionary.id2token
dictionary.token2id
dictionary.num_pos
dictionary.num_nnz
dictionary.num_docs
# 对文本进行向量化，得到每首诗词的稀疏向量，向量的每一个元素代表了一个 word 在这首诗词中的出现次数
corpus = [dictionary.doc2bow(doc) for doc in docs]



######### atm 模型 ##########
''' author topic model '''

# 使用 atm 模型进行训练, 设置100个主题
model = AuthorTopicModel(corpus, author2doc=author2doc, id2word=dictionary, num_topics=100)
# 保存模型
model_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/atm.model'
model.save(model_file)



######### 模型信息与降维 ##########
'''  模型信息与降维 '''

model_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/atm.model'
model = AuthorTopicModel.load(model_file)
# 模型的一些信息
model.id2author
model.author2id
model.author2doc
# 作者主题概率
model['李白@唐代']
model.get_author_topics('李白@唐代')
# 查看3个主题
model.show_topics(num_topics=3）
# 查看编号为1的主题 
model.print_topic(1)
model.get_topic_terms(1)
# 查看某个关键词在corpus中出现次数
dictionary.dfs[dictionary.token2id['归省']]


# 对作者主题特征向量降维s
tsne = TSNE(n_components=2, random_state=0)
# 最少写了0首诗词的诗人id列表
MIN_DOCS_NUM = 0
author_ids = [model.author2id[author] for author in model.author2id.keys() if len(model.author2doc[author]) >= MIN_DOCS_NUM]
# 将目标诗人的主题信息进行降维
embeddings = tsne.fit_transform(model.state.gamma[author_ids, :])
embeddings_file_w = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/embeddings.bin', 'wb')
pickle.dump(embeddings, embeddings_file_w)
embeddings_file_w.close()
# 降维前的作者主题特征向量
model.state.gamma
# 降维(二维)后的作者主题特征向量
embeddings


# 根据降维后的信息画图
def plot_embs(authors, model=model, embeddings=embeddings, figsize=(8, 5)):
	author_embs = [embeddings[model.author2id[i]] for i in authors]
	# # 显示中文
	# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
	# matplotlib.rcParams['font.family'] = 'sans-serif'
	# 显示负号
	matplotlib.rcParams['axes.unicode_minus'] = False
	# 图像大小
	plt.figure(figsize=figsize)
	for i, author in enumerate(authors):
		x = author_embs[i][0]
		y = author_embs[i][1]
		plt.scatter(x, y)
		#plt.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')


# def plot_embs2(authors, model=model, embeddings=embeddings, figsize=(8, 5)):
#     tsne = TSNE(n_components=2, random_state=0)
#     author_embs2 = tsne.fit_transform([embeddings[model.author2id[i]] for i in authors])
# 	# # 显示中文
# 	# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# 	# matplotlib.rcParams['font.family'] = 'sans-serif'
# 	# 显示负号
#     matplotlib.rcParams['axes.unicode_minus'] = False
# 	# 图像大小
#     plt.figure(figsize=figsize)
#     for i, label in enumerate(authors):
#         x, y = author_embs2[i, :]
#         plt.scatter(x, y)
# 		#plt.annotate(label, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom')



embeddings_file_r = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/embeddings.bin', 'rb')
embeddings = pickle.load(embeddings_file_r)
embeddings_file_r.close()


authors = ['柳永@宋代','晏殊@宋代','欧阳修@宋代','李煜@宋代','李清照@宋代','范仲淹@宋代','苏轼@宋代','辛弃疾@宋代','岳飞@宋代']
plot_embs(uthors)
# plot_embs2(authors)



######### 基于降维信息聚类 ##########
'''  基于降维信息作者相似度与作者聚类 '''
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# 基于降维信息进行K-均值聚类
N_CLUSTERS = 5
cls = KMeans(N_CLUSTERS).fit(embeddings)
#cls_2 = KMeans(N_CLUSTERS).fit(model.state.gamma)
markers = ['x', 'o', '*', '^', '+']
colors = ['red', 'green', 'blue', 'yellow', 'black']

plt.figure(figsize=(15, 10))
for i in range(len(embeddings)):
    plt.scatter(embeddings[i][0], embeddings[i][1], marker=markers[cls.labels_[i]], c=colors[cls.labels_[i]], alpha=0.5)


for key, value in cluster_authors.items():
    print(key, ' ', len(value))

# 各类的诗人和用词信息
cluster_authors = {'0': [], '1': [], '2': [], '3': [], '4': []}
cluster_words = {'0':[], '1': [], '2': [], '3': [], '4': []}
for i in range(len(embeddings)):
    cluster_words[str(cls.labels_[i])] += author_wordCount[model.id2author[i]]
    cluster_authors[str(cls.labels_[i])].append(model.id2author[i])
    
for key in cluster_words.keys():
    cluster_words[key] = Counter(cluster_words[key])
    cluster_words[key] = sorted(cluster_words[key].items(), key=lambda t: t[1], reverse=True)    
  

cluster_authors_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/cluster_authors.json'
cluster_words_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/cluster_words.json'
with open(cluster_authors_file, 'w', encoding='utf-8') as file_obj:
    json.dump(cluster_authors, file_obj, ensure_ascii=False, indent=4)
with open(cluster_words_file, 'w', encoding='utf-8') as file_obj:
    json.dump(cluster_words, file_obj, ensure_ascii=False, indent=4)



# 各类的标签信息
cluster_tags = {'0': {}, '1': {}, '2': {}, '3': {}, '4': {}}

for i in range(len(embeddings)):
    for tag, tag_num in sta_author[model.id2author[i]]['a_tag'].items():
        if tag in cluster_tags[str(cls.labels_[i])]:
            cluster_tags[str(cls.labels_[i])][tag] += tag_num
        else:
            cluster_tags[str(cls.labels_[i])][tag] = tag_num

for key in cluster_tags.keys():
    cluster_tags[key] = Counter(cluster_tags[key])
    cluster_tags[key] = sorted(cluster_tags[key].items(), key=lambda t: t[1], reverse=True)    

cluster_tags_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/cluster_tags.json'
with open(cluster_tags_file, 'w', encoding='utf-8') as file_obj:
    json.dump(cluster_tags, file_obj, ensure_ascii=False, indent=4)




######### 基于标签的余弦相似度 ##########
''' 基于标签信息余弦相似度 '''

import math
import numpy as np

sta_tag_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_tag.json'
with open(sta_tag_file, 'r', encoding='utf-8') as file_obj:
	sta_tag = json.load(file_obj)

sta_author_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_author.json'	
with open(sta_author_file, 'r', encoding='utf-8') as file_obj:
	sta_author = json.load(file_obj)

db_file =  '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db3.json'
with open(db_file, 'r', encoding='utf-8') as file_obj:
	db = json.load(file_obj)


# 计算余弦相似度的函数
def get_similarity(x, y):
	x_keys = sorted(x.keys())
	y_keys = sorted(y.keys())

	x_squareSum = math.sqrt(sum(np.array([x[key] for key in x_keys]) ** 2))
	y_squareSum = math.sqrt(sum(np.array([y[key] for key in y_keys]) ** 2))

	xy_sum = 0
	i = j = 0
	while i < len(x_keys) and j < len(y_keys):
		if x_keys[i] == y_keys[j]:
			xy_sum += x[x_keys[i]] * y[y_keys[j]]
			i += 1
			j += 1
		elif x_keys[i] < y_keys[j]:
			i += 1
		elif x_keys[i] > y_keys[j]:
			j += 1

	return xy_sum / (x_squareSum * y_squareSum)


''' 直接的余弦相似度 ''' 
# 李白-杜甫相似度为 0.78517
LiBai = sta_author['李白@唐代']['a_tag']
DuFu = sta_author['杜甫@唐代']['a_tag']
get_similarity(LiBai, DuFu)
    


''' 调整的余弦相似度 '''
# 0的平滑：对于那些没有带标签的诗词的诗人
# 除以带标签诗词数——诗人诗词数的不平衡
# 减去标签项的均值——处理数量上的差异


# sta_author 中新增 'a_tagPome_num'
for author, author_info in sta_author.items():
	author_info['a_tagPoem_num'] = 0
	author_info['a_tagVector'] = {}

for file_name, poem_info in db.items():
	if poem_info['tags'] != '':
		sta_author[poem_info['author'] + '@' + poem_info['dynasty']]['a_tagPoem_num'] += 1

# 一些常量
# d = 92136 首诗词
poem_num = sum(author_info['a_poem_num'] for author_info in sta_author.values())
# c = 6141 首带标签的诗词
tagPoem_num = sum(author_info['a_tagPoem_num'] for author_info in sta_author.values())
# 1323个诗人，其中730个诗人有带标签的诗
# 949 种标签

# 0的平滑及诗人诗词数不平衡调整后的标签向量
for author, author_info in sta_author.items():
	# 有带标签的诗词的诗人，标签诗词数单位化
	if len(author_info['a_tag']) > 0:
		for tag, tag_num in author_info['a_tag'].items():
			author_info['a_tagVector'][tag] = tag_num / author_info['a_tagPoem_num']
	# 没有带标签的诗词的诗人，进行平衡
	else:
		for tag, tag_info in sta_tag.items():
			author_info['a_tagVector'][tag] = author_info['a_poem_num'] * tag_info['t_num'] * (poem_num + 1) / (tagPoem_num ** 2 * (author_info['a_poem_num'] + 1))

# 标签信息新增 alpha
for tag, tag_info in sta_tag.items():
	temp = 0
	for author, author_info in sta_author.items():
		if tag in author_info['a_tagVector']:
			temp += author_info['a_tagVector'][tag]
		tag_info['alpha'] = temp / len(sta_author)

for author, author_info in sta_author.items():
	for tag in author_info['a_tagVector'].keys():
		author_info['a_tagVector'][tag] -= sta_tag[tag]['alpha']
		

a = '李白@唐代'
b = '杜甫@唐代'        
get_similarity(sta_author[a]['a_tag'], sta_author[b]['a_tag'])
get_similarity(sta_author[a]['a_tagVector'], sta_author[b]['a_tagVector'])


sta_tag3_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_tag3.json'
with open(sta_tag3_file, 'w', encoding='utf-8') as file_obj:
    json.dump(sta_tag, file_obj, ensure_ascii=False, indent=4)	

sta_author3_file = sta_author_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_author3.json'
with open(sta_author3_file, 'w', encoding='utf-8') as file_obj:
    json.dump(sta_author, file_obj, ensure_ascii=False, indent=4) 
                                                  



######### 计算相似度 ##########                                                                                                                                                                     	
''' 用一个 n * (n - 1) / 2 的上三角矩阵存储诗人间的相似性 '''
# 基于主题降维信息和标签余弦相似度计算相似度

# 载入数据
model_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/atm.model'
model = AuthorTopicModel.load(model_file)

embeddings_file_r = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/embeddings.bin', 'rb')
embeddings = pickle.load(embeddings_file_r)
embeddings_file_r.close()

sta_author_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_author3.json'	
with open(sta_author_file, 'r', encoding='utf-8') as file_obj:
	sta_author = json.load(file_obj)


# 存储结构示例
# 入
author_num = 10
examples = [[-1 for i in range(author_num - idd - 1)] for idd in range(author_num) if idd < author_num - 1]
examples
for row in range(author_num - 1):
    for col in range(author_num - row - 1):
        examples[row][col] = str(row) + '_' + str(author_num - col - 1)
examples
# 出
target = 9
result = []
if target >= 0 and target < author_num - 1:
    for col in range(len(examples[target])):
        result.append({author_num - col - 1: examples[target][col]})
    for row in range(target - 1, -1, -1):
        result.append({row: examples[row][author_num - target - 1]})
elif target == author_num - 1:
    for row in range(target):
        result.append({row: examples[row][0]})
result        



# 基于主题降维信息计算距离
author_num = len(model.id2author.keys())
emb_distances = [[-1 for i in range(author_num - idd - 1)] for idd in range(author_num) if idd < author_num - 1]
for row in range(author_num - 1):
	print(row)
    for col in range(author_num - row - 1):
        emb_distances[row][col] = math.sqrt((embeddings[row][0] - embeddings[author_num - col - 1][0]) ** 2 + (embeddings[row][1] - embeddings[author_num - col - 1][1]) ** 2)

emb_distances_file_w = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/emb_distances.bin', 'wb')
pickle.dump(emb_distances, emb_distances_file_w)
emb_distances_file_w.close()


# 基于标签向量计算余弦相似度
tag_similarities = [[-1 for i in range(author_num - idd - 1)] for idd in range(author_num) if idd < author_num - 1]
for row in range(author_num - 1):
	print(row)
    for col in range(author_num - row - 1):
        tag_similarities[row][col] = get_similarity(sta_author[model.id2author[row]]['a_tagVector'], sta_author[model.id2author[author_num - col - 1]]['a_tagVector'])

tag_similarities_file_w = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/tag_similarities.bin', 'wb')
pickle.dump(tag_similarities, tag_similarities_file_w)
tag_similarities_file_w.close()



 # 取距离
emb_distances_file_r = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/emb_distances.bin', 'rb')
emb_distances = pickle.load(emb_distances_file_r)
emb_distances_file_r.close()

tag_similarities_file_r = open('/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/atm_model/tag_similarities.bin', 'rb')
tag_similarities = pickle.load(tag_similarities_file_r)
tag_similarities_file_r.close()


def get_similarAuthors(author, num=10, emb_distances=emb_distances, tag_similarities=tag_similarities, model=model):
	target = model.author2id[author]
	author_num = len(model.id2author.keys())
	# 基于主题降维距离
	emb_result = []
	if target >= 0 and target < author_num - 1:
	    for col in range(len(emb_distances[target])):
	        emb_result.append({model.id2author[author_num - col - 1]: emb_distances[target][col]})
	    for row in range(target - 1, -1, -1):
	        emb_result.append({model.id2author[row]: emb_distances[row][author_num - target - 1]})
	elif target == author_num - 1:
	    for row in range(target):
	        emb_result.append({model.id2author[row]: emb_distances[row][0]})
	emb_result = sorted(emb_result, key=lambda x: list(x.values())[0], reverse=False)
	# 基于标签调整余弦相似
	tag_result = []
	if target >= 0 and target < author_num - 1:
	    for col in range(len(tag_similarities[target])):
	        tag_result.append({model.id2author[author_num - col - 1]: tag_similarities[target][col]})
	    for row in range(target - 1, -1, -1):
	        tag_result.append({model.id2author[row]: tag_similarities[row][author_num - target - 1]})
	elif target == author_num - 1:
	    for row in range(target):
	        tag_result.append({model.id2author[row]: tag_similarities[row][0]})
	tag_result = sorted(tag_result, key=lambda x: list(x.values())[0], reverse=True)
	# 返回
	return emb_result[:num], tag_result[:num]




