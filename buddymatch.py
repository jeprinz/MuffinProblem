#an experiment on using repeated buddy-matching to find bounds, keeping track of only one piece

import interval

import functools
from fractions import Fraction

o = Fraction(1)#makes typing some things less tedious

#A function here is a tuple (a,b) which represents f(x) = ax + b

def findEquilibrium(f):
	"""Given function, find equilibrium point"""
	a, b = f
	return b/(1-a)

def compose(funcList):
	"""Given list of functions, compose them all together"""
	def comp2(f, g):
		a1, b1 = f
		a2, b2 = g
		return (a1*a2, a1*b2 + b1)
	return functools.reduce(comp2,funcList)

def genMatchFunctions(m, s):
	"""Given an (m,s), generate a tuple (MVm1, MV) which has the match functions.
	There are two match functions because which one is to be used depends on
	weather the piece is a V share or a V-1 share. The MV works for V shares, and
	the MVm1 works for V-1 shares."""
	m, s = Fraction(m), Fraction(s)

	V = interval.findV(m,s)

	MV = (-o/(V-1), m/s/(V-1))
	MVm1 = (-o/(V-2), m/s/(V-2))
	return (MV, MVm1)

def makeSequence(pairs, m, s, startSmall=True):
	"""Valid sequences of buddy match function consist of iterations of:
	A) n MVm1 matches, B) buddy, C)  m MV, D) buddy
	in other words, there must be a buddy before switching between the V and V-1 matches.
	Thus, input is given as pairs = [(n, m), (n, m), (n, m)]
	and this function will return sequence of functions
	startSmall refers to if it does V first, rather than V-1"""

	MV, MVm1 = genMatchFunctions(m,s)
	B = (-1, 1)

	kind1, kind2 = None, None

	if startSmall:
		kind1, kind2 = MV, MVm1
	else:
		kind1, kind2 = MVm1, MV
		

	functions = []
	for (n,m) in pairs:
		for i in range(n):
			functions.append(kind1)
		functions.append(B)
		for i in range(m):
			functions.append(kind2)
		functions.append(B)
	
	return functions


def solveSequence(pairs, m,s, startSmall=True):
	"""Takes sequence of pairs (as above function) and returns bound given"""
	seq = makeSequence(pairs, m,s, startSmall)
	f = compose(seq)
	return findEquilibrium(f)

