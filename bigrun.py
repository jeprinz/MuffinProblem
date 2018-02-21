from sympy import *
import integers
import symflip
import math
from symflip import lcm
import findq
import V3program
from fractions import Fraction

#this file contains a bunch of functions to generate procedures for the muffin problem.
#This file is the interface that I use to generate procedures.
#For example, to make procedures for f(m,s), run getProcedures(m,s), or optionally getProcedures(m,s,Q=Fraction(,))

o = Fraction(1)


def floorciel(m,s):
	m = S(m)
	s = S(s)
	arg1 = m/(s*ceiling(2*m/s))
	arg2 = 1 - m/(s*floor(2*m/s))
	return max(S(1)/3, min(arg1, arg2))

def getPiecesDenom(m,s):#returns (piece size list, denominator)
	fc = floorciel(m,s)
	intv = 1


	intervals = symflip.doit(m,s)
	if not intervals == EmptySet():
		points = list(intervals.boundary)
		intv = points[0]
		if intv < fc:
			return intervalToPieces(m,s,intervals)


	#try:
	#	intervals = symflip.doit(m,s)
	#	if not intervals == EmptySet():
	#		points = list(intervals.boundary)
	#		intv = points[0]
	#		if intv < fc:
	#			return intervalToPieces(m,s,intervals)
	#except Exception as e:
	#	print('exception is:')
	#	print(e)
	#	pass
	
	#or, if floor cieling:
	intervals = symflip.getIntervals(m,s,fc, ceiling(2*m/s))
	return intervalToPieces(m,s,intervals)

def intervalToPieces(m,s,intervals):#returns (pieces size list, denominator)
	points = list(intervals.boundary)
	d = lcm([fraction(f)[1] for f in points] + [s]) #denominator that we are going to use is lcm
	lowest, highest = int(points[0] * d), int(points[-1]*d + 1) #smallest and biggest pieces, working in units of 1/d
	pieces = [n for n in range(lowest, highest) if intervals.contains(S(n)/d)] #get all pieces
	return (pieces, d)
	
def procedures(m,s):
	pieces, d = getPiecesDenom(m,s)
	return integers.solve(m,s,d=d, pieces=pieces, intervals=Interval(0,1))

def getRow(m,s):
	pieces, d = getPiecesDenom(m,s)
	#numProc = len(list(procedures(m,s)))
	hasElem = any(True for _ in procedures(m,s))
	return (m, s, d, pieces, hasElem)

def bigrun(maxM, maxS):
	for m in range(1, maxM+1):
		for s in range(1, maxS+1):#7, maxS+1):
			if m > s+1:
				if math.gcd(m,s) == 1:
					yield getRow(m,s)

def biggrid(maxM, maxS):
	lines = []
	for m in range(1, maxM+1):
		values = []
		for s in range(1, maxS+1):
			if m > s:
				#(m,s,d,pieces,hasElem) = getRow(m,s)
				#pieces, d = getPiecesDenom(m,s)
				#bound = pieces[0]/d
				#if hasElem:
				inter=1
				try:
					inter = findq.findQ(m,s,spew=False)
				except:
					pass
				fc = floorciel(m,s)
				bound = min(inter,fc)
				if bound == S(1)/3:
					values.append(str(bound))
				else: values.append(str(0))
			else:
				values.append(str(0))
		lines.append(";".join(values))
	text = "\n".join(lines)
	text_file = open("girdy3.csv", "w")
	text_file.write(text)
	text_file.close()

def graphMOverS(maxM, maxS):
	lines = []
	for m in range(1, maxM+1):
		values = []
		for s in range(1, maxS+1):
			if m > s:
				(m,s,d,pieces,hasElem) = getRow(m,s)
				pieces, d = getPiecesDenom(m,s)
				bound = float(pieces[0])/float(d)
				mOverS = float(m)/float(s)
				if hasElem:
					lines.append(str(mOverS) + ", " + str(bound))
	text = "\n".join(lines)
	text_file = open("plot.csv", "w")
	text_file.write(text)
	text_file.close()

def graphMOverSFunky(maxM, maxS):
	lines = []
	for m in range(1, maxM+1):
		values = []
		for s in range(1, maxS+1):
			if m > s:
				(m,s,d,pieces,hasElem) = getRow(m,s)
				pieces, d = getPiecesDenom(m,s)
				bound = float(pieces[0])/float(d)
				mOverS = float(m)/float(s)
				if hasElem:
					lines.append(str(mOverS) + ", " + str(bound*(s/m)**0.5))
	text = "\n".join(lines)
	text_file = open("funky-plot.csv", "w")
	text_file.write(text)
	text_file.close()

def resultsToStr(results):
	lines = []
	for result in results:
		(m,s,d,pieces,hasElem) = result
		pieceStr = ','.join([str(piece) for piece in pieces])
		line = "%d, %d, %d, [%s], %s"%(m,s,d,pieceStr,str(hasElem))
		lines.append(line)
	return '\n'.join(lines)

def resultsToFile(results, filename):
	text_file = open(filename, "w")
	text_file.write(resultsToStr(results))
	text_file.close()

def stupidStr(results):
	lines = []
	for result in results:
		(m,s,d,pieces,hasElem) = result
		size = float(pieces[0] / d)
		if not hasElem:
			line = "%d, %d, %s"%(m,s,str(size))
			lines.append(line)
	return '\n'.join(lines)

def procedureToString(procedure):
	lines = []
	muffins, students = procedure
	lines.append("Muffins:")
	for muffin in muffins:
		count, pieces = muffin
		lines.append(str(count) + " x " + str(pieces))
	lines.append("Students:")
	for student in students:
		count, pieces = student
		lines.append(str(count) + " x " + str(pieces))
	return '\n'.join(lines)
	

def getProcedures(m,s,Q=None):
	pieces, d = None, None
	if Q == None:
		pieces, d = getPiecesDenom(m,s)
	else:
		#d = Q.denominator
		#numer = Q.numerator
		d = lcm(Q.denominator,s)
		numer = Q.numerator * d / Q.denominator
		lowest, highest = numer, d - numer #smallest and biggest pieces, working in units of 1/d
		pieces = [n for n in range(lowest, highest+1)] #get all pieces
	procedures = list(integers.solve(m,s,d=d, pieces=pieces, intervals=Interval(0,1)))
	print("denominator: " + str(d))
	for procedure in procedures:
		print(procedureToString(procedure))
	if len(procedures) == 0:
		print('No procedures found')
	
	
def testUpperBounds(ms, ss, Qs):
	"""ms is a list of ms values, ss is a list of s values, Qs is a list of Q values.
	Will check if can find lower bound for each Q value, and output list of booleans, where each boolean
	corresponds to whether a bound was found for that particular case"""
	results = []
	for (m,s,Q) in zip(ms,ss,Qs):
		interval = Interval(Q, 1-Q)
		pieces, d = intervalToPieces(m,s,interval)
		procedures = integers.solve(m,s,d=d, pieces=pieces, intervals=Interval(0,1))
		if next(procedures, False):
			results.append(True)
		else:
			results.append(False)
	return results

def testConjecture(iToM, iToS, iToQ, maxI):
	"""Tests a conjecture of the form f(iToM(i), iToS(i)) >= iToQ(i)
	for each i from 0 to maxI"""
	ms = [iToM(i) for i in range(0, maxI+1)]
	ss = [iToS(i) for i in range(0, maxI+1)]
	Qs = [iToQ(i) for i in range(0, maxI+1)]
	return testUpperBounds(ms, ss, Qs)

def testV3Program(maxA, maxD, maxK):
	for a in range(1, maxA+1):
		for d in range(1, maxD+1):
			if math.gcd(a,d) == 1 and (a+d)%a != 0:
				X = V3program.solve(a,d,0)
				#print("Testing a,d = %d,%d"%(a,d))
				for k in range(0, maxK+1):
					#res = testUpperBounds([a+d+3*d*k], [a+3*d*k], [(o*d*k + X)/(3*d*k+a)])[0]
					res = testUpperBounds([a+d+3*d*k], [a+3*d*k], [X])[0]
					if not res:
						print("Failed on a,d=%d,%d with X = %s"%(a,d,str(X)))
					else:
						print("f(%d, %d) = %s"%(a+d+3*d*k, a+3*d*k, str((X))))
						pass
	print("Done")
					

