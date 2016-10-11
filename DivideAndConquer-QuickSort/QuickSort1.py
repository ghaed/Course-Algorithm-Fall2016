import math
# Implements Quick Sort
# 9/18/2016

# Quick sort lifted to a class


class QuickSort:
    def __init__(self):
        self.comparison_count = 0
        self.logging = False
        return

    # Number of comparisons
    comparison_count = 0
    logging = False
    pivot_type = 'first'    # Type of pivot 'first'/'last'/'median'

    # Quick sort method
    # INPUTS
    # -a: input array
    def quick_sort(self, a, first_index, last_index):
        if self.logging:
            print 'Recursive call for sub-set of a=', a[first_index:last_index]
        if last_index-first_index <= 1:
            return

        # do the partitioning and return the pivot location
        pivot_index = self.partition(a, first_index=first_index, last_index=last_index)

        self.comparison_count += last_index - first_index - 1
        if self.logging:
            print 'After partitioning subset is=', a[first_index:last_index], ' Pivot index:', pivot_index

        self.quick_sort(a, first_index=first_index, last_index=pivot_index)     # Sort the left partition
        self.quick_sort(a, first_index=pivot_index+1, last_index=last_index)    # Sort the right partition

        return

    # Takes an array a and partitions it such that
    # [ {all elements<pivot} ,pivot, {all elements >pivot} ]
    # There are 3 pivot options: 'first', 'last', 'median'
    def partition(self, a, first_index, last_index):
        if self.pivot_type == 'first':      # Just use first element as pivot
            pass
        elif self.pivot_type == 'last':     # Swap first and last element
            a[first_index], a[last_index-1] = a[last_index-1], a[first_index]
        elif self.pivot_type == 'median':      # Swap first and median element
            mid_index = first_index + int(math.floor((last_index - 1 - first_index)/2))
            if a[first_index] < a[mid_index] < a[last_index-1] or a[last_index-1] < a[mid_index] < a[first_index]:
                median_index = mid_index
            elif a[first_index] < a[last_index-1] < a[mid_index] or a[mid_index] < a[last_index-1] < a[first_index]:
                median_index = last_index-1
            else:
                median_index = first_index
            a[first_index], a[median_index] = a[median_index], a[first_index]
        i = first_index + 1     # pointer to future pivot position
        for j in range(first_index+1, last_index):     # pointer to current element being swept
            # print "i,j:", i, j
            if a[j] < a[first_index]:
                a[j], a[i] = a[i], a[j]
                i += 1
        a[first_index], a[i-1] = a[i-1], a[first_index]     # Swap the pivot with the last element in the left partition
        return i-1     # Return the partitioned array and the location of the pivot


f = open('data.txt')
lines = f.readlines()
input_array = map(int, lines)
# input_array = [ 4, 6, 7, 1, 9, 12, 3, 99, 2, 5, 11]


for pivot_type in ['first', 'last', 'median']:
    test_array = input_array[:]
    q = QuickSort()
    q.pivot_type = pivot_type
    q.quick_sort(test_array, first_index=0, last_index=len(test_array))
    print ('after quick sort with pivot=:'), pivot_type, ':',  test_array
    print ('total number of comparisons:'), q.comparison_count
