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

    # Load dataset
    data = generateItem(inputFile)
	
	# Preprocess data
    data = sortData(data)
    
	# Generate Subset
    Lk = findItemSet(data, threshold)
	
    # Save results
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

        # Count apparition of itemset on data
        Ck_ = countCandidate(data, Ck)

        # Keep only itemset with a frequency above the limit
        Lk = removeBelowLimit(Ck_, sup_min)

		# Save previous subset
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
    - data: { frozenset(item1, item2, ...): 5, ... }
Output:
    - { frozenset( item1, ...):0, ... }
"""
def extractItem(data):
    items = frozenset([])

    for line in data:
        items = items.union(line)
    print 'extractItem', 'Nb items', len(items)
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
    prim_elements = frozenset()
    for key in Lk.keys():
        prim_elements = prim_elements.union(key)

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
    for setItems in Ck:
        for line in data:
            if setItems <= line:
                Lk[setItems] += data[line]

    return Lk


def removeBelowLimit(list, threshold):
    Lk = copy.deepcopy(list)
    for setItems in list:
        if list[setItems] < threshold:
            Lk.pop(setItems)

    return Lk


def writeItemsSet(Lk, filename):
    file = open(filename, "w+")

    # Lk = sorted(Lk, key=lambda k: k['distance'])
    nbSize = len(Lk)
    for i in range(0, nbSize):
        # for s in Lk[i].keys():
        for s,itm in sorted(Lk[i].iteritems(), key=lambda (item, support): support, reverse=True):
            file.write(" ".join([str(it) for it in s]) + ' (' + str(Lk[i][s]) + ') \n')

def sortFile(fileName):
    file = open(fileName, 'r')

    setline = []
    for line in file.readlines():
        setline.append({'set': line.strip().split('(')[0], 'support': int(line.strip().split('(')[1].split(')')[0])})

    file.close()
    setline = sorted(setline, key=lambda k: k['support'])

    fileOut = open(fileName, 'w')
    for line in setline:
        fileOut.write(line['set'] + '(' + str(line['support']) + ')\n')

    fileOut.close()

if __name__ == '__main__':
    start_time = time.clock()

	## Threshold but as 80% of the total number of line
    print apriori_based("Data/chess.dat", 3000, "Data/chess_output.dat")
    sortFile("Data/chess_output.dat")
    # print apriori_based("Data/chess_custom.dat", 2556, "Data/chess_custom_output3.dat")
	
    # print apriori_based("Data/mushroom.dat", 3000, "Data/mushroom_output.dat")
    # print apriori_based("Data/pumsb.dat", 46593, "Data/pumsb_output.dat")

    print("%s seconds" % (time.clock() - start_time))