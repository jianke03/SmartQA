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
file2 = open('result.txt','a')

index =0
for l in file1:
	index+=1
	if(2001=<index<=4000):
		l=l.strip()
		parse_str = doParse(l)
		words,quality = parseResult(parse_str)
		Type,critical = doExtract(words,quality)
		if len(critical==0):
			finalanswer="NO ANSWER"
			print(index,'\t',finalanswer)
			file2.write(str(index)+'\t'+finalanswer+'\n')
		else:
			critical.append(Type)
			returnParas = doFindPara(critical)
			reglist = getModels(words,Type)
			finalanswer = doChoose(reglist,returnParas,Type,critical,obj)
			print(index,'\t',finalanswer)
			file2.write(str(index)+'\t'+finalanswer+'\n')
		continue	
file1.close()	

