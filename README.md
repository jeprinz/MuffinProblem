# This is a collection of code related to the muffin problem.

There are three main programs contained in this repository.

## Procedure generation program
The algorithm for the procedure generation program is described in the LaTeX write up (remember to put in repo). The main code based on that algorithm is located in the file integers.py.

The main entry point to use the code is the function getProcedures in bigrun.py. Call this function with m, s, and Q, or by default will use an Interval theorem upper bound of Q.

## V3 upper bound program.
The V = 3 upper bound program is located in the file V3program.py.

## Interval theorem upper bound program
The second upper bound program is based on the interval theorem. It is located mainly in findq.py.
