"""
About

Robert
21/02/2019
"""

class Question:
	"""
	Base class to be inherited for questions.
	"""

	def __init__(self):
		self.difficulty = 0
		self.maxDifficulty = 0

	def generate(self):
		raise NotImplementedError("Please Implement this method.")

	def incrementDifficulty(self):
		""" Return True if incremented successfully. """
		if self.difficulty < self.maxDifficulty:
			self.difficulty += 1
			return True
		return False

	def decrementDifficulty(self):
		""" Return True if decremented successfully. """
		if self.difficulty > 0:
			self.difficulty -= 1
			return True
		return False

class TestQuestion(Question):

	def __init__(self):
		super().__init__()

	def generate(self):
		if self.difficulty == 0:
			return 'question', 'answer'