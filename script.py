#!/usr/bin/env python

"""
Command line tool that uses main.py to generate math worksheets.
"""

from subprocess import Popen
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
	if sect == 'main': # only sect that doesn't have questions
		continue
	questions = []
	d = [int(x) for x in cfg.get(sect, 'difficulty').split(' ')]
	for di in d:
		for i in range(cfg.getint(sect, 'questions')):
			questions.append(
				Question(
					question=cfg.get(sect, 'type'),
					difficulty=di,
				),
			)
	sections.append(
		Section(
			cfg.get(sect, 'name'),
			questions = questions,
		)
	)

worksheet = Worksheet(
	cfg.get('main', 'student'),
	lesson = cfg.getint('main', 'lesson'),
	sections=sections,
)

fname = 'Lesson {} Homework'.format(cfg.getint('main', 'lesson'))

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
# os.remove('{}.tex'.format(fname))
os.remove('{}.aux'.format(fname))