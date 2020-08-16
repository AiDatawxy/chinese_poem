# 中国古诗词文本挖掘

***作为课程学习，学习和复现了 https://github.com/liuhuanyong/PoemMining 的项目，并用 python tkinter 简单搭建了一个本地 UI 界面***

* city_map.txt
  * 地名信息
  * 地名，地点，经纬度
  
* prepare_data.py
  * 将诗词数据 .txt 文本，整合到 db/db.json 文件中
  * 统计朝代信息 result_statistics/sta_dynasty.json
  * 统计诗人信息 result_statistics/sta_author.json
  * 统计意象意境信息 result_statistics/sta_tag.json
  * 统计诗词正文及标题中地名信息 result_statistics/sta_location.json
  * 将诗词正文及标题中地名信息添加到 db/db.json 信息后，并保存为 db/db2.json
  
 * content_participle.py
  * 分词
  * 使用 jieba 包对诗词正文分词，结果添加到 db/db2.json 信息中，并保存为 db/db3.json	
  
* plot_location.py
  * 绘制诗人足迹图
  * 从百度百科获取诗人人物生平信息，结果保存为 db/author_desc.json
  * 使用 pyltp 包，对人物生平信息进行分词、词性标注、命名实体识别
  * 提取地名实体，并根据 city_map.txt 或调用腾讯地图接口获取地名经纬度，结果保存为 db/author_locations.json
  * 使用 pyecharts 包中 Geo 画诗人足迹图，结果保存在 result_plotLocation/ 中
  
* plot_wordCloud.py
  * 使用 wordcloud 包中 WordCloud 画诗人词云图，结果保存在 result_plotWordCloud/ 中
  
* atm.py
  * 使用 gensim 包中 AuthorTopicModel 构建诗人主题模型，结果保存为 atm_model/atm.* 系列文件
  * 使用 sklearn.manifold 包中 TSNE 对诗人主题模型特征变量降维，结果保存为 atm_model/embeddings.bin
  * 使用降维后的特征对诗人进行K均值聚类
  * 使用降维后的特征计算诗人间的相近度，结果保存为 atm_model/emb_distances.bin
  * 根据意象意境信息，使用调整后的余弦相似度方法计算诗人间的相似度，结果保存为 atm_model/tag_similarities.bin
  

  
