
from choose import relate
BETA = [0.5,0.2,0.17,0.13]
GAMA = 0.2
DELTA = 0.2
ALFA = 1.6
def chooseAns(ansList, typeStr,typeInfo,obj):
	ansDict = {}
	for i in range(len(ansList)):
		#if typeStr != "null":
		#	if ansList[i][1].startswith(typeStr) and ansList[i][1].startswith("nz") and ansList[i][1].startswith("nt"):
		#		continue
		if ansList[i][0] not in ansDict:#ansDict.has_key(ansList[i][0]) == False:
			ansDict[ansList[i][0]] = 1
		else:
			ansDict[ansList[i][0]] = ansDict[ansList[i][0]] + 1

	cntpos = -1
	lenpos = -1
	length = -1
	cnt = 1
	keyList = list(ansDict.keys())
	mx=0
	for i in keyList:
		tempscore = relate(i,typeInfo,obj)
		mx =max(mx,tempscore)
	limit = 0
	if mx>=0.5:
		limit = 0.5
	elif mx>=0.25:
		limit = 0.25			

	for i in range(len(keyList)):
		if relate(keyList[i],typeInfo,obj)<limit:
			continue
		if ansDict[keyList[i]] > cnt:
			cntpos = i
			cnt = ansDict[keyList[i]]
		if len(keyList[i]) > length:
			lenpos = i
			length = len(keyList[i])
	if cnt > 1:
		#result.write("\n**FINAL ANSWER IS: "+keyList[cntpos].encode('utf-8')+"\n")
		return keyList[cntpos]
	elif length > 0:
		#result.write("\n**FINAL ANSWER IS: "+keyList[lenpos].encode('utf-8')+"\n")
		return keyList[lenpos]
	else:
		return "null"