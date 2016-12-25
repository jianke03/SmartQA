def makeModel(signs):
	reg = ""
	group = 1
	place = 1
	token = '。，：！？；,.;’ ()（）'
	for s in signs:
		if s == '?':
			reg += "([a-zA-Z0-9\u4e00-\u9fa5]{0,10})"
			place = group
			group += 1
		elif s[0:2] == '\w':
			reg += "[a-zA-Z0-9\u4e00-\u9fa5]" + s[2:]
		elif token.find(s) >= 0:
			reg += ""
		else:
			reg += "("
			file = None
			try:
				file = open("./syn/"+s)
			except:
				pass
			if file == None:
				reg += s
			else:
				reg += s
				line = file.readline()[:-1]
				while line != "":
					reg += "|" + line
					line = file.readline()[:-1]
			reg += ")"
			group += 1
	reg += ""
	return (reg, place)

def findIn(words, word):
	idx = 0
	for w in words:
		if w.find(word) >= 0:
			return idx
		idx += 1
	return -1

def isNorm(c):
	if c.find('n') >= 0 or c == 'r':
		return True
	return False

def isVerb(c):
	if c.find('v') >= 0 or c == 'p':
		return True
	return False

def isQuan(c):
	if c == 'q':
		return True
	return False

def findNorm(chara, start, d):
	if d == 0:
		ok = False
		while start < len(chara) and start >= 0:
			if isNorm(chara[start]):
				ok = True
			else:
				if ok:
					return start - 1
			start += 1
		if ok:
			return start - 1
		return len(chara)
	elif d == 1:
		while start >= 0 and start < len(chara):
			if isNorm(chara[start]):
				return start
			start -= 1
		return -1

def findVerb(chara, start, d):
	if d == 0:
		while start < len(chara) and start >= 0:
			if isVerb(chara[start]):
				return start
			start += 1
		return len(chara)
	elif d == 1:
		while start >= 0 and start < len(chara):
			if isVerb(chara[start]):
				return start
			start -= 1
		return -1

def getModels(words, chara, Type):
	#print(words,Type)
	model = []
	if Type == 'People':
		idx = -1
		try:
			idx = words.index('谁')
		except:
			pass
		if idx >= 0:
			if idx >= 1 and words[idx-1] == '是':
				if idx < len(words) - 1 and words[idx+1] == '的':
					flag1 = findNorm(chara, idx-2, 1)
					flag2 = findNorm(chara, idx+2, 0)
					if flag1 >= 0 and flag2 < len(chara):
						model.append(makeModel([words[flag1],'\w{0,5}','是','?',words[idx+1],'\w{0,5}',words[flag2]]))
						model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2],'是','\w{0,5}',words[flag1]]))
					if flag2 < len(chara):
						model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
					return model
				else:
					flag1 = findNorm(chara, idx-2, 1)
					if flag1 >= 0:
						model.append(makeModel([words[flag1],'\w{0,5}','是','?']))
						model.append(makeModel(['?','是','\w{0,5}',words[flag1]]))
					return model
			elif idx < len(words) - 1 and words[idx+1] == '的':
				flag2 = findNorm(chara, idx+2, 0)
				if flag2 < len(chara):
					model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
				return model
			elif idx < len(words) - 1 and words[idx+1] == '是':
				flag2 = findNorm(chara, idx+2, 0)
				if flag2 < len(chara):
					model.append(makeModel(['?','是','\w{0,5}',words[flag2]]))
					model.append(makeModel([words[flag2],'\w{0,2}','是','?']))
				return model
			elif idx < len(words) - 1 and isVerb(chara[idx+1]):
				flag2 = findNorm(chara, idx+2, 0)
				if flag2 < len(chara):
					model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
				else:
					model.append(makeModel(['?',words[idx+1]]))
				return model
			elif idx > 0 and isVerb(chara[idx-1]):
				flag1 = findNorm(chara, idx-2, 1)
				if flag1 >= 0:
					model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?']))
				return model
	elif Type == 'Number':
		idx = -1
		idx = findIn(words, '几')
		if idx >= 0:
			if words[idx] == '第几':
				if idx < len(words) - 1:
					model.append(makeModel(['第','?',words[idx+1]]))
				else:
					model.append(makeModel(['第','?']))
				return model
			elif idx > 0 and words[idx-1] == '第':
				if len(words[idx]) > 1:
					model.append(makeModel(['第','?',words[idx][1:]]))
				else:
					model.append(makeModel(['第','?']))
				return model
			else:
				if words[idx][0] != '几':
					pass
				elif words[idx] == '几':
					if idx < len(words) - 1 and isQuan(chara[idx+1]):
						if idx > 0 and isVerb(chara[idx-1]):
							flag2 = findNorm(chara, idx+2, 0)
							flag1 = findNorm(chara, idx-2, 1)
							if flag2 < len(words) and flag1 >= 0:
								model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?',words[idx+1],'\w{0,5}',words[flag2]]))
							if flag2 < len(words):
								model.append(makeModel([words[idx-1],'?',words[idx+1],'\w{0,5}',words[flag2]]))
								model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
							if flag1 >= 0:
								model.append(makeModel([words[flag1],'\w{0,5}','?',words[idx+1]]))
							model.append(makeModel(['?',words[idx+1]]))
							return model
						else:
							flag2 = findNorm(chara, idx+2, 0)
							if flag2 < len(words):
								model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
							model.append(makeModel(['?',words[idx+1]]))
							return model
				else:
					if idx > 0 and isVerb(chara[idx-1]):
						flag2 = findNorm(chara, idx+1, 0)
						flag1 = findNorm(chara, idx-2, 1)
						if flag2 < len(words) and flag1 >= 0:
							model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?',words[idx][1:],'\w{0,5}',words[flag2]]))
						if flag2 < len(words):
							model.append(makeModel([words[idx-1],'?',words[idx][1:],'\w{0,5}',words[flag2]]))
							model.append(makeModel(['?',words[idx][1:],'\w{0,5}',words[flag2]]))
						if flag1 >= 0:
							model.append(makeModel([words[flag1],'\w{0,5}','?',words[idx][1:]]))
						model.append(makeModel(['?',words[idx][1:]]))
						return model
					else:
						flag2 = findNorm(chara, idx+1, 0)
						if flag2 < len(words):
							model.append(makeModel(['?',words[idx][1:],'\w{0,5}',words[flag2]]))
						model.append(makeModel(['?',words[idx][1:]]))
						return model
		idx = -1
		try:
			idx = words.index('多少')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				if idx >= 1 and isVerb(chara[idx-1]):
					flag1 = findNorm(chara, idx-2, 1)
					if flag1 >= 0:
						model.append(makeModel([words[flag1],'\w{0,3}',words[idx-1],'?']))
					else:
						model.append(makeModel([words[idx-1],'?']))
					return model
			elif idx + 1 < len(words) and isQuan(chara[idx+1]):
				if idx >= 1 and isVerb(chara[idx-1]):
					flag1 = findNorm(chara, idx-2, 1)
					flag2 = findNorm(chara, idx+2, 0)
					if flag1 >= 0 and flag2 < len(words):
						model.append(makeModel([words[flag1],'\w{0,3}',words[idx-1],'?',words[idx+1],'\w{0,5}',words[flag2]]))
					if flag1 >= 0:
						model.append(makeModel([words[flag1],'\w{0,3}',words[idx-1],'?',words[idx+1]]))
					if flag2 < len(words):
						model.append(makeModel([words[idx-1],'?',words[idx+1],'\w{0,5}',words[flag2]]))
					if len(model) == 0:
						model.append(makeModel(['?',words[idx+1]]))
					return model
				else:
					flag2 = findNorm(chara, idx+2, 0)
					if flag2 < len(words):
						model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
					if len(model) == 0:
						model.append(makeModel(['?',words[idx+1]]))
					return model
			elif idx + 1 < len(words) and isNorm(chara[idx+1]):
				model.append(makeModel(['?','\w{0,5}',words[idx+1]]))
				return model
		idx = -1
		idx = findIn(words, '多少')
		if idx >= 0:
			if words[idx][0] == '多':
				flag2 = findNorm(chara, idx+1, 0)
				if flag2 < len(words):
					model.append(makeModel(['?',words[idx][2:],'\w{0,5}',words[flag2]]))
				else:
					model.append(makeModel(['?',words[idx][2:]]))
				return model
	elif Type == 'Place':
		idx = -1
		try:
			idx = words.index('位于')
		except:
			pass
		if idx >= 0:
			flag1 = findNorm(chara, idx-1, 1)
			if flag1 >= 0:
				model.append(makeModel([words[flag1],'\w{0,3}','位于','?']))
				model.append(makeModel([words[flag1],'\w{0,3}','在', '?']))
			return model
		idx = -1
		try:
			idx = words.index('在')
		except:
			pass
		if idx >= 0:
			flag1 = findNorm(chara, idx-1, 1)
			if flag1 >= 0:
				model.append(makeModel([words[flag1],'\w{0,3}','位于','?']))
				model.append(makeModel([words[flag1],'\w{0,3}','在', '?']))
			return model
		idx = -1
		try:
			idx = words.index('哪里')
		except:
			pass
		if idx >= 0:
			if idx + 1 < len(words) and isVerb(chara[idx+1]):
				flag2 = findNorm(chara, idx+2, 0)
				if flag2 < len(words):
					model.append(makeModel(['?',words[idx+1],'\w{0,5}',words[flag2]]))
				model.append(makeModel(['?',words[idx+1]]))
			return model
	elif Type == 'Time':
		idx = -1
		try:
			idx = words.index('哪一年')
		except:
			pass
		if idx >= 0:
			model.append(makeModel(['?','年']))
			return model
		idx = -1
		try:
			idx = words.index('哪年')
		except:
			pass
		if idx >= 0:
			model.append(makeModel(['?','年']))
			return model
		idx = -1
		try:
			idx = words.index('多少年')
		except:
			pass
		if idx >= 0:
			model.append(makeModel(['?','年']))
			return model
	else:
		idx = -1
		try:
			idx = words.index('哪')
		except:
			pass
		if idx >= 0:
			if idx < len(words) - 2 and isNorm(chara[idx+2]):
				if idx >= 1 and isVerb(chara[idx-1]):
					model.append(makeModel([words[idx-1],'?',words[idx+2]]))
			elif idx < len(words) - 1 and isNorm(chara[idx+1]):
				if idx >= 1 and isVerb(chara[idx-1]):
					model.append(makeModel([words[idx-1],'?',words[idx+1]]))				
				return model
			if idx >= 1 and isVerb(chara[idx-1]):
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type]))
			else:
				if Type != 'NO':
						model.append(makeModel(['?',Type]))
			return model
		idx = -1
		try:
			idx = findIn(words, '哪')
		except:
			pass
		if idx >= 0:
			if idx < len(words) - 1 and isNorm(chara[idx+1]):
				if idx >= 1 and isVerb(chara[idx-1]):
					model.append(makeModel([words[idx-1],'?',words[idx+1]]))				
				return model
			if idx >= 1 and isVerb(chara[idx-1]):
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type]))
			else:
				if Type != 'NO':
					model.append(makeModel(['?',Type]))
			return model
		idx = -1
		try:
			idx = words.index('是')
		except:
			pass
		if idx >= 0 and (idx == len(words) - 1 or words[idx+1] == '什么'):
			flag1 = findNorm(chara, idx-1, 1)
			if flag1 >= 0:
				model.append(makeModel([words[flag1],'\w{0,3}','是','?']))
				model.append(makeModel(['?','是','\w{0,8}',words[flag1]]))
			return model
		idx = -1
		try:
			idx = findIn(words, '什么')
		except:
			pass
		if idx >= 0:
			if words[idx] == '什么':
				if idx >= 1 and isVerb(chara[idx-1]):
					flag1 = findNorm(chara, idx-2, 1)
					flag2 = findNorm(chara, idx+1, 0)
					if flag1 >= 0 and flag2 < len(chara):
						model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?',words[flag2]]))
					if flag1 >= 0:
						model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?']))
					if flag2 < len(chara):
						model.append(makeModel(['?',words[flag2]]))
					return model
				else:
					verb2 = findVerb(chara, idx+1, 0)
					flag2 = findNorm(chara, idx+1, 0)
					if verb2 < len(chara) and flag2 < len(chara) and flag2 < verb2:
						model.append(makeModel(['?',words[flag2],'\w{0,3}',words[verb2]]))
					if verb2 < len(chara):
						model.append(makeModel(['?','\w{0,8}',words[verb2]]))
					if flag2 < len(chara) and flag2 - idx < 3:
						model.append(makeModel(['?',words[flag2]]))
					return model
			elif words[idx][0] == '什':
				if idx >= 1 and isVerb(chara[idx-1]):
					flag1 = findNorm(chara, idx-2, 1)
					if flag1 >= 0:
						model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?',words[idx][2:]]))
						model.append(makeModel([words[flag1],'\w{0,5}',words[idx-1],'?']))
						model.append(makeModel(['?',words[idx][2:]]))
					return model
				else:
					verb2 = findVerb(chara, idx+1, 0)
					if verb2 < len(chara):
						model.append(makeModel(['?',words[idx][2:],'\w{0,3}',words[verb2]]))
						model.append(makeModel(['?','\w{0,8}',words[verb2]]))
						model.append(makeModel(['?',words[idx][2:]]))
					return model

	return model
