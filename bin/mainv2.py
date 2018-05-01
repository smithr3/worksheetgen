#!/usr/bin/env python

"""
Engine to generate math worksheets with random values.
"""

__author__ = 'Robert'

import os
import random
from subprocess import check_output

from sympy import *


class Worksheet(object):
	fileHeader = \
r"""
\documentclass[fleqn]{exam}
\usepackage{amsmath,amsthm,amssymb}
\usepackage{multicol}
\usepackage{enumitem}
\rhead{Robert Smith}
\lhead{Student Name - Lesson X Homework}
\begin{document}
"""
	answerPage = \
r"""
\newpage
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
\begin{multicols}{COL}
\begin{enumerate}[label=(\alph*)]
"""
	section_end = \
r"""
\end{enumerate}
\end{multicols}
"""

	def __init__(self, heading, **kwargs):
		self.questions = kwargs.get('questions')
		self.desc = kwargs.get('desc','')
		self.heading = heading

		if kwargs.get('all'):
			if self.heading == 'Algebra':
				self.questions = [
					Question('collect', q=algebra_collect(n=0)),
					Question('eval', fn=algebra_randexpr, arg={'allowed':'mdp'}),
					Question('eval', q=algebra_simplify(n=0)),
					Question('eval', q=algebra_simplify(n=1)),
					Question('eval', q=algebra_simplify(n=2)),
					Question('eval', q=algebra_simplify(n=3)),
					Question('solve', q=algebra_rearrange(n=0)),
					Question('solve', q=algebra_randexpr()),
					Question('solve', q=algebra_randeq()),
					Question('solve', fn=algebra_randeq),
					Question('progress', q=algebra_randexpr(progress=True, iter=3)),
				]
			elif self.heading == 'Fractions':
				self.questions = [
					Question('eval', q=fraction_add(n=0)),
					Question('eval', q=fraction_add(n=0)),
					Question('eval', q=fraction_add(n=0)),
				]

	def generateLatex(self, **kwargs):
		answersOnly = kwargs.get('answersOnly', False)

		latex = Section.section_start\
			.replace('COL', '2')\
			.replace('HEADING', self.heading)\
			.replace(r'\noindent TEXT', self.desc)

		if answersOnly:
			for q in self.questions:
				latex += r'\item $ \displaystyle ' + q.generateLatex(answerOnly=True) + '$\n'
			latex += Section.section_end
		else:
			for q in self.questions:
				latex += r'\item $ \displaystyle ' + q.generateLatex() + '$\n'
			latex += Section.section_end
		return latex

class Question(object):
	# types
	types = ['solve', 'eval', 'collect']

	def __init__(self, qtype, **kwargs):
		self.sym_q = kwargs.get('q') # symbolic question
		self.sym_a = None # symbolic answer
		self.qtype = qtype
		self.var = var(kwargs.get('var', 'x'))
		self.complexity = kwargs.get('complexity', 12) # complexity in terms of depth of expression tree

		self.fn = kwargs.get('fn')

		if self.fn is not None:
			i = 0
			while not self.goodAnswer():
				print i
				self.sym_q = self.fn(**kwargs.get('arg',{}))
				self.solve()
				i+=1
		else:
			self.solve()

	def solve(self):
		print 'Q:', self.sym_q
		if self.qtype == 'solve':
			soln = solve(self.sym_q, self.var)
			print 'soln', soln, type(soln)
			if len(soln) == 1:
				self.sym_a = Eq(
					self.var,
					soln[0],
				)
		elif self.qtype == 'collect':
			w = Wild('w') # collect all like symbols
			self.sym_a = collect(self.sym_q, w)
		elif self.qtype == 'eval':
			self.sym_a = self.sym_q.doit()
		print 'A:', self.sym_a

	def generateLatex(self, **kwargs):
		answerOnly = kwargs.get('answerOnly', False)

		if answerOnly:
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
	]
	collect = collect_x + collect_xy
	# EXPAND ##########################################
	expand_x = [
		a*(x+b),
		x*(a+b),
	]
	expand_xy = [
		a*(x+y),
		x*(a+y),
	]
	expand = expand_x + expand_xy
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
	variables = symbols('x y z')
	x, y, z = variables
	constants = symbols('a b c d e', real=True)
	a, b, c, d, e = constants
	#######################################################
	addition = [
		1/a + 1/b,
		a/b + c/d,
		# a/b + c/d,
		# Rational(a,b) + Rational(c,d),
		# Frac(a,b) + Frac(c,d),
	]

def algebra_collect(**kwargs):
	nvar = kwargs.get('nvar')
	n = kwargs.get('n') # nth version of question
	if nvar == 1:
		expr = random.choice(Algebra.collect_x)
	elif nvar == 2:
		expr = random.choice(Algebra.collect_xy)
	else:
		expr = random.choice(Algebra.collect)

	if type(n) is int:
		if n < len(Algebra.collect):
			expr = Algebra.collect[n]
		else:
			return -1
	return subRandom(expr)

def algebra_simplify(**kwargs):
	"""
	Types
	i   index
	l   logarithm
	c   collecting
	"""

	n = kwargs.get('n') # nth version of question

	if type(n) is int:
		if n < len(Algebra.indexlaws):
			expr = Algebra.indexlaws[n]
		else:
			return -1
	return subRandom(expr, low=2, high=6)

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
	depth = kwargs.get('iter', 3)
	ldepth = kwargs.get('lhs', depth)
	rdepth = kwargs.get('rhs', depth-1)
	rv = Eq(
		algebra_randexpr(iter=ldepth),
		algebra_randexpr(iter=rdepth),
		evaluate=False,
	)
	# print 'rv', rv
	return rv

def fraction_add(**kwargs):
	n = kwargs.get('n')

	expr = Fractions.addition[0]

	if type(n) is int:
		if n < len(Fractions.addition):
			expr = Fractions.addition[n]
		else:
			expr = -1

	return subRandom(expr)
	# return subRandom(Fractions.addition[0])

def subRandom(expr, **kwargs):
	eval = kwargs.get('evaluate', False)
	low = kwargs.get('low', 1)
	high = kwargs.get('high', 10)

	if len(Algebra.constants) >= high - low + 1:
		randomValues = [random.randint(low, high) for _ in range(len(Algebra.constants))]
	else:
		randomValues = random.sample(range(low, high), len(Algebra.constants))

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
		with evaluate(eval):
			expr = expr.replace(old, new)

	return expr

