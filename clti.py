"""
Command Line Text Interface functions.

Robert
21/02/2019
"""

import sys
import msvcrt
import inspect
import algebra

def createTopicDict():
	"""
	Creates a dictionary to map input to topics:
		{1: 'Algebra', 2:'Fractions', 'i':2, 'text':'[1] Algebra [2] Fractions'}
	And a dictionary of topics with subtopics, arranged as so:
		{
		'Algebra' : {1: 'SimpleManipulations', 2: 'Expanding', 'i':2, 'text' : '[1] SimpleManipulations [2] Expanding'},
		'Fractions' : {1: 'Addition', 'text' : '[1] Addition'}
		}
	:return; tuple of topic and subtopic dicts
	"""
	d = {}
	t = {}
	tText = []
	j = None
	for j, topic in enumerate([algebra]):
		t[j+1] = topic.NAME
		tText.append('[{}] {}'.format(j+1, topic.NAME))
		i = 1
		text = []
		tmp = {}
		for name, obj in classesInModule(topic):
			text.append('[{}] {}'.format(i, name))
			tmp[i] = obj
			i += 1
		tmp['text'] = ' '.join(text)
		tmp['i'] = i - 1
		d[topic.NAME] = tmp
	t['text'] = ' '.join(tText)
	t['i'] = j + 1

	return t, d

def askTopic(t):
	answer = None
	while answer is None:
		print('Topic?')
		print(t['text'])
		raw = getch()
		try:
			raw = int(raw)
			if raw in range(t['i']+1):
				answer = raw
		except ValueError:
			pass

	answer = t[answer]
	# print('You chose {}.\n'.format(answer))
	return answer

def askSubTopic(t, d):
	answer = None
	while answer is None:
		print('Subtopic?')
		print(d[t]['text'])
		raw = getch()
		try:
			raw = int(raw)
			if raw in range(d[t]['i']+1):
				answer = raw
		except ValueError:
			pass

	answer = d[t][answer]
	# print('You chose {}.\n'.format(answer))
	return answer

def askNSections():
	answer = None
	while answer is None:
		print('How many sections?')
		raw = getch()
		try:
			raw = int(raw)
			if raw in range(10):
				answer = raw
		except ValueError:
			pass
	return answer

def askNQuestions(nCols):
	answer = None
	while answer is None:
		print('Number of questions? (cols is {})'.format(nCols))
		raw = getInput()
		try:
			raw = int(raw)
			if raw in range(26):
				answer = raw
		except ValueError:
			pass
	# print('You chose {} questions.\n'.format(answer))
	return answer

def makeQuestion(question, n, total, allQuestions):
	satisfied = False
	lq, la = None, None
	# question = questionClass() # instantiate class, maybe make static class?
	# qFn = getFunction(topic, subtopic)
	while not satisfied:
		print('New question ({}/{}):'.format(n, total))
		q, a, lq, la = question.generate()
		while lq in allQuestions: # prevent duplicates
			q, a, lq, la = question.generate()
		print('{}\nA:\n{}'.format(q, a))
		answer = getch()
		if answer == '+':
			question.incrementDifficulty()
			printDifficulty(question)
		elif answer == '-':
			question.decrementDifficulty()
			printDifficulty(question)
		elif answer == '0':
			satisfied = True
		elif answer == '.':
			pass
		else:
			print(q)
			print(allQuestions)
			pass # input not recognised, ignored
	return lq, la

def printDifficulty(question):
	print('({}/{}) {}'.format(
		question.difficulty,
		question.maxDifficulty,
		question.description[question.difficulty]
	))

def askSectionName(question):
	answer = None
	while answer is None:
		print('Section name?')
		print('[1] {}'.format(question.defaultTitle))
		raw = getInput()
		try:
			raw = int(raw)
			if raw == 1:
				answer = question.defaultTitle
		except ValueError:
			answer = raw
	# print('This section will be named "{}".\n'.format(answer))
	return answer

def askFinished():
	answer = None
	while answer is None:
		print('Finished worksheet?')
		raw = getch()
		if raw in ['y', '0']:
			answer = True
		elif raw in ['n', '.']:
			answer = False
	return answer

def askRule():
	answer = None
	while answer is None:
		print('Add rule and reset section counter?')
		raw = getch()
		if raw in ['y', '0']:
			answer = True
		elif raw in ['n', '.']:
			answer = False
	return answer

def askNRules():
	answer = None
	while answer is None:
		print('Add rule after every how many sections?')
		raw = getch()
		try:
			raw = int(raw)
			if raw in range(10):
				answer = raw
		except ValueError:
			pass
	return answer

def getch():
	print('>', end='')
	sys.stdout.flush()
	bytestring = msvcrt.getch()
	string = bytestring.decode('utf-8')
	print(string)
	return string

def getInput():
	return input('>')

def classesInModule(module):
	classes = inspect.getmembers(module, inspect.isclass)
	return [c for c in classes if c[1].__module__ == module.__name__]