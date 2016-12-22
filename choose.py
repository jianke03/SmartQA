from scrap_baike import get_hypernym
import jieba.posseg as pseg
import re
from collections import defaultdict
import csv
BETA = [0.5,0.2,0.17,0.13]
GAMA = 0.2
DELTA = 0.2
ALFA = 1.6
def extractUpper(word):
	tags,meta,first = get_hypernym(word)
	tagset = set(tags)
	meta = meta.strip().split('。')[0]
	sq = pseg.cut(meta)
	thisword="NO"
	for i in sq:
		if (i.flag)[0]=='n':
			thisword = i.word
	if thisword!="NO":
		tagset.add(thisword)
	secondword = "NO"		
	first = first.strip().split('。')[0]
	sq = pseg.cut(first)
	for i in sq:
		if (i.flag)[0]=='n':
			secondword= i.word
	if 	secondword != "NO":
		tagset.add(secondword)
	file1 = open('upperWord/'+word,'w')
	writer1 = csv.writer(file1)
	for tag in tagset:
		writer1.writerow([tag])
	file1.close()	
	return tagset		
def relate(word,Type,obj):
	find = False
	tags = set()
	try:
		file2=open('upperWord/'+word,'r')
		find=True
	except:
		pass
	if find:
		for l in file2:
			l=l.strip()
			tags.add(l)
		file2.close()
	else:
		tags = extractUpper(word)
	score = -2
	#print(tags,'     ',word)
	for tag in tags:
		tempscore = obj.calc(Type, tag, BETA, GAMA, DELTA, ALFA)
		score = max(score , tempscore)
	#print(word,'  ',Type,'  ',score)
	if score > 0:
		if score> 0.5:
			return 0.5
		if score>0.25:
			return 0.25
		if score >0.125:
			return 0.125		
		return score	
	return 0			
def caldisweight(critical,Para,word):
	iniloc = Para.find(word)
	totaldis = 0
	if iniloc==-1:
		print('flase!')
	matchNum = 0
	for criword in critical:
		tempindex = Para.find(criword)
		if tempindex!=-1:
			totaldis+=abs(tempindex-iniloc)
			matchNum+=1
	score = matchNum/totaldis
	return 	score




def doChoose(regList,paras,Type,critical,obj):
	wordlist = set()
	wordreliable = defaultdict(float)
	wordParaweight = defaultdict(float)
	wordDisweight = defaultdict(float)
	paraweight=0
	for para in paras:
		paraweight+=1
		for regpart in regList:
			result = re.search(regpart[0],para)
			if result == None:
				continue
			thispart = result.group(regpart[1])
			sq = pseg.cut(thispart)
			index = 0
			for i in sq:
				index+=1  # 
			tempindex = 0	
			needqua = 'n'	
			if Type=="Time" or Type=="Number":
				needqua = 'm'
			else:
				needqua = 'n'
			sq = pseg.cut(thispart)		
			for i in sq:
				weight = min(tempindex+1,index-tempindex)
				tempindex+=1
				if (i.flag)[0]==needqua:
					wordlist.add(i.word)
					# weight decided by the index in the matched part
					tempRel = regpart[2]/float(weight)
					thisweight = int(paraweight/5)+1
					#print(i.word,'this weight :',thisweight)
					tempPar = 1/thisweight
					tempDis = caldisweight(critical,para,i.word)
					if tempRel+tempDis+tempPar > (wordreliable[i.word]
						+wordParaweight[i.word]+wordDisweight[i.word]):
						wordreliable[i.word] = tempRel
						# weight decided by the para the word in 
						wordParaweight[i.word] = tempPar
						# weight decided by the distance to cri
						wordDisweight[i.word] = tempDis
	wordscore = dict()
	for i in wordlist:
		wordscore[i]=wordreliable[i]+wordParaweight[i]+wordDisweight[i]	
		#print(i,wordreliable[i],wordParaweight[i],wordDisweight[i])				
	sortedlist = sorted(wordscore.items(),key=lambda i:i[1],reverse=True)
	#print(sortedlist)
	if len(sortedlist) == 0:
		return "NO ANSWER"
	if Type=="Time" or Type=="Number":
		return sortedlist[0]
	if Type=="People":
		Type="人"
	if Type=="Place":
		Type="地点"
	maxword="asaa"
	first = True
	topscore = 0			
	for i in range(min(len(sortedlist),3)):
		if first:
			topscore = sortedlist[i][1]+ relate(sortedlist[i][0],Type,obj)
			maxword = sortedlist[i][0]
			first = False
		else:
			tempscore = relate(sortedlist[i][0],Type,obj)
			if sortedlist[i][1]+tempscore > topscore:
				topscore = sortedlist[i][1]+tempscore
				maxword = sortedlist[i][0]	
	return maxword						
		

		
	
