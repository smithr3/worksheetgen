"""
Creates questions of every type.

Robert
15/04/2019
"""

from clti import *
from latex import Worksheet

t, d = createTopicDict()

sheet = Worksheet('all')

for topic_idx in t.keys():
	if type(topic_idx) is int:
		topic = t[topic_idx] # topic module NAME
	else:
		continue

	for sub_idx in d[topic].keys():
		if type(sub_idx) is int:
			questionClass = d[topic][sub_idx]
		else:
			continue

		print(topic, questionClass)
		question = questionClass()

		# for each difficulty, create a section with one row of questions of that difficulty
		for difficulty in range(question.maxDifficulty):
			qs = []
			ans = []
			difficulty += 1
			question.difficulty = difficulty
			# create a row of questions
			for i in range(question.taskColumns):
				q, a, lq, la = question.generate()
				qs.append(lq)
				ans.append(la)
			name = '{}: {} ({}/{})'.format(topic, question.description[difficulty], difficulty, question.maxDifficulty)
			sheet.addSection(name, qs, ans, questionClass.taskColumns, False)

sheet.render()
sheet.write()