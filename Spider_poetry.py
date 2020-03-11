import re
import requests
from lxml import etree
import os
import csv


class spider:
    def __init__(self,start_url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'  #noqa
        }
        self.base_url='http://so.gushiwen.org'

    def crawl_title(self):
        html = requests.get(start_url,headers=self.headers).content
        # print(html)
        selector = etree.HTML(html)
        poetry_link = selector.xpath("//div[@class='typecont']//@href ")
        # print(title_str)
        # title = re.findall()
        file_path = os.path.split(os.path.realpath(__file__))[
                0] + os.sep + "poetryData" + os.sep +"feng.csv"

        csvfile = open(file_path,"a+",encoding='utf-8',newline='')
        for link in poetry_link:

            url = self.base_url + link
            # print(url)
            res=requests.get(url,headers=self.headers).content
            selector = etree.HTML(res)
            title=selector.xpath("//div[@class='cont']//h1/text()")[0]
            # print(title)

            #朝代
            dynasty_str = selector.xpath("//div[@class='cont']//p[@class='source']/a/text()")
            dynasty = dynasty_str[0]
            #作者
            author = dynasty_str[1]

            # print(dynasty)
            # print(author)

            #内容
            c = selector.xpath("//div[@class='sons'][1]//div[@class='contson']")[0]
            info = c.xpath("string(.)")
            
            content = ''
            content = content.join(info)
            # print(content)

            writer = csv.writer(csvfile)
            data_row = [author,dynasty,title,content,"风"]
            writer.writerow(data_row)
        csvfile.close()



    def start(self):
        self.crawl_title()

def merge(file_path):
    with open("./poetryData/allPoetry.csv","a+",encoding='utf-8',newline='') as f:
        file = open(file_path,"r",encoding='utf-8')
        reader = csv.reader(file)
        writer = csv.writer(f)
        for item in reader:
            writer.writerow(item)



if __name__ == '__main__':
    # merge("./poetryData/feng.csv")
    '''
    以爬取“写风”的诗词为例
    '''
    start_url='http://so.gushiwen.org/gushi/feng.aspx'
    pp = spider(start_url)
    pp.start()