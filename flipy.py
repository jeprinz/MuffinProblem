import math
from fractions import Fraction

#Well everything but intersections works properly

#a Set is an interface that requires "hasPoint" and "hasOpen" method

class Open:
	"""Represents an open interval of the rational line"""
	def __init__(self, a, b):
		self.a = Fraction(a)
		self.b = Fraction(b)
	def low(self):
		return self.a
	def high(self):
		return self.b
	def hasPoint(self, x):
		return x > self.a and x < self.b
	def hasOpen(self, op):
		return op.low() >= self.a and op.high() <= self.b
	def __str__(self):
		return "(%s,%s)" % (str(self.a), str(self.b))
	__repr__ = __str__

class Set:
	"""Represents a set of rational numbers"""
	def __init__(self, union, intersection):
		self.open = []
		for s in union:
			if type(s) == Open:
				self._appendOpen(s)
			elif type(s) == Set:
				for op in s.open:
					self._appendOpen(op)
		for s in intersection:
			if type(s) == Open:
				self.open = self._intersectOpen(s)
			elif type(s) == Set:
				subIntersects = [self._intersectOpen(op) for op in s.open]
				self.open = Set(subIntersects, []).open#kill me

	def _appendOpen(self, op):
		if self.hasOpen(op):
			return
		lower = self._whoHasPoint(op.low())
		upper = self._whoHasPoint(op.high())
		if lower != None and upper != None:
			self.open.append(Open(lower.low(), upper.high()))
			self.open.remove(lower)
			self.open.remove(upper)
		elif lower != None:
			self.open.append(Open(lower.low(), op.high()))
			self.open.remove(lower)
		elif upper != None:
			self.open.append(Open(op.low(), upper.high()))
			self.open.remove(upper)
		else:
			self.open = [x for x in self.open if not op.hasOpen(x)]
			self.open.append(op)
	def _intersectOpen(self, op):#now no side effects
		contains = [x for x in self.open if op.hasOpen(x)]
		lower = self._whoHasPoint(op.low())
		upper = self._whoHasPoint(op.high())
		if lower != None:
			contains.append(Open(op.low(), lower.high()))
		if upper != None and lower != upper:
			contains.append(Open(upper.low(), op.high()))
		return contains
	def _whoHasPoint(self, x):
		for op in self.open:
			if op.hasPoint(x):
				return op
		return None
	def hasPoint(self, x):
		for op in self.open:
			if op.hasPoint(x):
				return True
		return False
	def hasOpen(self, x):
		for op in self.open:
			if op.hasOpen(x):
				return True
		return False
	def map(self, f):
		new = [f(x) for x in self.open]
		return Set(new,[])
	def getUnions(self):
		self._sort()
		return self.open.copy()
	def _sort(self):
		self.open.sort(key = lambda op: op.low())
	def getIntervals(self):
		self._sort()
		return [(op.low(), op.high()) for op in self.open]
	def __str__(self):
		self._sort()
		if len(self.open) == 0:
			return "{}"
		else:
			return " U ".join([str(op) for op in self.open])
	__repr__ = __str__

def union(things):
	return Set(things, [])
def intersection(things):
	return Set([things[0]],things[1:])

CENTER = Fraction(1,2)
		
def flipOpen(op):
	return Open(-op.high() + 2*CENTER, -op.low() + 2*CENTER)

def flippy(s):
	return s.map(flipOpen)

def flippyDippy(s):
	return intersection([s, flippy(s)])
