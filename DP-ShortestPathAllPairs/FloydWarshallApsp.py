class Graph(object):
    """ Defines a graph"""

    def __init__(self):
        """ Constructor to initialize an empty matrix representation of the graph. """
        self.a = []         # Each node number will be its hash
        self.n = 0          # Number of vertices, i.e. nodes
        self.m = 0          # Number of arcs, i.e. edges

    def read_graph_from_file(self, file_name):
        """ Fills self.a[0] with the matrix representation of the graph which is suited for Floyd-Warshall algorithm
        Note that indexing of a[n][n] follows Python's 0..n-1 notation"""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        line_strings = line.split()
        self.n = int(line_strings[0])
        self.m = int(line_strings[1])
        # Construct the 3D array for Floyd-Warshall algorithm
        self.a = [[[float("inf") for x in range(self.n + 1)] for y in range(self.n + 1)] for z in range(2)]
        for i in range(1, self.n + 1):  # Distance to self is zero
            self.a[0][i][i] = 0

        for line in lines[1:]:
            line_strings = line.split()
            node_id_a = int(line_strings[0])
            node_id_b = int(line_strings[1])
            length = int(line_strings[2])
            self.a[0][node_id_a][node_id_b] = length

    def floyd_warshall(self):
        """ Solves the all-pairs shortest path problem using Floyd-Warshall algorithm"""
        for k in range(1, self.n + 1):
            print 'k=', k
            for i in range(1, self.n + 1):
                for j in range(1, self.n + 1):
                    choice_1 = self.a[0][i][j]
                    choice_2 = self.a[0][i][k] + self.a[0][k][j]
                    self.a[1][i][j] = min(choice_1, choice_2)

            for i in range(1, self.n + 1):  # Copy new lengths to the array to conserve space
                for j in range(1, self.n + 1):
                    self.a[0][i][j] = self.a[1][i][j]

    def has_neg_cost_cycle(self):
        for i in range(1, self.n + 1):
            if self.a[1][i][i] < 0:
                return True
        return False

    @property
    def min_path_len(self):
        cur_min = float("inf")
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                cur_min = min(self.a[1][i][j], cur_min)
        return cur_min



g = Graph()
# g.read_graph_from_file('test_case_-6.txt')
# g.read_graph_from_file('test_case_-10003.txt')
g.read_graph_from_file('g3.txt')
g.floyd_warshall()
# print g.a[1]
print g.has_neg_cost_cycle()
print g.min_path_len

# g1-> Has negative cycle
# g2 -> Has negative cycle
# g3 -> -19