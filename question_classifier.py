import os
import jieba
import numpy as np


def get_feature_word(file_path):
	words = []
	f = open(file_path,encoding='utf-8')
	lines = f.readlines()
	for line in lines:
		words.append(line.strip())
	# print(words)
	return words



class QuestionClassifier:
	def __init__(self):
		cur_dir = os.path.split(os.path.realpath(__file__))[0] 
		# self.vocab_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'vocab.txt'
		self.author_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'author.txt'
		self.dynasty_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'dynasty.txt'
		self.poetry_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'poetry.txt'
		self.tag_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'tag.txt'
		self.other_feature_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'other.txt'

		self.stopwords_path = cur_dir + os.sep + 'poetryData'+ os.sep +  'stop_words.utf8'
		# self.word2vec_path = cur_dir + os.sep + 'poetryData'+ os.sep +  'merge_sgns_bigram_char300.txt'
		self.stopwords = [w.strip() for w in open(self.stopwords_path, 'r', encoding='utf8') if w.strip()]
		# self.tfidf_path = cur_dir + os.sep + 'model' + os.sep + 'tfidf_model.m'
		# self.nb_path = cur_dir + os.sep + 'model' + os.sep + 'intent_reg_model.m'

		self.author_path = cur_dir + os.sep + 'poetryData'+ os.sep + 'author.txt'
		# print(self.author_path)
		self.poetry_path = cur_dir + os.sep + 'poetryData'+ os.sep +  'poetry.txt'
		self.dynasty_path = cur_dir + os.sep + 'poetryData'+ os.sep +  'dynasty.txt'
		self.tag_path = cur_dir + os.sep + 'poetryData'+ os.sep +  'tag.txt'

		self.author_word = get_feature_word(self.author_path)
		# print(self.author_word)
		self.poetry_word = get_feature_word(self.poetry_path)
		self.dynasty_word = get_feature_word(self.dynasty_path)
		self.tag_word = get_feature_word(self.tag_path)
		self.all_words = list(set(self.author_word + self.poetry_word + self.dynasty_word + self.tag_word))


		self.belong_tag = ['属于什么类型', '什么类型', '类型','什么风格','风格','描写什么','描写']
		self.write_wd = ['哪些诗', '写了什么诗', '有哪些作品', '作品','有哪些诗']
		self.dynasty_wd = ['什么朝代的人','哪个朝代', '朝代']
		self.author_wd = ['作者是谁', '作者', '谁写的']
		self.content_wd = ['内容','什么内容','内容是什么','背诵']

		if not os.path.exists(self.other_feature_path):
			self.other_features()
		return


	def other_features(self):
		'''
		将有可能的问句存入txt
		由于诗的名字可能带有'·',所以将后半部分词存入，防止jieba分词时将词分割
		'''
		f = open(self.other_feature_path,'w',encoding='utf-8')
		f.write('\n'.join(list(self.belong_tag)))
		f.write('\n')
		f.write('\n'.join(list(self.write_wd)))
		f.write('\n')
		f.write('\n'.join(list(self.dynasty_wd)))
		f.write('\n')
		f.write('\n'.join(list(self.author_wd)))
		f.write('\n')
		f.write('\n'.join(list(self.content_wd)))
		f.write('\n')
		for p_w in self.poetry_word:
			if '·' in p_w:
				f.write(p_w.split('·')[1])
				f.write('\n')
		f.close()



	def extractor_question(self,question):
		result = {}
		# jieba.load_userdict(self.vocab_path)
		jieba.load_userdict(self.author_path)
		jieba.load_userdict(self.dynasty_path)
		jieba.load_userdict(self.tag_path)
		jieba.load_userdict(self.poetry_path)
		jieba.load_userdict(self.other_feature_path)

		# words = jieba.cut(question)
		words = [w.strip() for w in jieba.cut(question) if w.strip() and w.strip() not in self.stopwords]
		# print(words)
		n  = len(words)
		poetry_name = ""
		author_name = ""
		feature_word = ""
		label = ""
		intent = ""
		for i in range(n):
			if words[i] == '·':
				poetry_name = words[i-1] + '·' + words[i+1]
			elif words[i] in self.poetry_word:
				poetry_name = words[i]
			if words[i] in self.author_word:
				author_name = words[i]


			if words[i] in self.belong_tag:
				feature_word = words[i]
			if words[i] in self.write_wd:
				feature_word = words[i]
			if words[i] in self.dynasty_wd:
				feature_word = words[i]
			if words[i] in self.author_wd:
				feature_word = words[i]
			if words[i] in self.content_wd:
				feature_word = words[i]
		
		# print(poetry_name)
		# print(author_name)
		# print(feature_word)

		entity_word = ""
		if poetry_name:
			entity_word = poetry_name
			label = "Poetry"
		else:
			entity_word = author_name
			label = "Author"
		# print(entity_word)

		if author_name and feature_word in self.write_wd:
			intent = "query_poetry"	
		elif author_name and feature_word in self.dynasty_wd:
			intent = "query_dynasty"
		elif poetry_name and feature_word in self.author_wd:
			intent = "query_author"
		elif poetry_name and feature_word in self.belong_tag:
			intent = "query_tag"
		elif poetry_name and feature_word in self.content_wd:
			intent = "query_content"
		else:
			print("问题无法解析")
		# print(intent)
		result["entity"] = entity_word
		result["label"] = label
		result["intention"] = intent
		# print(result)

		return result




# if __name__ == '__main__':
# 	question = QuestionClassifier()
	# question.other_features()
	# question.extractor_question("六幺令·绿阴春尽这首诗的风格")
	# question.extractor_question("生查子·元夕这首诗的风格")
