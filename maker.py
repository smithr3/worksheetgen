"""
Command line interface to create a worksheet.

Robert
21/02/2019
"""

from clti import *
from latex import Worksheet

t, d = createTopicDict()
print(t)
print(d, '\n')

sheet = Worksheet()

finished = False

while not finished:

	topic = askTopic(t)
	questionClass = askSubTopic(topic, d)
	nQuestions = askNQuestions()

	# Make questions
	qs, ans = [], []
	for i in range(nQuestions):
		q, a = makeQuestion(questionClass, i+1, nQuestions)
		qs.append(q)
		ans.append(a)

	name = askSectionName()
	sheet.addSection(name, qs, ans)

	finished = askFinished()

sheet.render()
# print(sheet.latex)
sheet.write()