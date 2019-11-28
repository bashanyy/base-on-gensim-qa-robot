声明：里面的ip和端口要设置好。
查看已经开放的端口
firewall-cmd --list-ports
开启端口
firewall-cmd --zone=public --add-port=6379/tcp --permanent
重启防火墙
firewall-cmd --reload
把mongo数据库的数据配置好之后，就可以按照设置的问答语料库回答问题了。
1.接口说明
url	/api/v1/qa/
请求方式	POST
2.请求说明（请求值全部为string类型，返回json）
参数名称	必须	值	描述	其他参数	是否必须	值	返回
qaid	是	1001	获取每个省的问题分类	Bigfenlei	是	例：100001002017、
100001002018	
qaid	是	1002	聊天框答题	wenti	是	例：你是谁？	
							
							
qaid		10021		wenti			
				bigfenlei			
qaid	是	1003	点击详细分类进入第二页	bigfenlei	是	例：100001002018	
				wentifenlei	是	例：100003	
qaid	是	1004	通过搜索框，返回三条以内问题和答案，最靠前的相似度最高	wenti	是	例：建筑施工企业安管人员配置的最低数量是多少？	
				bigfenlei	是	例：100001002018	
qaid	是	1005	聊天答案是否满意。请求无返回，主要是后台做统计。	mo_id	是	5dcd290082b3e08882d4d8fe
（参数是qaid=1002的时候，返回的"data": ["5dcd290082b3e08882d4d8fe", "你是谁？?", "我是机器人！"]）	
				yes	是	1的时候，表示回答有效，2的时候表示机器人回答无效	
				newwenti	是	例：你好啊，你是谁？
（此处问题是对话中上面用户问的问题，直接传过来就行）	
				yonghuid	是	控制评价次数	
qaid		1006	点赞那里	mo_id		5dcd1c5822d90bfc35f9206d	
				yes		1表示点赞，2表示反对	
				yonghuid	是	控制点赞次数	
							
qaid		1007		mo_id		5dcd1c5822d90bfc35f9206d	
							





服务器配置：

1.安装mongo数据库
下载：
cd  /usr/local/mongodb
把下载好的文件放到这个目录
tar -zxvf mongodb-linux-x86_64-4.0.0.tgz


（1）配置环境变量
vim /etc/profile
加入：
MONGODB_HOME=/usr/local/mongodb/mongodb-linux-x86_64-4.0.0
PATH=$PATH:$MONGODB_HOME/bin

（2）创建数据库目录以及日志目录
mkdir -p /usr/local/mongodb/data
mkdir -p /usr/local/mongodb/logs

（3）创建配置文件
vim /usr/local/mongodb/mongo.conf

加入：
dbpath=/usr/local/mongodb/data
logpath=/usr/local/mongodb/logs/mongo.log #事先创建该文件
logappend=true
journal=true
quiet=true
port=27017
fork=true #后台运行
bind_ip=0.0.0.0 #允许任何IP进行连接
auth = true
（4）启动服务
cd /usr/local/mongodb/mongodb-linux-x86_64-4.0.0
#使用配置文件启动服务
/usr/local/mongodb/mongodb-linux-x86_64-4.0.0/bin/mongod -f /usr/local/mongodb/mongo.conf --auth

（5）进入shell
cd  /usr/local/mongodb/mongodb-linux-x86_64-4.0.0/bin
./mongo --host 127.0.0.1:8102

(6)配置密码
use admin
db.createUser({ user: "xxxx", pwd: "xxxx", roles: [{ role: "userAdminAnyDatabase", db: "admin" }] })
db.auth("xxxxx", "xxxx") 如果返回1，则表示成功。
db.grantRolesToUser( "xxxxx" , [ { role: "root", db: "xxxxx" } ])
重启服务
ps -aux |grep mongo找到mongo的pid
Kill pid
/usr/local/mongodb/mongodb-linux-x86_64-4.0.0/bin/mongod -f /usr/local/mongodb/mongo.conf --auth


(7)安装py3.5
yum install git -y
yum -y install gcc make patch gdbm-devel openssl-devel sqlite-devel readline-devel Zlib-devel bzip2-devel
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
cd ~
vi .bash_profile
添加下面代码：
export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
输入命令 pyenv 不报错说明正确安装pyenv，如果报错，换个shell一下试试

安装python
(1)	cd /root/.pyenv
(2)	mkdir cache
把下载的安装包放到这个文件夹，可以用传输工具
cd /root/.pyenv/versions/
pyenv install 3.5.3 -v
pyenv global 3.5.3 
输入python 然后看到版本3.5.3即可
(7)安装python库
pip install boto==2.49.0
pip install boto3==1.10.14
pip install botocore==1.13.14
pip install certifi==2019.9.11
pip install chardet==3.0.4
pip install Django==1.11.3
pip install djangorestframework==3.10.3
pip install docutils==0.15.2
pip install gensim==3.8.1
pip install idna==2.8
pip install isodate==0.6.0
pip install jieba==0.39
pip install jmespath==0.9.4
pip install mysqlclient==1.4.4
pip install numpy==1.17.3
pip install pandas==0.25.3
pip install pymongo==3.9.0
pip install pyparsing==2.4.4
pip install python-dateutil==2.8.0
pip install pytz==2019.3
pip install rdflib==4.2.2
pip install REfO==0.13
pip install requests==2.22.0
pip install s3transfer==0.2.1
pip install scipy==1.3.1
pip install six==1.13.0
pip install smart-open==1.9.0
pip install SPARQLWrapper==1.8.4
pip install urllib3==1.25.6
pip install xlrd==1.2.0

(8)进入到项目目录
先把项目放到服务器，然后进入项目根目录，执行下列命令，关闭shell即可。
数据库我会重新初始化，项目参数需要配置

(9)安装uwsgi
pip install uwsgi
cd ~
Vim qa.ini

添加：
[uwsgi]
http = 0.0.0.0:xxxx  
chmod-socket = 666  
chdir           =  /root/django_for_qa
wsgi-file = /root/django_for_qa/django_for_qa/wsgi.py
module          = django_for_qa.wsgi:application
master          = true
buffer-size=65536
proccess=4
threads = 2

vhost = true
static-map = /static=/root/django_for_qa/static
vacuum          = true

启动uWSGI服务器:
nohup uwsgi --ini qa.ini &



