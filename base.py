"""
About

Robert
21/02/2019
"""

import random
from sympy import pretty

class Question:
	"""
	Base class to be inherited for questions.
	"""

	def __init__(self, defaultDifficulty, maxDifficulty):
		# todo move everything but difficulty to class variables
		self.difficulty = int(defaultDifficulty) # minimum difficulty is 1, this is the default
		self.maxDifficulty = int(maxDifficulty)
		self.description = None # dict mapping difficulty to description for it
		self.defaultTitle = None # string for default section title made from this classes questions

	def generate(self):
		raise NotImplementedError("Please implement this method.")

	def incrementDifficulty(self):
		""" Return True if incremented successfully. """
		if self.difficulty < self.maxDifficulty:
			self.difficulty += 1
			return True
		return False

	def decrementDifficulty(self):
		""" Return True if decremented successfully. """
		if self.difficulty > 1:
			self.difficulty -= 1
			return True
		return False

	def setDifficulty(self, value):
		if 0 < value <= self.maxDifficulty:
			self.difficulty = value
		else:
			raise Exception('Trying to set difficulty above max')


	def getDescription(self):
		# todo unused - either use, or make description a class attribute instead of object attribute
		return self.description[self.difficulty]

class TestQuestion(Question):
	"""
	Sample question for testing and demonstration.
	"""
	taskColumns = 4
	maxDifficulty = 3

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Description of difficulty 1',
			2 : 'Description of difficulty 2',
			3 : 'Description of difficulty 3',
		}
		self.defaultTitle = 'Test questions'

	def generate(self):
		if self.difficulty == 1:
			Q = 'Q diff 1'
			A = 'A diff 1'
			LQ = Q
			LA = A
			return Q, A, LQ, LA
		elif self.difficulty == 2:
			Q = 'Q diff 2'
			A = 'A diff 2'
			LQ = Q
			LA = A
			return Q, A, LQ, LA
		elif self.difficulty == 3:
			Q = 'Q diff 3'
			A = 'A diff 3'
			LQ = Q
			LA = A
			return Q, A, LQ, LA

def getPretty(expr):
	return pretty(expr, use_unicode=False)

def randIntExcept(low, high, forbidden=0):
	"""
	Produces a random integer within the given range, but excluding a list of values (default 0)
	"""
	if type(forbidden) is int:
		forbidden = [forbidden]
	while True:
		val = random.randint(low, high)
		if val not in forbidden:
			return val