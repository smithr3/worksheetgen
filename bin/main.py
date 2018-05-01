__author__ = 'Robert'

import os
import random
from subprocess import check_output

from question import *


# test = open('testing/test.tex')
# print '%r' % test.read()

# delete previous
for filename in os.listdir("."):
	# print filename
	if filename.startswith("worksheet"):
		# print '\tdeleted'
		os.remove(filename)

# create new
latex = ''
latex_fh = file('worksheet.txt', 'w')
print '\ncreated worksheet.txt\n'

latex += header + '\n'

#####  QUESTIONS  ######################################################################
latex += new_question(2, "Fractions", "Calculate and simplify the following.")
for _ in range(20):
	sel = random.randint(1, 5)
	if sel == 1:
		latex += Question(add_two_fractions).generateInstance() + '\n'
	elif sel == 2:
		latex += Question(sub_two_fractions).generateInstance() + '\n'
	elif sel == 3:
		latex += Question(mult_two_fractions).generateInstance() + '\n'
	elif sel == 4:
		latex += Question(mult_two_fractions_brackets).generateInstance() + '\n'
	elif sel == 5:
		latex += Question(div_two_fractions).generateInstance() + '\n'
latex += question_end

latex += new_question(3, "Fractions 2", "Calculate and simplify the following 2.")
for _ in range(9):
	latex += Question(add_two_fractions).generateInstance() + '\n'
latex += question_end
#####  QUESTIONS  ######################################################################

latex += footer

latex_fh.write(latex)
latex_fh.close()
print
print latex

os.rename('worksheet.txt', 'worksheet.tex')
print '\nrenamed from .txt to .tex'

cmd = 'pdflatex worksheet.tex'
print 'running command "{}"\n'.format(cmd)
print check_output(cmd, shell=True)