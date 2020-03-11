from py2neo import Graph


class Answer:
	"""docstring for ClassName"""
	def __init__(self):
		super(Answer, self).__init__()
		self.graph = Graph("http://localhost:7474", username="neo4j", password="****")

	def question_parser(self, data):
		sqls = {}
		if data:
			sql = self.transfor_to_sql(data['label'],data['entity'],data['intention'])
			sqls['sql'] = sql
			sqls['intention'] = data['intention']
			sqls['entity'] = data['entity']
		return sqls




	def transfor_to_sql(self, label, entities, intent):
		sql = []
		#询问作者有哪些诗
		if intent == "query_poetry" and label == "Author":
			sql = ["MATCH (d:Author)-[r:HAS_POETRY]->(s) where d.name='{}' RETURN s.name".format(entities)]

		#询问作者的朝代
		if intent == "query_dynasty" and label == "Author":
			sql = ["MATCH (d:Author)-[r:DYNASTY_IS]->(s) where d.name='{}' RETURN s.name".format(entities)]

		#询问诗的作者
		if intent == "query_author" and label == "Poetry":
			sql = ["MATCH (s:Author)-[r:HAS_POETRY]->(d) where d.name='{}' RETURN s.name".format(entities)]

		#询问诗的类型tag
		if intent == "query_tag" and label == "Poetry":
			sql = ["MATCH (d:Poetry)-[r:TAG_IS]->(s) where d.name='{}' RETURN s.name".format(entities)]

		#询问诗的内容
		if intent == "query_content" and label == "Poetry":
			sql = ["MATCH (d:Poetry) where d.name= '{}' RETURN d.content".format(entities)]
		return sql[0]



	def answer_template(self, intent, answers,entity):
		'''
		param answers:知识图谱中查到的答案
		这里的entity还要考虑一下 是提取主体还是附属也要  例如王维的诗/作品有哪些
		'''
		final_answer = ""
		if not answers:
			return "抱歉，没有找到答案"
		if intent == "query_poetry":
			poetry_set = list(set([answer['s.name'] for answer in answers]))
			final_answer = "{}写有 {}".format(entity,poetry_set)
		if intent == "query_dynasty":
			final_answer = "{}的朝代是{}".format(entity,answers[0]['s.name'])
		if intent == "query_author":
			final_answer = "{}这首诗的作者是{}".format(entity,answers[0]['s.name'])
		if intent == "query_tag":
			final_answer = "{}这首诗主要描写{}".format(entity,answers[0]['s.name'])
		if intent == "query_content":
			final_answer = "{}这首诗的内容是：{}".format(entity,answers[0]['d.content'])
		return final_answer


	def searching(self,sqls):
		intent = sqls['intention']
		queries = sqls['sql']
		answers = self.graph.data(queries)
		# print(answers[0]['s.name'])
		# answers = self.graph.run(queries).data()
		entity = sqls['entity']
		final_answer = self.answer_template(intent, answers,entity)
		return final_answer




# if __name__ == '__main__':
# 	ans = Answer()
# 	# sql = ans.transfor_to_sql("Author","柳永","query_poetry")
# 	# ans = self.graph.data("MATCH (d:Poetry)-[r:TAG_IS]->(s) where d.name='生查子·元夕' RETURN s.name")
# 	print(ans)



