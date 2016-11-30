""" Implement the KnapSack Algorithm """

class Knapsack(object):
    def __init__(self):
        self.w = []     # Weight array
        self.v = []     # Value array
        self.capacity = 0   # Total capacity
        self._a = []         # Solution Matrix
        self.num_items = 0  #

    def read_from_file(self, file_name):
        """ Reads from a file.
        First row is self.capacity self.num_items
        All other rows have the value weight format ..."""
        f = open(file_name)
        lines = f.readlines()
        line = lines[0].rstrip()
        line_strings = line.split()
        self.capacity = int(line_strings[0])
        self.num_items = int(line_strings[1])
        self._a = [[0]*(self.capacity + 1)]*(self.num_items + 1)
        self.v = [0]*self.num_items
        self.w = [0]*self.num_items
        i = 0
        for line in lines[1:]:
            line = line.rstrip()
            line_strings = line.split()
            self.v[i] = int(line_strings[0])
            self.w[i] = int(line_strings[1])
            i += 1

    def solve(self):
        """ Solves the Knapsap problem by filling the array self.a """
        for i in range(1, self.num_items + 1):
            for x in range(self.capacity + 1):
                option_selected = self._a[i-1][x]
                option_not_selected = self._a[i-1][x-self.w[i-1]] + self.v[i-1]
                self._a[i][x] = max(option_selected, option_not_selected)

    @property
    def a(self):
        result = ""
        for line in self._a:
            result += str(line) + '\n'
        return result

    @property
    def status(self):
        result = "v \tw \ta \n"
        for i in range(self.num_items):
            result += str(self.v[i]) + '\t'
            result += str(self.w[i]) + '\t'
            result += str(self._a[i])
            result += '\n'
        return result



k = Knapsack()
k.read_from_file('test_case_13.txt')
print k.status
k.solve()
print k.status

