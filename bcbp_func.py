## Author : Hamish Allan, 2007 - 2014, Nicolas Farrugia 2017

import sys
import gc
import probstat
import random
from utils import PriorityQueue
from sets import Set

def triad_perms(triad):
    return [''.join(x) for x in probstat.Permutation([c for c in triad])]

def group_distrib(group):
    distrib = []
    for triad in group:
        for i in range(3):
            c = triad[i]
            o = ord(c) - 65
            while len(distrib) <= o:
                distrib.append([0, 0, 0])
            distrib[o][i] = distrib[o][i] + 1
    return distrib

def group_distrib_scores(group_distrib):
    return [max(x) - min(x) for x in group_distrib]

class GroupNode:
    def __init__(self, group):
        self.group = group
        self.distrib = group_distrib(group)
        self.score = sum(group_distrib_scores(self.distrib))

    def __str__(self):
        return group.__str__()

    def successors(self):
        succs = []

        for triad_index in range(len(self.group)):
            triad = self.group[triad_index]
            perms = triad_perms(triad)
            for perm_index in range(len(perms)):
                new_perm = perms[perm_index]
                if (new_perm != triad):
                    new_group = list(self.group)
                    new_group[triad_index] = new_perm
                    
                    new_node = GroupNode(new_group)
                    if (new_node.score < self.score):
                        succs.append(GroupNode(new_group))

        return succs

def random_perm(triad):
    return random.choice(triad_perms(triad))

def bcbp_secondpass(groups):

    print len(groups)
    while len(groups) > 0:
        
        failures = []

        for group in groups:

            random_group = [random_perm(triad) for triad in group]
            first_node = GroupNode(random_group)
#            print first_node.group, first_node.distrib

            fringe = PriorityQueue(min, lambda node: node.score)
            fringe.append(first_node)

            if sum([sum(x) for x in first_node.distrib]) / len(first_node.distrib) == 3:
                goal_score = 0
            else:
                goal_score = len(first_node.distrib)

            visited = []
            while True:

                if len(fringe) == 0:
                    print 'No solutions'
                    break
                node = fringe.pop()
                visited.append(hash(tuple(node.group)))

                if len(visited) >= 10000:
#                    print 'failure!', len(visited)
                    failures.append(node.group)
                    break

                if node.score == goal_score:
#                    print
#                    print
#                    print 'success!', len(visited)
                    print node.group
                    print
                    break

                succs = node.successors()
                new_succs = [x for x in succs if hash(tuple(x.group)) not in visited]

                fringe.extend(new_succs)
                gc.collect()

        groups = failures
        print 'looping', len(failures)


