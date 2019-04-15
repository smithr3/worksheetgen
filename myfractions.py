"""
About

Robert
5/04/2019
"""

from base import Question, getPretty
import random
from sympy import symbols, simplify, latex, evaluate

NAME = 'Fractions'

class AddSubFractions(Question):
	"""
	Adding and subtracting fractions and whole numbers.
		1/2 + 3/4
		3 - 5/6
	Extensions
		multiple fractions/numbers at once
		combinations of adding/subtracting
		including mixed fractions
	"""
	taskColumns = 4
	maxDifficulty = 5

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Adding with simple fractions',
			2 : 'Adding with fractions and whole numbers',
			3 : 'Subtracting with simple fractions',
			4 : 'Subtracting with fractions and whole numbers',
			5 : 'Adding/subtracting with fractions and whole numbers',
		}
		self.defaultTitle = 'Adding/Subtracting Fractions'

	def generate(self):
		a, b, c, d, e, f = symbols('a b c d e f')
		if self.difficulty == 1:
			expr = random.choice([
				a/b + c/d,
			])
			substitutions = [
				(a, random.randint(1, 7)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 7)),
				(d, random.randint(2, 7)),
			]
			for old, new in substitutions:
				with evaluate(False):
					expr = expr.replace(old, new)
			soln = simplify(expr)
			Q = getPretty(expr)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(expr))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 2:
			expr = random.choice([
				a/b + c/d,
				a/b + c,
				a + c/d,
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 7)),
			]
			for old, new in substitutions:
				with evaluate(False):
					expr = expr.replace(old, new)
			soln = simplify(expr)
			Q = getPretty(expr)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(expr))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 3:
			expr = random.choice([
				a/b - c/d,
				-a/b + c/d,
			])
			substitutions = [
				(a, random.randint(1, 7)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 7)),
				(d, random.randint(2, 7)),
			]
			for old, new in substitutions:
				with evaluate(False):
					expr = expr.replace(old, new)
			soln = simplify(expr)
			Q = getPretty(expr)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(expr))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 4:
			expr = random.choice([
				a/b - c/d,
				a/b - c,
				a - c/d,
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 7)),
			]
			for old, new in substitutions:
				with evaluate(False):
					expr = expr.replace(old, new)
			soln = simplify(expr)
			Q = getPretty(expr)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(expr))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 5:
			expr = random.choice([
				a/b + c/d,
				a/b + c,
				a + c/d,
				a/b - c/d,
				a/b - c,
				a - c/d,
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 10)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 10)),
			]
			for old, new in substitutions:
				with evaluate(False):
					expr = expr.replace(old, new)
			soln = simplify(expr)
			Q = getPretty(expr)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(expr))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA

class MultDivFractions(Question):
	"""
	Multiplying and dividing fractions and whole numbers.
		1/2 + 3/4
		3 - 5/6
	Extensions
		multiple fractions/numbers at once
		combinations of multiplying/dividing
		including mixed fractions
	"""
	taskColumns = 4
	maxDifficulty = 5

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Multiplying with simple fractions',
			2 : 'Multiplying with fractions and whole numbers',
			3 : 'Dividing with simple fractions',
			4 : 'Dividing with fractions and whole numbers',
			5 : 'Multiplying/dividing with fractions and whole numbers',
		}
		self.defaultTitle = 'Multiplying/Dividing Fractions'

	def generate(self):
		a, b, c, d, e, f = symbols('a b c d e f')
		substitutions, expr, LQ = [], None, None
		if self.difficulty == 1:
			expr, LQ = random.choice([
				(a/b * c/d, r'\frac{{{a}}}{{{b}}} \times \frac{{{c}}}{{{d}}}')
			])
			substitutions = [
				(a, random.randint(1, 7)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 7)),
				(d, random.randint(2, 7)),
			]
		elif self.difficulty == 2:
			expr, LQ = random.choice([
				(a/b * c/d, r'\frac{{{a}}}{{{b}}} \times \frac{{{c}}}{{{d}}}'),
				(a/b * c, r'\frac{{{a}}}{{{b}}} \times {c}'),
				(a * c/d, r'{a} \times \frac{{{c}}}{{{d}}}'),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 7)),
			]
		elif self.difficulty == 3:
			expr, LQ = random.choice([
				((a/b) / (c/d), r'\frac{{{a}}}{{{b}}} \div \frac{{{c}}}{{{d}}}'),
				(-(a/b) / (c/d), r'-\frac{{{a}}}{{{b}}} \div \frac{{{c}}}{{{d}}}'),
			])
			substitutions = [
				(a, random.randint(1, 7)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 7)),
				(d, random.randint(2, 7)),
			]
		elif self.difficulty == 4:
			expr, LQ = random.choice([
				((a/b) / (c/d), r'\frac{{{a}}}{{{b}}} \div \frac{{{c}}}{{{d}}}'),
				((a/b) / c, r'\frac{{{a}}}{{{b}}} \div {c}'),
				(a / (c/d), r'{a} \div \frac{{{c}}}{{{d}}}'),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 7)),
			]
		elif self.difficulty == 5:
			expr, LQ = random.choice([
				(a/b * c/d, r'\frac{{{a}}}{{{b}}} \times \frac{{{c}}}{{{d}}}'),
				(a/b * c, r'\frac{{{a}}}{{{b}}} \times {c}'),
				(a * c/d, r'{a} \times \frac{{{c}}}{{{d}}}'),
				((a/b) / (c/d), r'\frac{{{a}}}{{{b}}} \div \frac{{{c}}}{{{d}}}'),
				((a/b) / c, r'\frac{{{a}}}{{{b}}} \div {c}'),
				(a / (c/d), r'{a} \div \frac{{{c}}}{{{d}}}'),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(2, 10)),
				(c, random.randint(1, 10)),
				(d, random.randint(2, 10)),
			]
		assert len(substitutions) > 0
		for old, new in substitutions:
			with evaluate(False):
				expr = expr.replace(old, new)
		a = substitutions[0][1]
		b = substitutions[1][1]
		c = substitutions[2][1]
		d = substitutions[3][1]
		soln = simplify(expr)
		Q = getPretty(expr)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(LQ.format(a=a, b=b, c=c, d=d))
		LA = '$\displaystyle {}$'.format(latex(soln))
		return Q, A, LQ, LA

class AllFractions(Question):
	"""
	Addition, subtraction, multiplication and division of fractions.
	"""
	taskColumns = 4
	maxDifficulty = 1

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Add/sub/mult/div fractions and whole numbers'
		}
		self.defaultTitle = 'Fractions'
		self.addSubFractions = AddSubFractions(5)
		self.multDivFractions = MultDivFractions(5)

	def generate(self):
		if self.difficulty == 1:
			question = random.choice([
				self.addSubFractions,
				self.multDivFractions,
			])
			Q, A, LQ, LA = question.generate()
			return Q, A, LQ, LA