from django.shortcuts import render,HttpResponse
import json
import pymongo
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from jiangong_qa.jiangong_qa import Jiangong_qa
from rest_framework.response import Response
from bson.objectid import ObjectId
import unittest
from rest_framework.throttling import SimpleRateThrottle#节流，每天1000次，登录注册还有,局部添加
from api.mylogs import logs
import pandas
class MyThrottle(SimpleRateThrottle):
    rate = '60/m'
    scope = 'MyThrottle'
    def get_cache_key(self, request, view):
        return request.META.get('REMOTE_ADDR')


#进入问答机器人
@csrf_exempt
def qarobot(request):
    return render(request,'qarobot.html')


class Qarobots(APIView):
    throttle_classes = [MyThrottle, ]
    def post(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        qaid=request.POST.get("qaid")

        if qaid=="1001":
            dicts={}
            dicts['code']=100000
            dicts['msg']="请求成功"
            bigfenleiid=request.POST.get("bigfenlei")
            results=Jiangong_qa().get_bigfenlei1(bigfenleiid)
            bigfenlei=Jiangong_qa().get_bigfenlei2(bigfenleiid)
            lists=[]
            for i in results:
                lists.append({"wentifenlei":i['wentifenlei'],"wentifenlei_id":i['wentifenlei_id']})
            dicts['data']={"bigfenleiid":bigfenleiid,"lists":lists,"bigfenlei":bigfenlei}
            return HttpResponse(json.dumps(dicts, ensure_ascii=False))

        elif qaid=="1002":
            wenti = request.POST.get('wenti')

            dicts = {}
            if wenti == "":
                dicts["code"] = 100002
                dicts['msg'] = "没输入内容"
                dicts['data'] = ["null",]
                logs().info(wenti)
                logs().info(dicts)
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))
            else:
                result = Jiangong_qa()
                # result.build_dicts()
                res = result.return_xiangsi(wenti)
                lists = []
                if len(res) == 0:
                    dicts["code"] = 100003
                    dicts['msg'] = "抱歉，这个问题太难了，您也可以输入“转人工”咨询人工客服"
                    dicts['data'] = ["null",]
                    logs().info(wenti)
                    logs().info(dicts)
                    return HttpResponse(json.dumps(dicts, ensure_ascii=False))
                for i in res:
                    # if 'pdf' in i['asks']:
                    #     i['asks'] = "laws/" + i['asks']
                    lists.append({"mo_id":str(i["_id"]),"questions":i['questions'].split("|")[0], "asks":i['asks']})
                dicts["code"] = 100000
                dicts['msg'] = "请求成功"
                dicts['data'] = lists[0]
                logs().info(wenti)
                logs().info(dicts)
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))

        elif qaid=="10021":
            wenti = request.POST.get('wenti')
            bigfenlei=request.POST.get('bigfenlei')
            if bigfenlei=="":
                dicts = {}
                dicts["code"] = 100004
                dicts['msg'] = "没输入内容"
                dicts['data'] = ["您好！当前时间客服不在线，人工客服在线时间：工作日 8:30~18:00。", ]
                logs().info(wenti)
                logs().info(dicts)
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))
            bigfenlei = Jiangong_qa().get_bigid(bigfenlei)
            dicts = {}
            if wenti == "":
                dicts["code"] = 100002
                dicts['msg'] = "没输入内容"
                dicts['data'] = ["null",]
                logs().info(wenti)
                logs().info(dicts)
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))
            else:
                result = Jiangong_qa()
                result.build_dicts2(bigfenlei)
                res = result.return_xiangsi2(wenti,bigfenlei)
                lists = []
                if len(res) == 0:
                    dicts["code"] = 100003
                    dicts['msg'] = "抱歉，这个问题太难了，您也可以输入“转人工”咨询人工客服"
                    dicts['data'] = ["null",]
                    logs().info(wenti)
                    logs().info(dicts)
                    return HttpResponse(json.dumps(dicts, ensure_ascii=False))
                for i in res:
                    # if 'pdf' in i['asks']:
                    #     i['asks'] = "laws/" + i['asks']
                    lists.append({"mo_id":str(i["_id"]),"questions":i['questions'].split("|")[0], "asks":i['asks']})
                dicts["code"] = 100000
                dicts['msg'] = "请求成功"
                dicts['data'] = lists[0]
                logs().info(wenti)
                logs().info(dicts)
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))

        elif qaid=="1003":
            bigfenleiid=request.POST.get("bigfenlei")

            bigfenlei=Jiangong_qa().get_bigid(bigfenleiid)
            wentifenleiid=request.POST.get("wentifenlei")

            wentifenlei=Jiangong_qa().get_wentiid(wentifenleiid)
            result=Jiangong_qa().get_wentifenlei(bigfenlei,wentifenlei)

            dicts={}
            dicts['code']=100000
            dicts['msg'] = "请求成功"

            dicts['data'] = {"bigfenlei":bigfenlei,"bigfenleiid":bigfenleiid,"wentifenlei":wentifenlei,"wentifenleiid":wentifenleiid,"lists":result}

            return HttpResponse(json.dumps(dicts,ensure_ascii=False))
        elif qaid=="1004":
            # wenti=request.query_params.get('wenti')
            wenti=request.POST.get('wenti')
            bigfenlei1=request.POST.get('bigfenlei')

            bigfenlei=Jiangong_qa().get_bigid(bigfenlei1)
            dicts={}
            if wenti == "":
                dicts["code"]=100002
                dicts['msg']="没输入内容"
                dicts['data']="null"
                return HttpResponse(json.dumps(dicts, ensure_ascii=False))
            else:
                result = Jiangong_qa()
                result.build_dicts1(bigfenlei)
                res = result.return_xiangsi1(wenti,bigfenlei)
                lists = []
                if len(res) == 0:
                    dicts["code"] = 100003
                    dicts['msg'] = "抱歉，这个问题太难了，您也可以输入“转人工”咨询人工客服"
                    dicts['data'] = "null"
                    return HttpResponse(json.dumps(dicts, ensure_ascii=False))
                for i in res:
                    if 'pdf' in i['asks']:
                        i['asks'] = "laws/" + i['asks']
                    lists.append({"mo_id":str(i["_id"]),"questions":i['questions'].split("|")[0], "asks":i['asks']})
                dicts["code"] = 100000
                dicts['msg'] = "请求成功"
                dicts['data'] = {"bigfenleiid":bigfenlei1,"bigfenlei":bigfenlei,"lists":lists}
                return HttpResponse(json.dumps(dicts,ensure_ascii=False))
        elif qaid=="1005":
            mo_id=request.POST.get("mo_id")
            yes=request.POST.get("yes")
            newwenti=request.POST.get("newwenti")
            yonghuid=request.POST.get("yonghuid")
            try:
                res1 = Jiangong_qa()
                hh=res1.set_countqa(mo_id, yes, newwenti,yonghuid)
                if hh=="不能重复投票":
                    dicts = {}
                    dicts["code"] = 100002
                    dicts['msg'] = "不能重复投票"
                    dicts['data'] = "null"
                else:
                    dicts={}
                    dicts["code"] = 100000
                    dicts['msg'] = "投票成功"
                    dicts['data'] = "null"
            except:
                dicts = {}
                dicts["code"] = 111111
                dicts['msg'] = "请求参数错误"
                dicts['data'] = "null"
            return HttpResponse(json.dumps(dicts, ensure_ascii=False))
        elif qaid=="1006":
            mo_id = request.POST.get("mo_id")
            yes = request.POST.get("yes")
            yonghuid = request.POST.get("yonghuid")
            try:
                res1 = Jiangong_qa()
                hh=res1.set_countqa1(mo_id, yes,yonghuid)
                if hh=="不能重复点赞":
                    dicts = {}
                    dicts["code"] = 100002
                    dicts['msg'] = "不能重复点赞"
                    dicts['data'] = "null"
                elif hh=="参数错误":
                    dicts = {}
                    dicts["code"] = 111111
                    dicts['msg'] = "请求参数错误"
                    dicts['data'] = "null"
                else:
                    dicts = {}
                    dicts["code"] = 100000
                    dicts['msg'] = "投票成功"
                    dicts['data'] = "null"
            except Exception as e:
                print(e)
                dicts = {}
                dicts["code"] = 111111
                dicts['msg'] = "请求参数错误"
                dicts['data'] = "null"
            return HttpResponse(json.dumps(dicts, ensure_ascii=False))
        elif qaid=="1007":
            mo_id = request.POST.get("mo_id")
            try:
                res1 = Jiangong_qa()
                results=res1.set_liulanliang(mo_id)
                dicts = {}
                dicts["code"] = 100000
                dicts['msg'] = "增加浏览量"
                dicts['data'] = {"mo_id":mo_id,"bigfenlei":results["bigfenlei"],"wentifenlei":results["wentifenlei"],"questions":results["questions"].split("|")[0],'asks':results["asks"],'times':results['times'],"liulanliang":results['liulanliang']}
            except:
                dicts = {}
                dicts["code"] = 111111
                dicts['msg'] = "请求参数错误"
                dicts['data'] = "null"
            return HttpResponse(json.dumps(dicts, ensure_ascii=False))
        else:
            dicts={}
            dicts["code"] = 111111
            dicts['msg'] = "请求参数错误"
            dicts['data'] = "null"
            return HttpResponse(json.dumps(dicts, ensure_ascii=False))

def index(request):
    duixiang=Jiangong_qa()
    results=duixiang.jiangong_qa_v1.find()
    results=list(results)
    for i in results:
        i['idid']=i['_id']
    return render(request,'xtreme-html/ltr/index.html',{"results":results})

def cnmd(request,pk):
    duixiang = Jiangong_qa()
    results = duixiang.jiangong_qa_v1.delete_one({"_id":ObjectId(pk)})
    results = duixiang.jiangong_qa_v1.find()
    results = list(results)
    for i in results:
        i['idid'] = i['_id']
    return render(request,'xtreme-html/ltr/index.html',{"results":results})

def cebianlan(request):
    p1=request.POST.get("p1")
    xixi123=request.POST.get("xixi123")
    duixiang = Jiangong_qa()
    results = duixiang.jiangong_qa_v1.find_one({"_id":ObjectId(p1)})
    results=dict(results)
    results['xixi123']=xixi123
    results['_id']=str(results['_id'])
    return HttpResponse(json.dumps(results,ensure_ascii=False))

def xiugai(request):
    yijifenlei890=request.POST.get("yijifenlei890")
    yijifenlei345=request.POST.get("yijifenlei345")
    yijifenlei456=request.POST.get("yijifenlei456")
    Jiangong_qa().jiangong_qa_v1.update_one({"_id":ObjectId(yijifenlei890)},{"$set":{"questions":yijifenlei345,"asks":yijifenlei456}})
    return HttpResponse(123)

def wendaceshi(request):
    aa=Jiangong_qa().idyingshe.find()
    bb=set()
    for i in aa:
        bb.add((i['bigfenlei'],i['bigfenlei_id']))

    return render(request, 'xtreme-html/ltr/pages-profile.html',{"big":list(bb)})

def bumanyiwenti(request):
    result1=Jiangong_qa().countqa.find()
    result1 = list(result1)
    for i in result1:
        i['idid'] = i['_id']
    return render(request, 'xtreme-html/ltr/table-basic.html',{"result1":result1})
def cnmd1(request,pk):
    duixiang = Jiangong_qa()
    duixiang.countqa.delete_one({"_id":ObjectId(pk)})
    results1 = Jiangong_qa().countqa.find()
    results1 = list(results1)
    for i in results1:
        i['idid'] = i['_id']
    return render(request, 'xtreme-html/ltr/table-basic.html', {"result1": results1})

def bumanyidaan(request):
    result = Jiangong_qa().jiangong_qa_v1.find({"weight": {"$lt": "0"}}).sort("weight",pymongo.DESCENDING)
    result = list(result)
    for i in result:
        i['idid'] = i['_id']
    return render(request, 'xtreme-html/ltr/icon-material.html',{"result":result})

def cnmd2(request,pk):
    Jiangong_qa().jiangong_qa_v1.update_one({"_id":ObjectId(pk)},{"$set":{"weight":"0"}})
    result = Jiangong_qa().jiangong_qa_v1.find({"weight": {"$lt": "0"}}).sort("weight", pymongo.DESCENDING)
    result = list(result)
    for i in result:
        i['idid'] = i['_id']
    return render(request, 'xtreme-html/ltr/icon-material.html', {"result": result})
def cnmd3(request):
    file=request.FILES.get("cnm1")

    # -------
    import datetime
    times = datetime.datetime.now()
    strs = times.strftime('%Y-%m-%d')
    excel = pandas.read_excel(file)
    lll = {'bigfenlei': "河南省安管人员交流群", "wentifenlei": str(excel.loc[0]['一级分类']).strip(),
           "questions": str(excel.loc[0]['标准问题']) + "|" + str(excel.loc[0]['相似问题']) + "|" + str(excel.loc[0]['关联问题']),
           'asks': str(excel.loc[0]['标准答案']), 'fenci': "null",
           'weight': "0", 'times': strs, 'liulanliang': "0"}
    xixixi=[]
    for i in range(1, len(excel)):
        # print(excel.loc[i]['标准问题'])
        if pandas.isna(excel.loc[i]['标准问题']):
            hhh = ""
            if pandas.notna(excel.loc[i]['相似问题']):
                hhh = "|" + str(excel.loc[i]['相似问题'])
            if pandas.notna(excel.loc[i]['关联问题']):
                hhh = "|" + str(excel.loc[i]['关联问题'])
            lll['questions'] += hhh
            continue
        else:
            print(lll)
            xixixi.append(lll)
            lll = {'bigfenlei': "河南省安管人员交流群", "wentifenlei": str(excel.loc[i]['一级分类']).strip(),
                   "questions": str(excel.loc[i]['标准问题']) + "|" + str(excel.loc[i]['相似问题']) + "|" + str(
                       excel.loc[i]['关联问题']), 'asks': str(excel.loc[i]['标准答案']), 'fenci': "null",
                   'weight': "0", 'times': strs, 'liulanliang': "0"}
    print(lll)
    xixixi.append(lll)
    # -------
    mess={}
    mess['code']=100
    mess['msg']="暂不启用"
    mess['data']=xixixi

    return HttpResponse(json.dumps(mess,ensure_ascii=False))
def tianjiaxinwenti(request):
    aa=Jiangong_qa().get_bigfenleiall()
    return render(request, 'xtreme-html/ltr/starter-kit.html',{'res1':aa})

def downloads(request):
    return render(request,'download.html')
def cnmd12345(request):
    wenti=request.POST.get("cnmd12345")
    duixiang = Jiangong_qa()
    results = duixiang.jiangong_qa_v1.find({'$or':[{"questions":{"$regex":wenti}},{"asks":{"$regex":wenti}}]})
    results = list(results)
    for i in results:
        i['idid'] = i['_id']
    return render(request, 'xtreme-html/ltr/index.html', {"results": results})
def changerji(request):
    haha=request.POST.get("haha")
    aa=Jiangong_qa().get_wentifenleiall(haha)
    return HttpResponse(json.dumps(list(aa),ensure_ascii=False))
def tianjia(request):
    yijifenlei=request.POST.get("yijifenlei")
    erjifenlei=request.POST.get("erjifenlei")
    wenti=request.POST.get("wenti")
    daan=request.POST.get("daan")
    if wenti=="":
        return HttpResponse("问题不能为空")
    if daan=="":
        return HttpResponse('答案不能为空')
    ssss=Jiangong_qa().set_tainjiaxinshuju(yijifenlei,erjifenlei,wenti,daan)
    if ssss==1:

        return HttpResponse("添加成功")

    else:
        return HttpResponse("添加失败")

def xuexi(request):
    Jiangong_qa().fenci()
    return HttpResponse("学习成功！")
