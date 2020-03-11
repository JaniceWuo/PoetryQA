from answer_question import Answer
from question_classifier import QuestionClassifier


class QA:
	def __init__(self):
		self.extractor = QuestionClassifier()
		self.searcher = Answer()

	def answer(self,input_ques):
		all_query = self.extractor.extractor_question(input_ques)
		if not all_query:
			print("sorry")
		sqls = self.searcher.question_parser(all_query)
		final_answer = self.searcher.searching(sqls)
		return final_answer



if __name__ == '__main__':
	handler = QA()
	while True:
		question = input("请输入问题：")
		answer = handler.answer(question)
		print(answer)
		print("-"*10)
