## Author : Hamish Allan, 2007 - 2014, Nicolas Farrugia 2017

import bcbp_func
import sys
import gc
import probstat
import random
from utils import PriorityQueue
from sets import Set

def whole(n):
    return n == int(n) and n != 1

def groupnums(numpieces):
    r = []
    numcoms = len(probstat.Combination(range(numpieces), 3))
    numofeachletter = float(numcoms * 3) / numpieces
    for numgroups in range(2, numcoms):
        comspergroup = float(numcoms) / numgroups
        eachletterpergroup = numofeachletter / numgroups
        if whole(comspergroup) and whole(eachletterpergroup):
            r.append(numgroups)
    return r

def groupsizes(numpieces):
    r = []
    numcoms = len(probstat.Combination(range(numpieces), 3))
    numofeachletter = float(numcoms * 3) / numpieces
    for numgroups in range(2, numcoms):
        comspergroup = float(numcoms) / numgroups
        eachletterpergroup = numofeachletter / numgroups
        if whole(comspergroup) and whole(eachletterpergroup):
            r.append(numcoms / numgroups)
    return r

def var(l):
    n = len(l)
    m = float(sum(l)) / n
    return sum([(i - m) * (i - m) for i in l]) / (n - 1)

class Node:
    def __init__(self, groups, distrib):
        self.groups = groups
        self.distrib = distrib
        self.score = sum([var(i) for i in distrib])

    def __str__(self):

        return '\n\n'.join(['\n'.join([' '.join([''.join(i) \
            for i in probstat.Permutation([c for c in triad])]) \
                for triad in group]) \
                    for group in self.groups])

#        return '\n\n'.join([' '.join([''.join([''.join(c) \
#            for c in triad]) \
#                for triad in group]) \
#                    for group in self.groups])

    def successors(self):
        numgroups = len(self.groups)
        eachletter = sum(self.distrib[0]) / len(self.distrib[0])

        succs = []
        for groupnum in range(numgroups):
            if len(succs) > 2:
                break

            d = self.distrib[groupnum]
            overletters, underletters = [], []
            for i in range(len(d)):
                if d[i] > eachletter:
                    overletters.append(chr(65 + i))
                elif d[i] < eachletter:
                    underletters.append(chr(65 + i))

            group = self.groups[groupnum]

            for overletter in overletters:
                offeredtriads = [triad for triad in group if overletter in triad]
                for offeredtriad in offeredtriads:
                    for underletter in underletters:
                        if underletter in offeredtriad:
                            continue
                        wantedlist = [c for c in offeredtriad.replace(overletter, underletter)]
                        wantedlist.sort()
                        wantedtriad = ''.join(wantedlist)
                        for othergroupnum in range(numgroups):
                            if othergroupnum == groupnum:
                                continue
                            othergroup = self.groups[othergroupnum]
                            if wantedtriad in othergroup:
                                newgroups = [[i for i in j] for j in self.groups]
                                newdistrib = [[i for i in j] for j in self.distrib]
                                groupcopy = newgroups[groupnum]
                                othergroupcopy = newgroups[othergroupnum]
                                groupcopy[groupcopy.index(offeredtriad)] = wantedtriad
                                othergroupcopy[othergroupcopy.index(wantedtriad)] = offeredtriad
                                underletterpos = ord(underletter) - 65
                                overletterpos = ord(overletter) - 65
                                newdistrib[groupnum][overletterpos] -= 1
                                newdistrib[groupnum][underletterpos] += 1
                                newdistrib[othergroupnum][overletterpos] += 1
                                newdistrib[othergroupnum][underletterpos] -= 1
                                newnode = Node(newgroups, newdistrib)
                                succs.append(newnode)
                                break
        return succs

def firstNode(numpieces, groupsize):

    pieces = [chr(65 + i) for i in range(numpieces)]
    coms = [''.join(triad) for triad in probstat.Combination(pieces, 3)]
    numcoms = len(coms)
    numgroups = numcoms / groupsize
    groups = [[coms[j] for j in range(i, numcoms, numgroups)] \
        for i in range(0, numgroups)]
    used = [[j for j in ''.join(i)] for i in groups]
    distrib = [[len([i for i in u if i == piece]) \
        for piece in pieces] for u in used]

    return Node(groups, distrib)

def main():

    if len(sys.argv) < 2:
        print 'Usage: python %s <number of pieces> <group size>' % (sys.argv[0])
        return
    if len(sys.argv) == 2:
        numpieces = int(sys.argv[1])
        gs = groupsizes(numpieces)
        if len(gs) == 1:
            numgroups = gs[0]
        else:
            print 'Usage: python %s %d [ %s ]' % (sys.argv[0], numpieces, \
                ' | '.join([str(i) for i in gs]))
            return

    if len(sys.argv) == 3:
        numpieces = int(sys.argv[1])
        numgroups = int(sys.argv[2])

    fringe = PriorityQueue(min, lambda node: node.score)

    node = firstNode(numpieces, numgroups)
    fringe.append(node)

    while True:
        if len(fringe) == 0:
            print 'No solutions'
            break
        node = fringe.pop()
        print node.score
        if node.score == 0: # goal state
            break
        fringe.extend(node.successors())
        if len(fringe.A) > 100:
            fringe.A = fringe.A[:100]
        gc.collect()

    print node.score
    print node.groups
    print node.distrib
    
    bal_groups = bcbp_func.bcbp_secondpass(node.groups)
    
    print "-------------final result-------------"
    if len(bal_groups) == 0:
        print "failed"
    else:
        bcbp_func.write_stimlist(bal_groups)
    
        print "-------------SUCESSFUL !-------------"

if __name__ == '__main__':
    main()

