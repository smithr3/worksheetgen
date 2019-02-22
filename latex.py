"""
Contains Worksheet class, which manages creating the LaTeX file.

Robert
21/02/2019
"""

import os
from subprocess import Popen

DOC_START = r"""
\documentclass[fleqn]{exam}
\usepackage{amsmath,amsthm,amssymb}
\usepackage{tasks}
\usepackage{enumitem}

\renewcommand\thesubsection{Q\arabic{subsection}}

\newcommand{\qbreak}{%
\noindent\makebox[\linewidth]{\rule{\textwidth}{0.4pt}}%
\setcounter{section}{0}%
\setcounter{subsection}{0}%
}

\rhead{Robert Smith - \today}
%\lhead{Student Name - X}

\begin{document}
"""
SECTION_START = r"""
\subsection{HEADING}
%\noindent TEXT
\begin{tasks}(COL)
"""
SECTION_END = r"""
\end{tasks}
"""
ANSWERS_PAGE = r"""
\newpage
\setcounter{subsection}{0}
\section*{Answers}
"""
DOC_END = r"""
\end{document}
"""

class Worksheet:

	def __init__(self):
		self.fname = 'generated'
		self.latex = ''
		self.sections = []

	def addSection(self, name, qs, ans, cols, rule):
		self.sections.append(Section(name, qs, ans, cols, rule))

	def render(self):
		self.add(DOC_START)
		# questions
		for section in self.sections:
			if section.rule:
				self.add('\qbreak')
			self.add(
				SECTION_START.replace('HEADING', section.name).replace('COL', str(section.cols))
			)
			tasks = []
			for q in section.qs:
				tasks.append(r'\task ' + q)
			self.add('\n'.join(tasks))
			self.add(SECTION_END)
		# answers
		self.add(ANSWERS_PAGE)
		for section in self.sections:
			if section.rule:
				self.add('\qbreak')
			self.add(
				SECTION_START.replace('HEADING', section.name).replace('COL', str(section.cols))
			)
			tasks = []
			for a in section.ans:
				tasks.append(r'\task ' + a)
			self.add('\n'.join(tasks))
			self.add(SECTION_END)
		self.add(DOC_END)

	def add(self, code):
		if code[-1] != '\n':
			code += '\n'
		self.latex += code

	def write(self):
		os.chdir("generated/")
		if os.path.isfile('{}.tex'.format(self.fname)):
			print('Overwriting existing generated files')
			for filename in os.listdir('.'):
				if filename.startswith(self.fname):
					print('\tdeleted {}'.format(filename))
					deleted = False
					while not deleted:
						try:
							os.remove(filename)
						except PermissionError as e:
							print(e)
							input("Press Enter to try again.")
							continue
						deleted = True

		latex_fh = open(self.fname+'.tex', 'w')
		latex_fh.write(self.latex)
		latex_fh.close()

		# https://stackoverflow.com/questions/8085520/generating-pdf-latex-with-python-script
		proc = Popen(['pdflatex', '{}.tex'.format(self.fname)])
		proc.communicate()

		returncode = proc.returncode

		if not returncode == 0:
			raise Exception('It broke.')

		os.remove('{}.log'.format(self.fname))
		os.remove('{}.aux'.format(self.fname))

class Section:

	def __init__(self, name, qs, ans, cols, rule):
		assert cols is not None
		self.name = name
		self.qs = qs
		self.ans = ans
		self.cols = cols
		self.rule = rule