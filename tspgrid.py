
from collections import defaultdict
import itertools
import math
import pprint
import copy

#for debugging
pp = pprint.PrettyPrinter()
def printmatrix(arrry2d):
    for bla in arrry2d:
        print(bla)
    print()

class Graph():
    def __init__(self, dimensions):
        self._g = {}
        self.dimensions = dimensions
    
    #adds 2 nodes to weighted graph
    def add(self, n1, n2, w):
        if n1 not in self._g:
            edges = {}
            self._g[n1] = edges
        if n2 not in self._g:
            edges = {}
            self._g[n2] = edges
        self._g[n1][n2] = w
        self._g[n2][n1] = w
        
    
    def create_distance_matrix(self):
        m, n = self.dimensions
        
        distances = [[math.inf]*(m*n+1) for i in range((m*n+1))] #max size 101*101
        for n1 in self._g.keys():
            for n2 in self._g[n1]:
                i = self.node_index(n1)
                j = self.node_index(n2)
                weight = self._g[n1][n2]
                distances[i][j] = weight
        return distances
    
    #not needed anymore (for previous iteration)
    def make_bits(self, subset):
        #the point of the bits is to make a unique indicator for which nodes are in the subset
        #subset looks like [(1,1), ... (i,j), ...()]
        bits = 0
        for k in subset:
            bits |= (1<<k)
        return bits
    
    def node_index(self, node):
        i = node[0]
        j = node[1]
        return j + (i-1)*self.dimensions[1]
    
    def distances(self, start,end, distances):
        row = self.node_index(start)
        col = self.node_index(end)
        return distances[row][col]
        
    
    def get_new_paths(self, prev_endpoint, prev_path, pathlength, distances):
        #given a path, check to see if new paths can be made by stepping one node in a cardinal direction
        i, j = prev_endpoint[0], prev_endpoint[1]
        left_right_up_down = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
        new_paths = []
        for endpoint in left_right_up_down:
            row, col = endpoint[0], endpoint[1]

            #boundaries
            if row < 1 or row > m or col < 1 or col > n:
                continue
            #already visited
            if prev_path[row][col] !=-1:
                continue
            #path is a new possible path that works
            newpath = copy.deepcopy(prev_path)
            dist = self.distances((i,j),(row,col),distances)
            newpath[row][col] = prev_path[i][j] + dist
            new_paths.append((newpath,endpoint, pathlength+1))
        return new_paths
            
    def start_path_len2(self,distances):
        m,n = self.dimensions
        two_edge_paths = []
        
        path1 = [[-1 for x in range(n+1)] for y in range(m+1)]
        path1[1][1] = 0
        path1[1][2] = self.distances((1,1),(1,2), distances)
        two_edge_paths.append((path1,(1,2),2))
        
        #one of 1,2 and 2,1 must be the beginning, the other must be the end, direction symmetry means I can halve the number of paths
        return two_edge_paths
    
        #brainstorm notes--- other ways to encode graphs
        #different ways to encode a graph:
        #left-right-straight...
        #save the graph as a set of nodes that hit
        #graph w/ order
        # like: [[1,2],[4,3]] for counterclockwise
        #all_paths = [prev_paths=[pl]]
        #rearrange matrix to be [[2 edge paths], [3 edge paths...]] maybe?
    
    def get_minimum_full_path_distance(self, potential_end_paths, distances):
        min_path_dist = math.inf
        for path, endpoint, pathlength in potential_end_paths:
            
            #2,1 is the end, don't need to check
            if endpoint == (2,1) and path[2][1]+self.distances((1,1),(2,1), distances) < min_path_dist:
                min_path_dist = path[2][1]+ self.distances((1,1),(2,1), distances)
        return min_path_dist
    
    def find_possible_paths(self,distances):
        m,n = self.dimensions
       
        all_paths = []
        all_paths.append(self.start_path_len2(distances))
        pathlength = 2
        
        while  pathlength < m*n:
            prev_paths = all_paths[pathlength-2]
            
            paths_of_size_prevplusone = []
            #for each path length of size pathlength, generate new posible paths of len pathlength+1, add them to paths_of_size_prevplusone, then do so again with the next size of pathlen
            for prev_path, prev_endpoint, pathlength in prev_paths:
                some_new_paths = self.get_new_paths(prev_endpoint, prev_path, pathlength, distances)
                for new_path, new_endpoint, newpathlength in some_new_paths:
                    paths_of_size_prevplusone.append((new_path, new_endpoint, newpathlength))
            all_paths.append(paths_of_size_prevplusone)
            pathlength +=1
        
        potential_end_paths = all_paths[-1]
        dist = self.get_minimum_full_path_distance(potential_end_paths, distances)
        return dist

         
    def tsp(self):
        if self.dimensions == (1,1):
            return 0
        
        distances = self.create_distance_matrix()
        total_dist = self.find_possible_paths(distances)
        if total_dist == math.inf:
            return 0
        return total_dist
        
m,n = input().strip().split()
m, n = [int(m), int(n)]

def create_graph(g, dimensions):
    m = dimensions[0]
    n = dimensions[1]
    for i in range(1, m+1):
        line = input().strip().split()
        for j in range(1, n):
            weight = int(line[j-1])
            g.add((i,j),(i,j+1), weight)
    for i in range(1, m):
        line = input().strip().split()
        for j in range(1, n+1):
            weight = int(line[j-1])
            g.add((i,j), (i+1, j), weight)
    return g

dimensions = (m,n)
g = Graph(dimensions)
g = create_graph(g, dimensions)
soln = g.tsp()
print(soln)


