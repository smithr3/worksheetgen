"""
Command Line Text Interface functions.

Robert
21/02/2019
"""

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
		for name, obj in inspect.getmembers(algebra):
			if inspect.isclass(obj):
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
		raw = input('>')
		try:
			raw = int(raw)
			if raw in range(t['i']+1):
				answer = raw
		except ValueError:
			pass

	answer = t[answer]
	print('You chose {}.\n'.format(answer))
	return answer

def askSubTopic(t, d):
	answer = None
	while answer is None:
		print('Subtopic?')
		print(d[t]['text'])
		raw = input('>')
		try:
			raw = int(raw)
			if raw in range(d[t]['i']+1):
				answer = raw
		except ValueError:
			pass

	answer = d[t][answer]
	print('You chose {}.\n'.format(answer))
	return answer

def askNQuestions():
	answer = None
	while answer is None:
		print('Number of questions?')
		raw = input('>')
		try:
			raw = int(raw)
			if raw in range(26):
				answer = raw
		except ValueError:
			pass
	print('You chose {} questions.\n'.format(answer))
	return answer

def makeQuestion(questionClass, n, total):
	satisfied = False
	lq, la = None, None
	question = questionClass() # instantiate class, maybe make static class?
	# qFn = getFunction(topic, subtopic)
	while not satisfied:
		print('New question ({}/{}):'.format(n, total))
		q, a, lq, la = question.generate()
		print('{}\nAns: {}'.format(q, a))
		answer = input('>')
		if answer == '+':
			q.incrementDifficulty()
		elif answer == '-':
			q.decrementDifficulty()
		elif answer == '0':
			satisfied = True
		elif answer == '.':
			pass
		else:
			pass # input not recognised, ignored
	return lq, la

def askSectionName():
	answer = None
	while answer is None:
		print('Section name?')
		answer = input('>')
	print('This section will be named "{}".\n'.format(answer))
	return answer

def askFinished():
	answer = None
	while answer is None:
		print('Finished worksheet?')
		raw = input('>')
		if raw in ['y', '0']:
			answer = True
		elif raw in ['n', '.']:
			answer = False
	return answer