from find import doFindPara
from parse import doParse
from model import getModels
from choose import doChoose
from extract import *
from similarity import *
from closeAnsFind import ansFind
from poem import judgePoem
BETA = [0.5,0.2,0.17,0.13]
GAMA = 0.2
DELTA = 0.2
ALFA = 1.6
obj = WordSimilarity()
glossaryfile = './hownet/glossary.dat'
sememefile = './hownet/WHOLE.DAT'
obj.init(sememefile,glossaryfile)


file1 = open('question.txt','r')
file2 = open('result.txt','a')
file4 = open('result_2.txt','a')

index =0
for l in file1:
	index+=1
	if(index <= 10 and index>=1):
		l=l.strip()
		poemresult = judgePoem(l,index)
		if poemresult =="NO":	
			parse_str = doParse(l)
			words,quality = parseResult(parse_str)
			Type,critical = doExtract(words,quality)
			if len(critical)==0:
				finalanswer="NO ANSWER"
				print(index,'\t',finalanswer)
				file2.write(str(index)+'\t'+finalanswer+'\n')
				file4.write(str(index)+'\t'+finalanswer+'\n')
			else:
				critical.append(Type)
				find =False
				returnParas=[]
				try:
					file3 = open('searchResult/'+str(index),'r')
					find=True
					for resultline in file3:
						resultline = resultline.strip()
						returnParas.append(resultline)
					file3.close()
					#print('do not need to search')
				except:
					pass
				if not find:
					returnParas = doFindPara(critical)
					file3 = open('searchResult/'+str(index),'w')
					for resultline in returnParas:
						file3.write(resultline+'\n')
					file3.close()
					#print('create a search file')				
				reglist = getModels(words,Type)
				finalanswer_1 = doChoose(reglist,returnParas,Type,critical,obj)
				finalanswer_2 = ansFind(returnParas, Type, parse_str)
				print(index,'\t',finalanswer_1)
				print(index,'\t',finalanswer_2)
				file2.write(str(index)+'\t'+finalanswer_1+'\n')
				file4.write(str(index)+'\t'+finalanswer_2+'\n')
		else:
			print(index,'\t',poemresult)
			file2.write(str(index)+'\t'+poemresult+'\n')
			file4.write(str(index)+'\t'+poemresult+'\n')	
file1.close()	
file2.close()
file4.close()

