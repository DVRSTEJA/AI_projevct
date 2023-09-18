#!/usr/bin/python3
#####################################################
#############  LEAVE CODE BELOW  ALONE  #############
# Include base directory into path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

# Import tester
from tester import failtest, passtest, assertequals, runcmd, preparefile, runcmdsafe
#############    END UNTOUCHABLE CODE   #############
#####################################################

###################################
# Write your testing script below #
###################################
python_bin = sys.executable
import pickle
from slidingpuzzle import *

# prepare necessary files
preparefile('./test.py')
preparefile('./input')

# run test file
b_stdout, b_stderr, b_exitcode = runcmdsafe(f'"{python_bin}" ./test.py')


# convert stdout bytes to utf-8
stdout = ""
stderr = ""
try:
	stdout = b_stdout.decode('utf-8')
	stderr = b_stderr.decode('utf-8')
except:
	pass

def replay(board, moves):
        st = State(board, [], 0)
        while len(moves) > 0:
                nextact = moves[0]
                moves = moves[1:]
                if nextact not in st.board.actions(): return False
                st = st.step(nextact)
        return st.goal()


# stdout comparison with expected.txt here
try:
	with open('input', 'rb') as file1, open('output', 'rb') as file2:
		inputboard = pickle.load(file1)
		outputmoves = pickle.load(file2)
		if replay(inputboard, outputmoves):  
			runcmdsafe('rm ./output')
			passtest('')
		else:
			runcmdsafe('rm ./output')
			failtest(stdout+"\n\n"+stderr)
except FileNotFoundError:
	failtest(stdout+"\n\n"+stderr)
