#!/usr/bin/env python

"""
Engine to generate math worksheets with random values.
Actually generates maths expr/eqns with sympy then prints to latex the question/answer.
"""

__author__ = 'Robert'

import random
from sympy import *

# todo https://tex.stackexchange.com/questions/333448/margin-notes-arent-next-to-text

class Worksheet(object):
	fileHeader = \
r"""
\documentclass[fleqn]{exam}
\usepackage{amsmath,amsthm,amssymb}
\usepackage{tasks}
\usepackage{enumitem}
\rhead{Robert Smith - \today}
\lhead{Student Name - Lesson X Homework}
\begin{document}
"""
	answerPage = \
r"""
\newpage
\setcounter{section}{0}
\section*{Answers}
"""
	fileFooter = \
r"""
\end{document}
"""

	def __init__(self, student, **kwargs):
		self.sections = kwargs.get('sections')
		self.student = student
		self.lessonN = kwargs.get('lesson', 1)

		if self.sections is None:
			self.sections = [
				Section('Algebra', all=True, desc=r'Solve the following for $x$.'),
				Section('Fractions', all=True, desc=r'Simplify or evaluate the following.'),
			]

	def generateLatex(self):
		latex = ''
		latex += Worksheet.fileHeader\
			.replace('X', str(self.lessonN))\
			.replace('Student Name', self.student)
		for section in self.sections:
			latex += section.generateLatex()
		latex += Worksheet.answerPage
		for section in self.sections:
			latex += section.generateLatex(answersOnly=True)
		latex += Worksheet.fileFooter
		return latex

class Section(object):
	section_start = \
r"""
\section{HEADING}
\noindent TEXT
\begin{tasks}(COL)
"""
	section_end = \
r"""
\end{tasks}
"""

	def __init__(self, heading, **kwargs):
		self.questions = kwargs.get('questions')
		random.shuffle(self.questions)
		self.desc = kwargs.get('desc','')
		self.heading = heading

	def generateLatex(self, **kwargs):
		answersOnly = kwargs.get('answersOnly', False)

		latex = Section.section_start\
			.replace('COL', '3')\
			.replace('HEADING', self.heading)\
			.replace(r'\noindent TEXT', self.desc)

		if answersOnly:
			for q in self.questions:
				latex += r'\task $ \displaystyle ' + q.generateLatex(answerOnly=True) + '$\n'
			latex += Section.section_end
		else:
			for q in self.questions:
				latex += r'\task $ \displaystyle ' + q.generateLatex() + '$\n'
			latex += Section.section_end
		return latex

class Question(object):
	# types = ['solve', 'eval', 'collect', 'progress']

	def __init__(self, question='fraction_add', difficulty=1):
		self.sym_q = None # symbolic question
		self.sym_a = None # symbolic answer
		self.qtype = None
		self.var = var('x')
		self.complexity = 12 # complexity in terms of depth of expression tree
		self.fn = None

		q_eval = ['fraction_add', 'fraction_mixed']
		q_collect = ['algebra_collect']
		q_expand = ['algebra_expand']
		q_factorise = ['algebra_factorise']
		q_simplify = ['algebra_simplify']
		q_solve = ['algebra_randeq', 'algebra_trig', 'algebra_solve']
		self.sym_q = globals()[question](difficulty=difficulty)
		if question in q_eval:
			self.qtype = 'eval'
		elif question in q_collect:
			self.qtype = 'collect'
		elif question in q_expand:
			self.qtype = 'expand'
		elif question in q_factorise:
			self.qtype = 'factorise'
		elif question in q_simplify:
			self.qtype = 'simplify'
		elif question in q_solve:
			self.qtype = 'solve'
		else:
			raise NotImplementedError

		if self.fn is not None:
			i = 0
			while not self.goodAnswer():
				print i
				self.sym_q = self.fn()
				self.solve()
				i+=1
		else:
			self.solve()

	def solve(self):
		print 'Q:', self.sym_q
		if self.qtype == 'solve':
			soln = solve(self.sym_q, self.var)
			print 'soln', soln, type(soln)
			if len(soln) == 0:
				self.sym_a = None
			elif len(soln) == 1:
				self.sym_a = Eq(
					self.var,
					soln[0],
				)
			elif len(soln) == 2:
				self.sym_a = [
					Eq(self.var, soln[0]),
					Eq(self.var, soln[1]),
				]
			else:
				raise NotImplementedError
		elif self.qtype == 'collect':
			w = Wild('w') # collect all like symbols
			self.sym_a = expand(collect(self.sym_q, w))
		elif self.qtype == 'expand':
			self.sym_a = expand(self.sym_q)
		elif self.qtype == 'factorise':
			self.sym_a = factor(self.sym_q)
		elif self.qtype == 'simplify':
			self.sym_a = simplify(self.sym_q)
		elif self.qtype == 'eval':
			self.sym_a = self.sym_q.doit()
		print 'A:', self.sym_a, latex(self.sym_a)

	def generateLatex(self, **kwargs):
		# used to print answers
		answerOnly = kwargs.get('answerOnly', False)

		if answerOnly:
			if type(self.sym_a) is list:
				return '{}, \ {}'.format(latex(self.sym_a[0]), latex(self.sym_a[1]))
			else:
				return latex(self.sym_a)
		else:
			if self.qtype == 'progress':
				return self.progressRender()
			else:
				return latex(self.sym_q) #+ r'\\' + latex(self.sym_a)

	def progressRender(self):
		rv = ''
		for line in self.sym_q:
			rv += latex(line) + r'\\'
		return rv

	def goodAnswer(self):
		# todo check all unique answers to avoid duplicate questions
		# answer must exist
		if self.sym_a is None:
			return False
		# solving types should have interesting answers
		if self.qtype == 'solve' and self.sym_a.rhs == 0:
			return False
		# complexity of answer should not be too high
		i = 0
		for arg in preorder_traversal(self.sym_a):
			i+=1
			# print 'ARGS='+str(i)
		if i > self.complexity:
			return False
		return True

class Algebra(object):
	variables = symbols('x y z')
	x, y, z = variables
	constants = symbols('a b c d e', real=True)
	a, b, c, d, e = constants
	functions = symbols('f g h')
	f, g, h = functions
	# COLLECT ###############################################
	collect_x = [
		a*x + b*x,
		a*x + b*x + c*x,
	]
	collect_xy = [
		a*x + b*x + c*y + d*y,
		a*y + b*x + c*x + d*y,
		a*x + b*x*y + c*x,
		a*y + b*x*y+ d*y + c*x*y,
	]
	collect = collect_x + collect_xy
	# EXPAND ##########################################
	expand_x = [
		a*(x+b),
		x*(a+x),
		a*x*(a+b*x),
	]
	expand_xy = [
		a*(x+y),
		x*(a+y),
		a*x*(y+b*x),
		a*x*(x+b*y),
		a*y*(b*x+c*y),
	]
	expand = expand_x + expand_xy
	# FACTORISE ##########################################
	factorise_hcf = [
		a*(x+b*y),
		x*(a+b*y),
		a*(x+b*y+c*z),
		a*(b*x+c*y+d*z),
		a*x*(b*x+c*y+d*z),
	]
	factorise_quad = [
		(x+a)*(x+b),
	]
	# TRIG ##########################################
	trig = [
		Eq(sin(x), 1/y),
	]
	# SIMPLE ##########################################
	simple = [
		x + a,
		x - a,
		a - x,
		a*x,
		x/a,
		a/x,
	]
	simple2 = [
		a*x + b,
		x/a + b,
		a/x + b,
		b + a*x,
		b + x/a,
		b + a/x,
	]
	# SIMPLIFY MID ALGEBRA ##################################
	alg_simplify = [
		a*(x+b)/c,
		a*(x+b) - b,
	]
	# REARRANGE ##########################################
	rearrange = [
		Eq(f, a),
		Eq(f, g),
		Eq(f/g, a),
		Eq(f/a, g/b),
		Eq(f, c*y),
		Eq(f/a+b*y, c),
		Eq(a/f+b*y, c*y),
	]
	# INDEXLAWS ############################################
	indexlaws = [
		x**a * x**b,
		x**a / x**b,
		(x**a * y**b) / x**a,
		x**a * (x**b)**c,
	]
	#######################################################
	all_expr = collect + expand

class Fractions(object):
	constants = symbols('a b c d e', real=True)
	a, b, c, d, e = constants
	#######################################################
	addition = [
		1/a + 1/b,
		a/b + c/d,
		# Rational(a,b) + Rational(c,d),
		# Frac(a,b) + Frac(c,d),
	]
	subtraction = [
		1/a - 1/b,
		a/b - c/d,
	]
	mixed = [
		a + 1/b,
		a + b/c,
	]

def algebra_collect(**kwargs):
	# todo no auto factorising!!
	n = kwargs.get('difficulty', 1)
	if n == 1:
		expr = Algebra.collect_x[0]
		return subRandom(expr, low=1, high=4)
	elif n == 2:
		expr = random.choice(Algebra.collect_x)
		return subRandom(expr, low=1, high=8, negatives=True)
	elif n == 3:
		expr = random.choice(Algebra.collect_xy)
		return subRandom(expr, low=1, high=4, negatives=True)
	elif n == 4:
		expr = random.choice(Algebra.collect_xy)
		return subRandom(expr, low=1, high=8, negatives=True)

def algebra_simplify(**kwargs):
	"""
	Types
	i   index
	l   logarithm
	c   collecting
	"""
	n = kwargs.get('difficulty', 1)

	if n == 1:
		expr = random.choice(Algebra.alg_simplify)
		return subRandom(expr, low=2, high=7, negatives=True)
	elif n == 2:
		expr = random.choice(Algebra.alg_simplify)
		return subRandom(expr, low=2, high=7, negatives=True)

def algebra_rearrange(**kwargs):
	n = kwargs.get('n')
	# expr = Add(random.choice(Algebra.all), algebra_collect(), evaluate=False)
	expr = random.choice(Algebra.rearrange)

	if type(n) is int:
		if n < len(Algebra.rearrange):
			expr = Algebra.rearrange[n]
		else:
			return -1

	return subRandom(expr, includeFunctions=True)

def algebra_randexpr(**kwargs):
	"""
	Allowed:
	m   multiplication
	d   division
	a   addition
	s   subtraction
	p   powers
	r   roots
	"""

	finished = False
	eval = kwargs.get('evaluate', True)
	depth = kwargs.get('iter', 2)
	progress = kwargs.get('progress', False)
	allowed = kwargs.get('allowed', 'mads')

	prog = []

	while not finished:
		expr = var('x')
		for _ in range(depth-1):
			prog.append(expr)
			r = random.choice(allowed)
			# todo make constant selection sampling (no dup)
			new = random.choice(Algebra.variables + Algebra.constants)
			if r == 'a':
				expr += new
			elif r == 's':
				expr -= new
			elif r == 'm':
				expr *= new
			elif r == 'd':
				expr /= new
			elif r == 'p':
				expr = expr ** new
		if var('x') in expr.free_symbols:
			finished = True

	if progress:
		return prog
	else:
		return subRandom(expr, evaluate=eval)

def algebra_randeq(**kwargs):
	n = kwargs.get('difficulty', 1)
	ldepth = kwargs.get('lhs', n+2)
	rdepth = kwargs.get('rhs', n+1)
	rv = Eq(
		algebra_randexpr(iter=ldepth),
		algebra_randexpr(iter=rdepth),
		evaluate=False,
	)
	return rv

def algebra_expand(**kwargs):
	"""
	2 (x + 4) = 2x + 8
	"""
	n = kwargs.get('difficulty', 1)

	if n == 1:
		expr = random.choice(Algebra.expand_x[:2])
		return subRandom(expr, low=2, high=7)
	elif n == 2:
		expr = random.choice(Algebra.expand_x)
		return subRandom(expr, low=2, high=7, negatives=True)
	elif n == 3:
		expr = random.choice(Algebra.expand_xy[:2])
		return subRandom(expr, low=2, high=7)
	elif n == 4:
		expr = random.choice(Algebra.expand_xy)
		return subRandom(expr, low=2, high=9, negatives=True)

def algebra_factorise(**kwargs):
	"""
	Questions created by first expanding a good answer.
	"""
	n = kwargs.get('difficulty', 1)

	if n == 1:
		expr = random.choice(Algebra.factorise_hcf[:2])
		return expand(subRandom(expr, low=2, high=7))
	elif n == 2:
		expr = random.choice(Algebra.factorise_hcf)
		return expand(subRandom(expr, low=2, high=7, negatives=True))
	elif n == 3:
		expr = random.choice(Algebra.factorise_quad)
		return expand(subRandom(expr, low=2, high=7))
	elif n == 4:
		expr = random.choice(Algebra.factorise_quad)
		return expand(subRandom(expr, low=2, high=9, negatives=True))

def algebra_trig(**kwargs):
	"""
	Practicing algebra on basic trig ratios
	"""
	n = kwargs.get('difficulty', 1)

	if n == 1:
		expr = random.choice(Algebra.trig)
		return subRandom(expr, low=2, high=7)
	elif n == 2:
		expr = random.choice(Algebra.trig)
		return subRandom(expr, low=2, high=7, negatives=True)

def algebra_solve(**kwargs):
	"""
	Solve for x.
	"""
	n = kwargs.get('difficulty', 1)

	if n == 1:
		left = random.choice(Algebra.simple)
		right = Algebra.a
		return Eq(
			subRandom(left, low=1, high=7),
			subRandom(right, low=0, high=7),
		)
	elif n == 2:
		left = random.choice(Algebra.simple2)
		right = Algebra.a
		return Eq(
			subRandom(left, low=1, high=7, negatives=True),
			subRandom(right, low=0, high=7, negatives=True),
		)
	elif n == 3:
		left = random.choice(Algebra.expand_x)
		right = 0
		return Eq(
			subRandom(left, low=2, high=7),
			right,
		)
	elif n == 4:
		left = random.choice(Algebra.expand_x)
		right = 0
		return Eq(
			subRandom(left, low=2, high=7),
			right,
		)
	elif n == 5:
		left = random.choice(Algebra.factorise_quad)
		right = 0
		return Eq(
			subRandom(left, low=2, high=7, negatives=True),
			right,
		)
	elif n == 6:
		left = random.choice(Algebra.factorise_quad)
		right = 0
		return Eq(
			expand(subRandom(left, low=2, high=7)),
			right,
		)


def fraction_add(**kwargs):
	"""
	8/6 + 10/4 = 23/6
	"""
	n = kwargs.get('difficulty', 1)

	# note: if sub in a constant of 1, then latex breaks for some reason
	if n == 1:
		expr = Fractions.addition[0]
		return subRandom(expr, low=2, high=7)
	elif n == 2:
		expr = Fractions.addition[0]
		return subRandom(expr, low=2, high=12)
	elif n == 3:
		expr = Fractions.addition[1]
		return subRandom(expr, low=2, high=7)
	else:
		expr = Fractions.addition[1]
		return subRandom(expr, low=2, high=12)

def fraction_mixed(**kwargs):
	"""

	"""
	n = kwargs.get('difficulty', 1)

	all_expr = Fractions.addition + Fractions.mixed + Fractions.subtraction
	expr = random.choice(all_expr)

	if n == 1:
		return subRandom(expr, low=2, high=7, negatives=True)
	else:
		return subRandom(expr, low=2, high=12, negatives=True)

def subRandom(expr, **kwargs):
	doEval = kwargs.get('evaluate', False)
	low = kwargs.get('low', 1)
	high = kwargs.get('high', 10)

	assert(type(expr) != type(list))

	# make constants unique if possible
	if len(Algebra.constants) >= high - low + 1:
		randomValues = [random.randint(low, high) for _ in range(len(Algebra.constants))]
	else:
		randomValues = random.sample(range(low, high), len(Algebra.constants))

	if kwargs.get('negatives', False):
		for i, val in enumerate(randomValues):
			if random.randint(0,1):
				randomValues[i] *= -1

	substitutions = zip(
		Algebra.constants,
		randomValues,
	)

	if kwargs.get('includeFunctions'): # prevents inf recursion somehow
		substitutions += [
			(var('f'), subRandom(algebra_randexpr())),
			(var('g'), subRandom(algebra_randexpr())),
			(var('h'), subRandom(random.choice(Algebra.all_expr+list(Algebra.variables)))),
		]

	# https://github.com/sympy/sympy/issues/12017
	# return expr.subs(substitutions, evaluate=False)
	# if type(expr) is not int:
	for old, new in substitutions:
		with evaluate(doEval):
			expr = expr.replace(old, new)

	return expr