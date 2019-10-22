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
				Eq(a*x + b/d, c),
				Eq(a*x - b, c),
				Eq(a*x - b/d, c),
				Eq(x/a + b, c),
				Eq(x/a - b, c),
			])
			# todo flip sides of equations randomly
			eqn = eqn.subs([
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(0, 10)),
				(d, random.randint(2, 7)),
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
				# this one causes exception since eqn=boolean for some reason
				# (Eq((a*x + b)/(c*x), d), r'\frac{{ {a}x+{b} }}{{ {c}x }} = {d}'.format(a=a, b=b, c=c, d=d)),
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
				(Eq(AF1 - AF2, AF3), '{} - {} = {}'.format(AFL1, AFL2, AFL3)),
			])
		try:
			soln = Eq(x, solve(eqn, x)[0])
		except IndexError:
			# no solution
			soln = 'No solution'
		except TypeError as e:
			# print('TypeError', e)
			# print('diff', self.difficulty)
			# print('eqn', eqn)
			# print('LQ', LQ)

			# no solution either, something like -4x + 4x leaving no x's and no solution
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
				(Eq(x*(x+a/b), 0), r'x(x+\frac{{{a}}}{{{b}}}) = 0'),
				(Eq(x*(x-a), 0), r'x(x-{a}) = 0'),
				(Eq(a*x*(x+b), 0), r'{a}x(x+{b}) = 0'),
				(Eq(a*x*(x-b), 0), r'{a}x(x-{b}) = 0'),
				(Eq(a*x*(x-b/c), 0), r'{a}x(x-\frac{{{b}}}{{{c}}}) = 0'),
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

class SolvingQuadratic(Question):
	"""
	Solving quadratic equations, requiring factorisation first. Monic and non-monic, DoTS, completing the square?
	x^2 + 4x + 3
	"""
	taskColumns = 3
	maxDifficulty = 4

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : 'Highest common factor',
			2 : 'Cross method',
			3 : 'Difference of perfect squares',
			4 : 'Non-monic',
		}
		self.defaultTitle = 'Solving Quadratics'

	def generate(self):
		x = symbols('x')
		a, b, c, d, e, f = symbols('a b c d e f')
		substitutions, eqn, LQ = [], None, None
		# HCF
		if self.difficulty == 1:
			expr = expand(random.choice([
				x*(x+a),
				x*(x-a),
			]))
			if random.random() < 0.3:
				expr *= b
			if random.random() < 0.3:
				expr *= -1
			eqn = Eq(expr, 0)
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(2, 10)),
				(c, random.randint(2, 10)),
				(d, random.randint(1, 10)),
			]
		# Cross
		elif self.difficulty == 2:
			expr = expand(random.choice([
				(x+a)*(x+b),
				(x-a)*(x+b),
				(x+a)*(x-b),
				(x-a)*(x-b),
			]))
			if random.random() < 0.5:
				expr *= c
			eqn = Eq(expr, 0)
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(1, 6)),
				(c, random.randint(2, 5)),
				(d, random.randint(1, 10)),
			]
		# DOPS
		elif self.difficulty == 3:
			expr = expand(random.choice([
				(x+a)*(x-a),
				(a*x+b)*(a*x-b),
			]))
			if random.random() < 0.3:
				expr *= c
			eqn = Eq(expr, 0)
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(1, 10)),
				(c, random.randint(2, 5)),
				(d, random.randint(1, 10)),
			]
		# Non-monic
		elif self.difficulty == 4:
			expr = expand(random.choice([
				(a*x+b)*(x+d),
				(a*x+b)*(c*x+d),
			]))
			if random.random() < 0.3:
				expr *= a
			eqn = Eq(expr, 0)
			substitutions = [
				(a, random.randint(2, 4)),
				(b, random.randint(2, 10)),
				(c, random.randint(2, 5)),
				(d, random.randint(2, 5)),
			]
		for old, new in substitutions:
			with evaluate(True):
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
		LQ = '$\displaystyle {}$'.format(latex(eqn))
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
			2 : 'Linear - hard algebraic fraction questions',
			3 : 'Quadratic - two solutions',
		}
		self.defaultTitle = 'Solving'
		self.solvingLinear = SolvingLinear()
		self.solvingAlgebraicFractions = SolvingAlgebraicFractions()
		self.solvingNullFactor = SolvingNullFactor()
		# todo solvingQuadratic

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
				(self.solvingAlgebraicFractions, random.randint(1, self.solvingAlgebraicFractions.maxDifficulty)),
			])
			question.difficulty = difficulty
			Q, A, LQ, LA = question.generate()
			return Q, A, LQ, LA
		elif self.difficulty == 3:
			question, difficulty = random.choice([
				(self.solvingNullFactor, random.randint(1,self.solvingNullFactor.maxDifficulty)),
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
				(a/d*(b*x+c), r'\frac{{ {a} }}{{ {d} }} ({b}x+{c})'),
				(d + a*(b*x-c), r'{d}+{a}({b}x-{c})'),
				(d + a*(b*x-c/e), r'{d}+{a}({b}x-\frac{{ {c} }}{{ {e} }})'),
				(-a*(b*x+c*y), r'-{a}({b}x+{c}y)'),
				(d-a*(-b*x+c*y), r'{d}-{a}(-{b}x+{c}y)'),
				(a*x*(b*y+c*z), r'{a}x({b}y+{c}z)'),
			])
			substitutions = [
				(a, random.randint(2, 10)),
				(b, random.randint(2, 7)),
				(c, random.randint(2, 10)),
				(d, random.randint(2, 7)),
				(e, random.randint(2, 10)),
			]
		elif self.difficulty == 2:
			eqn, LQ = random.choice([
				((a*x+b)*(c*x+d), r'({a}x+{b})({c}x+{d})'),
				((a/e*x+b)*(c*x+d), r'(\frac{{ {a}x }}{{ {e} }}+{b})({c}x+{d})'),
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
		soln = expand(eqn)
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

class Rearrange(Question):
	"""
	Challenging and varied rearranging questions. Rearrange for x.
	2xy = 3
	5/2x + y = 1/2
	3x/2y = 5z/2
	1 = y/(2x+1)
	"""
	taskColumns = 3
	maxDifficulty = 2

	# todo solve for something different can give more interesting answers
	# todo more variety in techniques

	def __init__(self, defaultDifficulty=1):
		super().__init__(defaultDifficulty, self.maxDifficulty)
		self.description = {
			1 : '3 iterations',
			2 : '5 iterations',
		}
		self.defaultTitle = 'Rearrange for x'

		self.pronumerals = None
		self.used = None

	def generate(self):
		iters = 1
		if self.difficulty == 1:
			iters = 3
		elif self.difficulty == 2:
			iters = 5

		x = symbols('x')
		# self.pronumerals = symbols('a b c d e f k m n p r t w y z', real=True)
		self.pronumerals = symbols('a b c w y z', real=True)
		self.used = []
		substitutions, eqn, LQ = [], None, None

		# left and right hand expressions
		lh = x
		rh = 0

		for i in range(iters):
			# chance to make RHS a pronumeral
			if i == 0 and random.random() < 0.5:
				rh = self.getVar()

			# ensure something is done to LHS
			if i < 2:
				lh = self.extend(lh)
			# otherwise 50-50 it's LHS or RHS
			elif random.random() < 0.5:
				lh = self.extend(lh)
			else:
				rh = self.extend(rh)

		eqn = Eq(lh, rh)
		try:
			soln = solve(eqn, x)[0]
			soln = Eq(x, soln)
		except IndexError as e:
			print(e)
			soln = 'No solution'

		Q = getPretty(eqn)
		A = getPretty(soln)
		LQ = '$\displaystyle {}$'.format(latex(eqn))
		LA = '$\displaystyle {}$'.format(latex(soln))
		return Q, A, LQ, LA

	def extend(self, expr):
		x = random.random()
		if x < 0.3: # higher chance of adding than subbing
			expr += self.getVar()
		elif x < 0.4:
			expr -= self.getVar()
		elif x < 0.6:
			expr *= self.getVar()
		elif x < 0.8:
			expr = self.getVar() / expr
		else:
			expr /= self.getVar()
		return expr

	def getVar(self):
		pronumeral = random.choice(self.pronumerals)
		while pronumeral in self.used:
			pronumeral = random.choice(self.pronumerals)
		self.used.append(pronumeral)
		return pronumeral