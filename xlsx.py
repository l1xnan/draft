'''
参考：http://docs.xlwings.org/en/stable/index.html
'''

import xlwings as wx

'''
basepath = 'E:\\教务\\2016年下\\20160821-成绩数据分析\\'
name = '2015-2016学年第二学期期期末考试登分表.xlsx'
'''


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
    # 返回所需的工作薄
    sht = book.sheets[index]
    # 工作薄的有效数据范围
    rng = sht.range('A1').current_region
    values = rng.value
    book.close()
    return values
