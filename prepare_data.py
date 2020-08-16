''' 数据准备 '''

################################################################
''' 将所有 .txt 文件保存到 db.json 文件中 '''
import os 
import io
import json

db = {}

# 本地
poems_dir = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/corpus_poem/'
# 服务器
# poems_dir = '/home/sufedc_nvidia_didi/Xu/poems/PoemMining-master/corpus_poem/'
poems = os.listdir(poems_dir)
for i in range(len(poems)):
    poem = poems[i]
    data = {}
    with io.open(poems_dir + poem, encoding = 'utf-8') as file_object:
        lines = file_object.readlines()
        for line in lines:
            key = line.split(':')[0].strip()
            peom = line.split(':')[1].strip()
            if key == 'star' or key == 'author_stars':
                data[key] = eval(peom)
            else:
                data[key] = peom
    db[poem.split('.')[0]] = data
    print(i)

# 写
db_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db.json'
with open(db_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(db, file_obj, ensure_ascii = False, indent = 4)



################################################################
''' 基本统计信息 '''

# 读取
db_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db.json'
with open(db_file, 'r', encoding = 'utf-8') as file_obj:
    db = json.load(file_obj)
# 例
db[list(db.keys())[0]]


# 诗扩展：地名列表  
#   'location': [{'location': location, 'lon': lon, 'lat': lat}, ...]

# 朝代：总诗词数 总诗词星数 总诗人数 总诗人星数
#   dynasty: {'d_poem_num': d_poem_num, 'd_poem_star': d_poem_star,
#               'd_author_num': d_author_num, 'd_author_star': d_poem_star}

# 诗人：总诗词数 总诗词星数 诗人星数 标签统计列表 地点统计列表
#   author@dynasty: {'a_poem_num': a_poem_num, 'a_poem_star': a_poem_star,
#              'a_author_star': a_author_star, 
#              'a_tag': {tag1: times, ...},
#              'a_location': {location1: times}}

# 标签：key列表 key列表长度
#   tag: {'t_num': t_num, 't_list': [fileName1, ...]}

# 地点：key列表 key列表长度 经度 纬度
#   location: {'l_num': l_num, 'l_list': [fileName1, ...], 'lon': lon, 'lat': lat}



db_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db.json'
with open(db_file, 'r', encoding = 'utf-8') as file_obj:
    db = json.load(db_file)


city_map_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/city_map.txt'
city_map = {i.strip().split(',')[0]: i.strip().split(',')[2:] for i in open(city_map_file) if len(i.strip().split(',')) == 5}


# 诗扩展： 地名列表
db2 = {}
for key, value in db.items():
    location = []
    content_title = value['content'] + value['title']
    nss = set([i for i in city_map if i in content_title])
    for ns in nss:
        location.append({'location': ns, 'lon': city_map[ns][2], 'lat': city_map[ns][1]})
    value['location'] = location
    db2[key] = value    

db2_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/db/db2.json'
with open(db2_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(db2, file_obj, ensure_ascii = False, indent = 4)


#
sta_dynasty = {}
sta_author = {}
sta_tag = {}
sta_location = {}

for key, poem in db2.items():
    # 基本信息
    author = poem['author']
    author_star = poem['author_stars']
    dynasty = poem['dynasty']
    poem_star = poem['star']
    tags = poem['tags'].split(';')
    title = poem['title'].replace(' ', '')
    content = poem['content']
    locations = poem['location']

    # 朝代
    if dynasty in sta_dynasty:
        # 该朝代多了多了一首诗
        sta_dynasty[dynasty]['d_poem_num'] += 1
        sta_dynasty[dynasty]['d_poem_star'] += poem_star
    else:
        # 该朝代多了一个诗人，多了一首诗
        sta_dynasty[dynasty] = {'d_poem_num': 1, 'd_poem_star': poem_star, 'd_author_num': 1, 'd_author_star': author_star}
        # 该诗人多写了一首诗
        a_tag = {}
        if tags[0] != '':
            for tag in tags:
                a_tag[tag] = 1
        a_location = {}
        if locations:
            for location in locations:
                a_location[location['location']] = 1
        sta_author[author + '@' + dynasty] = {'a_poem_num': 1, 'a_poem_star': poem_star, 'a_author_star': author_star, 'a_tag': a_tag , 'a_location': a_location}

    # 诗人
    if author + '@' + dynasty in sta_author:
        # 该诗人多了一首诗
        sta_author[author + '@' + dynasty]['a_poem_num'] += 1
        sta_author[author + '@' + dynasty]['a_poem_star'] += poem_star
        if tags[0] != '':
            for tag in tags:
                if tag in sta_author[author + '@' + dynasty]['a_tag']:
                    sta_author[author + '@' + dynasty]['a_tag'][tag] += 1
                else:
                    sta_author[author + '@' + dynasty]['a_tag'][tag] = 1
        if locations:
            for location in locations:
                if location['location'] in sta_author[author + '@' + dynasty]['a_location']:
                    sta_author[author + '@' + dynasty]['a_location'][location['location']] += 1
                else:
                    sta_author[author + '@' + dynasty]['a_location'][location['location']] = 1
    else:
        # 该朝代多了一位诗人
        sta_dynasty[dynasty]['d_author_num'] += 1
        sta_dynasty[dynasty]['d_author_star'] += author_star
        # 该诗人多了一首诗
        a_tag = {}
        if tags[0] != '':
            for tag in tags:
                a_tag[tag] = 1
        a_location = {}
        if locations:
            for location in locations:
                a_location[location['location']] = 1
        sta_author[author + '@' + dynasty] = {'a_poem_num': 1, 'a_poem_star': poem_star, 'a_author_star': author_star, 'a_tag': a_tag , 'a_location': a_location}

    # 标签
    if tags[0] != '':
        for tag in tags:
            if tag in sta_tag:
                sta_tag[tag]['t_num'] += 1
                sta_tag[tag]['t_list'].append(key)
            else:
                sta_tag[tag] = {'t_num': 1, 't_list': [key]}

    # 地点
    if locations:
        for location in locations:
            if location['location'] in sta_location:
                sta_location[location['location']]['l_num'] += 1
                sta_location[location['location']]['l_list'].append(key)
            else:
                sta_location[location['location']] = {'l_num': 1, 'l_list': [key], 'lon': location['lon'], 'lat': location['lat']}


# 朝代信息按诗词数降序
sta_dynasty = dict(sorted(sta_dynasty.items(), key = lambda x: x[1]['d_poem_num'], reverse = True))
sta_dynasty_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_dynasty.json'
with open(sta_dynasty_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(sta_dynasty, file_obj, ensure_ascii = False, indent = 4)

# 诗人信息按诗词数降序
sta_author = dict(sorted(sta_author.items(), key = lambda x: x[1]['a_poem_num'], reverse = True))
sta_author_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_author.json'
with open(sta_author_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(sta_author, file_obj, ensure_ascii = False, indent = 4)

# 标签信息按诗词数降序
sta_tag = dict(sorted(sta_tag.items(), key = lambda x: x[1]['t_num'], reverse = True))
sta_tag_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_tag.json'
with open(sta_tag_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(sta_tag, file_obj, ensure_ascii = False, indent = 4)

# 地点信息按诗词数降序
sta_location = dict(sorted(sta_location.items(), key = lambda x: x[1]['l_num'], reverse = True))
sta_location_file = '/Users/wxy/Documents/Sufepost/Courses/文本挖掘/report/MyPoemMining/result_statistics/sta_location.json'
with open(sta_location_file, 'w', encoding = 'utf-8') as file_obj:
    json.dump(sta_location, file_obj, ensure_ascii = False, indent = 4)



