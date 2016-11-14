""" Calculates the median using heap"""
import heapq

f = open('test_case_large.txt')
lines = f.readlines()
x_list = [int(numeric_string) for numeric_string in lines]
# x_list = [1, 2, 3, 4, 5]

heap_high = []  # Min- heap
heap_low = []   # Also min-heap, stored as negative numbers
medians_sum = 0

x0 = x_list[0:3]
larger = max(x_list[0:3])
smaller = min(x_list[0:3])
x0.remove(larger)
x0.remove(smaller)
median = x0[0]
medians_sum += x_list[0] + min(x_list[0:2]) + median

heapq.heappush(heap_high, larger)
heapq.heappush(heap_low,  -smaller)


for x in x_list[3:]:
    smaller = min(x, median)
    larger = max(x, median)
    if len(heap_low) == len(heap_high):
        heapq.heappush(heap_high, larger)
        if smaller < -heap_low[0]:
            median = -heapq.heappop(heap_low)
            heapq.heappush(heap_low, -smaller)
        else:
            median = smaller
    else:
        heapq.heappush(heap_low, -smaller)
        if larger > heap_high[0]:
            median = heapq.heappop(heap_high)
            heapq.heappush(heap_high, larger)
        else:
            median = larger
    medians_sum = (medians_sum + median)%10000

print 'median=', median, ', medians_sum=', medians_sum
