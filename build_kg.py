from py2neo import Graph, Node, Relationship
import re
import os
import csv

class  poetryGraph(object):
	"""docstring for  poetryGraph"""
	def __init__(self):
		super( poetryGraph, self).__init__()
		self.graph = Graph("http://localhost:7474", username="neo4j", password="*****")

	def read_csv(self):
		file_name = os.path.split(os.path.realpath(__file__))[0] \
		+ os.sep + "poetryData" + os.sep +"allPoetry.csv"
		csvFile = open(file_name, "r",encoding='utf-8')
		reader = csv.reader(csvFile)

		author_to_dynasty = []  #作者与朝代的关系

		author_to_title = []  #作者和题目的关系
		poetry_to_tag = []  #诗和标签的关系
		poetry_to_content = []

		poetry_info = []  #诗的info
		author_info = []
		dynasty_info = []
		tag_info = []
		name_info = []
		content_info = []


		for item in reader:
			poetry_dict = {}

			poetry_dict["name"] = item[2]
			poetry_dict["content"] = item[3]
			poetry_dict["tag"] = item[4]

			tag_info.append(item[4])
			dynasty_info.append(item[1])
			author_info.append(item[0])
			name_info.append(item[2])
			content_info.append(item[3])


			author_to_dynasty.append([item[0],item[1]])
			author_to_title.append([item[0],item[2]])
			poetry_to_tag.append([item[2],item[4]])
			poetry_to_content.append([item[2],item[3]])



			poetry_info.append(poetry_dict)
		return set(author_info),set(dynasty_info),set(tag_info),set(name_info),set(content_info),\
		       author_to_dynasty,author_to_title,poetry_to_tag,poetry_to_content,poetry_info
		# print(author_to_title)
			# print(item[3])

		csvFile.close()

	def create_node(self,label,nodes):
		for node_name in nodes:
			node = Node(label,name = node_name)
			self.graph.create(node)
		return

	def create_poetry_node(self,poetry_info):
		count = 0
		for poetry_dict in poetry_info:
			node = Node("Poetry",name = poetry_dict["name"],
				        content = poetry_dict["content"],tag = poetry_dict["tag"])
			count+=1
			self.graph.create(node)
		# print(count)
		return

	def create_graphNode(self):
		author,dynasty,tag,name,content,rel_a_d,rel_a_t,rel_p_t,rel_p_c,rel_info = self.read_csv()
		self.create_poetry_node(rel_info)
		self.create_node("Author",author)
		self.create_node("Dynasty",dynasty)
		self.create_node("Tag",tag)


	def create_relationship(self,start_node, end_node, edges,rel_type, rel_name):
		set_edges = []
		for edge in edges:
			set_edges.append('###'.join(edge))

		for edge in set(set_edges):
			edge = edge.split('###')
			p = edge[0]
			q = edge[1]
			query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
				start_node, end_node, p, q, rel_type, rel_name)
			try:
				self.graph.run(query)
			except Exception as e:
				print(e)
		return

	def create_graphRels(self):
		author,dynasty,tag,name,content,rel_a_d,rel_a_t,rel_p_t,rel_p_c,rel_info = self.read_csv()
		self.create_relationship("Author","Dynasty",rel_a_d,"DYNASTY_IS","所属朝代")
		self.create_relationship("Poetry","Tag",rel_p_t,"TAG_IS","诗的标签")
		self.create_relationship("Author","Poetry",rel_a_t,"HAS_POETRY","写了诗")



	def export_data(self):
		author,dynasty,tag,name,content,rel_a_d,rel_a_t,rel_p_t,rel_p_c,rel_info = self.read_csv()
		file_author = open("poetryData/author.txt",'w+',encoding='utf-8')
		file_poetry = open("poetryData/poetry.txt",'w+',encoding='utf-8')
		file_dynasty = open("poetryData/dynasty.txt",'w+',encoding='utf-8')
		file_tag = open("poetryData/tag.txt",'w+',encoding='utf-8')

		file_author.write('\n'.join(list(author)))
		file_poetry.write('\n'.join(list(name)))
		file_dynasty.write('\n'.join(list(dynasty)))
		file_tag.write('\n'.join(list(tag)))

		file_author.close()
		file_poetry.close()
		file_tag.close()
		file_dynasty.close()

		return



if __name__ == '__main__':
	poetry = poetryGraph()
	poetry.create_graphNode()
	poetry.create_graphRels()
	# poetry.export_data()
