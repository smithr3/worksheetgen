"""
About

Robert
21/02/2019
"""

import base

NAME = 'Algebra'

class SimpleManipulations(base.Question):

	def __init__(self):
		super().__init__()

	def generate(self):
		if self.difficulty == 0:
			k = 3
			lq = '$ x + {}$'.format(k)
			la = '$-{}$'.format(k)
			q = 'x + {}'.format(k)
			a = '-{}'.format(k)
			return q, a, lq, la
