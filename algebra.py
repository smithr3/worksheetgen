"""
About

Robert
21/02/2019
"""

from base import Question, getPretty, randIntExcept
import random
from sympy import Eq, symbols, solve, latex, evaluate, expand, simplify

NAME = 'Algebra'

def algebraicFraction(x, a, b, c):
	# x symbol, a/b/c int
	return random.choice([
		(x/a, r'\frac{{ x }}{{ {a} }}'.format(a=a, b=b, c=c)),
		((a*x + b)/c, r'\frac{{ {a}x+{b} }}{{ {c} }}'.format(a=a, b=b, c=c)),
		((a*x - b)/c, r'\frac{{ {a}x-{b} }}{{ {c} }}'.format(a=a, b=b, c=c)),
		((b - a*x)/c, r'\frac{{ {b}-{a}x }}{{ {c} }}'.format(a=a, b=b, c=c)),
	])

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
	taskColumns = 3
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

# class SolvingAlgebraicFractions(Question):
# 	"""
# 	Solving with fractions:
# 		(x + 3) / 2 = 1
# 		(4 - x) / 4 = x
# 		(2x + 1) / x = 3
# 	Possible extensions:
# 		(x + 3) / 2 = (2x - 1) / 3
# 		(x + 3) / 2 = (2x - 1) / 3x
# 	"""
# 	taskColumns = 4
# 	maxDifficulty = 3
#
# 	def __init__(self, defaultDifficulty=1):
# 		super().__init__(defaultDifficulty, self.maxDifficulty)
# 		self.description = {
# 			1 : 'One x',
# 			2 : 'x on RHS',
# 			3 : 'x in numerator and denominator',
# 		}
# 		self.defaultTitle = 'Solving with Fractions'
#
# 	def generate(self):
# 		x = symbols('x')
# 		a, b, c, d, e, f = symbols('a b c d e f')
# 		substitutions, eqn, LQ = [], None, None
# 		if self.difficulty == 1:
# 			eqn, LQ = random.choice([
# 				(Eq((a*x + b)/c, d), r'\frac{{ {a}x+{b} }}{{ {c} }} = {d}'),
# 				(Eq((a*x - b)/c, d), r'\frac{{ {a}x-{b} }}{{ {c} }} = {d}'),
# 				(Eq((a*x + b)/-c, d), r'\frac{{ {a}x+{b} }}{{ -{c} }} = {d}'),
# 			])
# 			substitutions = [
# 				(a, random.randint(2, 10)),
# 				(b, random.randint(1, 10)),
# 				(c, random.randint(2, 10)),
# 				(d, random.randint(2, 5)),
# 			]
# 		elif self.difficulty == 2:
# 			eqn, LQ = random.choice([
# 				(Eq((a*x + b)/c, x), r'\frac{{ {a}x+{b} }}{{ {c} }} = x'),
# 				(Eq((a*x - b)/c, d*x), r'\frac{{ {a}x-{b} }}{{ {c} }} = {d}x'),
# 				(Eq((a*x + b)/-c, d*x), r'\frac{{ {a}x+{b} }}{{ -{c} }} = {d}x'),
# 				(Eq((b - a*x)/c, d*x), r'\frac{{ {b}-{a}x }}{{ {c} }} = {d}x'),
# 			])
# 			substitutions = [
# 				(a, random.randint(2, 10)),
# 				(b, random.randint(1, 10)),
# 				(c, random.randint(2, 10)),
# 				(d, random.randint(2, 5)),
# 			]
# 		elif self.difficulty == 3:
# 			eqn, LQ = random.choice([
# 				(Eq((a*x + b)/(c*x), d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = {d}'),
# 				(Eq((a*x + b)/(c*x), -d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = -{d}'),
# 				(Eq((b - a*x)/(c*x), d), r'\frac{{ {b}-{a}x }}{{ {c}x }} = {d}'),
# 				(Eq((a*x + b)/(-c*x), -d), r'\frac{{ {a}x+{b} }}{{ -{c}x }} = -{d}'),
# 			])
# 			substitutions = [
# 				(a, random.randint(2, 10)),
# 				(b, random.randint(1, 10)),
# 				(c, random.randint(2, 10)),
# 				(d, random.randint(2, 5)),
# 			]
# 		for old, new in substitutions:
# 			with evaluate(False):
# 				eqn = eqn.replace(old, new)
# 		try:
# 			soln = Eq(x, solve(eqn, x)[0])
# 		except IndexError:
# 			# no solution
# 			soln = 'No solution'
# 		a = substitutions[0][1]
# 		b = substitutions[1][1]
# 		c = substitutions[2][1]
# 		d = substitutions[3][1]
# 		Q = getPretty(eqn)
# 		A = getPretty(soln)
# 		LQ = '$\displaystyle {}$'.format(LQ.format(a=a, b=b, c=c, d=d))
# 		LA = '$\displaystyle {}$'.format(latex(soln))
# 		return Q, A, LQ, LA

class SolvingAlgebraicFractions(Question):
	"""
	Solve linear equations constructed from algebraic fractions, defined as
		AF = (a*x + b)/c
	Eg:
		AF = a
		AF = ax
		AF = AF
		AF +- AF = a
		AF +- AF = AF
		don't */ because then non linear terms may be introduced
	"""
	taskColumns = 3
	maxDifficulty = 3

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'One algebraic fraction',
			2 : 'Two algebraic fractions',
			3 : 'Three algebraic fractions',
		}
		self.defaultTitle = 'Solving with Algebraic Fractions'

	def generate(self):
		LQ, eqn = None, None
		x = symbols('x')
		a, b, c, d, e, f = symbols('a b c d e f')
		# generate algebraic fractions and their latex representation
		AF1, AFL1 = algebraicFraction(x, randIntExcept(2, 5), randIntExcept(2, 5),  randIntExcept(2, 5))
		AF2, AFL2 = algebraicFraction(x, randIntExcept(2, 5), randIntExcept(2, 5),  randIntExcept(2, 5))
		AF3, AFL3 = algebraicFraction(x, randIntExcept(2, 5), randIntExcept(2, 5),  randIntExcept(2, 5))
		if self.difficulty == 1:
			a = randIntExcept(2, 10)
			b = randIntExcept(2, 10)
			c = randIntExcept(-7, 7)
			d = randIntExcept(-7, 7)
			eqn, LQ = random.choice([
				(Eq(AF1, a), '{} = {}'.format(AFL1, a)),
				(Eq(AF1, a*x), '{} = {}x'.format(AFL1, a)),
				(Eq((a*x + b)/(c*x), d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = {d}'.format(a=a, b=b, c=c, d=d)),
			])
		elif self.difficulty == 2:
			# I want a 0 to appear more often than 1/20 times, i.e. 30% instead of 5%
			if random.random() < 0.7:
				a = randIntExcept(-10, 10)
			else:
				a = 0
			eqn, LQ = random.choice([
				(Eq(AF1, AF2), '{} = {}'.format(AFL1, AFL2)),
				(Eq(AF1 + AF2, a), '{} + {} = {}'.format(AFL1, AFL2, a)),
				(Eq(AF1 - AF2, a), '{} - {} = {}'.format(AFL1, AFL2, a)),
				# (Eq(AF1 * AF2, a), '{} \times {} = {}'.format(AFL1, AFL2, a)),
				# (Eq(AF1 / AF2, a), '{} \div {} = {}'.format(AFL1, AFL2, a)),
			])
		elif self.difficulty == 3:
			eqn, LQ = random.choice([
				(Eq(AF1 + AF2, AF3), '{} + {} = {}'.format(AFL1, AFL2, AFL3)),
				(Eq(AF1 - AF2, AF3), '{} + {} = {}'.format(AFL1, AFL2, AFL3)),
			])
		try:
			soln = Eq(x, solve(eqn, x)[0])
		except IndexError:
			# no solution
			soln = 'No solution'
		Q = getPretty(eqn)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(LQ)
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
		methods level
		(x+1)(cos x)
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
				(a, random.randint(2, 10)),
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
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(2, 10)),
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

class AllSolving(Question):
	"""
	All solving for x questions, sorted into linear (one solution) and quadratic (2 solutions) difficulty buckets.
	"""
	taskColumns = 3
	maxDifficulty = 3

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Linear - max one algebraic fraction',
			2 : 'Quadratic - two solutions',
			3 : 'Linear - hard algebraic fraction questions',
		}
		self.defaultTitle = 'Solving'
		self.solvingLinear = SolvingLinear()
		self.solvingAlgebraicFractions = SolvingAlgebraicFractions()
		self.solvingNullFactor = SolvingNullFactor()

	def generate(self):
		if self.difficulty == 1:
			question, difficulty = random.choice([
				(self.solvingLinear, random.randint(1, self.solvingLinear.maxDifficulty)),
				(self.solvingAlgebraicFractions, 1),
			])
			question.difficulty = difficulty
			Q, A, LQ, LA = question.generate()
			return Q, A, LQ, LA
		elif self.difficulty == 2:
			question, difficulty = random.choice([
				(self.solvingNullFactor, random.randint(1,self.solvingNullFactor.maxDifficulty)),
			])
			question.difficulty = difficulty
			Q, A, LQ, LA = question.generate()
			return Q, A, LQ, LA
		elif self.difficulty == 3:
			question, difficulty = random.choice([
				(self.solvingLinear, random.randint(1, self.solvingLinear.maxDifficulty)),
				(self.solvingAlgebraicFractions, random.randint(1, self.solvingLinear.maxDifficulty)),
			])
			question.difficulty = difficulty
			Q, A, LQ, LA = question.generate()
			return Q, A, LQ, LA

class Expand(Question):
	"""
	Expand the given expression.
	-5(2x + y)
	-2x(-5y + x)
	(3x + 1)(3y + 1)
	"""
	taskColumns = 3
	maxDifficulty = 2

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : '1 by 2-3 terms',
			2 : '2 by 2-3 terms',
			# 3 : '2 by 2 by 2 terms',
		}
		self.defaultTitle = 'Expand'

	def generate(self):
		x, y, z = symbols('x y z')
		a, b, c, d, e, f = symbols('a b c d e f')
		substitutions, eqn, LQ = [], None, None
		if self.difficulty == 1:
			eqn, LQ = random.choice([
				(a*(b*x+c), r'{a}({b}x+{c})'),
				(d + a*(b*x-c), r'{d}+{a}({b}x-{c})'),
				(-a*(b*x+c*y), r'-{a}({b}x-{c})'),
				(d-a*(-b*x+c*y), r'{d}-{a}({b}x-{c})'),
				(a*x*(b*y+c*z), r'{a}x({b}y+{c}z)'),
			])
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(2, 10)),
				(d, random.randint(1, 7)),
				(e, random.randint(2, 10)),
			]
		elif self.difficulty == 2:
			eqn, LQ = random.choice([
				((a*x+b)*(c*x+d), r'({a}x+{b})({c}x+{d})'),
				((-a*x+b)*(c*x-d), random.choice([r'(-{a}x+{b})({c}x-{d})', r'({c}x-{d})(-{a}x+{b})'])),
				((a*y+b*x)*(c*y+d+e*z), r'({a}y+{b}x)({c}y+{d}+{e}z)'),
			])
			substitutions = [
				(a, random.randint(2, 7)),
				(b, random.randint(2, 10)),
				(c, random.randint(2, 7)),
				(d, random.randint(2, 10)),
				(e, random.randint(2, 5)),
			]
		for old, new in substitutions:
			with evaluate(False):
				eqn = eqn.replace(old, new)
		soln = simplify(expand(eqn))
		a = substitutions[0][1]
		b = substitutions[1][1]
		c = substitutions[2][1]
		d = substitutions[3][1]
		e = substitutions[4][1]
		Q = getPretty(eqn)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(LQ.format(a=a, b=b, c=c, d=d, e=e))
		LA = '$\displaystyle {}$'.format(latex(soln))
		return Q, A, LQ, LA