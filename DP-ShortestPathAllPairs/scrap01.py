n = 2
a = [[float("inf") for x in range(n + 1)] for y in range(n + 1)]
a[0][0] = 1
a[0][1] = 2
a[1][1] = -1
print min(min(a))