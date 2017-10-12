import math
import functools
import constraint

from sympy import *
from sympy.abc import x

import symflip

def waysToAddTo(numbers, addTo):
	"""Input is numbers = list of numbers, addTo is number
	output is list of lists of numbers
	Each list in output sums to addTo"""
	def waysToAddToImpl(numbers, addTo, numsSoFar):
		for n in numbers:#try adding each number
			nextList = numsSoFar + [n]
			sumn = sum(nextList)
			if sumn == addTo:
				yield nextList
			elif sumn < addTo:
				lowerNumbers = [num for num in numbers if num <= n]#wlog, pieces decrease in size from first to last
				yield from waysToAddToImpl(lowerNumbers, addTo, nextList)
			else:#sumn > addTo:
				yield from []#there has to be a better way to do this
				
	return waysToAddToImpl(numbers, addTo, [])


def solve(m,s):
	"""Creates matrix system that represents any possible solution of f(m,s) given denom d and assumption Q"""
	#calculate some initial things we need
	intervals = symflip.doit(m,s)
	points = list(intervals.boundary)
	Q = points[0] #bound predicted by interval theorem
	d = lcm([fraction(f)[1] for f in points]) #denominator that we are going to use is lcm of denominators on ends of intervals

	lowest, highest = int(points[0] * d), int(points[-1]*d + 1) #smallest and biggest pieces, working in units of 1/d
	pieces = [n for n in range(lowest, highest) if intervals.contains(S(n)/d)] #get all pieces
	muffins = list(waysToAddTo(pieces, d)) #all possible muffins
	students = list(waysToAddTo(pieces, m*d//s)) #all possible students
	# now create matrix
	M = [] #each sublist is a row, each row is a piece size (except last two, to come later)
	for p in pieces:#create row for each peice
		M.append([])
	for student in students:#for each possible student, add how many of each piece it has to its column (one column per student)
		for i in range(len(pieces)):
			rowForPiece = M[i]
			howMany = student.count(pieces[i])#how many of this piece does this student have
			rowForPiece.append(howMany) #add to the row
	for muffin in muffins:#for each possible muffin, add how many of each piece it has to its column (one column per muffin)
		for i in range(len(pieces)):
			rowForPiece = M[i]
			howMany = muffin.count(pieces[i])#how many of this piece does this muffin have
			rowForPiece.append(-howMany) #add to the row, negative this time so that total adds to zero

	#now add zeros on end of each row, as this is an equation with the right size of "=" being 0
	for row in M:
		row.append(0)
	
	#not create two rows, one for total muffins, other for total students
	#remember, left half of matrix is students, right half is muffins
	M.append([1] * len(students) + [0] * len(muffins) + [s])#muffin total adds to m
	M.append([0] * len(students) + [1] * len(muffins) + [m])#student total adds to s

	print("matrix before rref")
	print(M)

	print("num muffs: " + str(len(muffins)))
	print("num studs: " + str(len(students)))

	augmented = Matrix(M).rref()[0]
	print("Matrix:")
	print(augmented)

	(mat, b) = deAugment(augmented)

	res = constraintSolveMat(m,s,mat,b)
	res = [res['x'+str(i)] for i in range(len(res))]
	print("res:" + str(res))

	print("Muffins:")
	index = 0
	for student in students:
		print(str(res[index]) + " student gets" + str(student))
		index += 1
	for muffin in muffins:
		print(str(res[index]) + " muffin split into " + str(muffin))
		index += 1
		


def deAugment(aug):
	mat = aug.copy()
	b = aug.copy()
	mat.col_del(-1)
	for i in range(mat.cols):
		b.col_del(0)
	print(mat)
	print(b)
	return (mat,b)

def constraintSolveMat(m, s, mat, b):
	cols = mat.cols
	varlist = ['x' + str(i) for i in range(cols)]

	problem = constraint.Problem()
	for var in varlist:
			problem.addVariable(var, list(range(m + 1)))#for now, can be better TODO
	for (row, bVal) in zip(mat.tolist(), list(b)):
		nonzero = [i for i in range(len(row)) if row[i] != 0] #indices where the row is not zero
		vars = [varlist[i] for i in nonzero]

		test = makeTest(row, bVal, nonzero)
				
		problem.addConstraint(test, vars)
	
	return problem.getSolution()

def makeTest(row, bVal, nonzero):
	def test(*args):
		total = 0
		var = 0
		for i in nonzero:
			total += args[var] * row[i]
			var += 1
		return total == bVal
	return test
	
	


def posIntSolve(numbers, addTo):
	"""Find set of vectors of nonnegative integers that can be dot producted with numbers list to get addTo"""
	def posIntSolveImpl(numbers, addTo, numsSoFar):
		#numbers is [(number, info)] where info is anything you want
		for value in numbers:#try adding each number
			(n, info) = value
			nextList = numsSoFar + [value]
			sumn = sum([n for (n,info) in nextList])
			if sumn == addTo:
				yield nextList
			elif sumn < addTo:
				lowerNumbers = [(num, i) for (num, i) in numbers if num <= n]#wlog, pieces decrease in size from first to last
				yield from posIntSolveImpl(lowerNumbers, addTo, nextList)
			else:#sumn > addTo:
				yield from []#there has to be a better way to do this
	values = [(numbers[i], i) for i in range(len(numbers)) if numbers[i] != 0]
	results = posIntSolveImpl(values, addTo, [])
	indices = [[info for (n, info) in possibility] for possibility in results] #this is a list of lists of indices of numbers used
	return [[possibility.count(n) for n in range(len(numbers))] for possibility in indices]

		

def lcm(args):
	def lcm2(a, b):
		return a * b // math.gcd(a, b)
	return functools.reduce(lcm2, args)
