# -*- coding: utf-8 -*-
"""
Date : 
Author : Becld
Desc :更新jiangong_qa_v1里面存的分词，节约时间，没必执行要每次都重新分词，在数据问题答案有问题的时候重新分词
数据库为测试服务器xxxxxxx，数据保持完整
"""
import jiangong_qa

jiangong_qa.Jiangong_qa().fenci()