from sympy import *
import findq
import interval


def mapunion(s,f):
	#print(s)
	ends = list(s.boundary)
	ends.reverse
	intervals = []
	middle = False
	if len(ends) % 2 != 0: #this means we have piece left over in middle
		middle = True
		if not s.contains(S(1)/2):
			raise Error("this should never happen.. something is wrong")
		ends.remove(S(1)/2)#this is only way this should ever happen...
	for i in range(0,len(ends),2):
		x,y = ends[i], ends[i+1]
		x,y = f(x,y)
		intervals.append(Interval(x,y))
	if middle:
		intervals.append(Interval(S(1)/2, S(1)/2))
	return Union(*intervals)

def flippy(s):
	return mapunion(s, lambda x,y: (-y+1,-x+1))

def flippyDippy(s):
	return Intersection(s, flippy(s))

def getIntervals(m,s,Q,V):
	m,s,Q = S(m),S(s),S(Q)
	f = m/s - (V-1)*Q
	g = m/s - V + 2 + Q*(V-2)
	#print((Q,f,g,1-Q))
	intervals = Union(Interval(Q,f), Interval(g,1-Q))
	flipped = Union(Interval(Q, 1-g),Interval(1-f, 1-Q))
	#return flippyDippy(intervals)
	return Intersection(intervals, flipped)

def doit(m,s):
	V = interval.findV(m,s)
	Q = findq.findQ(m,s, spew=False)
	(sV, sVm1) = interval.getShares(m,s,V)
	intervals = getIntervals(m,s,Q,V)
	#print (sV, sVm1, V)
	return intervals
	#if len(intervals.boundary) == 4: #two interval case
	#	print("Muffins in ranges " + str(intervals) + " with quantities " + str(sV * V) + ", " +str(sVm1 * (V-1)))
	#elif len(intervals.boundary) == 6 and sVm1*(V-1) - sV*V > 0: #three interval case
	#	print("Muffins in ranges " + str(intervals) + " with quantities " + str(sV*V) + ", " +str(sVm1*(V-1) - sV*V) + ", " + str(sV*V))
	#else:
	#	print("fuck off")
		

