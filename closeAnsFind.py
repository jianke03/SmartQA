# coding=utf-8

import convert
import ansExtract
import ansDecide
import codecs
import jieba
import jieba.posseg as pseg

def ansFind(wikiList, typeInfo, Ques,obj):
	wordList = convert.solve(Ques)
	keyList =  convert.getKeyWords(wordList)
	for j in range(len(wordList)):
		if j >= len(wordList):
			break
		if wordList[j][1].startswith("u") or wordList[j][1].startswith("x") or wordList[j][1].startswith("p"):
			del wordList[j]
			j = j-1
	
	sourceList = []
	for i in range(len(wikiList)):
		words = pseg.cut(wikiList[i])
		relevantList = []
		for w in words:
			wordsGroup = [w.word,w.flag]
			relevantList.append(wordsGroup)
		sourceList.append(relevantList)

	typeStr = ansExtract.getTypeStr(typeInfo)
	ansList = ansExtract.check(sourceList, wordList, typeStr, typeInfo,obj)
	return ansDecide.chooseAns(ansList, typeStr,typeInfo,obj)
