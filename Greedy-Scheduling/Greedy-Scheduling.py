from operator import attrgetter
class Task(object):
    """ Stores a task"""
    def __init__(self, num, w, l):
        self.num = num
        self.w = w
        self.l = l
        self.score = 0
        self.cost = 0

    def update_score(self, method='ratio'):
        if method == 'ratio':
            self.score = 1.0 * self.w / self.l
        else:
            self.score = self.w - self.l

class Schedule(object):
    """ Includes methods for optimal scheduling"""
    def __init__(self):
        self.size = 0
        self.tasks = []
        self.method = 'ratio'
        self._total_cost = 0

    def read_from_file(self, file_name):
        """ Reads the weights and lengths from a file"""
        file_handle = open(file_name)
        self.size = int(file_handle.readline())
        for i in range(self.size):
            line = file_handle.readline().split()
            self.tasks.append(Task(i, int(line[0]), int(line[1])))

    def update_score(self):
        """ Updates the score for a given method"""
        for task in self.tasks:
            task.update_score(method=self.method)

    def sort(self):
        """ Sorts the tasks based on score"""
        self.update_score()
        self.tasks.sort(key=attrgetter('score', 'w'), reverse=True)
        t = 0
        self._total_cost = 0
        for task in self.tasks:
            t += task.l
            task.cost = task.w * t
            self._total_cost += task.cost

    @property
    def total_cost(self):
        return self._total_cost


    def to_string(self):
        """ Displays the tasks"""
        print 'Task# Width Height Length Score Cost'
        for task in self.tasks:
            print task.num, task.w, task.l, task.score, task.cost
        print '**** Total Cost = ', self._total_cost



schedule = Schedule()
# schedule.read_from_file('test_case_61545_60213.txt')
schedule.read_from_file('jobs.txt')
schedule.method = 'ratio'
schedule.sort()
print schedule.total_cost