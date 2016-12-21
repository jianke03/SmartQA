from find import doFindPara
from parse import doParse
from model import getModels
from choose import doChoose
from extract import *
from similarity import *
BETA = [0.5,0.2,0.17,0.13]
GAMA = 0.2
DELTA = 0.2
ALFA = 1.6
obj = WordSimilarity()
glossaryfile = './hownet/glossary.dat'
sememefile = './hownet/WHOLE.DAT'
obj.init(sememefile,glossaryfile)


file1 = open('question.txt','r')
index =0
for l in file1:
	index+=1
	if(index==2):
		l=l.strip()
		parse_str = doParse(l)
		words,quality = parseResult(parse_str)
		Type,critical = doExtract(words,quality)
		critical.append(Type)
		returnParas = doFindPara(critical)
		print(returnParas)
		reglist = getModels(words,Type)
		print(reglist)
		#finalanswer = 
		doChoose(reglist,returnParas,Type,critical,obj)
		#print(finalanswer)	
		break
file1.close()	

