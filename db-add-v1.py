# from mongoengine import connect
# connect('maple_pds', host='10.57.0.92', port='27017')

from pymongo import MongoClient
from datetime import datetime

import xlwings as wx


def get_xlsx_data(pathname, index=0):
    '''
    args:
        pathname: 需要获取数据的 Excel 文件路径.
        index: 需要获取的工作薄的索引或名称，默认值为 0，即第一个工作薄

    return:
        二维列表，返回工作薄的数据
    '''
    # 静默状态下打开 Excel
    # 打开所需的工作表
    app = wx.App(visible=False)
    try:
        book = app.books.open(pathname)
    except FileNotFoundError:
        print('文件没有找到！')
        raise
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        print('sucess open file!')
    # 返回所需的工作薄
    sht = book.sheets[index]
    # 工作薄的有效数据范围
    rng = sht.range('A1').current_region
    values = rng.value
    book.close()
    return values


client = MongoClient('mongodb://10.57.0.92:27017')
db = client['maple_pds']
print('connect maple_pds')

values = get_xlsx_data('data/2015-2016-期末-登分表.xlsx')[1:]


gra_s = ['悉尼', '哥伦比亚', '普林斯顿', '多伦多', '斯坦福', '牛津', '剑桥', '耶鲁', '哈佛']
num_zh = ['一', '二', '三', '四', '五', '六', '七', '八', '九']


for val in values:
    gra_name = val[1][:-2]
    cla_name = val[1][-2:-1]

    gra_id = gra_s.index(gra_name) + 1
    cla_id = str(datetime.now().year -
                 gra_s.index(gra_name) - 1) + str(num_zh.index(cla_name) + 1).zfill(2)

    print(gra_id, cla_id)
    # 2016-01-00001
    # 2016年-1月-考试编号
    # 01: 第一次月考
    # 02: 期中
    # 03: 第二次月考
    # 04: 期末
    # 05: 周清
    # 06: 日常
    exam_id = '2016060001'
    doc = {
        '_id': exam_id + val[8][1:],
        'exam_id': exam_id,
        'student_id': val[8],
        'name': val[2],
        'grade_id': gra_id,
        'class_id': cla_id,
        'score': {
            'chinese': {
                'state': 0 if type(val[5]) in [int, float] else 1,
                'final': val[5],
                'full': 100 if gra_id <= 6 else 120,
            },
            'math': {
                'state': 0 if type(val[5]) in [int, float] else 1,
                'final': val[6],
                'full': 100 if gra_id <= 6 else 120,
            },
        },
    }
    db.finalexam.replace_one({'_id': doc['_id']}, doc, True)
    print(doc)
print('=' * 30)
