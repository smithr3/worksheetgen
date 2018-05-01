#!/usr/bin/env python

"""
Command line tool that uses mainv2.py to generate math worksheets.
"""

__author__ = 'Robert'

import argparse

from mainv2 import *

parser = argparse.ArgumentParser(description=__doc__)
# parser.add_argument()

worksheet1 = Worksheet(
	'Jerry Sammut',
	lesson=11,
	sections=[
		Section(
			'Solving',
			questions=[
				# Question('solve', fn=algebra_randeq),
				# Question('solve', fn=algebra_randeq),
				# Question('solve', fn=algebra_randeq),
				# Question('solve', fn=algebra_randeq),
				Question('solve', q=algebra_rearrange(n=4)),
				Question('solve', q=algebra_rearrange(n=5)),
				Question('solve', q=algebra_rearrange(n=6)),
			]
		),
		Section(
			'Index Laws',
			questions=[
				Question('eval', q=algebra_simplify(n=0)),
				Question('eval', q=algebra_simplify(n=1)),
				Question('eval', q=algebra_simplify(n=2)),
				Question('eval', q=algebra_simplify(n=3)),
			]
		)
	]
)

worksheet2 = Worksheet(
	'Jackson Serratore',
	lesson=13,
	sections=[
		Section(
			'Algebra',
			questions=[
				Question('solve', q=algebra_rearrange(n=4)),
				Question('solve', q=algebra_rearrange(n=5)),
				Question('solve', q=algebra_rearrange(n=5)),
				Question('solve', q=algebra_rearrange(n=6)),
				Question('solve', q=algebra_rearrange(n=6)),
				Question('solve', q=algebra_rearrange(n=6)),
			]
		),
		Section(
			'Fractions',
			questions=[
				Question('solve', fn=algebra_randeq),
			]
		)
	]
)

worksheet3 = Worksheet(
	'Otis C',
	lesson=1,
	sections=[
		Section(
			'BODMAS',
			questions=[
				Question('solve', q=algebra_rearrange(n=4)),
				Question('solve', q=algebra_rearrange(n=5)),
				Question('solve', q=algebra_rearrange(n=5)),
				Question('solve', q=algebra_rearrange(n=6)),
				Question('solve', q=algebra_rearrange(n=6)),
				Question('solve', q=algebra_rearrange(n=6)),
			]
		),
		Section(
			'Fractions',
			questions=[
				Question('solve', fn=algebra_randeq),
			]
		)
	]
)

fname = 'worksheet4'

# delete previous
for filename in os.listdir("."):
	# print filename
	if filename.startswith(fname):
		# print '\tdeleted'
		os.remove(filename)


latex_fh = file(fname+'.txt', 'w')
latex_fh.write(worksheet2.generateLatex())
latex_fh.close()

os.rename(fname+'.txt', fname+'.tex')
# print '\nrenamed from .txt to .tex'

cmd = 'pdflatex {}.tex'.format(fname)
# print 'running command "{}"\n'.format(cmd)
print check_output(cmd, shell=True)