from pulp import *
from functools import reduce
import sympy
import interval
from fractions import Fraction

#####################################################################
# This code runs the algorithm associated with the "Fun with Algorithms" submission.
##################################################################### 

#Some constants
X = sympy.symbols('X') #sympy variable X to be used in algebra
a, d, k = sympy.symbols('a d k') #also a, d, k variables
o = Fraction(1) #for convenience when I need a fraction value
S = sympy.S

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

def makeEasyConstraints(eVals, intervalTotals, aNum, dNum, kNum):

	sums = [0] * len(intervalTotals)
	total = 0
	for index in eVals:
		eVar = eVals[index]
		for i in range(len(sums)):
			sums[i] += index[i] * eVar
		total += eVar
	intervalConstraints = [sum == intervalTotal for (sum, intervalTotal) in zip(sums, intervalTotals)]
	return intervalConstraints + [total == 2*dNum] #there are 2d 3-students

def findCutPoints(eVals, intervals, aNum, dNum, kNum):
	"""Finds values of X where below that value, some e variable must be 0.
	returns (list of constraints that always happen, cut list)
	cut list is ordered list of (Xcut, constraint, expressionForXToBeGreaterThan)
	intervals is a list of [(min,max), (min,max)]
	where min and max are sympy expressions with X as a variable"""

	substitutions = {a: aNum, d: dNum, k: kNum}

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
		#allowedXValues = sympy.solve([minValue <= total, total <= maxValue], X).as_set()
		allowedXValues, wasMinAndNotMax = manualSolveALessBLessC(minValue.subs(substitutions), total.subs(substitutions), maxValue.subs(substitutions))
		XshouldBeGreaterThan = None
		if wasMinAndNotMax:
			XshouldBeGreaterThan = sympy.solve([minValue - total], X)
		else:
			XshouldBeGreaterThan = sympy.solve([maxValue - total], X)

		XshouldBeGreaterThan = getValFromDict(XshouldBeGreaterThan)

		#note 2a/5 below. Bill sent me this bound in an email. Is this actually where X should start?
		if allowedXValues == sympy.EmptySet() or allowedXValues.end <= 0:# 2*a/5:#if the constraint can never be met or is smaller than X can be
			always.append(eVar == 0)#add constraint that variable is zero
		else:#otherwise if the constraint can be met
			cuts.append((allowedXValues.end, eVar == 0, XshouldBeGreaterThan))#add on (min val of X where constraint can't be met, constraint that variable is zero)
	cuts = sorted(cuts, key=lambda cut: cut[0])
	return (always, cuts)

def manualSolveSystem(linear, total):
	"""linear should be A+B*X, total should be number
	returns set X values so that linear <= total"""
	coeffs = sympy.Poly(linear, X).all_coeffs()
	A,B = 0,0
	if len(coeffs) == 1:
		A = coeffs[0]
		B = 0
	else:
		B, A = coeffs
	
	if B > 0:
		return sympy.Interval(-sympy.oo, (total-A)/B)
	elif B < 0:
		return sympy.Interval((total-A)/B, sympy.oo)
	else:
		if A <= total:
			return sympy.Interval(-sympy.oo, sympy.oo)
		else:
			return sympy.EmptySet()

def manualSolveALessBLessC(A,B,C):
	"""B is number, A and C are linear functions of X
	returns set of allowed X so A <= B <= C"""
	int1 = manualSolveSystem(A,B)
	int2 = manualSolveSystem(-C,-B)
	intersection = sympy.Intersection(int1, int2)
	if int1 == intersection:
		return (intersection, True)
	elif int2 == intersection:
		return (intersection, False)
	else:
		raise "This should never happen"

def getValFromDict(x):
	if x == []:
		return None
	for v in x.values():
		return v

			
def findX(intervals, totals, aNum, dNum, kNum):
	"""intervals is a list of intervals [(min(X), max(X)), (min(X), max(X))],
	totals is a list of the same length which has all of the total amount of peices in the intervals"""
	prob = LpProblem("The problem", LpMinimize) #define pulp problem

	eVals = makeEVals(dNum, len(intervals))
	constraints = makeEasyConstraints(eVals, totals, aNum, dNum, kNum)
	for constraint in constraints:
		prob += constraint
	
	(always, cuts) = findCutPoints(eVals, intervals, aNum, dNum, kNum)

	for constraint in always:
		prob += constraint
	
	currentGuess = 0
	XCuts = []

	for cut in cuts:
		status = prob.solve()
		if status != 1:
			return (currentGuess, XCuts)
		else:
			prob += cut[1]
			XCuts.append(str(cut[2]))
			currentGuess = cut[0]

def doFirstCase(aNum,dNum,kNum):
	
	#the total is m/s = 3dk + a + d/3dk + a 
	denom = 3*d*k + a #this comes up alot

	total = S(3*d*k + a + d) / denom #total muffin for one student

	values = [val / denom for val in [d*k + X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+(a+d)/2, d*k+a+d - 2*X]]

	#The four intervals reffered to in the paper. Note that 0 indexing means e.g. interval 2 is Intervals[1]
	Intervals = [(values[0], values[1]), (values[1], values[2]), (values[4], values[5]), (values[5], values[6])]
	totals = [aNum+dNum, aNum+dNum, 2*dNum-aNum, 2*dNum-aNum]

	return findX(Intervals, totals, aNum, dNum, kNum)

def doSecondCase(aNum,dNum,kNum):
	#This is case where a <= 5d/7

	#Add variable in interval sizes
	y = LpVariable('y_pulp_var', 0, 2*dNum + aNum, LpInteger)

	denom = 3*d*k+a
	values = [d*k+X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+2*a-2*X, d*k+3*X, d*k+(a+d)/2, d*k+a+d-3*X, d*k+a+d-3*X, d*k+d-a+2*X, d*k+a+d-2*X]
	vald = [val / denom for val in values]
	intervals = [(vald[0],vald[1]),(vald[1],vald[2]),(vald[4],vald[5]),(vald[6],vald[7]),(vald[7],vald[8]),(vald[10],vald[11])]
	totals = [aNum+dNum, aNum+dNum, y, 2*dNum-aNum-y, 2*dNum-aNum-y, y]

	return findX(intervals, totals, aNum, dNum, kNum)

def doThirdCase(aNum,dNum,kNum):

	y = LpVariable('y_pulp_var', 0, 2*dNum + aNum, LpInteger)

	denom = 3*d*k+a
	values = [d*k+X, d*k+a/2, d*k+a-X, d*k+2*X, d*k+2*X, d*k+a+d-3*X, d*k+d-a+2*X, d*k+d-a+2*X, d*k+(a+d)/2, d*k+2*a-2*X, d*k+3*X, d*k+a+d-2*X]
	vald = [val / denom for val in values]
	intervals = [(vald[0],vald[1]),(vald[1],vald[2]),(vald[4],vald[5]),(vald[7],vald[8]),(vald[8],vald[9]),(vald[10],vald[11])]
	totals = [aNum+dNum, aNum+dNum, y, 2*dNum-aNum-y, 2*dNum-aNum-y, y]

	return findX(intervals, totals, aNum, dNum, kNum)
	

def solve(a,d,k):
	a = o*a
	d = o*d
	k = o*k
	X=0
	if 2*d+1 <= a <= 3*d:
		return o/3
	elif a <= 5*d/7:
		X,cuts = doSecondCase(a,d,k)
	elif a <= d:
		X,cuts = doThirdCase(a,d,k)
	elif d <= a <= 2*d-1:
		X,cuts = doFirstCase(a,d,k)
	elif d == 1 and a == 2:
		return o/3 + o/3/(a+3*d*k)
	else:
		print("Did not meet any case for a,d,k = %d,%d,%d" % (a,d,k))
		return o/(a + 3*d*k)
	for cut in cuts:
		print("X > " + cut)
	return (d*k + X)/(3*d*k+a)
		
def f(m,s):
	m,s=o*m,o*s
	d = m - s
	a = s % (3*d)
	if a == 0:
		a += 3*d
	k = (s - a)/(3*d)
	return solve(a,d,k)
