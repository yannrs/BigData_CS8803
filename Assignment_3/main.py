import time
import itertools
import copy
import set

""" Implementation of the Apriori Algorithm
Input:
    - inputFile: name of the input file
    - threshold: integer, minimum support count
    - outputFile: name of the output file
        each line as: A B C (5)
        where A,B,C are items and 5 is the support count
"""
def apriori_based(inputFile, threshold, outputFile):

    print 'begin extract'
    data = generateItem(inputFile)
    print 'second step'
    Lk = findItemSet(data, threshold)
    print 'third step'
    writeItemsSet(Lk, outputFile)

    return Lk


""" Find all itemsets that have minimum support - frequent itemsets

"""
def findItemSet(data, sup_min):

    Ck = []         # Candidate itemset of size k
    Lk_save = []     # frequent itemset of size k        <- Need to be saved at each step

    print 'ici1'
    Lk = extractItem(data)
    # print 'Lk', Lk
    guard = 0
    maxIt = len(Lk['candidates'])
    k = 1
    while Lk['candidates'] and guard < maxIt:
        print 'i: ', guard
        # Generate Candidate with a size k
        Ck = generateCandidateFromLk(Lk, k)
        # print 'Ck', Ck

        # Count apparition of itemset on data
        Ck_ = countCandidate(data, Ck)
        # print 'Ck_', Ck_

        # Keep only itemset with a frequency above the limit
        # Lk = filter((lambda x: x > sup_min), Ck)
        Lk = removeBelowLimit(Ck_, sup_min)
        # print 'Lk', Lk

        Lk_save.append(copy.deepcopy(Lk))
        k += 1

        guard += 1

    return Lk_save




def extractItem(data):
    items = []

    for line in data:
        for item in line:
            if item not in items:
                items.append(item)

    items.sort()
    return {'candidates': [[str(key)] for key in items]}



def removeBelowLimit(list, threshold):
    candidate = list['candidates']
    Lk = {}
    newItem = []
    index = 0
    for c in range(0, len(candidate)):
        if list[str(c)] > threshold:
            newItem.append(candidate[c])
            Lk[index] = list[str(c)]
            index += 1

    Lk['candidates'] = newItem
    return Lk


NBLINE = 0

def generateItem(filenameInput):
    global NBLINE
    array = []
    NBLINE = 0
    with open(filenameInput, "r") as lines:
        for line in lines:
            NBLINE += 1
            array.append(line.strip().split(" "))

    return array


def writeItemsSet(Lk, filename):

    file = open(filename, "w+")

    nbSize = len(Lk)
    for i in range(0, nbSize):
        for s in range(0, len(Lk[i]['candidates'])):
            file.write(" ".join(Lk[i]['candidates'][s]) + ' (' + str(Lk[i][s]) + ') \n')



""" From a set of value: [ A,...] generate all combinations with a dimension k+1
Input:
    - Lk: Dico('value', ... 'candidate')
    - nb_items: size of packet
"""
def generateCandidateFromLk(Lk, nb_items):
    # Extract primitive element of key
    prim_elements = []
    for key in Lk['candidates']:
        for k in key:
            if k not in prim_elements:
                prim_elements.append(k)

    print prim_elements
    # Generate all permutation with k elements
    comb = list(itertools.combinations(prim_elements, nb_items))

    comb = [list(s) for s in comb]
    return comb


""" Compute the frequency for each Candidate from the list Ck
Input:
    - data: List( [ value, ... ]) where value=[ keys +]
    - Ck: [ [ item, ... ], ... ]
Output:
    - Dico( 'value': frequency )
"""
def countCandidate(data, Ck):
    if not Ck:
        return {'candidates': []}
    Lk = {str(i): 0 for i in range(0, len(Ck))}
    nbElement = len(Ck[0])
    for line in data:
        for key in range(0, len(Ck)):
            i = 0
            while i < nbElement and Ck[key][i] in line:
                i += 1
            if i == nbElement:
                Lk[str(key)] += 1

    for key in Lk:
        Lk[key] /= float(NBLINE)

    Lk['candidates'] = Ck
    return Lk




""" From frequent itemsets generate rules
"""
def generateRules():
    return


if __name__ == '__main__':
    # data = ['A', 'B', 'C', 'D', 'E']
    # print generateCandidateFromLk(data, 3)
    start_time = time.clock()

    print apriori_based("Data/chess.dat", 0.8, "Data/chess_output.dat")
    # print apriori_based("Data/mushroom.dat", , "Data/mushroom_output.dat")

    print("--- %s seconds ---" % (time.clock() - start_time))