# -*- coding: utf-8 -*-
"""
Date : 
Author : Becld
Desc : 
"""
# pip install jieba -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
from gensim import corpora, models, similarities
from collections import defaultdict
import jieba
import pymongo
import pandas
import numpy as np
import pandas as pd
from pprint import pprint
import os,time
import platform
from bson.objectid import ObjectId
from django_for_qa.settings import BASE_DIR
class Jiangong_qa:
    def __init__(self):
        # self.client = pymongo.MongoClient("xxxx", xxxx)
        # self.jiangong_qa = self.client['jiangong_qa']  # 使用或者创建库
        # self.jiangong_qa_v1 = self.jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
        # self.jiangong_qa_corpus = self.jiangong_qa['jiangong_qa_corpus']  # 使用或者创建表

        self.client = pymongo.MongoClient("xxxxx", xxx)
        self.db = self.client.admin  # 先连接系统默认数据库admin
        self.db.authenticate("xxxxx", "xxxxx", mechanism='SCRAM-SHA-1')
        self.jiangong_qa = self.client['jiangong_qa']  # 使用或者创建库
        self.jiangong_qa_v1 = self.jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
        self.jiangong_qa_corpus = self.jiangong_qa['jiangong_qa_corpus']  # 使用或者创建表
        self.jiangong_qa_corpus1 = self.jiangong_qa['jiangong_qa_corpus1']  # 使用或者创建表
        self.countqa=self.jiangong_qa['countqa']
        self.idyingshe=self.jiangong_qa['idyingshe']
        self.kongzhicishu=self.jiangong_qa['kongzhicishu']#控制评价次数
        self.kongzhicishu1=self.jiangong_qa['kongzhicishu1']#控制点赞次数
        self.duihua=self.jiangong_qa['duihua']#对话语料存储

    def get_bigid(self,ids):
        result=self.idyingshe.find_one({"bigfenlei_id":ids})
        return result['bigfenlei']
    def get_wentiid(self,ids):
        result = self.idyingshe.find_one({"wentifenlei_id": ids})
        return result['wentifenlei']

    def get_bigfenlei(self,strs):
        bigfenlei=set()
        for i in self.jiangong_qa_v1.find({'bigfenlei':strs}):
            bigfenlei.add(i['wentifenlei'])
        return bigfenlei
    def get_bigfenlei1(self,ids):
        return self.idyingshe.find({'bigfenlei_id':ids})
    def get_bigfenlei2(self,ids):
        return self.idyingshe.find_one({'bigfenlei_id':ids})['bigfenlei']

    def get_wentifenlei(self,strs1,strs2):
        result=self.jiangong_qa_v1.find({'bigfenlei':strs1,"wentifenlei":strs2},{"bigfenlei":1,"wentifenlei":1,"questions":1,"asks":1,"_id":1})

        lists=[]
        for i in result:
            lists.append({"questions":i["questions"].split("|")[0],"asks":i["asks"],"mo_id":str(i['_id'])})
        return lists

    def set_countqa1(self,mo_id,yes,yonghuid):
        lists=self.kongzhicishu1.find({"mo_id":mo_id,"yonghuid":yonghuid})
        if len(list(lists))==0:

            result = self.jiangong_qa_v1.find({"_id": ObjectId(mo_id)})
            if result:

                for i in result:
                    if yes=="1":
                        self.jiangong_qa_v1.update({"_id": ObjectId(mo_id)}, {"$set": {"weight": str(int(i['weight']) + 1)}})
                    else:
                        self.jiangong_qa_v1.update({"_id": ObjectId(mo_id)}, {"$set": {"weight": str(int(i['weight']) - 1)}})
                self.kongzhicishu1.insert({"mo_id": mo_id, "yonghuid": yonghuid})
            else:
                return "参数错误"
        else:
            return "不能重复点赞"

    def set_liulanliang(self,mo_id):
        result = self.jiangong_qa_v1.find_one({"_id": ObjectId(mo_id)})
        self.jiangong_qa_v1.update({"_id": ObjectId(mo_id)}, {"$set": {"liulanliang": str(int(result['liulanliang']) + 1)}})
        return result

    def set_countqa(self,mo_id,yes,newwenti,yonghuid):
        result=self.jiangong_qa_v1.find({"_id":ObjectId(mo_id)})
        try:
            result1=self.countqa.find({"newwenti":newwenti})
            result1_list=list(result1)
            if len(result1_list)==0:
                for i in result:
                    dicts = {}
                    dicts['countqaid'] = mo_id
                    dicts['bigfenlei'] = i['bigfenlei']
                    dicts['wentifenlei'] = i['wentifenlei']
                    dicts['questions'] = i['questions']
                    dicts['asks'] = i['asks']
                    dicts['newwenti'] = newwenti
                    if yes == "1":
                        dicts['weight'] = "1"
                    else:
                        dicts['weight'] = "-1"

                    self.countqa.insert(dicts)
                    res1=self.countqa.find({"countqaid":mo_id,"newwenti":newwenti})
                    self.kongzhicishu.insert({"newwentiid":str(list(res1)[0]["_id"]),"yonghuid":yonghuid})
            else:
                res1 = self.countqa.find({"countqaid": mo_id, "newwenti": newwenti})
                caonima=str(list(res1)[0]["_id"])
                res2=self.kongzhicishu.find({"newwentiid":caonima,"yonghuid":yonghuid})
                hhh=len(list(res2))
                if hhh==0:
                    for i in result1_list:
                        if yes=="1":
                            self.countqa.update({"newwenti":newwenti}, {"$set": {"weight": str(int(i['weight'])+1)}})
                        else:
                            self.countqa.update({"newwenti":newwenti}, {"$set": {"weight": str(int(i['weight'])-1)}})
                    self.kongzhicishu.insert({"newwentiid": caonima, "yonghuid": yonghuid})
                else:
                    return "不能重复投票"
        except:
            for i in result:
                dicts={}
                dicts['countqaid']=mo_id
                dicts['bigfenlei']=i['bigfenlei']
                dicts['wentifenlei']=i['wentifenlei']
                dicts['questions']=i['questions']
                dicts['asks']=i['asks']
                dicts['newwenti']=newwenti
                if yes=="1":
                    dicts['weight']="1"
                else:
                    dicts['weight'] = "-1"
                self.countqa.insert(dicts)

    @staticmethod
    def ruku():
        # client = pymongo.MongoClient("xxxxx", xxxx)
        # jiangong_qa = client['jiangong_qa']  # 使用或者创建库
        # jiangong_qa_v1 = jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
        client = pymongo.MongoClient("xxxxx", xxxx)
        db = client.admin  # 先连接系统默认数据库admin
        db.authenticate("xxxxxx", "xxxx", mechanism='SCRAM-SHA-1')
        jiangong_qa = client['jiangong_qa']  # 使用或者创建库
        jiangong_qa_v1 = jiangong_qa['jiangong_qa_v1']  # 使用或者创建表

        excel=pandas.read_excel(r'E:\Becld_Codes\man_fool\webs_fool\django_for_qa\jiangong_qa\documents\问题库导入模版(补充相似问题) 2019-10-26.xlsx', sheet_name='在此页填写你的内容')
        for i in range(len(excel)):
            if i%4==0:
                words=str(excel.loc[i]['标准问题'])+"|"+str(excel.loc[i]['相似问题'])+"|"+str(excel.loc[i+1]['相似问题'])+"|"+str(excel.loc[i+2]['相似问题'])+"|"+str(excel.loc[i+3]['相似问题'])
                daan=str(excel.loc[i]['标准答案'])
                fenci="null"
                bigfenlei="河南继续教育"
                wentifenlei="密码登录相关"
                weight="0"
                jiangong_qa_v1.insert({'bigfenlei':bigfenlei,"wentifenlei":wentifenlei,"questions":words,'asks':daan,'fenci':fenci,'weight':weight})

    @staticmethod
    def ruku1():
        client = pymongo.MongoClient("xxxxx", xxxxx)
        jiangong_qa = client['jiangong_qa']  # 使用或者创建库
        jiangong_qa_v1 = jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
        excel = pandas.read_excel('E:\Becld_Codes\Spiders_Codes\人工智能库\jiangong_qa\documents\学达云--问题库导入模版(补充相似问题) 2019-10-26.xlsx')
        counts=0
        for i in range(len(excel)):
            counts+=1
            words=str(excel.loc[i]['标准问题'])+str(excel.loc[i]['相似问题'])
            asks=str(excel.loc[i]['标准答案'])
            fenci="null"
            jiangong_qa_v1.insert({"questions": words, 'asks': asks, 'fenci': fenci})
        print(counts)

    @staticmethod
    def ruku2():
        h=os.getcwd()+'\documents\laws'
        lists=os.listdir(h)
        for i in lists:
            words=i.replace(".pdf","")
            pprint(words)
            client = pymongo.MongoClient("xxxx", xxxxxx)
            jiangong_qa = client['jiangong_qa']  # 使用或者创建库
            jiangong_qa_v1 = jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
            fenci="null"
            jiangong_qa_v1.insert({"questions": words, 'asks': i, 'fenci': fenci})

    # 获取停用词,注意空格加进停词
    def stopwords(self):
        dirname=os.path.dirname(__file__)
        stopwords = set()
        path=os.path.join(dirname,'documents/chineseStopWords.txt').replace("\\","/")
        file = open(path, 'r', encoding='gbk')
        for line in file:
            stopwords.add(line.strip())
        file.close()
        return stopwords

    #分词去停词存储--每次从数据库取出数据，然后分词后更新fenci列
    #更新后再分词
    #建表的时候fenci列置空
    def fenci(self):
        texts = []
        for line in self.jiangong_qa_v1.find():
            words = ' '.join(jieba.cut_for_search(line['questions'])).split(' ')  # 利用jieba工具进行中文分词
            text = []
            # 过滤停用词，只保留不属于停用词的词语
            for word in words:
                if word not in self.stopwords():
                    text.append(word)
            self.jiangong_qa_v1.update({"_id": line['_id']}, {"$set": {"fenci": text}})
            texts.append(text)
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]

        if len(list(self.jiangong_qa_corpus.find())) == 0:
            self.jiangong_qa_corpus.insert({"corpus": corpus})
            pass
        else:
            self.jiangong_qa_corpus.update({"_id": [i['_id'] for i in self.jiangong_qa_corpus.find()][0]},{"$set": {"corpus": corpus}})
        sss=os.path.dirname(__file__)
        sss=os.path.join(sss,'deerwester.dict')
        dictionary.save(sss)

        # -------------------------------重新规划------------------------------ #
        # texts1 = []
        # for line in self.jiangong_qa_v1.find():
        #     questions_list=line['questions'].split("|")
        #     text1=[]
        #     for question_list in questions_list:
        #         word = ' '.join(jieba.cut_for_search(question_list)).split(' ')  # 利用jieba工具进行中文分词
        #         text1.append(word)
        #     # 过滤停用词，只保留不属于停用词的词语
        #     for hh in text1:
        #         text = []
        #         for word in hh:
        #             if word not in self.stopwords():
        #                 text.append(word)
        #         texts1.append(text)
        # dictionary1 = corpora.Dictionary(texts1)
        # corpus1 = [dictionary.doc2bow(text) for text in texts1]
        #
        # if len(list(self.duihua.find())) == 0:
        #     self.duihua.insert({"corpus": corpus1})
        # else:
        #     self.duihua.update({"_id": [i['_id'] for i in self.duihua.find()][0]},
        #                                    {"$set": {"corpus": corpus1}})
        # sss1 = os.path.dirname(__file__)
        # sss1 = os.path.join(sss1, 'deerwester1.dict')
        # dictionary1.save(sss1)


    #把需要对比的字符串，进行分词并且去停词
    def new_fenci(self,strs):
        words = ' '.join(jieba.cut_for_search(strs)).split(' ')
        new_text = []
        for word in words:
            if word not in self.stopwords():
                new_text.append(word)
        return new_text

    #创建字典赋值到self.dictionary供函数return_xiangsi使用，存储corpus到mongo数据库
    def build_dicts(self):
        texts=[]
        for i in self.jiangong_qa_v1.find():
            texts.append(i['fenci'])
        dictionary = corpora.Dictionary(texts)
        corpus=[dictionary.doc2bow(text) for text in texts]
        if len(list(self.jiangong_qa_corpus.find()))==0:
            self.jiangong_qa_corpus.insert({"corpus":corpus})
            pass
        else:
            self.jiangong_qa_corpus.update({"_id": [i['_id'] for i in self.jiangong_qa_corpus.find()][0]}, {"$set": {"corpus": corpus}})
        self.dictionary=dictionary

        # 创建字典赋值到self.dictionary供函数return_xiangsi使用，存储corpus到mongo数据库
    def build_dicts1(self,strs):
        texts = []
        for i in self.jiangong_qa_v1.find({"bigfenlei":strs}):
            texts.append(i['fenci'])
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        if len(list(self.jiangong_qa_corpus1.find())) == 0:
            self.jiangong_qa_corpus1.insert({"corpus": corpus})
        else:

            self.jiangong_qa_corpus1.update({"_id": [i['_id'] for i in self.jiangong_qa_corpus1.find()][0]},
                                           {"$set": {"corpus": corpus}})
        self.dictionary = dictionary

    def build_dicts2(self,strs):
        texts = []
        for i in self.jiangong_qa_v1.find({"bigfenlei":{"$in":[strs,'日常用语']}}):
            texts.append(i['fenci'])
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        if len(list(self.jiangong_qa_corpus1.find())) == 0:
            self.jiangong_qa_corpus1.insert({"corpus": corpus})
        else:

            self.jiangong_qa_corpus1.update({"_id": [i['_id'] for i in self.jiangong_qa_corpus1.find()][0]},
                                           {"$set": {"corpus": corpus}})
        self.dictionary = dictionary

    #返回最相似结果,返回结果是一个列表，返回最相似的三个结果，最靠前的最相似
    def return_xiangsi(self,strs):
        sss = os.path.dirname(__file__)
        sss = os.path.join(sss, 'deerwester.dict')
        dictionary = corpora.Dictionary.load(sss)

        corpus = [i['corpus'] for i in self.jiangong_qa_corpus.find()][0]

        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        index = similarities.MatrixSimilarity(corpus_tfidf)

        new_vec = dictionary.doc2bow(self.new_fenci(strs))
        new_vec_tfidf = tfidf[new_vec]

        sims = index[new_vec_tfidf]

        sims_list = sims.tolist()

        sims_dict = {}

        for i, j in enumerate(sims_list):
            sims_dict[i] = j
        list1 = sorted(sims_dict.items(), key=lambda x: x[1], reverse=True)
        print(list1)
        data = pd.DataFrame(list(self.jiangong_qa_v1.find()))
        list_result = []
        if list1[0][1] <= 0.3:
            return []
        else:
            list_result.append(data.loc[list1[0][0]])
            return list_result

        # 返回最相似结果,返回结果是一个列表，返回最相似的三个结果，最靠前的最相似
    def return_xiangsi1(self, strs,strs1):
        corpus = [i['corpus'] for i in self.jiangong_qa_corpus1.find()][0]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        index = similarities.MatrixSimilarity(corpus_tfidf)
        new_vec = self.dictionary.doc2bow(self.new_fenci(strs))
        new_vec_tfidf = tfidf[new_vec]
        sims = index[new_vec_tfidf]
        sims_list = sims.tolist()
        sims_dict = {}
        for i, j in enumerate(sims_list):
            sims_dict[i] = j
        list1 = sorted(sims_dict.items(), key=lambda x: x[1], reverse=True)
        data = pd.DataFrame(list(self.jiangong_qa_v1.find({"bigfenlei":strs1})))
        list_result = []
        if list1[0][1] == 0:
            return []
        else:
            list_result.append(data.loc[list1[0][0]])
        if list1[1][1] == 0:
            return list_result
        else:
            list_result.append(data.loc[list1[1][0]])
        if list1[2][1] == 0:
            return list_result
        else:
            list_result.append(data.loc[list1[2][0]])
        return list_result

    def return_xiangsi2(self, strs,strs1):
        corpus = [i['corpus'] for i in self.jiangong_qa_corpus1.find()][0]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        index = similarities.MatrixSimilarity(corpus_tfidf)
        new_vec = self.dictionary.doc2bow(self.new_fenci(strs))
        new_vec_tfidf = tfidf[new_vec]
        sims = index[new_vec_tfidf]
        sims_list = sims.tolist()
        sims_dict = {}
        for i, j in enumerate(sims_list):
            sims_dict[i] = j
        list1 = sorted(sims_dict.items(), key=lambda x: x[1], reverse=True)
        data = pd.DataFrame(list(self.jiangong_qa_v1.find({"bigfenlei":{"$in":[strs1,'日常用语']}})))
        list_result = []
        if list1[0][1] <= 0.3:
            return []
        else:
            list_result.append(data.loc[list1[0][0]])
            return list_result



    def get_bigfenleiall(self):
        haha=set()
        aa=self.jiangong_qa_v1.find()
        for i in aa:
            haha.add(i['bigfenlei'])
        return haha
    def get_wentifenleiall(self,strs):
        haha=set()
        aa=self.jiangong_qa_v1.find({"bigfenlei":strs})
        for i in aa:
            haha.add(i['wentifenlei'])
        return haha
    def set_tainjiaxinshuju(self,s1,s2,s3,s4):
        aa=self.jiangong_qa_v1.find({"bigfenlei":s1,"wentifenlei":s2})
        l=len(list(aa))
        if l!=0:
            import datetime
            times = datetime.datetime.now()
            strs = times.strftime('%Y-%m-%d')
            self.jiangong_qa_v1.insert({"bigfenlei":s1,"wentifenlei":s2,"questions":s3,"asks":s4,"fenci":"null","weight":"0","times":strs,"liulanliang":"0"})
            return 1
        else:
            return 0

if __name__=="__main__":
    # Jiangong_qa.ruku()
    # 测试问
    strs='你好'
    result=Jiangong_qa()#实例化对象
    # result.fenci()#更新后再分词
    result.build_dicts()#创建字典赋值到self.dictionary供函数return_xiangsi使用，存储corpus到mongo数据库
    res=result.return_xiangsi(strs)#返回相似结果
    for i,j in enumerate(res):
        print(i,"问题：\n",j[3].split("|")[0],"\n答案：\n",j[4])

