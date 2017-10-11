import math
from sympy import *
from sympy.abc import x
from itertools import chain, combinations

#from stackoverflow
def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def possibPoly(numbers, total):
	polies = [Poly(1+x**n) for n in numbers]
	return prod(polies)**total

def possibilities(numbers, addTo):
	valid = []
	for subset in powerset(numbers):
		if len(subset) == 0:
			continue
		total = math.floor(addTo / min(subset))
		poly = possibPoly(subset, total)
		coeffs = poly.all_coeffs()
		if len(coeffs) >= addTo and poly.all_coeffs()[addTo] != 0:
			valid.append(subset)
	return valid
		

	
def poss2(numbers, addTo):
	
