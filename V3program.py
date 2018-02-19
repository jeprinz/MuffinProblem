from pulp import *
from functools import reduce
import sympy
import interval
from fractions import Fraction

#####################################################################
# This code is intended to run Bill's crazy program with all the cases for the V=3 case
# In addition, this is all for the case where d <= a <= 2d-1
##################################################################### 

X = sympy.symbols('X')
o = Fraction(1)

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
	for l in listsAddingTo(numIntervals, 3):
		index = tuple(l)
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

def findCutPoints(eVals, intervals, a, d, k):
	"""Finds values of X where below that value, some e variable must be 0.
	returns (list of constraints that always happen, cut list)
	cut list is ordered list of (Xcut, constraint)
	intervals is a list of [(min,max), (min,max)]
	where min and max are sympy expressions with X as a variable"""

	always = []
	cuts = []

	total = sympy.S(a+d+3*d*k)/(a+3*d*k)

	#Loop through each e variable, and find the minimum X that allows it to be nonzero.
	for index in eVals: 
		eVar = eVals[index]

		#minimum amount of muffin that can be found in given intervals from index
		minValue = sum(numInInterval * interval[0] for numInInterval, interval in zip(index, intervals))
		#maximum amount of muffin that can be found in given intervals from index
		maxValue = sum(numInInterval * interval[1] for numInInterval, interval in zip(index, intervals))

		#X values which will allow such a student to exist
		allowedXValues = sympy.solve([minValue <= total, total <= maxValue], X).as_set()

		#note 2a/5 below. Bill sent me this bound in an email. Is this actually where X should start?
		if allowedXValues == sympy.EmptySet() or allowedXValues.end <= 0:# 2*a/5:#if the constraint can never be met or is smaller than X can be
			always.append(eVar == 0)#add constraint that variable is zero
		else:#otherwise if the constraint can be met
			cuts.append((allowedXValues.end, eVar == 0))#add on (min val of X where constraint can't be met, constraint that variable is zero)
	cuts = sorted(cuts)
	return (always, cuts)
			
def findX(intervals, totals, a, d, k):
	"""intervals is a list of intervals [(min(X), max(X)), (min(X), max(X))],
	totals is a list of the same length which has all of the total amount of peices in the intervals"""
	prob = LpProblem("The problem", LpMinimize) #define pulp problem

	eVals = makeEVals(d, len(intervals))
	constraints = makeEasyConstraints(eVals, d, totals)
	for constraint in constraints:
		prob += constraint
	
	(always, cuts) = findCutPoints(eVals, intervals, a, d, k)

	for constraint in always: #NOTE FOR DEBUGGING LATER: ITS POSSIBLE THESE LINES WERE COMMENTED OUT LAST MEETING
		prob += constraint
	
	currentGuess = 0

	for cut in cuts:
		#print("Trying cut " + str(cut[0]))
		#print(prob)
		status = prob.solve()
		if status != 1:
			#print("No solution found, answer is previous try")
			prob += cut[1]
			return currentGuess
		else:
			#print("found solution, returning")
			prob += cut[1]
			currentGuess = cut[0]
			#return cut[0]

def doFirstCase(a,d,k):
	S = sympy.S
	a, d, k = S(a), S(d), S(k)
	
	#the total is m/s = 3dk + a + d/3dk + a 
	denom = 3*d*k + a #this comes up alot

	total = S(3*d*k + a + d) / denom #total muffin for one student

	values = [val / denom for val in [d*k + X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+(a+d)/2, d*k+a+d - 2*X]]
	print("values: " + str(values))
	print("bill values: " + str([val*(3*d*k+a) - d*k for val in values]))

	#The four intervals reffered to in the paper. Note that 0 indexing means e.g. interval 2 is Intervals[1]
	Intervals = [(values[0], values[1]), (values[1], values[2]), (values[4], values[5]), (values[5], values[6])]
	totals = [a+d, a+d, 2*d-a, 2*d-a]

	return findX(Intervals, totals, a, d, k)

def doSecondCase(a,d,k):
	#This is case where a <= 5d/7
	S = sympy.S
	a, d, k = S(a), S(d), S(k)

	#Add variable in interval sizes
	y = LpVariable('y', 0, 2*d + a, LpInteger)

	denom = 3*d*k+a
	values = [d*k+X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+2*a-2*X, d*k+3*X, d*k+(a+d)/2, d*k+a+d-3*X, d*k+a+d-3*X, d*k+d-a+2*X, d*k+a+d-2*X]
	vald = [val / denom for val in values]
	intervals = [(vald[0],vald[1]),(vald[1],vald[2]),(vald[4],vald[5]),(vald[6],vald[7]),(vald[7],vald[8]),(vald[10],vald[11])]
	totals = [a+d, a+d, y, 2*d-a-y, 2*d-a-y, y]

	return findX(intervals, totals, a, d, k)
	
def doSecondCase(a,d,k):
	#This is case where a <= 5d/7
	S = sympy.S
	a, d, k = S(a), S(d), S(k)

	#Add variable in interval sizes
	y = LpVariable('y', 0, 2*d + a, LpInteger)

	denom = 3*d*k+a
	values = [d*k+X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+2*a-2*X, d*k+3*X, d*k+(a+d)/2, d*k+a+d-3*X, d*k+a+d-3*X, d*k+d-a+2*X, d*k+a+d-2*X]
	vald = [val / denom for val in values]
	intervals = [(vald[0],vald[1]),(vald[1],vald[2]),(vald[4],vald[5]),(vald[6],vald[7]),(vald[7],vald[8]),(vald[10],vald[11])]
	totals = [a+d, a+d, y, 2*d-a-y, 2*d-a-y, y]

	return findX(intervals, totals, a, d, k)

def doThirdCase(a,d,k):
	
	S = sympy.S
	a, d, k = S(a), S(d), S(k)

	#Add variable in interval sizes
	y = LpVariable('y', 0, 2*d + a, LpInteger)

	denom = 3*d*k+a
	values = [d*k+X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+a+d-3*X, d*k+d-a+2*X, d*k+d-a+2*X, d*k+(a+d)/2, d*k+2*a-2*X, d*k+3*X, d*k+a+d-2*X]
	vald = [val / denom for val in values]
	intervals = [(vald[0],vald[1]),(vald[1],vald[2]),(vald[4],vald[5]),(vald[7],vald[8]),(vald[8],vald[9]),(vald[10],vald[11])]
	totals = [a+d, a+d, y, 2*d-a-y, 2*d-a-y, y]

	return findX(intervals, totals, a, d, k)
	

def solve(a,d,k):
	a = o*a
	d = o*d
	k = o*k
	X=0
	if 2*d+1 <= a <= 3*d:
		return o/3
	elif a <= 5*d/7:
		X = doSecondCase(a,d,k)
	elif a <= d:
		X = doThirdCase(a,d,k)
	else:
		X = doFirstCase(a,d,k)
	return (d*k + X)/(3*d*k+a)
		
def f(m,s):
	m,s=o*m,o*s
	d = m - s
	a = s % (3*d)
	k = (s - a)/(3*d)
	return solve(a,d,k)
