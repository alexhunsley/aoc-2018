# pythonObjects.py
#
# Ways of defining objects etc

from types import *
from collections import namedtuple

# plain old class.
# repr gives just address, e.g. '<__main__.Cls object at 0x107cd5390>'.
# equality is by object address.
# no param init provided.
class Cls:
	pass

a = Cls()
a.age = 7
a.name = 'Alex'
print('Plan class. a =', a)
# remove 'a' from instance
del a.age
a.age = 7

b = Cls()
b.age = 7
b.name = 'Alex'

print('Plain class. a == b: %s' % (a == b))


##########################################################
# SimpleNamespace

# Can pass arbitrary stuff into init.
# Nice repr ('eval(repr)' makes the object).
# equality defined based on properties dict.
# 
a = SimpleNamespace()
a.age = 7
a.name = 'Alex'
print('SimpleNamespace: a =', a)

b = SimpleNamespace(age = 7, name = 'Alex')

print('SimpleNamespace: a == b: %s' % (a == b))

##########################################################
# namedtuple

Point = namedtuple('Point', ['x', 'y'])

p = Point(11, y=22)
# readable repr
print('namedtuple: p =', p)

t=eval(repr(p))
print('made t from repr:', t)

print('sum: ', p[0] + p[1]) 
print('sum: ', p.x + p.y) 
x, y = p


