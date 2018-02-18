from pulp import *
from functools import reduce
import sympy
import interval

#####################################################################
# This code is intended to run Bill's crazy program with all the cases for the V=3 case
# In addition, this is all for the case where d <= a <= 2d-1
#####################################################################

def listsAddingTo(length, total):
	"""Returns all possible lists of length elements adding to total"""
	if length == 1:
		yield [total]
	elif total == 0:
		yield [0]*length
	else:
		for i in range(0, total+1):
			for rest in listsAddingTo(length - 1, total - i):
				yield [i] + rest
	

def makeEVals(a, d, numIntervals):
	"""Returns a bunch of LpVariable objects of all variables from the paper.
	Remember, for f(m,s), a = s and d = m-s"""
	eVals = {}
	for index in listsAddingTo(numIntervals, 3):
		name = "e_" + str(index)
		eVals[index] = LpVariable(name, 0, 2*d, LpInteger) #number of 3 students is at most 2d when V=3
	return eVals

def makeEasyConstraints(eVals, a, d, intervalTotals):
	sums = [0] * len(intervalTotals)
	total = 0
	for index in eVals:
		eVar = eVals[index]
		for i in range(len(sums)):
			sums[i] += index[i] * eVar
		total += eVar
	#note that bill wanted total == 6*d because he says s3 == 2d, but this is nonsense
	#TODO: figure out why bill was wrong
	V = interval.findV(a+d, a)
	(sV, sVm1) = interval.getShares(a+d, a, V)
	return [I1sum == a+d, I2sum == a+d, I3sum == 2*d-a, I4sum == 2*d-a, total == 2*d]

def findCutPoints(eVals, a, d, k=0):
	"""Finds values of X where below that value, some e variable must be 0.
	returns (list of constraints that always happen, cut list)
	cut list is ordered list of (Xcut, constraint)"""

	S = sympy.S
	a, d, k = S(a), S(d), S(k)
	
	#the total is m/s = 3dk + a + d/3dk + a 
	denom = 3*d*k + a #this comes up alot

	total = S(3*d*k + a + d) / denom #total muffin for one student
	X = sympy.symbols('X')

	values = [val / denom for val in [d*k + X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+(a+d)/2, d*k+a+d - 2*X]]
	print("values: " + str(values))
	print("bill values: " + str([val*(3*d*k+a) - d*k for val in values]))

	#The four intervals reffered to in the paper. Note that 0 indexing means e.g. interval 2 is Intervals[1]
	Intervals = [(values[0], values[1]), (values[1], values[2]), (values[4], values[5]), (values[5], values[6])]

	always = []
	cuts = []

	#Loop through each e variable, and find the minimum X that allows it to be nonzero.
	for key in eVals: 
		(j1, j2, j3, j4) = key
		eVar = eVals[key]

		minValue = j1 * Intervals[0][0] + j2 * Intervals[1][0] + j3 * Intervals[2][0] + j4 * Intervals[3][0]
		maxValue = j1 * Intervals[0][1] + j2 * Intervals[1][1] + j3 * Intervals[2][1] + j4 * Intervals[3][1]

		interval = sympy.solve([minValue <= total, total <= maxValue], X).as_set()

		#note 2a/5 below. Bill sent me this bound in an email. Is this actually where X should start?
		if interval == sympy.EmptySet() or interval.end <= 0:# 2*a/5:#if the constraint can never be met or is smaller than X can be
			always.append(eVar == 0)#add constraint that variable is zero
		else:#otherwise if the constraint can be met
			cuts.append((interval.end, eVar == 0))#add on (min val of X where constraint can't be met, constraint that variable is zero)
	cuts = sorted(cuts)
	return (always, cuts)
			
def findX(a,d,k=0):
	prob = LpProblem("The problem", LpMinimize) #define pulp problem

	eVals = makeEVals(a, d, 4) #HARD CODED CHANGE
	constraints = makeEasyConstraints(eVals, a, d) #HARD CODED CHANGE
	for constraint in constraints:
		prob += constraint
	
	(always, cuts) = findCutPoints(eVals, a, d, k)

	#for constraint in always:
	#	prob += constraint
	
	for cut in cuts:
		print("Trying cut " + str(cut[0]))
		#print(prob)
		status = prob.solve()
		if status != 1:
			print("No solution found, moving to next cut and adding constraint")
			prob += cut[1]
		else:
			print("found solution, returning")
			prob += cut[1]
			#return cut[0]
