# -*- coding: utf-8 -*-
"""
Date : 
Author : Becld
Desc : 
"""
import pymongo
import pandas

filename=r'E:\Becld_Codes\man_fool\webs_fool\django_for_qa\jiangong_qa\newshuju\活动群.xlsx'
excel = pandas.read_excel(filename,sheet_name="Sheet2")
counts=100012
client = pymongo.MongoClient("139.9.149.47", 8102)
db = client.admin  # 先连接系统默认数据库admin
db.authenticate("admin", "123456", mechanism='SCRAM-SHA-1')
jiangong_qa = client['jiangong_qa']  # 使用或者创建库
idyingshe = jiangong_qa['idyingshe']  # 使用或者创建表
for i in excel.values:
    dicts={}
    dicts['bigfenlei']=i[1]
    dicts['bigfenlei_id']=str(i[0])
    dicts['wentifenlei']=i[2]
    dicts['wentifenlei_id']=str(counts)
    counts+=1
    idyingshe.insert(dicts)

