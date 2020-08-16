''' 绘制诗人足迹图 '''

################################################################
''' 从百度百科获取人物生平信息 '''

from urllib import request
from lxml import etree
from urllib import parse
import json
import time
import random 


######### 请求数据 ##########  
# 输入 url
# 输出经过 utf-8 编码的 html 文件   
def get_html(url):
    return request.urlopen(url).read().decode('utf-8')


######### 获取诗人生平事迹 ##########
# 输入诗人名 word
# 输出百度百科中，该诗人的“人物生平”介绍字符串 desc
def extract_desc(word):
    # 诗人名 word 的百度百科
    url = "http://baike.baidu.com/item/%s" % parse.quote(word)
    html = get_html(url)
    # 百度百科中，'人物生平'的内容
    content = [i for i in html.split('<h2 class="title-text">') if word + '</span>人物生平</h2>' in i]
    if content:
        selector = etree.HTML(content[0])
        res = [i.xpath('string(.)').replace('\n','').replace('\xa0','') for i in selector.xpath('//div[@class="para"]')]
        desc = ''.join([i for i in res if i])
    else:
        desc = []
    print(url)
    return desc


######### 从百度百科获取信息 ##########
'''
author_poem 中，有 1323 条 '诗人@朝代'
去重单独的author有 1236 条
有87个重名的情况
其中有的是在不同朝代的两个同名的人，如“李治”分布出现在唐朝、元朝，但百度百科中只有唐朝李治的词条
有的是同一个人在不同诗中列属不同朝代，如丘处机同时出现在宋朝、元朝
简单起见，以 1236 条的这个处理

在百度百科中，有的诗人没有“人物生平”这项，如 王之望
'''

author_poem_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/author_poem.json'            
with open(author_poem_file, 'r', encoding = 'utf-8') as file_obj:
    author_poem = json.load(file_obj)

authors = []
for key in author_poem.keys():
    authors.append(key.split('@')[0])
authors = list(set(authors))    
len(authors)

# 爬取
author_life = {}
i = 0
for author in authors:
    desc = extract_desc(author)
    if desc: 
        author_life[author] = desc
    print(i)
    i += 1
    time.sleep(random.randint(3, 5))


i
j = i
authors[j]
author_life[authors[j]]


# 写 456 个诗人
author_desc_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/author_desc.json'
with open(author_desc_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(author_life, file_obj, ensure_ascii = False, indent = 4)




################################################################
''' LTP 分词、命名实体识别将人物生平中的地点提取出来 '''

# pyltp 分词、词性标准、命名实体标注集 http://ltp.ai/docs/appendix.html#id2

######### LTP分词准备 ##########
import os
import re
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer

LTP_DIR = ".../ltp_data"
# 分词
# B词首，I词中，E词尾，S单字成词
segmentor = Segmentor()
segmentor.load(os.path.join(LTP_DIR, "cws.model"))
# 词性标注
postagger = Postagger()
postagger.load(os.path.join(LTP_DIR, "pos.model"))
# 依存句法分析
parser = Parser()
parser.load(os.path.join(LTP_DIR, "parser.model"))
# 命名实体识别
# O这个词不是NE, S这个词单独构成一个NE，B这个词为一个NE的开始，I这个词为一个NE的中间，E这个词为一个NE的结尾
# Nh人名，Ni机构名，Ns地名
recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(LTP_DIR, "ner.model"))


######### 长句切分 ##########
# 输入内容
# 输出短句列表
# 将一个长句子去除干扰字符后按指定标点切分
def seg_long_sents(content):
    # 去除空格' ', 中文全角空格 '\u3000', 中文破折号'——'
    # 之后根据‘？’ ‘！’ '?' '!' '。' 换行 回车 切分长句
    return [sentence for sentence in re.split(r'[？?！!。\n\r]', content.replace(' ','').replace('\u3000','').replace('——','')) if sentence]


######### ltp基本操作 ##########
# 输入词向量words
# 输出词向量中各词的词性标柱postags和命名实体识别netags
def basic_parser(words):
    # 词性标柱
    postags = list(postagger.postag(words))
    # 命名实体识别
    netags = recognizer.recognize(words, postags)
    return postags, netags


######### 基于实体识别结果,整理输出实体列表 ##########
# 输入词向量words和命名实体识别netags
# 输出地名实体列表place_entity_list
def format_entity(words, netags):
    name_entity_list = []           # 人名实体列表
    place_entity_list = []          # 地点实体列表
    organization_entity_list = []   # 机构实体列表
    ntag_E_Nh = ""                  # 人名Nh
    ntag_E_Ni = ""                  # 机构名
    ntag_E_Ns = ""                  # 地名Ns
    index = 0
    # 词和识别命名实体的配对元组 item = [(word1, netag1), (word2, netag2), ...]
    for item in zip(words, netags):
        word = item[0]              # 词
        ntag = item[1]              # 识别命名实体    
        # 是NE
        if ntag[0] != "O":
            # 单独构成一个NE
            if ntag[0] == "S":
                # 人名
                if ntag[-2:] == "Nh":
                    name_entity_list.append(word)
                # 机构名
                elif ntag[-2:] == "Ni":
                    organization_entity_list.append(word)
                # 地名
                else:
                    place_entity_list.append(word)
            # 作为一个NE的开始
            elif ntag[0] == "B":
                if ntag[-2:] == "Nh":
                    ntag_E_Nh = ntag_E_Nh + word
                elif ntag[-2:] == "Ni":
                    ntag_E_Ni = ntag_E_Ni + word
                else:
                    ntag_E_Ns = ntag_E_Ns + word
            # 作为一个NE的中间
            elif ntag[0] == "I":
                if ntag[-2:] == "Nh":
                    ntag_E_Nh = ntag_E_Nh + word
                elif ntag[-2:] == "Ni":
                    ntag_E_Ni = ntag_E_Ni + word
                else:
                    ntag_E_Ns = ntag_E_Ns + word
            # E 作为一个NE的结尾
            else:
                if ntag[-2:] == "Nh":
                    ntag_E_Nh = ntag_E_Nh + word
                    name_entity_list.append(ntag_E_Nh)
                    ntag_E_Nh = ""
                elif ntag[-2:] == "Ni":
                    ntag_E_Ni = ntag_E_Ni + word
                    organization_entity_list.append(ntag_E_Ni)
                    ntag_E_Ni = ""
                else:
                    ntag_E_Ns = ntag_E_Ns + word
                    place_entity_list.append(ntag_E_Ns)
                    ntag_E_Ns = ""
        index += 1
    return place_entity_list


######### 整合获取地点列表的函数 ##########    
# 主调函数
# 输入内容
# 输出地点列表
def collect_locations(content):
    # 地点列表
    locations = []
    # 短句列表
    sents = seg_long_sents(content)
    for i in sents:
        # 分词为词列表
        words = list(segmentor.segment(i))
        # 词性标柱 + 命名实体识别
        postags, netags = basic_parser(words)
        # 根据命名实体识别结果获得地点实体列表
        locations += format_entity(words, netags)
    return locations





################################################################
''' 获取地点的坐标 '''


######### 从地点信息文件获取地点信息 ##########
# city_map.txt 是一个已知的地名字典  748个不重复的地名
# 地名及地名信息字典 key: 地名, peom: [市/地区, 经度, 纬度]
city_map = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/city_map.txt'
name_dict = {i.strip().split(',')[0]: i.strip().split(',')[2:] for i in open(city_map) if len(i.strip().split(',')) == 5}
base = '''
      <!DOCTYPE HTML>
       <html>
           <head>
               <meta charset="utf-8"><link rel="icon" href="https://static.jianshukeji.com/highcharts/images/favicon.ico">
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <script src="https://img.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
               <script src="https://img.hcharts.cn/highmaps/highmaps.js"></script>
               <script src="https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.3.6/proj4.js"></script>
           </head>
           <body>
               <div id="container" style=" height: 1000px"></div>
               <script src="https://data.jianshukeji.com/geochina/china.js"></script>
               <script>
                   var data = [
                           target_datas
                           ];

                   var map = new Highcharts.Map('container', {
                       title: {
                           text: 'author'
                       },
                       mapNavigation: {
                           enabled: true,
                           buttonOptions: {
                               verticalAlign: 'bottom'
                           }
                       },
                       tooltip: {
                           useHTML: true,
                           formatter: function() {
                               return this.point.name;
                           }
                       },
                       plotOptions: {
                           series: {
                               dataLabels: {
                                   enabled: true
                               },
                               marker: {
                                   radius: 3
                               }
                           }
                       },
                       series: [{
                           // 空数据列，用于展示底图
                           mapData: Highcharts.maps['cn/china'],
                           showInLegend: false
                       },{
                           type: 'mappoint',
                           name: 'author',
                           data: data
                       }]
                   });
               <!--});-->
               </script>
           </body>
       </html>
       '''


######### 调用远程api，获取绝对经纬度 ##########
# 输入地名 loc
# 返回 [地名, 市/地区, 经度, 纬度]
# 调用远程 api 获取
def get_abs_geo(loc):
    # 如关于上海信息的url: https://apis.map.qq.com/jsapi?qt=poi&wd=%E4%B8%8A%E6%B5%B7
    url = 'https://apis.map.qq.com/jsapi?qt=poi&wd=' + parse.quote(loc)
    data = request.urlopen(url).read().decode('gbk')
    data_json = json.loads(data)
    name = ''
    lon = 0
    lat = 0
    if 'pois' in data_json['detail']:
        if len(data_json['detail']['pois']) > 0:
            city_info = data_json['detail']['pois'][0]
            name = loc
            lon = str(city_info['pointx'])
            lat = str(city_info['pointy'])
    else:
        if 'city' in data_json['detail']:
            city_info = data_json['detail']['city']
            lon = str(city_info['pointx'])
            lat = str(city_info['pointy'])
            name = city_info['cname']

    if name == '全国':
        return []
    if name and lon and lat:
        print(loc, '>>> ', url)
        return [loc, name, lat, lon]
    else:
        return []


######### 综合地点坐标获取方法 ##########
# 输入地点 loc
# 返回 [地点, 市/区, 精度, 纬度]
def transfer_location(loc):
    # 从地名字典中获得 loc 地点的信息
    geo_info = name_dict.get(loc, 'na')
    # 从地名字典中获取信息
    if geo_info != 'na':
        print(loc, '>>> ', 'name_dict')
        return [loc] + geo_info
    # 或者调用远程api获取信息
    else:
        tmp = get_abs_geo(loc)
        if not tmp:
            return []
        else:
            return tmp


################################################################
''' 挖掘地点信息与作图 '''


######### 将诗人人物生平中的地点挖出来 ##########
author_desc_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/author_desc.json'
with open(author_desc_file, 'r', encoding = 'utf-8') as file_obj:
    author_desc = json.load(file_obj)


author_locations = {}
i = 1
for author in authors:
    print(i, '-----------------------', author, '-----------------------')
    locations = collect_locations(author_desc[author])
    if locations:
        locations = [transfer_location(i) for i in set(locations)]
        author_locations[author] = locations
    print('-----------------------', len(locations), '-----------------------')    
    i += 1


i_duplicate = i
j = i - 1
authors[j]
author_locations[authors[j]]


# 写
author_locations_file = '/home/sufedc_nvidia_didi/Xu/poems/db/author_locations.json'            
with open(author_locations_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(author_locations, file_obj, ensure_ascii = False, indent = 4)


######### 作图 ##########
import json
from pyecharts import Geo

author_locations_file = './db/author_locations.json'
with open(author_locations_file, 'r', encoding='utf-8') as file_obj:
  author_locations = json.load(file_obj)


author = '杜甫'

locations = [location for location in author_locations[author] if location != []] 
location_names = [location[0] for location in locations]

geo = Geo(author + '足迹图', title_pos='center', title_top='top', title_text_size=15, width=700, height=700)
for location in locations:
  geo.add_coordinate(location[0], location[3], location[2])

geo.add('', location_names, range(len(locations)), maptype='china', geo_normal_color='white', 
    geo_emphasis_color='skyblue', symbol_size=7, is_visualmap=True, is_label_show=False, 
    label_text_color='black', label_text_size=7, label_formatter='{b}')

geo.add("",
        location_names, range(len(locations), maptype="china", geo_normal_color='white', geo_emphasis_color='skyblue', symbol_size=7,
        is_visualmap=False, 
        is_label_show=True,
        label_text_color='black',
        label_text_size=7,
        label_formatter='{b}')         
geo.render("dufu.html") 


# 批量作图
count = 0
for author in author_locations.keys():

    locations = [location for location in author_locations[author] if location != []] 
    location_names = [location[0] for location in locations]


    geo = Geo(author + '足迹图', title_pos='center', title_top='top', title_text_size=15, width=1000, height=1000)
    for location in locations:
        geo.add_coordinate(location[0], location[3], location[2])


    geo.add('', location_names, range(len(locations)), maptype='china', geo_normal_color='white', 
        geo_emphasis_color='skyblue', symbol_size=7, is_visualmap=False, is_label_show=False)
    file_name = '/home/sufedc_nvidia_didi/Xu/poems/yanxin/result_plotLocation/{}.html'.format(author.encode('utf-8'))
    geo.render(file_name) 
    print(count)
    count += 1



