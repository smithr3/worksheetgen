"""
Command line interface to create a worksheet.

Robert
21/02/2019
"""

# https://github.com/thearn/examgen/blob/master/examgen/worksheet.py
# https://au.ixl.com/math/year-9
# https://www.ipracticemath.com/math-practice/algebra

# https://github.com/peterbrittain/asciimatics
# http://urwid.org/
# https://github.com/kennethreitz/clint

# https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df
# https://opensource.com/article/17/5/4-practical-python-libraries

# most promising
# https://github.com/CITGuru/PyInquirer
# https://github.com/prompt-toolkit/python-prompt-toolkit
# emulators? https://cmder.net/
# emulators? https://conemu.github.io/

from clti import *
from latex import Worksheet
import math

t, d = createTopicDict()

finished = False

sheet = Worksheet(askFName())
useDefaultNames = askUseDefaultNames()

nSections = askNSections()
nQPerSection = askNQuestionTypes()
nTotalQuestions = nQPerSection*nSections

# todo if list of answers is < 10, use getch() for fast single char response

# todo option to not use question titles

if nSections > 1:
	print('\nCreating presets for the sections in a question block.')
	sectPresets = {}
	for i in range(nQPerSection):
		print('\nSection {} of {}'.format(i+1, nQPerSection))
		topic = askTopic(t)
		questionClass = askSubTopic(topic, d)
		# print(questionClass, type(questionClass), questionClass.__dict__)
		startingDifficulty = askDifficulty(questionClass()) # todo I don't like instantiating the class just to get at the descriptions
		nQuestions = askNQuestions(questionClass.taskColumns)
		sectPresets[i] = {
			'topic' : topic,
			'questionClass' : questionClass,
			'nQuestions' : nQuestions,
			'startingDifficulty' : startingDifficulty,
		}
	print('\nFinished presets. Generating sections now.')
	# print('len(sectPresets)', len(sectPresets))

for i in range(nTotalQuestions):

	print('\nSection {} of {}'.format(
		math.floor(i/nQPerSection)+1,
		nSections
	))

	if nSections > 1:
		idx = i % nQPerSection
		# print(i, nSecPerRules, idx)
		topic = sectPresets[idx]['topic']
		questionClass = sectPresets[idx]['questionClass']
		nQuestions = sectPresets[idx]['nQuestions']
		startingDifficulty = sectPresets[idx]['startingDifficulty']
	else:
		idx = i
		topic = askTopic(t)
		questionClass = askSubTopic(topic, d)
		nQuestions = askNQuestions(questionClass.taskColumns)
		startingDifficulty = askDifficulty(questionClass()) # todo I don't like instantiating the class just to get at the descriptions

	# Make questionnQPerSections
	qs, ans = [], []
	question = questionClass(startingDifficulty)
	for j in range(nQuestions):
		q, a = makeQuestion(question, j+1, nQuestions, qs)
		qs.append(q)
		ans.append(a)
	# todo enable changing questionClass() mid questions, would require taking min of cols
	# use: mixing solvingLinear with solvingQuadratic
	# alternative: another class - questionGroup, sets random difficulty for each new question
	# 	and picks randomly from available question classes
	#   think I prefer this method, allows more presets and ease of use

	addRule = False
	# if starting new section and not first section
	if idx == 0 and i != 0:
		addRule = True

	if useDefaultNames:
		name = question.defaultTitle
	else:
		name = askSectionName(question)
	sheet.addSection(name, qs, ans, questionClass.taskColumns, addRule)

sheet.render()
sheet.write()