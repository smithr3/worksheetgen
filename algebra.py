"""
About

Robert
21/02/2019
"""

from base import Question, getPretty
import random
from sympy import Eq, symbols, solve, latex

NAME = 'Algebra'

class SimpleManipulations(Question):
	"""
	Practice for recognising manipulations.
		x + 2		ans: - 2
		3x - 1		ans: +1, div 3
	Possible extensions:
		sqrt(x)		ans: square
		1/x			ans: reciprocal or times by x
		ln(x)		ans: e^(ln(x))
		sin(x)		ans: arcsin
	"""
	taskColumns = 5

	def __init__(self):
		super().__init__(2)
		self.description = {
			1 : 'One manipulation',
			2 : 'Two manipulations'
		}
		self.defaultTitle = 'Recognising manipulations'

	def generate(self):
		if self.difficulty == 1:
			k = random.randint(2, 9)
			q, a, lq, la = random.choice([
				( 'x + {}'.format(k), '-{}'.format(k), None, None ),
				( 'x - {}'.format(k), '+{}'.format(k), None, None ),
				( '{}x'.format(k), r'\div {}'.format(k), None, None ),
				(
					'x/{}'.format(k), 'x {}'.format(k),
					r'$\displaystyle \frac{{x}}{{{}}}$'.format(k), r'$\times {}$'.format(k)
				),
			])
			if lq is None:
				lq = '${}$'.format(q)
			if la is None:
				la = '${}$'.format(a)
			return q, a, lq, la

		elif self.difficulty == 2:
			k = random.randint(2, 9)
			j = random.randint(2, 9)
			q, a, lq, la = random.choice([
				( '{}x + {}'.format(k, j), r'-{}, \ \div {}'.format(j, k), None, None ),
				( '{}x - {}'.format(k, j), r'+{}, \ \div {}'.format(j, k), None, None ),
				(
					'x/{} + {}'.format(k, j), r'-{}, \ \times {}'.format(j, k),
					r'$\displaystyle \frac{{x}}{{{}}} + {}$'.format(k, j), None
				),
				(
					'x/{} - {}'.format(k, j), r'+{}, \ \times {}'.format(j, k),
					r'$\displaystyle \frac{{x}}{{{}}} - {}$'.format(k, j), None
				),
			])
			if lq is None:
				lq = '${}$'.format(q)
			if la is None:
				la = '${}$'.format(a)
			return q, a, lq, la

class SolvingLinear(Question):
	"""
	Solving linear equations, such as:
		x + 4 = 8
		2x + 1 = 3
		4/x - 4 = 1    -> this is not linear x^-1, where to put / how to describe?
		2x - 1 + 3x = 0
		-5x - 5 = 3x + 2
	Possible extensions:
		x + k = 4
		ax + 3k = 8
	"""
	taskColumns = 4

	def __init__(self):
		super().__init__(2)
		self.description = {
			1 : 'One manipulation',
			2 : 'Two manipulations',
			# 3 : 'Requiring collection (one side)',
			# 4 : 'Requiring collection (both sides)'
		}
		self.defaultTitle = 'Solving'

	def generate(self):
		x = symbols('x')
		a, b, c, d, e, f = symbols('a b c d e f')
		if self.difficulty == 1:
			eqn = random.choice([
				Eq(x + a, b),
				Eq(x - a, b),
				Eq(a*x, b),
				Eq(x/a, b),
			])
			eqn = eqn.subs([
				(a, random.randint(2, 10)),
				(b, random.randint(0, 10)),
			])
			soln = Eq(x, solve(eqn, x)[0])
			Q = getPretty(eqn)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(eqn))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 2:
			eqn = random.choice([
				Eq(a*x + b, c),
				Eq(a*x - b, c),
				Eq(x/a + b, c),
				Eq(x/a - b, c),
			])
			# todo flip sides of equations
			eqn = eqn.subs([
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(0, 10)),
			])
			soln = Eq(x, solve(eqn, x)[0])
			Q = getPretty(eqn)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(eqn))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
