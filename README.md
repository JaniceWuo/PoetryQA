# PoetryQA
结合知识图谱(Knowledge Graph)做的有关诗词的问答demo

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

## 运行效果图
![]()
