import math
import functools

from sympy import *
from pulp import *

def solve(m, minVal, maxVal):
	"""takes an augmented matrix (sympy matrix) and returns a solution or None if no solution"""
	rows = m.tolist()
	numVars = m.cols - 1
	variables = [LpVariable('x' + str(i), minVal, maxVal, LpInteger) for i in range(numVars)] #make variables x0, x1, x2, ...
	prob = LpProblem("The problem", LpMinimize) #define pulp problem
	for row in rows: #make one constraint for each row in matrix
		varVector = row[:-1] #get the part of the matrix that corresponds with variables
		value = row[-1] #gets constant on other side of equals sign
		dotProduct = [var * coeff for (var, coeff) in zip(variables, varVector)]# if coeff != 0] #list of coefficients * xi
		prob += functools.reduce(lambda a, b: a + b, dotProduct) == value #make equation and add to problem
	status = prob.solve() #solve it
	if status != 1:
		return None
	else:
		return [int(var.varValue) for var in variables] #return list of values of variables
