from fractions import Fraction
import interval
import math

#Note that data is passed around in this form: (m,s,V,sV, sVm1)
#where m, s is muffins,students. V is variable from paper, sV is sV from paper, and sVm1 is sV-1 from paper

#Calculations for STATEMENT ONE
def findABCD1(dat):
	(m,s,V,sV, sVm1) = dat
	ceil = math.ceil(V*sV/sVm1)
	floor = math.floor((V*sV)/sVm1)
	A = floor + (V - 1 - floor)*(V - m/s - 1) - m/s
	B = floor + (V-2)*(V - 1 - floor)
	C = m/s - (V-1-ceil)*(m/s-V+2) - ceil*(1-m/s)
	D = ceil*(V-1) + (V-1-ceil)*(V-2)
	return (A,B,C,D)
	

def findMIN(A,B,C,D):
	if A <= 0 and B == 0:
		return 0
	if A > 0 and B == 0 and D > 0:
		return C/D
	if C <= 0 and D == 0:
		return 0
	if A > 0 and B == 0 and C > 0 and D == 0:
		return math.inf
	if A > 0 and B == 0 and D < 0:
		return math.inf
	if B < 0 and C > 0 and D == 0:
		return math.inf
	if B > 0 and C > 0 and D == 0:
		return A/B
	if B > 0 and D > 0:
		return min(A/B, C/D)

#Calculations for STATEMENT TWO
	
def findABCD2(dat):
	(m,s,V,sV, sVm1) = dat
	floor = math.floor((V-1)*sVm1/sV)
	A = m/s - (V - floor) * (1 - m/s)
	B = floor + (V - floor) * (V - 1)
	ceil = math.ceil((V-1)*sVm1 / sV)
	C = ceil * (V - m/s - 1) + (V - ceil) * m/s - m/s
	D = ceil * (V - 2) + (V - ceil) * (V - 1)
	return (A,B,C,D)

def findQ(m,s, spew=True):
	m = Fraction(m)
	s = Fraction(s)

	if (m<s and spew):
		print("The interval therum only works when m>s")
		return 1


	V = interval.findV(m,s)
	(sV, sVm1) = interval.getShares(m,s,V)
	dat = (m,s,V,sV,sVm1)

	if spew: print("V: " + str(V))
	if spew: print("sV: " + str(sV))
	if spew: print("sVm1: " + str(sVm1))

	if (sVm1 == 0 and spew):
		print("sVm1 is zero, so this in not a case handled by the interval theorum.")
		return 1

	#calc MINONE
	A1,B1,C1,D1 = findABCD1(dat)
	if spew:
		print("A1: " + str(A1))
		print("B1: " + str(B1))
		print("C1: " + str(C1))
		print("D1: " + str(D1))
	MINONE = findMIN(A1,B1,C1,D1)
	if spew: print("MINONE: " + str(MINONE))

	#calc MINTWO
	A2,B2,C2,D2 = findABCD2(dat)
	if spew:
		print("A2: " + str(A2))
		print("B2: " + str(B2))
		print("C2: " + str(C2))
		print("D2: " + str(D2))
	MINTWO = findMIN(A2,B2,C2,D2)
	if spew: print("MINTWO: " + str(MINTWO))

	#now, calculate Qv as per the paper

	Q1, Q2, Q3, Q4 = 1,1,1,1
	if MINONE != None and MINONE < (Fraction(1,2) - m/s + V - 2) / (V - 2):
		Q1 = MINONE
	if MINTWO != None and MINTWO < (m/s - Fraction(1,2)) / (V-1):
		Q2 = MINTWO
	if V*sV != (V-1)*sVm1:
		Q3 = (V - (m/s) - Fraction(3,2)) / (V-2)
	if V*sV != (V-1)*sVm1:
		Q4 = (m/s - Fraction(1,2)) / (V - 1)
	
	passes = [x for x in [Q1,Q2,Q3,Q4] if INIT(dat, x)]
	if (len(passes) == 0 and spew):
		print("none of Q1,Q2,Q3,Q4 passed INIT test")
		return 1
	else:
		return min(passes)
	


def INIT(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Fraction(V-2, 2*V-3) < Q
	cond2 = Q < min(m/sV, (V-1-m/s)/(V-1))
	return cond1 and cond2

