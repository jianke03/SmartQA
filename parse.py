#ecncoding=utf-8
import jieba.posseg as pseg
def doParse(question):
	sq = pseg.cut(question)
	result = []
	for w in sq:
		result.append((w.word, w.flag))
	sepaStr = ""
	for inner_item in result:
		sepaStr += (inner_item[0] + " " + str(inner_item[1]) + ", ")

	return sepaStr	