""" Calculates the two-sum problem using hashing"""


f = open('test_case_large.txt')
lines = f.readlines()
x_list = [int(numeric_string) for numeric_string in lines]
# x_list = [1, 2, 3, 4]

h = {}      # Form the hash table. h[x] is the number of x's in x_list
# for x in x_list:
#     if x in h:
#         h[x] += 1
#     else:
#         h[x] = 1

for x in x_list:
    h[x] = True

# t_list = [1, 4, 45, 6, 10, 10, 8]
# t_list = [4, 5, 9, 1, 3]
t_list = range(-10000,10001)
count = 0
for t in t_list:
    if t%100 == 0:
        print 't=', t, 'count=', count
    for x in x_list:
        if t-x in h and t-x != x:
            count += 1
            break


print count