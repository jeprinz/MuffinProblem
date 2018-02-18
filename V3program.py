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
	

def makeEVals(d, numIntervals):
	"""Returns a bunch of LpVariable objects of all variables from the paper.
	Remember, for f(m,s), a = s and d = m-s"""
	eVals = {}
	for index in listsAddingTo(numIntervals, 3):
		name = "e_" + str(index)
		eVals[index] = LpVariable(name, 0, 2*d, LpInteger) #number of 3 students is 2d when V=3
	return eVals

def makeEasyConstraints(eVals, d, intervalTotals):
	sums = [0] * len(intervalTotals)
	total = 0
	for index in eVals:
		eVar = eVals[index]
		for i in range(len(sums)):
			sums[i] += index[i] * eVar
		total += eVar
	intervalConstraints = [sum == intervalTotal for (sum, intervalTotal) in zip(sums, intervalTotals)]
	return intervalConstraints + [total == 2*d] #there are 2d 3-students

def findCutPoints(eVals, intervals):
	"""Finds values of X where below that value, some e variable must be 0.
	returns (list of constraints that always happen, cut list)
	cut list is ordered list of (Xcut, constraint)
	intervals is a list of [(min,max), (min,max)]
	where min and max are sympy expressions with X as a variable"""

	always = []
	cuts = []

	#Loop through each e variable, and find the minimum X that allows it to be nonzero.
	for index in eVals: 
		eVar = eVals[index]

		#minimum amount of muffin that can be found in given intervals from index
		minValue = sum(numIntervals * interval[0] for numInInterval, interval in zip(index, intervals))
		#maximum amount of muffin that can be found in given intervals from index
		maxValue = sum(numIntervals * interval[1] for numInInterval, interval in zip(index, intervals))

		#X values which will allow such a student to exist
		allowedXValues = sympy.solve([minValue <= total, total <= maxValue], X).as_set()

		#note 2a/5 below. Bill sent me this bound in an email. Is this actually where X should start?
		if allowedXValues == sympy.EmptySet() or allowedXValues.end <= 0:# 2*a/5:#if the constraint can never be met or is smaller than X can be
			always.append(eVar == 0)#add constraint that variable is zero
		else:#otherwise if the constraint can be met
			cuts.append((allowedXValues.end, eVar == 0))#add on (min val of X where constraint can't be met, constraint that variable is zero)
	cuts = sorted(cuts)
	return (always, cuts)
			
def findX(d, intervals, totals):
	"""intervals is a list of intervals [(min(X), max(X)), (min(X), max(X))],
	totals is a list of the same length which has all of the total amount of peices in the intervals"""
	prob = LpProblem("The problem", LpMinimize) #define pulp problem

	eVals = makeEVals(d, len(intervals))
	constraints = makeEasyConstraints(eVals, d, totals)
	for constraint in constraints:
		prob += constraint
	
	(always, cuts) = findCutPoints(eVals, intervals)

	for constraint in always: #NOTE FOR DEBUGGING LATER: ITS POSSIBLE THESE LINES WERE COMMENTED OUT LAST MEETING
		prob += constraint
	
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

def makeFirstCaseIntervals(a,d,k):
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
	return Intervals
