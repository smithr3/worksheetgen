"""
About

Robert
21/02/2019
"""

from sympy import pretty

class Question:
	"""
	Base class to be inherited for questions.
	"""

	def __init__(self, maxDifficulty):
		# todo move everything but difficulty to class variables
		self.difficulty = 1
		self.maxDifficulty = int(maxDifficulty)
		self.description = None # dict mapping difficulty to description for it
		self.defaultTitle = None # string for default section title made from this classes questions
		self.taskColumns = None # number of columns for LaTeX \task

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

	def getDescription(self):
		return self.description[self.difficulty]

class TestQuestion(Question):
	"""
	Sample question for testing and demonstration.
	"""

	def __init__(self):
		super().__init__(3)
		self.description = {
			1 : 'Description of difficulty 1',
			2 : 'Description of difficulty 2',
			3 : 'Description of difficulty 3',
		}
		self.defaultTitle = 'Test questions'
		self.taskColumns = 3

	def generate(self):
		if self.difficulty == 1:
			q = 'diff 1'
			a = 'diff 1'
			return q, a, q, a
		elif self.difficulty == 2:
			q = 'diff 2'
			a = 'diff 2'
			return q, a, q, a
		elif self.difficulty == 3:
			q = 'diff 3'
			a = 'diff 3'
			return q, a, q, a

def getPretty(expr):
	return pretty(expr, use_unicode=False)