def makeModel(signs, rel):
	reg = ""
	group = 1
	place = 1
	for s in signs:
		if s == '?':
			reg += "([a-zA-Z0-9\u4e00-\u9fa5]{0,10})"
			place = group
			group += 1
		elif s[0:2] == '\w':
			reg += "[a-zA-Z0-9\u4e00-\u9fa5]" + s[2:]
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
	return (reg, place, rel)

def findIn(words, word):
	idx = 0
	for w in words:
		if w.find(word) >= 0:
			return idx
		idx += 1
	return -1

def getModels(words, Type):
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
					if idx < len(words) - 2:
						model.append(makeModel([words[idx-2],'是','?',words[idx+1],words[idx+2]], 10))
						model.append(makeModel(['?',words[idx+1],words[idx+2],'是',words[idx-2]], 10))
						model.append(makeModel(['?',words[idx+1],words[idx+2]], 6))
						model.append(makeModel(['?'], 1))
					if idx < len(words) - 1:
						model.append(makeModel([words[idx-2],'是','?',words[idx+1]],9))
					return model
				model.append(makeModel([words[idx-2],'是','?'], 8))
				model.append(makeModel(['?','是',words[idx-2]], 8))
				#model.append(makeModel(['?'], 1))
				return model
			elif idx < len(words) - 1:
				model.append(makeModel(['?',words[idx+1]], 5))
				#model.append(makeModel(['?'], 1))
				return model
	elif Type == 'Number':
		idx = -1
		idx = findIn(words, '几')
		if idx >= 0:
			if words[idx] == '第几':
				if idx < len(words) - 1:
					model.append(makeModel(['第','?',words[idx+1]], 7))
				model.append(makeModel(['第','?'], 4))
				return model
			elif idx > 0 and words[idx-1] == '第':
				model.append(makeModel(['第','?',words[idx][1:]], 7))
				model.append(makeModel(['第','?'], 4))
				return model
			else:
				if words[idx][0] != '几':
					pass
				elif words[idx] == '几':
					if idx < len(words) - 2:
						model.append(makeModel(['?',words[idx+1],words[idx+2]], 9))
						if idx > 0:
							model.append(makeModel([words[idx-1],'?',words[idx+1], words[idx+2], 10]))
					if idx < len(words) - 1:
						model.append(makeModel(['?',words[idx+1]], 4))
						if idx > 0:
							model.append(makeModel([words[idx-1],'?',words[idx+1]], 8))
					if idx > 1:
						model.appemd(makeModel([words[idx-2],words[idx-1],'?'], 8))
					if idx > 0:
						model.append(makeModel([words[idx-1],'?']), 4)
					#model.append(makeModel(['?'], 1))
					return model
				else:
					if idx < len(words) - 1:
						model.append(makeModel(['?',words[idx][1:],words[idx+1]], 9))
					model.append(makeModel(['?',words[idx][1:]], 4))
					#model.append(makeModel(['?'], 1))
					return model
		idx = -1
		try:
			idx = words.index('多少')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				#model.append(makeModel(['?'], 1))
				if idx > 0 and words[idx-1] == '是':
					model.append(makeModel([words[idx-2],words[idx-1],'?'], 8))
					model.append(makeModel([words[idx-2],'?'], 7))
				return model
			elif idx + 1 == len(words) - 1:
				model.append(makeModel(['?',words[idx+1]], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				model.append(makeModel(['?',words[idx+1],words[idx+2]], 9))
				model.append(makeModel(['?',words[idx+1]], 4))
				#model.append(makeModel(['?'], 1))
				return model
		idx = -1
		idx = findIn(words, '多少')
		if idx >= 0:
			if words[idx][0] == '多':
				if idx + 1 < len(words):
					model.append(makeModel(['?',words[idx][2:],words[idx+1]], 9))
				model.append(makeModel(['?',words[idx][2:]], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				#model.append(makeModel(['?'], 1))
				return model
	elif Type == 'Place':
		idx = -1
		try:
			idx = words.index('位于')
		except:
			pass
		if idx >= 0:
			model.append(makeModel(['位于','?'], 4))
			model.append(makeModel(['在', '?'], 4))
			#model.append(makeModel(['?'], 1))
			return model
		idx = -1
		try:
			idx = words.index('在')
		except:
			pass
		if idx >= 0:
			model.append(makeModel(['位于','?'], 4))
			model.append(makeModel(['在', '?'], 4))
			#model.append(makeModel(['?'], 1))
			return model
		idx = -1
		try:
			idx = words.index('哪里')
		except:
			pass
		if idx >= 0:
			if idx + 1 < len(words):
				model.append(makeModel(['?',words[idx+1]], 5))
			#model.append(makeModel(['?'], 1))
			return model
	elif Type == 'Time':
		idx = -1
		try:
			idx = words.index('哪一年')
		except:
			pass
		if idx >= 0:
			model.append(makeModel([words[idx-2],words[idx-1],'?','年'], 10))
			model.append(makeModel([words[idx-1],'?','年'], 8))
			if idx < len(words) - 1:
				model.append(makeModel(['?','年',words[idx+1]], 8))
			model.append(makeModel(['?','年'], 4))
			#model.append(makeModel(['?'], 1))
			return model
	else:
		idx = -1
		try:
			idx = words.index('哪个')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				#model.append(makeModel(['?'], 1))
				return model
			elif idx == 0:
				if Type != 'NO':
					model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			elif idx < len(words) - 2:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?',words[idx+2]], 8))
				model.append(makeModel(['?',words[idx+2]], 4))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
		idx = -1
		try:
			idx = words.index('哪一')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				#model.append(makeModel(['?'], 1))
				return model
			elif idx == 0:
				if Type != 'NO':
					model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			elif idx < len(words) - 2:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?',words[idx+2]], 8))
				model.append(makeModel(['?',words[idx+2]], 4))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
		idx = -1
		try:
			idx = words.index('哪')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				#model.append(makeModel(['?'], 1))
				return model
			elif idx == 0:
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			elif idx < len(words) - 3:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?',words[idx+3]], 8))
				model.append(makeModel(['?',words[idx+3]], 4))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
		idx = -1
		try:
			idx = findIn(words, '哪')
		except:
			pass
		if idx >= 0:
			if idx == len(words) - 1:
				#model.append(makeModel(['?'], 1))
				return model
			elif idx == 0:
				if Type != 'NO':
					model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			elif idx < len(words) - 2:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?',words[idx+2]], 8))
				model.append(makeModel(['?',words[idx+2]], 4))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
			else:
				if Type != 'NO':
					model.append(makeModel([words[idx-1],'?',Type], 9))
				model.append(makeModel([words[idx-1],'?'], 4))
				model.append(makeModel(['?',Type], 4))
				#model.append(makeModel(['?'], 1))
				return model
		idx = -1
		try:
			idx = words.index('是')
		except:
			pass
		if idx >= 0 and (idx == len(words) - 1 or words[idx+1] == '什么'):
			model.append(makeModel([Type,'是','?'], 9))
			model.append(makeModel(['?','是','\w{0,15}',Type], 7))
			model.append(makeModel(['是','?'], 2))
			model.append(makeModel(['?','是'], 2))
			#model.append(makeModel(['?'], 1))
			return model
		idx = -1
		try:
			idx = findIn(words, '什么')
		except:
			pass
		if idx >= 0:
			if words[idx] == '什么':
				if idx < len(words) - 2:
					model.append(makeModel(['?',words[idx+1],words[idx+2]], 9))
					model.append(makeModel(['?',words[idx+2]], 5))
				if idx < len(words) - 1:
					model.append(makeModel(['?',words[idx+1]], 5))
				if idx > 2:
					model.append(makeModel([words[idx-2],words[idx-1],'?',Type], 10))
					model.append(makeModel([words[idx-2],'?',Type], 9))
					model.append(makeModel([words[idx-2],words[idx-1],'?'], 8))
					model.append(makeModel([words[idx-2],'?'], 4))
				if idx > 1:
					model.append(makeModel([words[idx-1],'?',Type], 9))
					model.append(makeModel([words[idx-1],'?'], 4))
				#model.append(makeModel(['?'], 1))
				return model

	model.append(makeModel([words[-1],'?'], 3))
	#model.append(makeModel(['?'], 1))
	return model
