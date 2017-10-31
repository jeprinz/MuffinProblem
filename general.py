from fractions import Fraction
import math
import itertools

#an interval is represented by (a,b) a tuple of Fractions

class Value(tuple):
	"""Represents 1st degree polynomial AQ + B"""
	def __new__ (self, a, b):
		return super(Value, self).__new__(self, tuple([a, b]))

	def __init__(self, a, b):
		self.a=Fraction(a)
		self.b=Fraction(b)
	def __repr__(self):
		return str(self)
	def __str__(self):
		return "%sQ + %s" % (str(self.a), str(self.b))
	def eval(self, Q):
		return self.a * Q + self.b

class Interval(tuple):
	"""Represents an interval"""
	def __new__ (self, a, b):
		return super(Interval, self).__new__(self, tuple([a, b]))

	def __init__(self, a, b):
		self.a=a
		self.b=b
	def __repr__(self):
		return str(self)
	def __str__(self):
		return "(%s, %s)" % (str(self.a), str(self.b))


def minQ(valA, valB, Qs):
	(a1, b1) = valA
	(a2, b2) = valB
	if a2 <= a1:
		return 0
	else:
		return (b1 - b2) / (a2 - a1)

def howIntersect(int1, int2, Qs, swap=False):
	"""tells in what case intervals intersect, and if swapped (case, swapped, Qmin)"""
	(A, B) = int1
	(C, D) = int2
	(a1, a2) = A
	(c1, c2) = C
	if not A == C:
		if A.eval(Qs)  == C.eval(Qs) and c1 > a2:
			return howIntersect(int2, int1, Qs, True)
		elif not A.eval(Qs) <= C.eval(Qs):
			return howIntersect(int2, int1, Qs, True)

	if B.eval(Qs) < C.eval(Qs):
		return (1, swap, minQ(B, C, Qs))
	elif A.eval(Qs) <= C.eval(Qs) and B.eval(Qs) <= D.eval(Qs):
		Qmin = max(minQ(A, C, Qs), minQ(B, D, Qs), minQ(C, B, Qs))
		return (2, swap, Qmin)
	elif A.eval(Qs) <= C.eval(Qs) and D.eval(Qs) <= B.eval(Qs):
		Qmin = max(minQ(A, C, Qs), minQ(D, B, Qs))
		return (3, swap, Qmin)
	else:
		raise Exception("this should never happen")

def union2(int1, int2, intersection):
	#intersection from howIntersect
	(case, swapped, Qmin) = intersection
	A, B = int1
	C, D = int2
	if swapped:
		int1, int2 = int2, int1
	intervals = None
	if case == 1:
		intervals = [int1, int2]
	elif case == 2:
		intervals = [(A, D)]
	elif case == 3:
		intervals = [int1]
	return (intervals, Qmin)

def intersect2(int1, int2, intersection):
	#intersection from howIntersect
	(case, swapped, Qmin) = intersection
	A, B = int1
	C, D = int2
	if swapped:
		int1, int2 = int2, int1
	intervals = None
	if case == 1:
		intervals = []
	elif case == 2:
		intervals = [(C, B)]
	elif case == 3:
		intervals = [int2]
	return (intervals, Qmin)
			

def union(ints, Qs):
	anyIntersections = True
	Qmin = 0
	while anyIntersections == True:
		anyIntersections = False
		Qmin = 0
		intervals = []
		print(ints)
		for (int1, int2) in itertools.combinations(ints, 2):
			intersection = howIntersect(int1, int2, Qs)
			(case, swapped, newQmin) = intersection
			print('case is' + str(case))
			if newQmin > Qmin: Qmin = newQmin#set Qmin to highest value
			if case != 1:# if they intersect
				anyIntersections = True
			(interval, Qmin) = union2(int1, int2, intersection)
			intervals += interval
		ints = intervals
	return (ints, Qmin)
#can do mergesort for union

def unionMergeFancy(ints, Qs):
	"""returns (intervals, Qmin)"""
	if len(ints) <= 1:
		return (ints, Qs)
	left = ints[:len(ints)/2]
	right = ints[len(ints)/2:]
	(unLeft, Qminl) = union(left, Qs)
	(unright, Qminr) = union(right, Qs)
	

def test():
	int1= Interval(Value(1,-Fraction(1,4)), Value(2,Fraction(1,5)))
	int2= Interval(Value(Fraction(1,3),-Fraction(3,4)), Value(1,Fraction(1,5)))
	int3= Interval(Value(1,-Fraction(1,5)), Value(-1,Fraction(1,5)))
	print(int1)
	print(int2)
	print(int3)
	intersection = howIntersect(int1, int2, Fraction(1,2))
	print("intersection: " + str(intersection))
	print("union2: " + str(union2(int1, int2, intersection)))

	print("union2: " + str(union2(int1, int3, intersection)))
	print(union([int1, int2, int3], Fraction(7,15)))
