""" Implement the KnapSack Algorithm """

class KnapsackRecursive(object):
    def __init__(self):
        self.w = []     # Weight array
        self.v = []     # Value array
        self.capacity = 0   # Total capacity, i.e. max total weight
        self.num_items = 0  # Number of items to consider
        self.solution_value = 0 # Final solution
        self.solutions = {}     # A hash table of the solutions

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
        self.v = [0]*(self.num_items + 1)
        self.w = [0]*(self.num_items + 1)
        i = 1
        for line in lines[1:]:
            if i % 100 == 0:
                print 'reading line ', i, '/', self.num_items
            line = line.rstrip()
            line_strings = line.split()
            self.v[i] = int(line_strings[0])
            self.w[i] = int(line_strings[1])
            i += 1

    def solve(self, num_remaining_items=-1, remaining_capacity=-1):
        """ Solves the Knapsap problem using a recursive approach
        Arguments:
        - remaining_capacity: remaining residual capacity, i.e. x
        - num_remaining_items: determines the items to look at, i.e. tells the function to look at
        self.v[0:num_remaining_items]
        """
        # Top case
        if num_remaining_items == -1 and remaining_capacity == -1:
            num_remaining_items = self.num_items
            remaining_capacity = self.capacity
            final_solution = True
        else:
            final_solution = False

        # Base case
        if num_remaining_items < 1:
            return 0

        # Cases that are already solved
        if (num_remaining_items, remaining_capacity) in self.solutions:
            return self.solutions[(num_remaining_items, remaining_capacity)]

        # Cases to be solved
        option_not_selected = self.solve(num_remaining_items-1, remaining_capacity)
        if self.w[num_remaining_items] > remaining_capacity:
            option_selected = option_not_selected
        else:
            option_selected = self.solve(num_remaining_items-1, remaining_capacity-self.w[num_remaining_items]) +\
                              self.v[num_remaining_items]
        solution_value = max(option_selected, option_not_selected)
        self.solutions[(num_remaining_items, remaining_capacity)] = solution_value
        if final_solution:  # Save the solution in class object
            self.solution_value = solution_value
        return solution_value

    @property
    def status(self):
        result = "i \tv \tw \n"
        for i in range(self.num_items + 1):
            result += str(i) + '\t'
            result += str(self.v[i]) + '\t'
            result += str(self.w[i]) + '\t'
            result += '\n'
        return result


import sys
sys.setrecursionlimit(10000) # 10000 is an example, try with different value

k = KnapsackRecursive()
# k.read_from_file('test_case_13.txt')
# k.read_from_file('test_case_5513.txt')
k.read_from_file('knapsack_big.txt')
# print k.status
k.solve()
# print k.status
print 'solution value =', k.solution_value
# solution_small = 2493893
# solution_big = 4243395
