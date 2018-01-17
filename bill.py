import bigrun
from sys import argv
from fractions import Fraction

if len(argv) != 4:
	print("Usage: " + argv[0] + " m s Q")
else:
	m = int(argv[1])
	s = int(argv[2])
	Q = Fraction(argv[3])
	bigrun.getProcedures(m,s,Q=Q)

