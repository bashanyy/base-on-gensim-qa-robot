# -*- coding: utf-8 -*-
"""
Date : 
Author : Becld
Desc : 
"""
import pandas
import pymongo
client = pymongo.MongoClient("x.x.x.x", xx)
db = client.admin  # 先连接系统默认数据库admin
db.authenticate("xxxxx", "xxxx", mechanism='SCRAM-SHA-1')
jiangong_qa = client['jiangong_qa']  # 使用或者创建库
jiangong_qa_v1 = jiangong_qa['jiangong_qa_v1']  # 数据总表
def henanerjian():
    excel=pandas.read_excel(r'', sheet_name='在此页填写你的内容')
    for i in range(len(excel)):
        if i % 4 == 0:
            words = str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                excel.loc[i + 1]['相似问题']) + "|" + str(excel.loc[i + 2]['相似问题']) + "|" + str(excel.loc[i + 3]['相似问题'])
            daan = str(excel.loc[i]['标准答案'])
            fenci = "null"
            bigfenlei = "xxxxxxx"
            wentifenlei = str(excel.loc[i]['一级分类'])
            weight = "0"
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            liulanliang="0"
            jiangong_qa_v1.insert(
                {'bigfenlei': bigfenlei, "wentifenlei": wentifenlei, "questions": words, 'asks': daan, 'fenci': fenci,
                 'weight': weight,'times':strs,'liulanliang':liulanliang})

def henanerjian2():
    excel = pandas.read_excel(r'')
    for i in range(len(excel)):
        if i % 4 == 0:
            words = str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                excel.loc[i + 1]['相似问题']) + "|" + str(excel.loc[i + 2]['相似问题']) + "|" + str(excel.loc[i + 3]['相似问题'])
            daan = str(excel.loc[i]['标准答案'])
            fenci = "null"
            bigfenlei = "xxxxx"
            wentifenlei = str(excel.loc[i]['一级分类'])
            weight = "0"
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            liulanliang = "0"
            jiangong_qa_v1.insert(
                {'bigfenlei': bigfenlei, "wentifenlei": wentifenlei, "questions": words, 'asks': daan, 'fenci': fenci,
                 'weight': weight, 'times': strs, 'liulanliang': liulanliang})

def henananguan():
    excel = pandas.read_excel(
        r'xxxxx')
    for i in range(len(excel)):
        if i % 4 == 0:
            words = str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                excel.loc[i + 1]['相似问题']) + "|" + str(excel.loc[i + 2]['相似问题']) + "|" + str(excel.loc[i + 3]['相似问题'])
            daan = str(excel.loc[i]['标准答案'])
            fenci = "null"
            bigfenlei = "xxxxx"
            wentifenlei = str(excel.loc[i]['一级分类'])
            weight = "0"
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            liulanliang = "0"
            jiangong_qa_v1.insert(
                {'bigfenlei': bigfenlei, "wentifenlei": wentifenlei, "questions": words, 'asks': daan, 'fenci': fenci,
                 'weight': weight, 'times': strs, 'liulanliang': liulanliang})

def henananguan1():
    import datetime
    times = datetime.datetime.now()
    strs = times.strftime('%Y-%m-%d')
    excel = pandas.read_excel(r'xxxx',sheet_name='xxxx')
    lll={'bigfenlei': "xxxx", "wentifenlei": str(excel.loc[0]['一级分类']).strip(), "questions": str(excel.loc[0]['标准问题'])+"|"+str(excel.loc[0]['相似问题'])+"|"+str(excel.loc[0]['关联问题']), 'asks': str(excel.loc[0]['标准答案']), 'fenci': "null",
     'weight': "0", 'times': strs, 'liulanliang': "0"}
    for i in range(1,len(excel)):
        # print(excel.loc[i]['标准问题'])
        if pandas.isna(excel.loc[i]['标准问题']):
            hhh=""
            if pandas.notna(excel.loc[i]['相似问题']):
                hhh="|"+str(excel.loc[i]['相似问题'])
            if pandas.notna(excel.loc[i]['关联问题']):
                hhh = "|" + str(excel.loc[i]['关联问题'])
            lll['questions']+=hhh
            continue
        else:
            print(lll)
            lll = {'bigfenlei': "xxxxx", "wentifenlei": str(excel.loc[i]['一级分类']).strip(), "questions": str(excel.loc[i]['标准问题'])+"|"+str(excel.loc[i]['相似问题'])+"|"+str(excel.loc[i]['关联问题']), 'asks': str(excel.loc[i]['标准答案']), 'fenci': "null",
     'weight': "0", 'times': strs, 'liulanliang': "0"}
    print(lll)
            


def richangyongyu():#日常用语.xlsx
    excel = pandas.read_excel(
        r'E:\Becld_Codes\man_fool\webs_fool\django_for_qa\jiangong_qa\newshuju\日常用语.xlsx')
    for i in range(len(excel)):
        if i % 4 == 0:
            words = str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                excel.loc[i + 1]['相似问题']) + "|" + str(excel.loc[i + 2]['相似问题']) + "|" + str(excel.loc[i + 3]['相似问题'])
            daan = str(excel.loc[i]['标准答案'])
            fenci = "null"
            bigfenlei = "日常用语"
            wentifenlei = str(excel.loc[i]['一级分类'])
            weight = "0"
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            liulanliang = "0"
            jiangong_qa_v1.insert(
                {'bigfenlei': bigfenlei, "wentifenlei": wentifenlei, "questions": words, 'asks': daan, 'fenci': fenci,
                 'weight': weight, 'times': strs, 'liulanliang': liulanliang})


def tongyong(filename,bigfenlei):
    #格式依据日常用语，每条问答四行，没有相似问题空着，相似问题多余四条，可以合并相似问题
    #第一行头信息不要更改
    excel = pandas.read_excel(filename)
    for i in range(len(excel)):
        if i % 4 == 0:
            words = str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                excel.loc[i + 1]['相似问题']) + "|" + str(excel.loc[i + 2]['相似问题']) + "|" + str(excel.loc[i + 3]['相似问题'])
            daan = str(excel.loc[i]['标准答案'])
            fenci = "null"
            wentifenlei = str(excel.loc[i]['一级分类'])
            weight = "0"
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            liulanliang = "0"
            jiangong_qa_v1.insert(
                {'bigfenlei': bigfenlei, "wentifenlei": wentifenlei, "questions": words, 'asks': daan, 'fenci': fenci,
                 'weight': weight, 'times': strs, 'liulanliang': liulanliang})


if __name__=="__main__":
    pass
    # henanerjian()
    # henanerjian2()
    # henananguan()
    # richangyongyu()
    henananguan1()