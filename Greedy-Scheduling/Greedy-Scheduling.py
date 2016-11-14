class Schedule(object):
    """ Includes methods for optimal scheduling"""
    def __init__(self):
        self.w = []     # List of weights indexed by task numbers
        self.l = []     # List of lengths indexed by task numbers
        self.score = []

    def read_from_file(self, file_name):
        file_handle = open(file_name)
        if 




schedule = Schedule()
