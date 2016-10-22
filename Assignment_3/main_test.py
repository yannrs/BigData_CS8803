import time
import itertools
import copy

NBLINE = 0

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
    print 'old length', len(data)
    # data = sortData(data)
    print 'new length', len(data)
    # print 'data', data
    print 'second step ', int(NBLINE*0.98)
    Lk = findItemSet(data, int(NBLINE*0.80))
    # Lk = findItemSet(data, threshold)
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
    print 'Lk', Lk
    guard = 0
    maxIt = len(Lk.keys())
    k = 1
    while Lk and guard < maxIt:
        print 'i: ', guard
        # Generate Candidate with a size k
        Ck = generateCandidateFromLk(Lk, k)
        print len(Ck)
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


""" Get data from a file
Input:
    - Filename = String
Output:
    - [ frozenset( order1, order2, ...), ... ]
"""
def generateItem(filenameInput):
    global NBLINE
    array = []
    NBLINE = 0
    with open(filenameInput, "r") as lines:
        for line in lines:
            NBLINE += 1
            array.append(frozenset([int(key) for key in line.strip().split(" ")]))

    print 'NBLINE', NBLINE
    return array


""" Aggregate repetitive lines
Input :
    - data : [ frozenset(item1, item2, ...), ... ]
Output :
    - { frozenset(item1, item2, ...): 5, ... }
"""
def sortData(data):
    data2 = {}
    for line in data:
        if line not in data2:
            data2[line] = 1
        else:
            data2[line] += 1

    return data2


""" Extract unique element
Input:
    - data: [ frozenset( item1, item2, ...), ....]
Output:
    - { frozenset( item1, ...):0, ... }
"""
def extractItem(data):
    items = frozenset([])

    for line in data:
        items = items.union(line)
    print 'extractItem', 'items', len(items)
    return {frozenset([key]): 0 for key in items}


""" From a frozenset of value: [ A,...] generate all combinations with a dimension k+1
Input:
    - Lk: Dico(frozenset1: 1, frozenset2: 2, ...)
    - nb_items: size of packet
Output:
    - frozenset( frozenset( item1, item2,...), ...)
"""
def generateCandidateFromLk(Lk, nb_items):
    # Extract primitive element of key
    # print 'generateCandidateFromLk',' Lk', Lk
    prim_elements = frozenset()
    for key in Lk.keys():
        prim_elements = prim_elements.union(key)

    # print 'generateCandidateFromLk ', 'prim_elements', prim_elements
    # Generate all permutation with k elements
    comb = [frozenset(key) for key in itertools.combinations(prim_elements, nb_items)]

    return comb


""" Compute the frequency for each Candidate from the list Ck
Input:
    - data: List( [ value, ... ]) where value=[ keys +]
    - Ck: [ [ item, ... ], ... ]
Output:
    - Dico( 'value': frequency )
"""
def countCandidate(data, Ck):
    Lk = {i: 0 for i in Ck}
    # nbElement = len(Ck[0])
    for setItems in Ck:
        for line in data:
            if setItems <= line:
                # Lk[setItems] += data[line]
                Lk[setItems] += 1

    # for key in Lk:
    #     Lk[key] /= float(NBLINE)

    # print 'countCandidate', 'k', Lk
    return Lk


def removeBelowLimit(list, threshold):
    Lk = copy.deepcopy(list)
    for setItems in list:
        if list[setItems] < threshold:
            Lk.pop(setItems)

    return Lk


def writeItemsSet(Lk, filename):

    file = open(filename, "w+")

    nbSize = len(Lk)
    for i in range(0, nbSize):
        for s in Lk[i].keys():
            # file.write(" ".join([str(it) for it in s]) + ' (' + str(Lk[i][s]*NBLINE) + ') \n')
            file.write(" ".join([str(it) for it in s]) + ' (' + str(Lk[i][s]) + ') \n')




""" From frequent itemsets generate rules
"""
def generateRules():
    return


if __name__ == '__main__':
    # data = ['A', 'B', 'C', 'D', 'E']
    # print generateCandidateFromLk(data, 3)
    start_time = time.clock()

    # print apriori_based("Data/chess.dat", 0.8, "Data/chess_output2.dat")
    print apriori_based("Data/chess.dat", 2556, "Data/chess_output3.dat")
    # print apriori_based("Data/chess_custom.dat", 2556, "Data/chess_custom_output3.dat")
    print apriori_based("Data/mushroom.dat", 3000, "Data/mushroom_output.dat")
    # print apriori_based("Data/mushroom_custom.dat", 3000, "Data/mushroom_custom_output.dat")
    # print apriori_based("Data/pumsb.dat", 3000, "Data/pumsb_output.dat")

    # print("--- %s seconds ---" % (time.clock() - start_time))
    print("%s seconds" % (time.clock() - start_time))