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