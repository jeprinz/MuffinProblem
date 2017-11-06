from fractions import Fraction
import math
import itertools
import numbers
import interval
import operator

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
	def __add__(self, other):
		if isinstance(other, numbers.Number):
			other = Value(0, Fraction(other))
		(oa, ob) = other
		return Value(self.a + oa, self.b + ob)
	def __radd__(self, other):
		return self+other
	def __mul__(self, other):
		return Value(self.a * other, self.b * other)
	def __rmul__(self, other):
		return self*other

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
	def __add__(self, other):
		return Interval(self.a+other, self.b+other)
	def __radd__(self, other):
		return self+other
	def __mul__(self, other):
		a = self.a*other
		b = self.b*other
		if other < 0:
			a, b = b, a
		return Interval(a, b)
	def __rmul__(self, other):
		return self*other



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
		if A.eval(Qs)  == C.eval(Qs) and c1 > a1:#was a2 instead of a1, i think that was a bug
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

def union2(int1, int2, relation):#TODO: add relation as named argument so it calls howIntersect if not supplied, or make another function w/2 argunemts that does that
	#relation from howIntersect
	(case, swapped, Qmin) = relation
	if swapped:
		int1, int2 = int2, int1
	A, B = int1
	C, D = int2
	intervals = None
	if case == 1:
		intervals = [int1, int2]
	elif case == 2:
		intervals = [Interval(A, D)]
	elif case == 3:
		intervals = [int1]
	return (intervals, Qmin)

def intersect2(int1, int2, relation):
	#relation from howIntersect
	(case, swapped, Qmin) = relation
	if swapped:
		int1, int2 = int2, int1
	A, B = int1
	C, D = int2
	intervals = None
	if case == 1:
		intervals = []
	elif case == 2:
		intervals = [Interval(C, B)]
	elif case == 3:
		intervals = [int2]
	return (intervals, Qmin)
			

def union(ints, Qs):
	anyIntersections = True
	Qmin = 0
	while anyIntersections == True:
		anyIntersections = False
		for (int1, int2) in itertools.combinations(ints, 2):
			if int1 in ints and int2 in ints:
				relation = howIntersect(int1, int2, Qs)
				(case, swapped, newQmin) = relation
				if newQmin > Qmin: Qmin = newQmin#set Qmin to highest value
				if case != 1:# if they intersect
					anyIntersections = True
				(interval, Qmin) = union2(int1, int2, relation)
				ints.remove(int1)
				ints.remove(int2)
				ints += interval
	return (ints, Qmin)
#can do mergesort for union

def intersection(seta, setb, Qs):
	ints = []
	Qmin = 0
	combinations =  [(a, b) for a in seta for b in setb]
	for (int1, int2) in combinations:
		relation = howIntersect(int1, int2, Qs)
		(interval, newQmin) = intersect2(int1, int2, relation)
		if newQmin > Qmin: Qmin = newQmin#set Qmin to highest value
		ints += interval
	(result, newQmin) = union(ints, Qs)
	return (result, max(Qmin, newQmin))


def unionMergeFancy(ints, Qs):
	"""returns (intervals, Qmin)"""
	if len(ints) <= 1:
		return (ints, Qs)
	left = ints[:len(ints)/2]
	right = ints[len(ints)/2:]
	(unLeft, Qminl) = union(left, Qs)
	(unright, Qminr) = union(right, Qs)
	
def sum_to_n(r, n):#sum_to_n(total, number of bins)
	if type(r) == Fraction and r.denominator == 1:
		r = int(r)
	if type(n) == Fraction and n.denominator == 1:
		n = int(n)
	size = n + r - 1
	for indices in itertools.combinations(range(size), n-1):
		starts = [0] + [index+1 for index in indices]
		stops = indices + (size,)
		yield tuple(map(operator.sub, stops, starts))

def whereAverage(ints, N, Qs):
	if len(ints) == 0:
		return (ints, 0) #Qmin is 0 because there is no minimum
	leftVals = [inter[0] for inter in ints]
	rightVals = [inter[1] for inter in ints]
	results = []
	for partition in sum_to_n(N, len(ints)):
		left = sum(a*b for (a,b) in zip(partition, leftVals)) * Fraction(1,N)
		right = sum(a*b for (a,b) in zip(partition, rightVals)) * Fraction(1,N)
		results.append(Interval(left, right))
	return union(results, Qs)

def constrainToSumT(ints, num, T, Qs):
	(R, Qmin1) = whereAverage(ints, num-1, Qs)
	Rprime = [T + -1*interval*(num - 1) for interval in R]
	(results, Qmin2) = intersection(Rprime, ints, Qs)
	return (results, max(Qmin1, Qmin2))

def constrain(m,s, Qs):
	m, s = Fraction(m), Fraction(s)
	V = interval.findV(m,s)
	sV, sVm1 = interval.getShares(m,s,V)

	Q = Value(1,0)
	M = [Interval(Q, 1 + -1*Q)]
	A = [Interval(Q, 1 + -1*Q)]
	B = [Interval(Q, 1 + -1*Q)]

	Qmin = 0#Qs

	while True:
		oldA, oldB, oldM = A, B, M
		#print("M, A, B:")
		#printIntervals(M, Qs)
		#printIntervals(A, Qs)
		#printIntervals(B, Qs)
		#print('A types:')
		#print([type(interval) for interval in A])
		#print('constrains')
		(M, Qminm) = constrainToSumT(M, 2, 1, Qs)
		(A, Qmina) = constrainToSumT(A, V - 1, m/s, Qs)
		(B, Qminb) = constrainToSumT(B, V, m/s, Qs)
		#print("M, A, B:")
		#printIntervals(M, Qs)
		#printIntervals(A, Qs)
		#printIntervals(B, Qs)
		#print('A types:')
		#print([type(interval) for interval in A])
		#print('intersections')
		Qmin = max(Qmin, Qmina, Qminb, Qminm)
		(A, Qmina) = intersection(A, M, Qs)
		(B, Qminb) = intersection(B, M, Qs)
		(M, Qminm) = union(A + B, Qs)
		Qmin = max(Qmin, Qmina, Qminb, Qminm)
		if oldA == A and oldB == B and oldM == M:
			break
	return M, Qmin

def contradictions(vShares, vm1Shares, T, V, Qs):#return (boolean is there contradiction, QMin)
	ints = union(vShares + vm1Shares, Qs)[0]#don't care about QMin

	#sort intervals
	print(ints)
	ints = sorted(ints, key=lambda i: i[0].eval(Qs))

	L = ints[0][0].eval(Qs)#left side of 0th interval
	R = ints[-1][1].eval(Qs)#right side of last interval


	# we now need v and v-1 shares that don't intersect
	overlap = len(vm1Shares) + len(vShares) - len(ints)
	numBijection = (len(ints) - overlap) // 2

	for i in range(numBijection):# for each pair of intervals
		vInteral = vShares[i]
		vm1Interval = vm1Shares[i]
		a1, b1 = vInteral
		a2, b2 = vm1Interval

		left1 = (T - V*R.eval(Qs))/(a2.eval(Qs) - R.eval(Qs))
		right1 = (T - L.eval(Qs)*V)/(a1.eval(Qs) - L.eval(Qs))

		left2 = (T - (V-1)*R.eval(Qs)) / (b2.eval(Qs) - R.eval(Qs))
		right2 = (T - L.eval(Qs)*(V-1)) / (b1.eval(Qs) - L.eval(Qs))

		contradict = right1 < left2 or right2 < left1


def printIntervals(ints, Qs):
	numbs = [(vala.eval(Qs), valb.eval(Qs)) for (vala, valb) in ints]
	print(numbs)

def test():
	one = Fraction(1)
	int1= Interval(Value(2,-Fraction(1,4)), Value(2,Fraction(1,5)))
	int2= Interval(Value(Fraction(1,3),-Fraction(3,4)), Value(1,Fraction(1,5)))
	int3= Interval(Value(1,-Fraction(1,5)), Value(-1,Fraction(1,1)))
	#print(int1)
	#print(int2)
	#print(int3)
	#relation = howIntersect(int1, int2, Fraction(1,2))
	#print("relation: " + str(relation))
	#print("union1 2: " + str(union2(int1, int2, relation)))
	#relation = howIntersect(int1, int3, Fraction(1,2))
	#print("union1 3: " + str(union2(int1, int3, relation)))
	#print("union all: " + str(union([int1, int2, int3], Fraction(7,15))))
	#print("intersect all: " + str(intersection([int1], [int2], Fraction(1,2))))
	(unionall, Qmin) = union([int1, int2, int3], Fraction(7,15))
	simple = Interval(Value(one, -one/2), Value(one, one/2))
	print("constrained: " + str(constrainToSumT([simple], 2, 3*one/2, Fraction(1,2))))

