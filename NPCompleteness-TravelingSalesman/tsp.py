""" Solves the traveling salesman problem using a dynamic programming approach"""

class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty matrix representation of the graph. """
        self._a = []        # Dyamic programming 2D matrix
        self._x = []        # x coordinates
        self._y = []        # y coordinates
        self._all_s = []        # a list of all possible sub-sets of the array
        self.n = 0          # Number of vertices, i.e. nodes

    def read_graph_from_file(self, file_name):
        """ Fills the x and y coordinates by reading the given file. Also, initializes the array self._a used
        in the Dynamic-Programming implementation of the TSP problem. Also fills the s array"""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        self.n = int(line)
        # Construct the 3D array for TSP
        self._a = [[float("inf") for x in range(self.n + 1)] for y in range(2**self.n)]
        for i in range(0, 2**self.n):  # Distance to self is zero
            self._a[i][1] = 0
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

    @property
    def a(self):
        result = [[float("inf") for x in range(self.n)] for y in range(2**self.n)]
        for i in range(2**self.n):
            for j in range(self.n):
                result[i][j] = self._a[i][j+1]
        return result

    def tsp(self):
        for m in range(2, self.n + 1):
            for i_s in range(1, 2**2):
                pass


    @property
    def x(self):
        return self._x[1:]

    @property
    def y(self):
        return self._y[1:]


g = Graph()
g.read_graph_from_file('test_case_6.47.txt')
print g.a
