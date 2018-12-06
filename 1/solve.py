# solve.py  1
#

from simpleeval import simple_eval

content = open("input.txt").read().replace('\n','')

# simple_eval can't handle an expression this big! sod it, use eval
# print(simple_eval(content))
print(eval(content))
