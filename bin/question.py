__author__ = 'Robert'

import re
import random

def new_question(columns, heading, instructions):
	rv = question_start

	col = re.findall(r'COL', rv)
	sector = re.findall(r'HEADING', rv)
	text = re.findall(r'TEXT\d+', rv)

	for x in col:
		rv = rv.replace(x, str(columns), 1) # replace COL
	for x in sector:
		rv = rv.replace(x, str(heading), 1) # replace COL
	for x in text:
		rv = rv.replace(x, str(instructions), 1) # replace TEXT

	return rv

class Question(object):

	def __init__(self, latex):
		self.latex = latex

	# def generateQuestions(self, n):
	# 	rv = []
	# 	for _ in range(n):
	# 		rv.append(self.generateInstance())
	# 	return rv

	def generateInstance(self):
		rv = self.latex
		random_ints = re.findall(r'RAND\d+-\d+', rv) # e.g. RAND1-10

		for x in random_ints:
			param = re.findall(r'\d+', x) # get the two parameters
			gen = random.randint(int(param[0]), int(param[1])) # generate the int
			rv = rv.replace(x, str(gen), 1) # replace RAND1-10

		print 'rv', rv
		print 'self.latex', self.latex
		return rv

	# def __call__(self, *args, **kwargs):

########################################################################################################################
#      TEMPLATES
########################################################################################################################

header = \
r"""
\documentclass[fleqn]{article}
\usepackage{amsmath,amsthm,amssymb}
\usepackage{multicol}
\usepackage{enumitem}
\begin{document}
"""
footer = \
r"""
\end{document}
"""

question_start = \
r"""
\section{HEADING}
\begin{multicols}{COL}
[
TEXT1
]
\begin{enumerate}[label=(\alph*)]
"""
question_end = \
r"""
\end{enumerate}
\end{multicols}
"""

add_two_fractions = \
	r'\item $ \displaystyle \frac{RAND1-10}{RAND2-10} + \frac{RAND1-10}{RAND2-10} $'
sub_two_fractions = \
	r'\item $ \displaystyle \frac{RAND1-10}{RAND2-10} - \frac{RAND1-10}{RAND2-10} $'
mult_two_fractions = \
	r'\item $ \displaystyle \frac{RAND1-10}{RAND2-10} \times \frac{RAND1-10}{RAND2-10} $'
mult_two_fractions_brackets = \
	r'\item $ \displaystyle \frac{RAND1-10}{RAND2-10} \left( \frac{RAND1-10}{RAND2-10} \right) $'
div_two_fractions = \
	r'\item $ \displaystyle \frac{RAND1-10}{RAND2-10} \div \frac{RAND1-10}{RAND2-10} $'