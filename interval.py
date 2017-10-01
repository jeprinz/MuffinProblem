import math
from fractions import Fraction

#This is an implementation of the interval theorem from https://arxiv.org/pdf/1709.02452.pdf

def findV(m,s):
	"""This function returns the variable V that is reffered to in the paper.  The value for V used here
	is simply a guess, not the only possible. However, it is the correct guess in many cases."""
	return Fraction(math.ceil(2*m/s))

def getShares(m,s,V):
	"""Returns the number of V students and V-1 students in a tuple (# V, # V-1)"""
	#(A, B) is (number of V students, number of V-1 students)
	#total shares is 2*m, need to find A*V + B*(V-1) = 2*m and A + B = s
	#If you work out the math, that means that A = 2m-Vs+s and B = s-A
	sV = 2*m - V*s + s
	sVm1 = s - sV
	return (sV, sVm1)
	

