""" Solves the traveling salesman problem using a dynamic programming approach"""


class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty matrix representation of the graph. """
        self._a = []        # Dyamic programming 2D matrix
        self._prior = []        # Dyamic programming 2D matrix, pointing to one-before-last index k
        self._x = []        # x coordinates
        self._y = []        # y coordinates
        self.all_subsets = []        # a list of all possible sub-sets of the array
        self.n = 0          # Number of vertices, i.e. nodes

    def read_graph_from_file(self, file_name):
        """ Fills the x and y coordinates by reading the given file. Also, initializes the array self._a used
        in the Dynamic-Programming implementation of the TSP problem. Also fills the s array"""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        self.n = int(line)
        # Construct the 2D array for TSP
        print 'Constructing 2D array'
        row_a = [1e9 for _ in range(self.n + 1)]
        row_prior = [0 for _ in range(self.n + 1)]
        progress = 0
        for y in range(2**self.n):
            if y % (2**(self.n-3)) == 0:
                progress += 12.5
                print 'Construction progress', progress, '%'
            self._a.append(row_a[:])
            self._prior.append(row_prior[:])
        # self._a = [[float("inf") for x in range(self.n + 1)] for y in range(2**self.n)]
        print 'Constructing 2D array completed'
        self._a[1][1] = 0
        self._x = [0.0]*(self.n+1)
        self._y = [0.0]*(self.n+1)
        i = 0       # node index
        for line in lines[1:]:
            i += 1
            line_strings = line.split()
            self._x[i] = float(line_strings[0])
            self._y[i] = float(line_strings[1])
        # The i_s (index of s out of 2^n) when converted to binary tells us what elements are present
        # eg: 0'b101 means that nodes 1 and 3 are present whearas node 2 is not
        # Fill all_s
        print 'Forming list of sub-arrays...'
        self.all_subsets = self.sub_sets(range(1, self.n+1))

    @staticmethod
    def sub_sets(input_set):
        """ Returns the sub-sets of a given array"""
        n = len(input_set)
        result = [[] for _ in range(2**n)]
        for i in range(2**n):
            j = i
            for k in range(n):
                if j & 0x01:
                    result[i].append(input_set[k])
                j >>= 1
        return result

    def tsp(self):
        for m in range(2, self.n + 1):  # Sweep sub-problem size
            print 'calculating TSP sub-problems of size m=', m
            subset_index = -1        # indexes the subset number in the self.all_subsets array. Will come handy later
            for s in self.all_subsets:  # Look at all sub-sets of size m that include 1
                subset_index += 1
                if not len(s) == m or 1 not in s:
                    continue
                for j in s:     # For reach sub-set s, look at each possible last path ending-point
                    if j == 1:
                        continue
                    min_a = float('inf')
                    for k in s:     # For each j, look at all possible one-before-last nodes, k
                        if k == j:
                            continue
                        # print 'updating 2D matricx: m=', m, 's=', s, 'j=', j, 'subset_index=', subset_index,
                        # 'k=', k, 'recur=', self._a[subset_index-2**(j-1)][k] + self.distance(k,j),
                        # 'min_a(before)=', min_a
                        min_a = min(min_a,  self._a[subset_index-2**(j-1)][k] + self.distance(k, j))
                        # print 'min_a(after)=', min_a
                    self._a[subset_index][j] = min_a
                    # print self.a_string

        result = float('inf')
        for j in range(2, self.n + 1):
            result = min(result, self._a[2**self.n - 1][j] + self.distance(j, 1))
        return result

    def distance(self, i, j):
        """ Calculates the distance between two points indexed by i and j"""
        return ((self._x[i] - self._x[j])**2 + (self._y[i] - self._y[j])**2)**0.5

    @property
    def x(self):
        return self._x[1:]

    @property
    def y(self):
        return self._y[1:]

    @property
    def a(self):
        result = [[100 for _ in range(self.n)] for _ in range(2 ** self.n)]
        for i in range(2 ** self.n):
            for j in range(self.n):
                result[i][j] = self._a[i][j + 1]
        return result

    @property
    def a_string(self):
        """ Returns a in a printable string format"""
        result = ""
        for elem in self.a:
            result += str(elem) + '\n'
        return result

g = Graph()
g.read_graph_from_file('test_case_6.47.txt')
# g.read_graph_from_file('test_case_7.89.txt')
# g.read_graph_from_file('tsp.txt')
# g.read_graph_from_file('tsp_simplified01.txt')
tsp_result = g.tsp()
print 'TSP Result=', tsp_result
