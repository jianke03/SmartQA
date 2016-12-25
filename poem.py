import re

def judgePoem(question, id):
	token = '。，：！？；,.;’ '
	content = ""
	#print(question)
	if re.search(r'“.*”', question):
		content = re.search(r'“(.*)”', question).group(1)
	else:
		return "NO"

	#print(content)
	d = 0
	num = 0
	if re.search(r'下句', question):
		d = 1
		num = 1
	elif re.search(r'下.*句', question):
		d = 1
		n = re.search(r'下(.*)句', question).group(1)
		if n == '一':
			num = 1
		elif n == '二' or n == '两':
			num = 2
		elif n == '三':
			num = 3
		else:
			num = 1
	elif re.search(r'上.*句', question):
		d = 0
		n = re.search(r'上(.*)句', question).group(1)
		if n == '一':
			num = 1
		elif n == '二' or n == '两':
			num = 2
		elif n == '三':
			num = 3
		else:
			num = 1
	elif re.search(r'上句', question):
		d = 0
		num = 1
	else:
		return "NO"

	#print(question)
	wiki = open('wiki.txt')
	find = False
	ofile = ""
	try:
		ofile = open('poem/'+str(id), 'r')
		find = True
		wiki.close()
		wiki = ofile
	except:
		pass

	if not find:
		ofile = open('poem/'+str(id), 'w')
	for line in wiki:
		
		end = 0
		left = num
		last = True
		if re.search(r'“.*'+content+r'.*”', line) == None:
			continue
		idx = line.find(content)
		if idx >= 0 and d == 1:
			#print(line)
			if not find:
				ofile.write(line)
			idx += len(content)
			if line[idx] == '”' or line[idx] == '“':
				continue
			if token.find(line[idx]) < 0:
				idx -= 1
			end = idx + 1
			while end < len(line):
				if token.find(line[end]) >= 0:
					if not last:
						left -= 1
						last = True
					if left == 0:
						break
				else:
					last = False
				if line[end] == '”' or line[end] == '“':
					if left == 1:
						left -= 1
					break
				end += 1
			if left == 0:
				wiki.close()
				return line[idx+1:end]
		elif idx >= 0 and d == 0:
			#print(line)
			end = idx - 1
			last = True
			if line[end] == '”' or line[end] == '“':
				continue
			while end >= 0:
				if token.find(line[end]) >= 0:
					if not last:
						left -= 1
						last = True
					if left == 0:
						break
				else:
					last = False
				if line[end] == '”' or line[end] == '“':
					if left == 1:
						left -= 1
					break
			if left == 0:
				wiki.close()
				return line[end+1:idx-1]
	ofile.close()
	try:
		wiki.close()
	except:
		pass
	return "NO"

'''
questions = open("questions.txt")
answers = open("poem_answers_open.txt", 'w')
num = 0
for question in questions:
	print(num)
	answer = judgePoem(question, num)
	answers.write(answer+'\n')
	num += 1

questions.close()
answers.close()
'''