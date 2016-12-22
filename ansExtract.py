

QuesWordList = ["什么","第几","几","多少","谁","何时","哪里","哪个","哪","那位","属于","那个"]
badWordList = ["..","问题","答案"]
numBadList = ["年","月","日","多","个"]
placeBadList = ["中国","世界","全球","城市"]
peopleList = ["者","人","家","员","代表","男","女","名字","代表"]
placeList = ["国籍","国家","洲","洋","山","河","地区","地点","县","市","省","州","处"]
timeList = ["年","月","日","时间"]
tagList = [peopleList,placeList,timeList]

def findAskPos(wordList):
	if wordList[len(wordList)-1][0] == "是":
		return len(wordList)
	for i in range(len(wordList)):
		for j in range(len(QuesWordList)):
			if wordList[i][0].find(QuesWordList[j]) != -1:
				return i
	return len(wordList)

def getTypeStr(typeInfo):
	tag = -1
	for i in range(3):
		for j in range(len(tagList[i])):
			if typeInfo.find(tagList[i][j]) != -1:
				tag = i
				break
		if tag != -1:
			break

	typeStr = ""
	if typeInfo.find("Place") != -1:
		typeStr = "ns"
	elif typeInfo.find("Time") != -1:
		typeStr = "m"
	elif typeInfo.find("Number") != -1:
		typeStr = "m"
	elif typeInfo.find("People") != -1:
		typeStr = "nr"
	else:
		if tag == 0:
			typeStr = "nr"
		elif tag == 1:
			typeStr = "ns"
		elif tag == 2:
			typeStr = "m"
		else:
			typeStr = "null"
	return typeStr


def check(sourceList, wordList, typeStr, typeInfo):
	AskPos = findAskPos(wordList)
	retList = []
	length = len(wordList)
	
	for i in range(len(sourceList)):
		goodVal = []
		ansList = []
		#如果这个词符合词性要求，或者根本对词性无要求时为名次，则作为候选答案
		for j in range(len(sourceList[i])):
			#print sourceList[i][j][0]+"|"+sourceList[i][j][1]
			if sourceList[i][j][1].startswith(typeStr) or sourceList[i][j][1].startswith("nz") or sourceList[i][j][1].startswith("nt") or (typeStr == "null" and sourceList[i][j][1].startswith("n")):
				#在问题中出现的词不能作为候选答案
				tag = 0
				for k in range(len(badWordList)):
					if sourceList[i][j][0].find(badWordList[k]) != -1:
						tag = 1
				if typeStr == "m":
					for k in range(len(numBadList)):
						if sourceList[i][j][0].find(numBadList[k]) != -1:
							tag = 1
				if typeStr == "ns":
					for k in range(len(placeBadList)):
						if sourceList[i][j][0].find(placeBadList[k]) != -1:
							tag = 1
				for k in range(len(wordList)):
					if sourceList[i][j][0]== wordList[k][0] or wordList[k][0].find(sourceList[i][j][0]) != -1:
						tag = 1
						break
				if tag == 1:
					continue
				ansList.append([sourceList[i][j][0],j])
				goodVal.append(0)

		if len(ansList) == 0:
			continue

		#goodVal值为对于问题中词在条目中的每次出现：出现位置与目标答案的距离*问题中词与疑问词的距离的倒数的乘积
		for j in range(len(sourceList[i])):
			for k in range(length):
				if sourceList[i][j][0] == wordList[k][0]:
					if k == AskPos:	#跳过疑问词
						continue
					elif typeInfo == wordList[k][0] and AskPos != length:	#如果问题类型不是“...是？”的形式，则跳过中心词，因为很可能在文本中不出现
						continue
					else:	
						for p in range(len(goodVal)):
							if j != ansList[p][1]: 
								goodVal[p] += abs(1.0/((j-ansList[p][1])*(k-AskPos)))			
		val = 0
		pos = 0
		for j in range(len(goodVal)):
			#print ansList[j][0]+"***"+str(goodVal[j])
			if goodVal[j] > val:
				val = goodVal[j]
				pos = j

		#result.write("ANSWER IS: "+ansList[pos][0].encode('utf-8')+"\n")
		retList.append([ansList[pos][0],sourceList[i][ansList[pos][1]][1]])
	
	return retList