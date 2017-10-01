from fractions import Fraction
import interval
import math

#Note that data is passed around in this form: (m,s,V,sV, sVm1)
#where m, s is muffins,students. V is variable from paper, sV is sV from paper, and sVm1 is sV-1 from paper

#Calculations for STATEMENT ONE
def findA1(dat):
	(m,s,V,sV, sVm1) = dat
	floor = math.floor((V*sV)/sVm1)
	return floor + (V - 1 - floor)*(V - m/s - 1) - m/s

def findB1(dat):
	(m,s,V,sV, sVm1) = dat
	floor = math.floor((V*sV)/sVm1)
	return floor + (V-2)*(V - 1 - floor)

def findC1(dat):
	(m,s,V,sV, sVm1) = dat
	ciel = math.ceil(V*sV/sVm1)
	return m/s - (V-1-ciel)*(m/s-V+2) - ciel*(1-m/s)

def findD1(dat):
	(m,s,V,sV, sVm1) = dat
	ciel = math.ceil(V*sV/sVm1)
	return ciel*(V-1) + (V-1-ciel)*(V-2)

def findMINONE(A,B,C,D):
	if A <= 0 and B == 0:
		return 0
	pass
	


def findQ(m,s, spew=True):
	m = Fraction(m)
	s = Fraction(s)
	V = interval.findV(m,s)
	(sV, sVm1) = interval.getShares(m,s,V)
	dat = (m,s,V,sV,sVm1)

	if spew: print("V: " + str(V))
	if spew: print("sV: " + str(sV))
	if spew: print("sVm1: " + str(sVm1))

	#calc MINONE
	A1 = findA1(dat)
	if spew: print("A1: " + str(A1))
	B1 = findB1(dat)
	if spew: print("B1: " + str(B1))
	C1 = findC1(dat)
	if spew: print("C1: " + str(C1))
	D1 = findD1(dat)
	if spew: print("D1: " + str(D1))
	#MINONE = findMINEONE(A1,B1,C1,D1)
	#if spew: print("MINONE: " + str(MINONE))
	##calc MINTWO
	#A2 = findA2(dat)
	#if spew: print("A2: " + str(A2))
	#B2 = findB2(dat)
	#if spew: print("B2: " + str(B2))
	#C2 = findC2(dat)
	#if spew: print("C2: " + str(C2))
	#D2 = findD2(dat)
	#if spew: print("D2: " + str(D2))
	#MINTWO = findMINETWO(A2,B2,C2,D2)
	#if spew: print("MINTWO: " + str(MINTWO))

