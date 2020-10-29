
# Neo4j知识图谱表示音乐信息
建立歌曲与演唱者、作曲者、作词者的图谱


## 环境要求

需要 Neo4j 4.1.3 服务

需要 Python 3.7.2 环境

需要 neo4j-driver 4.1.1 python包

## 须知
1.启动Neo4j服务后，浏览器进入localhost：7474后台管理页面，用户名为neo4j，修改密码为neo4jjj或自行修改main.py文件参数

2.注意解析数据所在目录，默认同一目录下

3.neo4j默认最大显示节点数目300，可在设置中更改

4.为方便建立项目，json数据文件只上传1000个左右


## 运行

```shell
命令行形式启动Neo4j服务
$ neo4j console

克隆项目
$ git clone git@github.com:Pleasecallmeboss/-Neo4j-.git

运行目录下的main.py文件
$python main.py
```




## 功能特性
1. 建立数据中歌手与歌曲关系并写入
2. 建立数据中作曲家与歌曲关系并写入
3. 建立数据中作词家与歌曲关系并写入



