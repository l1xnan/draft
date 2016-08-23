# from mongoengine import connect
# connect('maple_pds', host='10.57.0.92', port='27017')

from pymongo import MongoClient
from datetime import datetime

from xlsx import get_xlsx_data
client = MongoClient('mongodb://10.57.0.92:27017')
db = client['maple_pds']
print('connect maple_pds')

values = get_xlsx_data('2015-2016-期末-登分表.xlsx')[1:]

gra_s = ['悉尼', '哥伦比亚', '普林斯顿', '多伦多', '斯坦福', '牛津', '剑桥', '耶鲁', '哈佛']
num_zh = ['一', '二', '三', '四', '五', '六', '七', '八', '九']


for val in values:
    gra_name = val[1][:-2]
    cla_name = val[1][-2:-1]

    gra_id = gra_s.index(gra_name) + 1
    cla_id = str(datetime.now().year -
                 gra_s.index(gra_name) - 1) + str(num_zh.index(cla_name) + 1).zfill(2)

    print(gra_id, cla_id)
    # 2016-2-01-0001
    # 2016年-第二学期-期末-考试编号
    doc = {
        'exam_id': '2016201001',
        'name': val[2],
        'grade_id': gra_id,
        'class_id': cla_id,
        'score': {
            'chinese': [val[5], 100],
            'math': [val[6], 100],
        },
    }
    # db.finalexam.insert_one(doc)
    print(doc)
