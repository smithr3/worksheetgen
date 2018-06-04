#!/usr/bin/env python

"""
Command line tool that uses main.py to generate math worksheets.
"""

from subprocess import check_output, Popen
from sys import argv
from ConfigParser import SafeConfigParser
from main import *
import os
import time

cfg = SafeConfigParser()
cfg.read('cfg/{}.cfg'.format(argv[1]))

print cfg.get('main', 'student')

sections = []

for sect in cfg.sections():
	if sect == 'main':
		continue
	print sect
	questions = []
	for i in range(cfg.getint(sect, 'questions')):
		questions.append(
			Question('eval', q=algebra_simplify(n=0)),
		)
	sections.append(
		Section(
			cfg.get(sect, 'name'),
			questions = questions,
		)
	)

worksheet = Worksheet(
	cfg.get('main', 'student'),
	lesson = 12,
	sections=sections,
)

fname = cfg.get('main', 'title')

# delete previous
os.chdir("generated/")
print 'cwd', os.getcwd()
for filename in os.listdir('.'):
	print filename
	if filename.startswith(fname):
		# print '\tdeleted'
		os.remove(filename)

latex_fh = open(fname+'.txt', 'w')
latex_fh.write(worksheet.generateLatex())
latex_fh.close()

os.rename(fname+'.txt', fname+'.tex')

# https://stackoverflow.com/questions/8085520/generating-pdf-latex-with-python-script
proc = Popen(['pdflatex', '{}.tex'.format(fname)])
proc.communicate()

returncode = proc.returncode

if not returncode == 0:
	raise Exception('it broke')

os.remove('{}.log'.format(fname))
os.remove('{}.tex'.format(fname))
os.remove('{}.aux'.format(fname))