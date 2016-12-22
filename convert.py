

def solve( recordStr ):
	unsolvedList = recordStr.split(", ")

	wordList = []
	for i in range(len(unsolvedList)):
		splitList = list(unsolvedList[i].rpartition(" "))
		if len(splitList[0]) == 0 or splitList[0].isspace() == True:
			continue
		tmpList = [splitList[0],splitList[2]]
		wordList.append(tmpList)

	return wordList

def getKeyWords( wordList ):
	typeList = ["n","eng","t","o","i","l","j"]
	keyList = []
	for i in range(len(wordList)):
		for j in range(len(typeList)):
			if wordList[i][1].startswith(typeList[j]): 
				keyList.append(wordList[i][0])
	return keyList

def relateVal(source, keyList):
	val = 1
	for i in range(len(keyList)):
		if source.find(keyList[i]) == -1:
			val = 0
			break
	return val
