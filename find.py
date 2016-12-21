import csv
import re
noUsewords=['了','《','》','‘','’','“','”','，','？','。','（','）']
def refine(paras, keywords):
	line = ""
	penalty = 1
	sign = "[。，！？]"
	regions = []
	for p in paras:
		sentences = re.split(sign, p)
		if sentences[-1] == "":
			sentences = sentences[0:-1]
		penalty = 1
		line = ""
		for s in sentences:
			end = 0
			for w in keywords:
				if end == 1:
					break
				wordbag = [w]
				file = ""
				ok = 1
				try:
					file = open("./syn/"+w)
				except:
					ok = 0
				if ok == 1:
					fline = ""
					fline = file.readline()
					while fline != "":
						fline = fline.strip()
						wordbag.append(fline)
						fline = file.readline()
				for word in wordbag:	
					if s.find(word) > 0:
						penalty = 0
						line += s + "，"
						end = 1
						break
			if penalty == 0 and end == 0:
				line += s + "，"
				penalty = 1
		regions.append(line) 
	return regions
def findPara(cirticalwords):#包含关键词，最后一个词是中心词类型
	file1=open('wiki.txt','r')
	returnPara=[]
	totalScore=-1
	for line in file1:
		cirNum=len(cirticalwords)-1#关键词长度
		tempscore=0
		for i in range(cirNum):
			for word in cirticalwords[i]:	
				if line.find(word)!=-1:
					if word in cirticalwords[-1]:
						tempscore+=0.5
						break
					else:
						tempscore+=1
						break
		if tempscore>totalScore:
			returnPara=[]
			line=line.strip()
			returnPara.append(line)
			totalScore=tempscore
			continue
		if tempscore==totalScore:
			line=line.strip()
			returnPara.append(line)
	#print(str(totalScore))
	return returnPara		
def disscore(wordSyn,string):
	NumCri = len(wordSyn)-1
	firstin=-1
	lastin=-1
	matchNum=0 #匹配到关键词的数量
	for i in range(NumCri):
		matchthis=False
		thislast = -1
		for myword in wordSyn[i]:
			thisplace=string.find(myword)
			if thisplace!=-1:
				matchthis=True
				if thislast==-1:
					thislast=thisplace
				else:
					thislast = min(thislast,thisplace)
		if matchthis:
			matchNum+=1
			if lastin ==-1:
				lastin = thislast
			else:
				lastin = max(thislast,lastin)
			if firstin == -1:
				firstin = thislast
			else:
				firstin = min(firstin,thislast)	
	return 	(firstin - lastin)/matchNum		
def doFindPara(line):# line 是 一个词语的list		
	wordSyn=[]
	for word in line:
		thisLine=set()
		thisLine.add(word)
		find=False
		try:
			file2=open('syn/'+word,'r')
			find=True
		except:
			pass
		if find:
			for l in file2:
				l=l.strip()
				thisLine.add(l)
			file2.close()	
		wordSyn.append(thisLine)		
	returnPara=findPara(wordSyn)
	stringscore=dict()
	for string in returnPara:
		string=string.strip()
		score1= disscore(wordSyn,string)
		stringscore[string]=score1
	stringscorelist = sorted(stringscore.items(),key = lambda a:a[1],reverse=True)
	returnPara=[]
	for k in range(min(len(stringscorelist),10)):
		returnPara.append(stringscorelist[k][0].strip())		
	#returnParaRes=refine(returnPara,line[0:-1])
	return returnPara

