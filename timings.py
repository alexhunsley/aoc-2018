from timeit import timeit

'''
A big comment!

here
''' and None

s = """\
import numpy

a = numpy.array([0,1,2])
b = numpy.array([3,4,5])
c = a + b
"""

t = timeit(s)
print("numpy + operator", t)


s = """\
a = [1, 2, 3]
b = [3, 2, 1]

c = [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
"""

t = timeit(s)
print("Straightforward addition: ", t)


s = """\
a = [1, 2, 3]
b = [3, 2, 1]

a[0] += b[0]
a[1] += b[1]
a[2] += b[2]
"""

t = timeit(s)
print("Straightforward addition in-place: ", t)

# In Python 3, built in zip is same as izip now!
s = """\
a = [1, 2, 3]
b = [3, 2, 1]

c = map(sum, zip(a,b))
"""

t = timeit(s)
print("map(sum, zip(a, b)) ", t)



s = """\
a = [1, 2, 3]
b = [3, 2, 1]
for i, bi in enumerate(b): a[i] += b[i]
"""

t = timeit(s)
print("enumerate with index, add in-place", t)



s = """\
a = [1, 2, 3]
b = [3, 2, 1]
c = [0, 0, 0]
for i, bi in enumerate(b): c[i] = a[i] + b[i]
"""

t = timeit(s)
print("enumerate with index, add", t)





