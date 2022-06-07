from numpy import matrix
from numpy import linalg
from math import *
import copy
import itertools
import sys
import os

M = [
        [1000, 5, 1, 20, 10],
        [20, 1000, 1, 4, 10],
        [1, 20, 1000, 3, 10],
        [18, 4, 3, 1000, 10],
        [30, 10, 0, 10, 1000]
    ]

"""
(a) Use exact DP with starting city A to verify that the optimal tour is ABDECA with cost 20.
"""

def tsp(init, nodes):
    if((nodes==[]) and (init == 0)):
        return 0
    if((nodes==[]) and (init != 0)):
        return M[init][0]
    for i in nodes:
        nodes.remove(i)
        return M[init][i] + tsp(i, nodes)

def main_tsp(listOfNodes):
    minCost = 10000
    path = []
    for j in listOfNodes:
        liste = []
        for k in j:
            liste.append(k)
        tmp = copy.deepcopy(liste)
        val = tsp(0, liste)
        if (minCost > val):
            minCost = val
            path = tmp
    displayPath(minCost, path)

def displayPath(minC, path):
    p = []
    sc = [0]
    path.extend(sc)
    sc.extend(path)
    print('\n a) ************ Traveling salesman using dynamic programming ******************\n')
    display(minC, sc)
    
def display(minC, sc):
    p = []
    print('0, 1, 2, 3 and 4 respectively represent A, B, C, D and E\n')
    print('The minimum cost of the shortest path is : '+ str(minC))
    print('The path using numbers to represent cities is : ' + str(sc))
    for i in sc:
        if (i == 0): p.append('A')
        if (i == 1): p.append('B')
        if (i == 2): p.append('C')
        if (i == 3): p.append('D')
        if (i == 4): p.append('E')
    print('The corresponding path using letters is : ' + str(p)+'\n')

"""
(b) Verify that the nearest neighbor heuristic starting with city A generates
the tour ACDBEA with cost 48.
"""

def NearestNeighborBaseHeuristic(init, nodes):
    visited =[init]
    unvisited = nodes
    currentNode = init
    minCost = 0
    while (len(visited) < len(M[0])):
        tmp = {}
        for j in unvisited:
            v = M[currentNode][j]
            tmp[v] = j
        if (tmp!={}):
            valMin = min(tmp.keys())
            node = tmp[valMin]
            minCost = minCost + valMin
            currentNode = node
            visited.append(currentNode)
            unvisited.remove(node)
    minCost = minCost +  M[currentNode][init]
    visited.append(init)
    print('\n\n b) ******** Traveling salesman using nearest neighbor base heuristic *********\n')
    display(minCost, visited)

"""
(c) Apply rollout with one-step lookahead minimization, using as base heuristic
the nearest neighbor heuristic. Show that it generates the tour AECDBA
with cost 37.
"""

def rolloutOneStep(init, nodes, startCity):
    visited =[init]
    unvisited = nodes
    currentNode = init
    minCost = 0
    while (len(visited) < len(M[0])-1):
        tmp = {}
        for j in unvisited:
            v = M[currentNode][j]
            tmp[v] = j
        if (tmp!={}):
            valMin = min(tmp.keys())
            node = tmp[valMin]
            minCost = minCost + valMin
            currentNode = node
            visited.append(currentNode)
            unvisited.remove(node)
    minCost = minCost +  M[currentNode][startCity]
    visited.append(startCity)
    return minCost, visited

def main_rollout(startCity, nodes):
    nodesInit = copy.deepcopy(nodes)
    liste = []
    for i in nodes:
        init = i
        nodesInit.remove(i)
        tmp1 = copy.deepcopy(nodesInit)
        t = rolloutOneStep(init, tmp1, startCity)
        u = M[0][i] + t[0]
        liste.append(u)
        nodesInit.append(init)
    minCost = min(liste)
    lt = [startCity]
    lt.extend(t[1])
    print('\n\n c) ******* Traveling salesman using rollout with one-step lookahead ... ******\n')
    display(minCost, lt)


"""
(d) Apply rollout with two-step lookahead minimization, using as base heuristic
the nearest neighbor heuristic.
"""

def rolloutTwoStep(init, nodes, startCity):
    visited =[init]
    unvisited = nodes
    currentNode = init
    minCost = 0
    while (len(visited) < len(M[0])-2):
        tmp = {}
        for j in unvisited:
            v = M[currentNode][j]
            tmp[v] = j
        if (tmp!={}):
            valMin = min(tmp.keys())
            node = tmp[valMin]
            minCost = minCost + valMin
            currentNode = node
            visited.append(currentNode)
            unvisited.remove(node)
    minCost = minCost +  M[currentNode][startCity]
    visited.append(startCity)
    return minCost, visited

def main_rolloutTwoStep(startCity, nodes):
    listePerm = []
    dico = {}
    for i in nodes:
        l = copy.deepcopy(nodes)
        l.remove(i)
        listePerm.extend(list(itertools.permutations(l)))
        for t in listePerm:
            tl = list(t)
            k = tl[0]
            tl.remove(k)
            res = rolloutTwoStep(k, tl, 0)
            dico[res[0]] = res[1]
    minVal = min(dico.keys())
    stepNode = -1
    path = dico[minVal]
    for i in range(len(M)):
        if (i not in path):
            stepNode = i
    minVal = minVal + M[stepNode][path[startCity]] + M[startCity][stepNode]
    s = [startCity, stepNode]
    s.extend(path)
    path = s
    print('\n\n d) ******* Traveling salesman using rollout with two-step lookahead ... ******\n')
    display(minVal, path)


cities = [2, 1, 3, 4]
listOfCites = tuple(itertools.permutations(cities))
main_tsp(listOfCites)

NearestNeighborBaseHeuristic(0, cities)

citiesR = [2, 1, 3, 4]
main_rollout(0, citiesR)

main_rolloutTwoStep(0, citiesR)



"""
(e) Estimate roughly the complexity of the computations in parts (a), (b), (c),
and (d), assuming a generic N-city traveling salesman problem.

Answer: The exact DP algorithm requires O(N^5) computation.
The nearest neighbor heuristic that starts at city A performs
O(N) comparisons at each of N stages, so it requires O(N^2) computation.
The rollout algorithm at stage k runs the nearest neighbor heuristic N − k
times, so it must run the heuristic O(N^2) times for a total computation
of O(N^4).

"""
print('\n (e) Estimate roughly the complexity of the computations in parts (a), (b), (c), and (d)')
print('Answer: The exact DP algorithm requires O(N^5) computation.')
print('The nearest neighbor heuristic that starts at city A performs O(N) comparisons at each of N stages, so it requires O(N^2) computation.')
print('The rollout algorithm at stage k runs the nearest neighbor heuristic N − k times, so it must run the heuristic O(N^2) times for a total computationof O(N^4).\n\n')






