"""
About

Robert
21/02/2019
"""

from base import Question, getPretty, randIntExcept
import random
from sympy import Eq, symbols, solve, latex, evaluate

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
	maxDifficulty = 2

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
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
	maxDifficulty = 4

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'One manipulation',
			2 : 'Two manipulations',
			3 : 'Requiring collection once',
			4 : 'Requiring collection twice'
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
			# todo flip sides of equations randomly
			eqn = eqn.subs([
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(0, 10)),
			])
			# todo my own function that uses try/except to find no solutions
			soln = Eq(x, solve(eqn, x)[0])
			# todo Q, A = getPretty(eqn, soln)
			# todo LQ, LA = getLatex(eqn, soln)
			Q = getPretty(eqn)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(eqn))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 3:
			eqn = random.choice([
				Eq(a*x + b + c*x, d),
				Eq(a*x + b, d + c*x),
			])
			# todo random negative numbers without including 0
			substitutions = [
				(a, randIntExcept(-10, 10)),
				(b, randIntExcept(-10, 10)),
				(c, randIntExcept(-10, 10)),
				(d, randIntExcept(-10, 10)),
			]
			for old, new in substitutions:
				with evaluate(False):
					eqn = eqn.replace(old, new)
			try:
				soln = Eq(x, solve(eqn, x)[0])
			except IndexError:
				# no solution - lines are parallel
				soln = 'No solution'
			Q = getPretty(eqn)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(eqn))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA
		elif self.difficulty == 4:
			eqn = random.choice([
				Eq(a*x + b + c*x, d + e*x),
			])
			# todo random negative numbers without including 0
			substitutions = [
				(a, randIntExcept(-10, 10)),
				(b, randIntExcept(-10, 10)),
				(c, randIntExcept(-10, 10)),
				(d, randIntExcept(-10, 10)),
				(e, randIntExcept(-10, 10)),
			]
			for old, new in substitutions:
				with evaluate(False):
					eqn = eqn.replace(old, new)
			try:
				soln = Eq(x, solve(eqn, x)[0])
			except IndexError:
				# no solution - lines are parallel
				soln = 'No solution'
			Q = getPretty(eqn)
			A = getPretty(soln)
			LQ = '$\displaystyle {}$'.format(latex(eqn))
			LA = '$\displaystyle {}$'.format(latex(soln))
			return Q, A, LQ, LA

class SolvingAlgebraicFractions(Question):
	"""
	Solving with fractions:
		(x + 3) / 2 = 1
		(4 - x) / 4 = x
		(2x + 1) / x = 3
	Possible extensions:
		(x + 3) / 2 = (2x - 1) / 3
		(x + 3) / 2 = (2x - 1) / 3x
	"""
	# todo improve display of fractions, keeps simplifying when I don't want it to - may need to explicity define latex
	taskColumns = 4
	maxDifficulty = 3

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'One x',
			2 : 'x on RHS',
			3 : 'x in numerator and denominator',
		}
		self.defaultTitle = 'Solving with Fractions'

	def generate(self):
		x = symbols('x')
		a, b, c, d, e, f = symbols('a b c d e f')
		substitutions, eqn, LQ = [], None, None
		if self.difficulty == 1:
			eqn, LQ = random.choice([
				(Eq((a*x + b)/c, d), r'\frac{{ {a}x+{b} }}{{ {c} }} = {d}'),
				(Eq((a*x - b)/c, d), r'\frac{{ {a}x-{b} }}{{ {c} }} = {d}'),
				(Eq((a*x + b)/-c, d), r'\frac{{ {a}x+{b} }}{{ -{c} }} = {d}'),
			])
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(2, 10)),
				(d, random.randint(2, 5)),
			]
		elif self.difficulty == 2:
			eqn, LQ = random.choice([
				(Eq((a*x + b)/c, x), r'\frac{{ {a}x+{b} }}{{ {c} }} = x'),
				(Eq((a*x - b)/c, d*x), r'\frac{{ {a}x-{b} }}{{ {c} }} = {d}x'),
				(Eq((a*x + b)/-c, d*x), r'\frac{{ {a}x+{b} }}{{ -{c} }} = {d}x'),
				(Eq((b - a*x)/c, d*x), r'\frac{{ {b}-{a}x }}{{ {c} }} = {d}x'),
			])
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(2, 10)),
				(d, random.randint(2, 5)),
			]
		elif self.difficulty == 3:
			eqn, LQ = random.choice([
				(Eq((a*x + b)/(c*x), d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = {d}'),
				(Eq((a*x + b)/(c*x), -d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = -{d}'),
				(Eq((b - a*x)/(c*x), d), r'\frac{{ {b}-{a}x }}{{ {c}x }} = {d}'),
				(Eq((a*x + b)/(-c*x), -d), r'\frac{{ {a}x+{b} }}{{ -{c}x }} = -{d}'),
			])
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(2, 10)),
				(d, random.randint(2, 5)),
			]
		for old, new in substitutions:
			with evaluate(False):
				eqn = eqn.replace(old, new)
		try:
			soln = Eq(x, solve(eqn, x)[0])
		except IndexError:
			# no solution
			soln = 'No solution'
		a = substitutions[0][1]
		b = substitutions[1][1]
		c = substitutions[2][1]
		d = substitutions[3][1]
		Q = getPretty(eqn)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(LQ.format(a=a, b=b, c=c, d=d))
		LA = '$\displaystyle {}$'.format(latex(soln))
		return Q, A, LQ, LA

class SolvingNullFactor(Question):
	"""
	Solving with null factor law:
		x(x+1) = 0
		(x + 1)(x - 3) = 0
		(2x - 1)(3x + 3) = 0
	Possible extensions:
		(x + 3)(y - 2)(z - 1) = 0
		expand, then factorise again
		(x + 1)(x - 3) + 2 = 0
		(x + 1)(x - 3) = 4x
		constants
		2(x+1)(3x-3)
	"""
	taskColumns = 4
	maxDifficulty = 3

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'One x=0',
			2 : 'Two linear (x+a)',
			3 : 'Two linear (ax+b)',
		}
		self.defaultTitle = 'Solving using Null Factor Law'

	def generate(self):
		x = symbols('x')
		a, b, c, d, e, f = symbols('a b c d e f')
		substitutions, eqn, LQ = [], None, None
		if self.difficulty == 1:
			eqn, LQ = random.choice([
				(Eq(x*(x+a), 0), r'x(x+{a}) = 0'),
				(Eq(x*(x-a), 0), r'x(x-{a}) = 0'),
				(Eq(a*x*(x+b), 0), r'{a}x(x+{b}) = 0'),
				(Eq(a*x*(x-b), 0), r'{a}x(x-{b}) = 0'),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(1, 10)),
				(d, random.randint(1, 10)),
			]
		elif self.difficulty == 2:
			eqn, LQ = random.choice([
				(Eq((x+a)*(x+b), 0), r'(x+{a})(x+{b}) = 0'),
				(Eq((x+a)*(x-b), 0), random.choice([r'(x+{a})(x-{b}) = 0', r'(x-{b})(x+{a}) = 0'])),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(1, 10)),
				(d, random.randint(1, 10)),
			]
		elif self.difficulty == 3:
			eqn, LQ = random.choice([
				(Eq((a*x+b)*(x+b), 0), random.choice([r'({a}x+{b})(x+{b}) = 0', r'(x+{b})({a}x+{b}) = 0'])),
				(Eq((a*x-b)*(x-b), 0), random.choice([r'({a}x-{b})(x-{b}) = 0', r'(x-{b})({a}x-{b}) = 0'])),
				(Eq((a*x+b)*(c*x-d), 0), random.choice([r'({a}x+{b})({c}x-{d}) = 0', r'({c}x-{d})({a}x+{b}) = 0'])),
			])
			substitutions = [
				(a, random.randint(1, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(1, 10)),
				(d, random.randint(1, 10)),
			]
		for old, new in substitutions:
			with evaluate(False):
				eqn = eqn.replace(old, new)
		try:
			soln = solve(eqn, x)[0], solve(eqn, x)[1]
		except IndexError:
			# no solution
			soln = 'No solution'
		a = substitutions[0][1]
		b = substitutions[1][1]
		c = substitutions[2][1]
		d = substitutions[3][1]
		Q = getPretty(eqn)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(LQ.format(a=a, b=b, c=c, d=d))
		LA = '$\displaystyle x={}, \ {}$'.format(soln[0], soln[1])
		return Q, A, LQ, LA