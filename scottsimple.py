#implementation of Scott Huddleston's algorithm for the muffin problem

from fractions import Fraction
import math
import interval


def scott(muffins, majors, minors):
    """Computes the "scott muffin problem", which says, given Nm muffins and two groups of students,
    group 1 is the "majors" and group 2 is the "minors", cut up each muffin into Pm pieces and give to students.
    The value of each muffin is Vm, the value of majors are Vs1 and likewise for minors (meaning e.g. each major
    recieves Vs1 total muffin). Furthermore, each muffin must give at least one piece to a minor, and it must be
    that Vs1/Ps1 <= Vs2/Ps2.
    Find way of doing this so smallest piece is as large as possible.

    The following algorithm is (my best guess at figuring out) an algorithm created by Scott Huddleston from California.
    As far as we can tell, no one knows why it works. Furthermore, and again no one knows why, but the results of the
    algorithm are also optimal results for the traditional muffin problem.
    
    All inputs should be tuples of three Fraction objects.
    The output will be a tuple of three lists of piece sizes, (muffinPieces, majorPieces, minorPieces)
    which tells how to split the muffins, majors, and minors."""

    (Nm, Vm, Pm), (Ns1, Vs1, Ps1), (Ns2, Vs2, Ps2) = muffins, majors, minors

    #Assumption: muffins either give one piece to minor students and the rest to majors (major type muffins),
    #OR give one piece to one minor and another piece to another minor (minor type muffins)

    #There are (Ns2*Vs2 - Nm) minor type muffins, and (2*Nm - Ns2*Vs2) major type muffins.
    #We may make a graph with Ns2 nodes and (Ns2*Vs2 - Nm) edges. We call this the minor students graph.
    #It determines the arrangement of minor type muffins being given to the minor students

    #Assumption: The minor students graph will consist of "chains" of length L and L-1, where, L is
    #the number L calculated below.

    #Assumption: If we can't make chains like that, then we have already found the constraint on the muffin problem.
    #Below, we check if its possible to make chains. The following equation does so:

    print("scott((%s),(%s),(%s))"%(pfmap(muffins), pfmap(majors), pfmap(minors)))

    if Ns2 * Ps2 >= Nm + Ns2 or Ns2 == 0:
        return Vs1 / Ps1

    # this is the value of L which keeps Nm/Ns2 as close as possible to (Ps2*L - L + 1) / L.
    #That makes sense because it allows the average piece size in the chains to be as large as possible (TODO: check that that statement makes sense)
    L = Fraction(math.ceil(1/(Nm/Ns2 + 1 - Ps2)))

    #Given the above assumptions and value of L, we can calculate the number of L-length chains there are, b,
    #and the number of (L-1)-length chains, a. We can get two equations by looking at
    # the total number of minors and muffins involved in each chain. The use linear algegra to get below equations.
    a = L*Nm - L*Ps2*Ns2 + L*Ns2 - Ns2
    if L == 1:
        a = 0 #special case, the formula does not work for a in this case
    b = (Ns2 - a*(L - 1)) / L

    #But how do we actually make things work out with major type muffins, minor type muffins, and whatnot? Recursion!
    #We consider a new "scott muffin problem" with the old majors as new muffins, and the (L-1)-chains and L-chain as the
    #majors and minors. The old majors "give pieces to" the old minors.

    #The L-chains will be majors unless possibly p = 2 and Vm > Vs2. I may have made a miscalculation, though, because
    #In practice that seems to be wrong and it seems like the L-chains are just always the majors.

    #The following are the correct values of N, V, P for the L-chains and (L-1)-chains
    newPs1 = (L*Ps2 - 2*(L-1))*(Pm-1) + (L - 1) * (Pm - 2)
    newPs2 = ((L-1)*Ps2 - 2*(L-2))*(Pm-1) + (L - 2) * (Pm - 2)
    newMajors = (b, (L*Ps2 - (L-1))*Vm - L*Vs2, newPs1)
    newMinors = (a, ((L-1)*Ps2 - (L-2))*Vm - (L-1)*Vs2, newPs2)

    print("L = %s, a = %s, b = %s" %(L,a,b))

    return scott(majors, newMajors, newMinors)


def f(m,s):
    m = Fraction(m)
    s = Fraction(s)
    V = interval.findV(m,s)
    sV, sVm1 = interval.getShares(m,s,V)
    #sV are majors, sVm1 are minors
    return scott((m,1,2),(sV,m/s,V),(sVm1,m/s,V-1))

def pfmap(fractions):
    return str(tuple(map(pf, fractions)))

def pf(fraction):
    return "%s/%s"%(str(fraction.numerator), str(fraction.denominator))

