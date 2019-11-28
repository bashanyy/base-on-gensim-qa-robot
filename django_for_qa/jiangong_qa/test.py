import pymongo,pandas
client = pymongo.MongoClient("xxxx", xxxx)
db = client.admin  # 先连接系统默认数据库admin
db.authenticate("admin", "123456", mechanism='SCRAM-SHA-1')
jiangong_qa = client['jiangong_qa']  # 使用或者创建库
jiangong_qa_v1 =jiangong_qa['jiangong_qa_v1']  # 使用或者创建表
excel = pandas.read_excel(r'E:\Becld_Codes\man_fool\webs_fool\django_for_qa\jiangong_qa\newshuju\活动群.xlsx',sheet_name="Sheet2")
count=0
for i in excel.values:
    result=jiangong_qa_v1.find({"wentifenlei":i[2]})
    count+=len(list(result))
    # jiangong_qa_v1.update_many({"wentifenlei":i[4]},{"$set": {"wentifenlei":i[2].strip()}})
print(count)
