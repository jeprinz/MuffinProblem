from fractions import Fraction
import interval
import math

#Note that data is passed around in this form: (m,s,V,sV, sVm1)
#where m, s is muffins,students. V is variable from paper, sV is sV from paper, and sVm1 is sV-1 from paper

def mceil(x):
	return Fraction(math.ceil(x))
def mfloor(x):
	return Fraction(math.floor(x))

#Calculations for STATEMENT ONE
def findABCD1(dat):
	(m,s,V,sV, sVm1) = dat
	ceil = mceil(V*sV/sVm1)
	floor = mfloor((V*sV)/sVm1)
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
	floor = mfloor((V-1)*sVm1/sV)
	A = m/s - (V - floor) * (1 - m/s)
	B = floor + (V - floor) * (V - 1)
	ceil = mceil((V-1)*sVm1 / sV)
	C = ceil * (V - m/s - 1) + (V - ceil) * m/s - m/s
	D = ceil * (V - 2) + (V - ceil) * (V - 1)
	return (A,B,C,D)

def findQ7(m,s,sV,sVm1,V):

	if V*sV > m:
		return 1

	U = mceil((V*sV + 1) / sVm1)
	dUm1 = U*sVm1 - V*sV
	dU = V*sV - (U - 1)*sVm1

	if dU == 0 or dUm1 == 0:
		return 1

	Xu = mfloor((m - V*sV) / dU)
	XUm1 = mfloor((m - V*sV) / dUm1)

	A = m/s - (U + 1)*(1 - m/s) - (V - U - 2) * (m/s - V + 2)
	B = (U + 1) * (V - 1) + (V - U + 2) * (V - 2)

	Q72 = None
	if A <= 0:
		Q72 = 0
	elif B > 0:
		Q72 = A / B
	elif A > 0 and B <= 0:
		Q72 = math.inf
	
	if U >= sVm1:
		Q72 = 0

	C = (U - 2) + (V - U + 1)*(-m/s + V - 1) - m/s
	D = V**2 - U*V - V + 3*U - 4
	
	Q73 = None
	if C <= 0:
		Q73 = 0
	elif D > 0:
		Q73 = C / D
	elif C > 0 and D <= 0:
		Q73 = math.inf

	if U <= 1:
		Q73 = 0
	
	E = m/s - Xu*(m/s - V + 2) - (V - 1 - U - Xu)/2 - U*(1 - m/s)
	F = Xu*(V - 2) + U*(V - 1)
	G = XUm1*(1 - m/s + V - 2) + (V - U - XUm1)/2 + (U - 1) - m/s
	H = XUm1*(V - 2) + U - 1

	Q75 = None
	if E <= 0:
		Q75 = 0
	elif G <= 0:
		Q75 = 0
	elif E > 0 and F > 0 and G > 0 and H > 0:
		return min(E / F, G / H)
	elif E > 0 and F > 0 and G > 0 and H <= 0:
		return E / F
	elif E > 0 and F <= 0 and G > 0 and H > 0:
		return G / H
	elif E > 0 and F <= 0 and G > 0 and H <= 0:
		return math.inf
	
	lhs = max((V - 2)/(2*V - 3), Q72, Q73, Q75)
	rhs = min(m/(s*V), (V - 1 - m/s)/(V - 1), (Fraction(1,2) - m/s + V - 2)/(V - 2))

	if lhs <= rhs and V*sV <= m:
		return lhs
	else:
		return 1

def findQ8(m,s,sV,sVm1,V):

	if (V - 1)*sVm1 > m:
		return 1

	U = mceil(((V - 1)*sVm1 + 1) / sV)
	dUm1 = U*sV - (V - 1)*sVm1
	dU = (V - 1)*sVm1 - (U - 1)*sV

	if dU == 0 or dUm1 == 0:#TODO: tell bill
		return 1

	XU = mfloor((m - (V - 1)*sVm1) / dU)
	XUm1 = mfloor((m - (V - 1)*sVm1) / dUm1)

	A = (U + 1)*(V - m/s - 1) + (V - U - 1)*m/s - m/s
	B = (U + 1)*(V - 2) + (V - 1)*(V - 1 - U)

	Q82 = None
	if A <= 0:
		Q82 = 0
	elif B > 0:
		Q82 = A/B
	elif A > 0 and B <= 0:
		Q82 = math.inf
	
	if U >= sV:
		Q82 = 0
	
	C = m/s - (V - U + 2)*(1 - m/s)
	D = U - 2 + (V - U + 2)*(V - 1)

	Q83 = None
	if C <= 0:
		Q83 = 0
	elif D > 0:
		Q83 = C/D
	elif C > 0 and D <= 0:
		Q83 = math.inf
	
	if U <= 1:
		Q83 = 0
	
	E = (XU - 1)*m/s+ (V - U - XU)/2 + U*(-m/s + V - 1)
	F = XU*(V - 1) + U*(V - 2)
	G = m/s - (V - U + 1 - XUm1)/2 - XUm1*(1 - m/s)
	H = XUm1*(V - 1) + (U - 1)

	Q85 = None
	if E <= 0:
		Q85 = 0
	elif G <= 0:
		Q85 = 0
	elif E > 0 and F > 0 and G > 0 and H > 0:
		Q85 = min(E/F, G/H)
	elif E > 0 and F > 0 and G > 0 and H <= 0:
		Q85 = E/F
	elif E > 0 and F <= 0 and G > 0 and H > 0:
		Q85 = G/H
	elif E > 0 and F <= 0 and G > 0 and H <= 0:
		Q85 = math.inf
	
	lhs = max((V - 2) / (2*V- 3), Q82, Q83, Q85)
	rhs = max(m/(s*V), (V - 1 - m/s)/(V - 1), (m/s - Fraction(1,2))/(V - 1))

	if lhs <= rhs and (V - 1)*sVm1 <= m:
		return lhs
	else:
		return 1

def findQ9(m,s,sV,sVm1,V):
	val = (V - 2) / (2*V - 3) 
	rhs = min(m/(s*V), (V - 1 - m/s)/(V - 1), (Fraction(1,2) - m/s + V - 2)/(V - 2))
	if val <= rhs and V*sV > m:
		return val
	else:
		return 1

def findQ10(m,s,sV,sVm1,V):
	val = (V - 2) / (2*V - 3) 
	rhs = min(m/(s*V), (V - 1 - m/s)/(V - 1), (m/s - Fraction(1,2))/(V - 2))
	if val <= rhs and (V - 1)*sVm1 > m:
		return val
	else:
		return 1


def findQ(m,s, spew=True):
	m = Fraction(m)
	s = Fraction(s)

	if (m<s and spew):
		print("The interval therum only works when m>s")
		return 1


	V = interval.findV(m,s)
	(sV, sVm1) = interval.getShares(m,s,V)

	if sV == 0 or sVm1 == 0:#TODO: tell bill about this
		return 1#this means everyone gets same number of pieces

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

	Q1, Q2, Q3, Q4, Q5, Q6 = 1,1,1,1,1,1
	Q1 = MINONE
	if MINONE == None or not PREM1(dat, Q1, MINONE):
		Q1 = 1
	Q2 = MINTWO
	if MINTWO == None or not PREM2(dat, Q2, MINTWO):
		Q2 = 1
	Q3 = (V - (m/s) - Fraction(3,2)) / (V-2)
	if not PREM3(dat, Q3):
		Q3 = 1
	Q4 = (m/s - Fraction(1,2)) / (V - 1)
	if not PREM4(dat, Q4):
		Q4 = 1
	#Q5 = (V - 2) / (2*V - 3)
	Q5 = (m/s - Fraction(1)/2) / (V - 1)
	if not PREM5(dat, Q5):
		Q5 = 1
	#Q6 = (V - 2) / (2*V - 3)
	Q6 = (V - Fraction(3)/2 - m/s) / (V - 2)
	if not PREM6(dat, Q6):
		Q6 = 1
	
	Q7 = findQ7(m,s,sV,sVm1,V)
	Q8 = findQ8(m,s,sV,sVm1,V)
	Q9 = findQ9(m,s,sV,sVm1,V)
	Q10 = findQ10(m,s,sV,sVm1,V)

	if spew:
		print("Qs: " + str([Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10]))
	
	Q = min([Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8])
	return max(Fraction(1)/3, m/(s*(V+1)), 1 - m/(s*(V-2)), Q)
	
	


def INIT(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Fraction(V-2, 2*V-3) < Q
	cond2 = Q < min(m/(s*V), (V-1-m/s)/(V-1))
	return cond1 and cond2

#premises from paper
def PREM(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Fraction(V-2, 2*V-3) <= Q
	cond2 = Q < min(m/s/V, (V-1-m/s)/(V-1))
	return cond1 and cond2

def PREM1(dat, Q, MINONE):
	(m,s,V,sV, sVm1) = dat
	cond1 = MINONE <= Q
	cond2 = Q < (Fraction(1)/2 - m/s + V - 2)/(V-2)
	return PREM(dat, Q) and cond1 and cond2
def PREM2(dat, Q, MINTWO):
	(m,s,V,sV, sVm1) = dat
	cond1 = MINTWO<= Q
	cond2 = Q < (m/s - Fraction(1)/2) / (V - 1)
	return PREM(dat, Q) and cond1 and cond2
def PREM3(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Q == (V - m/s - Fraction(3)/2) / (V - 2)
	cond2 = V*sV != (V - 1) * sVm1
	return PREM(dat, Q) and cond1 and cond2
def PREM4(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Q == (m/s - Fraction(1)/2) / (V - 1)
	cond2 = V*sV != (V - 1) * sVm1
	return PREM(dat, Q) and cond1 and cond2
def PREM5(dat, Q):
	(m,s,V,sV, sVm1) = dat
	cond1 = Q >= (m/s - Fraction(1)/2) / (V - 1)#erik style
	cond2 = Q < m/s*V
	cond3 = V*sV > (V - 1)*sVm1
	return cond1 and cond2 and cond3 # and PREM(da, Q)
def PREM6(dat, Q):
	(m,s,V,sV, sVm1) = dat
	#cond1 = Q >= 1 - (m/s - Fraction(1)/2) / (V - 2)
	cond1 = Q >= (V - Fraction(3)/2 - m/s) / (V - 2)
	cond2 = Q < (V - m/s - 1)/(V - 1)
	cond3 = V*sV < (V - 1)*sVm1
	return cond1 and cond2 and cond3 # and PREM(dat, Q)
#def PREM5(dat, Q):
#	(m,s,V,sV, sVm1) = dat
#	A = (2*m - s) / (2*s*(V - 1))
#	B = (V - 2) / (2*V - 3)
#	cond1 = A < B and B == Q
#	cond2 = V*sV > (V - 1)*sVm1
#	return PREM(dat, Q) and cond1 and cond2
#def PREM6(dat, Q):
#	(m,s,V,sV, sVm1) = dat
#	A = (2*m - s) / (2*s*(V - 1))
#	B = (V - 2) / (2*V - 3)
#	cond1 = A < B and B == Q
#	cond2 = V*sV < (V - 1)*sVm1
#	return PREM(dat, Q) and cond1 and cond2
	
	
	

