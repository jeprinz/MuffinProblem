import math
from sympy import *
from sympy.abc import x
from itertools import chain, combinations

def waysToAddTo(numbers, addTo):
	"""Input is numbers = list of numbers, addTo is number
	output is list of lists of numbers
	Each list in output sums to addTo"""
	def waysToAddToImpl(numbers, addTo, numsSoFar):
		for n in numbers:
			nextList = numsSoFar + [n]
			sumn = sum(nextList)
			if sumn == addTo:
				yield nextList
			elif sumn < addTo:
				lowerNumbers = [num for num in numbers if num <= n]
				yield from waysToAddToImpl(lowerNumbers, addTo, nextList)
			else:#sumn > addTo:
				yield from []#there has to be a better way to do this
				
			
	return waysToAddToImpl(numbers, addTo, [])
