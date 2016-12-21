#encoding=utf-8
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.request import urlopen

def get_hypernym(keyword):
	taglist = []
	metadata = ""
	firstpara = ""
	url = "http://baike.baidu.com/item/" + (urlencode({"":keyword})[1:])
	try:
		htmlpage = urlopen(url)
	except:
		return (taglist, metadata, firstpara)
	bsObj = BeautifulSoup(htmlpage, "html.parser")

	try:
		tagtemp = bsObj.findAll("span", {'class':'taglist'})
		for item in tagtemp:
			taglist.append(item.get_text().strip())
	except:
		pass

	try:
		metadata += bsObj.find("meta", {'name':'description'})['content'].strip()
	except:
		pass

	try:
		firstpara += bsObj.find("div", {'class':'lemma-summary'}).find("div", {'class':'para'}).get_text().strip()
	except:
		pass

	return (taglist, metadata, firstpara)
