#implementation of Scott Huddleston's algorithm for the muffin problem

from fractions import Fraction
import math
import interval


def scott(muffins, majors, minors):
    """Computes the "scott muffin problem", which says, given Nm muffins and two groups of students,
    group 1 is the "majors" and group 2 is the "minors", cut up each muffin into Pm pieces and give to students.
    The value of each muffin is Vm, the value of majors are Vs1 and likewise for minors (meaning e.g. each major
    recieves Vs1 total muffin). Furthermore, Vs1/Ps1 <= Vs2/Ps2.
    Find way of doing this so smallest piece is as large as possible.

    The following algorithm is (my best guess at figuring out) an algorithm created by Scott Huddleston from California.
    As far as we can tell, no one knows why it works. Furthermore, and again no one knows why, but the results of the
    algorithm are also optimal results for the traditional muffin problem.
    
    All inputs should be tuples of three Fraction objects.
    The output will be a tuple of three lists of lists of piece sizes (muffinPieces, majorPieces, minorPieces)
    which tells how to split the muffins, majors, and minors.
    For example, muffinPieces is a list of lists, where each inner list represents a muffin"""

    (Nm, Vm, Pm), (Ns1, Vs1, Ps1), (Ns2, Vs2, Ps2) = muffins, majors, minors

    #Assumption: In optimal solution to the scott muffin problem, each muffin gives either exactly one piece to a minor
    #and the rest to majors (major type muffins), or exactly one piece to one minor, one piece to another minor, and the
    #rest to majors (minor type muffins).

    #There are (Ns2*Vs2 - Nm) minor type muffins, and (2*Nm - Ns2*Vs2) major type muffins.
    #We may make a graph with Ns2 nodes and (Ns2*Vs2 - Nm) edges. We call this the minor students graph.
    #It determines the arrangement of minor type muffins being given to the minor students

    #Assumption: The minor students graph will consist of "chains" of length L and L-1, where, L is
    #the number L calculated below.

    #Assumption: If we can't make chains like that, then we have already found the constraint on the muffin problem.
    #Below, we check if its possible to make chains. The following equation does so:

    if Ns2 == 0: #must always be that Nm*Vm = Ns1*Vs1, and Nm*Pm = Ns1*Ps1, so Vm/Pm = Vs1/Ps1
        #just divide all muffins and student evenly
        muffinPieces = [[Vm/Pm]*int(Pm)]*int(Nm)
        majorPieces = [[Vs1/Ps1]*int(Ps1)]*int(Ns1)
        return (muffinPieces, majorPieces, []) #no minors, so just an empty list in the last slot
    elif Ns1 == 0: #must always be that Nm*Vm = Ns2*Vs2, and Nm*Pm = Ns2*Ps2, so Vm/Pm = Vs2/Ps2
        #just divide all muffins and student evenly
        muffinPieces = [[Vm/Pm]*int(Pm)]*int(Nm)
        minorPieces = [[Vs2/Ps2]*int(Ps2)]*int(Ns2)
        return (muffinPieces, [], minorPieces) #no majors, so just an empty list in the middle slot
    elif Ns2 * Ps2 >= Nm + Ns2: #If this condition holds, then we can't divide minor students into chains (see below)
        #Assumption: under the above condition, the optimal solution involves making all major's pieces Vs1 / Ps1,
        #and furthermore the optimal solution has these pieces distributed as evenly as possible in the muffins.
        majorPieces = [[Vs1 / Ps1 for i in range(int(Ps1))] for j in range(int(Ns1))] #All major pieces of size Vs1 / Ps1

        #We find minorPieces and muffinPieces by solving a new "scott muffin problem". First, we divide the major pieces
        #among the muffins as evenly as possible, so
        P = Fraction(math.ceil(Ns1*Ps1 / Nm)) #Some muffins give P pieces to majors, and some give P-1 pieces.
        #a is the number that give P pieces, b is the number that give P-1
        a = Ns1*Ps1 - (P - 1)*Nm
        b = Nm - a
        #After working out the math, that means that the two groups of muffins we get are as follows:
        group1 = (a, Vm - P*Vs1/Ps1, Pm - P)
        group2 = (b, Vm - (P-1)*Vs1/Ps1, Pm - (P-1))
        #Next, check Vs/Ps to determine which group is majors and which group is minors. TODO: does it always go one way?
        #Also make variable to remember which group lost P pieces of size Vs1/Ps1, and which group lost (P-1) pieces of that size.
        newMajors, newMajorsLostPieces = None, None
        newMinors, newMinorsLostPieces = None, None
        if group1[1] / group1[2] > group2[1] / group2[2]:
            newMajors, newMinors = group1, group2
            newMajorsLostPieces, newMinorsLostPieces = int(P), int(P-1)
        else:
            newMajors, newMinors = group2, group1
            newMajorsLostPieces, newMinorsLostPieces = int(P-1), int(P)

        #Assumption: In this sub-problem, the smallest piece will be no smaller than Vs1/Ps1, so we have already found smallest piece size
        (subMuffinPieces, subMajorPieces, subMinorPieces) = scott(minors, newMajors, newMinors)#run the subproblem, next we need to reconstruct solution


        muffinPiecesFromMajors = [major + ([Vs1/Ps1]*newMajorsLostPieces) for major in subMajorPieces]
        muffinPiecesFromMinors = [minor + ([Vs1/Ps1]*newMinorsLostPieces) for minor in subMinorPieces]

        majorPieces = [[Vs1/Ps1]*int(Ps1) for i in range(int(Ns1))] #majors pieces are just all Vs1/Ps1

        return (muffinPiecesFromMajors + muffinPiecesFromMinors, majorPieces, subMuffinPieces)#minors became muffins for subproblem

        #return Vs1 / Ps1

    # this is the value of L which keeps Nm/Ns2 as close as possible to (Ps2*L - L + 1) / L.
    #That makes sense because it allows the average piece size in the chains to be as large as possible (TODO: check that that statement makes sense)
    L = Fraction(math.ceil(1/(Nm/Ns2 + 1 - Ps2)))

    #Given the above assumptions and value of L, we can calculate the number of L-length chains there are, b,
    #and the number of (L-1)-length chains, a. We can get two equations by looking at
    # the total number of minors and muffins involved in each chain. The use linear algegra to get below equations.
    a = L*Nm - L*Ps2*Ns2 + L*Ns2 - Ns2
    if L == 1:
        a = 0#the formula does not work in this special case. TODO: consider why
    b = (Ns2 - a*(L - 1)) / L

    #But how do we actually make things work out with major type muffins, minor type muffins, and whatnot? Recursion!

    #Assumption: In an optimal solution, the smallest piece going to a minor will be larger than the smallest piece going to a major,
    #So we can freely permute the way that majors are connected to a chain. The only thing that matters is which majors are
    #Connected to which chains. Therefore, 
    #We consider a new "scott muffin problem" with the old majors as new muffins, and the (L-1)-chains and L-chain as the
    #majors and minors. The old majors "give pieces to" the old minors.

    #The L-chains will be majors unless possibly p = 2 and Vm > Vs2. I may have made a miscalculation, though, because
    #In practice that seems to be wrong and it seems like the L-chains are just always the majors.

    #The following are the correct values of N, V, P for the L-chains and (L-1)-chains
    newPs1 = (L*Ps2 - 2*(L-1))*(Pm-1) + (L - 1) * (Pm - 2)
    newPs2 = ((L-1)*Ps2 - 2*(L-2))*(Pm-1) + (L - 2) * (Pm - 2)
    newMajors = (b, (L*Ps2 - (L-1))*Vm - L*Vs2, newPs1)
    newMinors = (a, ((L-1)*Ps2 - (L-2))*Vm - (L-1)*Vs2, newPs2)

    #return scott(majors, newMajors, newMinors)
    (subMuffinPieces, subMajorPieces, subMinorPieces) = scott(majors, newMajors, newMinors)
    deconstructedLChains = [deconstructLchain(pieces, Pm, Ps2, Vm, Vs2, L) for pieces in subMajorPieces] #L-chains became the sub-majors
    deconstructedLm1Chains = [deconstructLchain(pieces, Pm, Ps2, Vm, Vs2, L-1) for pieces in subMinorPieces] #(L-1)-chains became the sub-minors
    muffinPieces = sum([dchain[0] for dchain in deconstructedLChains + deconstructedLm1Chains], []) #get first elements out of tuples, so we have lists of students
    studentPieces = sum([dchain[1] for dchain in deconstructedLChains + deconstructedLm1Chains], [])

    return (muffinPieces, subMuffinPieces, studentPieces) #submuffins are majors, substudents are minors+muffins which were deconstructed


def f(m,s): #put it all together and calculate f(m,s)
    if m <= s:
        print("scott's algorithm only works for m>s")
        return

    m = Fraction(m)
    s = Fraction(s)
    V = interval.findV(m,s)
    sV, sVm1 = interval.getShares(m,s,V)
    #sV are majors, sVm1 are minors
    muffins, majors, minors = scott((m,Fraction(1),Fraction(2)),(sV,m/s,V),(sVm1,m/s,V-1))

    if muffins[0][0] < Fraction(1,3):
        print("scott's algorithm only works if f(m,s) > 1/3")
        return
    
    for muffin in muffins:
        print("Muffin: " + pfmap(muffin))
    for student in majors+minors:
        print("Student: " + pfmap(student))


#The following functions are used to deconstruct L-chains back into muffins and minors.
def deconstruct1chain(pieces, Pm, Ps2, Vm):
    """Input is list of pieces, output is [muffins, studentes] which are both lists of lists of pieces"""
    muffinsMissingLastPiece = divide_chunks(pieces, Pm-1)#first find list of most of muffins, missing last piece (connected to student)
    muffins = [partialM + [Vm - sum(partialM)] for partialM in muffinsMissingLastPiece]#find what the size of the last piece is
    student = [muffin[-1] for muffin in muffins]
    return (muffins, [student])

def deconstructLchain(pieces, Pm, Ps2, Vm, Vs2, L):
    """Input is list of pieces, output [muffins, students] which are both lists of lists of pieces."""
    if L <= 0:
        raise Exception("L should be at least 1, instead its " + str(L))
    Pm = int(Pm) #we need to make sure these are integers and not Fraction objects
    Ps2 = int(Ps2)
    if L == 1:
        return deconstruct1chain(pieces, Pm, Ps2, Vm)
    else: #We compute the left-most student (and his muffins) and then recurse
        #first, find the Ps2-1 muffins on the left-most student. Refer to these as left-muffins
        numLeftPieces = (Ps2-1)*(Pm-1)
        leftPieces = pieces[:numLeftPieces] #find pieces for left-muffins
        bridgePieces = pieces[numLeftPieces:numLeftPieces + Pm - 2] #Pieces that go to muffin connecting left student to next student
        leftOverPieces = pieces[numLeftPieces + Pm - 2:] #all the rest of the pieces

        muffinsMissingLastPiece = divide_chunks(leftPieces, Pm-1)#first find list of most of muffins, missing last piece (connected to student)
        muffins = [partialM + [Vm - sum(partialM)] for partialM in muffinsMissingLastPiece]#find what the size of the last piece is
        studentMissingLastPiece = [muffin[-1] for muffin in muffins]
        student = studentMissingLastPiece + [Vs2 - sum(studentMissingLastPiece)]
        newPieces = [student[-1]] + bridgePieces + leftOverPieces #add that last piece of the student on to the pieces to be used in recursion - this is bridge muffin piece

        (restOfMuffins, restOfStudents) = deconstructLchain(newPieces, Pm, Ps2, Vm, Vs2, L-1) #calculate the answer for smaller chain

        return (muffins + restOfMuffins, [student] + restOfStudents)

def divide_chunks(l, n): #divide a list into equal sized pieces
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def pfmap(fractions): #pretty print a list of fractions
    return str(tuple(map(pf, fractions)))
def pf(fraction): #pretty print a fraction
    return "%s/%s"%(str(fraction.numerator), str(fraction.denominator))
