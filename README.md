# PoetryQA
结合知识图谱(Knowledge Graph)做的有关诗词的问答demo 数据库用的neo4j   
文件夹poetyData下已存储按描写内容爬取的诗词

## 环境依赖
1.python3    
2.neo4j==3.5.5    
3.lxml(若不需要自行爬取诗词可省略)    
4.jieba    
5.py2neo

## 项目运行
1.首先运行neo4j：neo4j.bat console    
2.将build_kg.py中第10行的neo4j密码修改为`自己的`，然后python build_kg.py    
3.观察database中是否成功导入节点及关系：浏览器打开 http://localhost:7474/    
4.修改answer_question.py中第8行的neo4j密码，然后python main.py    
5.`[optional]`自行爬取诗词，代码见[Spider_poetry.py](https://github.com/JaniceWuo/PoetryQA/blob/master/Spider_poetry.py)，详细介绍见[【爬虫练手小demo】爬取古诗词](https://blog.csdn.net/qq_25590283/article/details/104632222)

## 运行效果图
![](https://github.com/JaniceWuo/PoetryQA/blob/master/img/1.JPG)    

## 诗词知识图谱
<img width="350" height="350" src="https://github.com/JaniceWuo/PoetryQA/blob/master/img/kg_dynasty.JPG">
![](https://github.com/JaniceWuo/PoetryQA/blob/master/img/kg_dynasty.JPG)
![](https://github.com/JaniceWuo/PoetryQA/blob/master/img/kg_tag.JPG)
![](https://github.com/JaniceWuo/PoetryQA/blob/master/img/kg_poetry.JPG)

## 详细介绍
1.此项目是本人学习知识图谱问答过程中做的小demo，顺便练习一下爬虫    
2.目前已有功能有：查询某一作者有哪些作品/诗；查询某一首诗的内容/描写什么（描写山、雨、爱情等等)    
                查询作者的朝代；查询诗的作者    
3.项目不足：问句的特征提取采取的是模板匹配式的，所以当用户改变另一种说法问时，可能答不上来。    
           目前回答完全是套用的模板。所以当数据集更大时，应该用seq2seq去训练数据以丰富答案。   
           可以考虑更加细致化的划分古诗词，例如按七言律诗、五言绝句等。 

## 学习资料补充
[neo4j windows下安装](https://www.cnblogs.com/ljhdo/archive/2017/05/19/5521577.html)    
[创建、查询neo4j节点](https://www.cnblogs.com/ljhdo/p/5516793.html)    
[Python爬虫利器三之Xpath语法与lxml库的用法](https://cuiqingcai.com/2621.html)
