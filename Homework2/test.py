from PQ import PriorityQueue # Old priority queue implementation
from Homework2 import *


test1 = [1,2,3,4,5,6,7,8,9,10]
print(UniformCostSearch(test1))

test2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(UniformCostSearch(test2))


test3 = [1,10,2,3,4,5,6,7,8,9]
print(UniformCostSearch(test3))


test4 = [10, 9, 8, 7, 6, 5, 4, 3, 1, 2]
print(UniformCostSearch(test4))

test5 = [1, 9, 8, 7, 6, 5, 4, 3, 2, 10]
print(UniformCostSearch(test5))
'''
test1 = [1,2,3,4,5,6,7,8,9,10]
print(AStar(test1))

test2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(AStar(test2))


test3 = [1,10,2,3,4,5,6,7,8,9]
print(AStar(test3))


test4 = [10, 9, 8, 7, 6, 5, 4, 3, 1, 2]
print(AStar(test4))

test5 = [1, 9, 8, 7, 6, 5, 4, 3, 2, 10]
print(AStar(test5))
'''

'''
test1 = [1,2,3,4,5,6,7,8,9,10]
print(goalCheck(test1))

test2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
print(goalCheck(test2))

test3 = [10, 9, 8, 7, 6, 5, 4, 3, 1, 2]
print(goalCheck(test3))

test4 = [1, 9, 8, 7, 6, 5, 4, 3, 2, 10]
print(goalCheck(test4))
'''
'''
# Testing Flip Function
test = [1,2,3,4,5,6,7,8,9,10]

flip(test, 0)
print(test)
flip(test, 0)
print(test)
print()

flip(test, 1)
print(test)
flip(test, 1)
print(test)
print()

flip(test, 2)
print(test)
flip(test, 2)
print(test)
print()

flip(test, 3)
print(test)
flip(test, 3)
print(test)
print()

flip(test, 4)
print(test)
flip(test, 4)
print(test)
print()

flip(test, 5)
print(test)
flip(test, 5)
print(test)
print()

flip(test, 6)
print(test)
flip(test, 6)
print(test)
print()

flip(test, 7)
print(test)
flip(test, 7)
print(test)
print()

flip(test, 8)
print(test)
flip(test, 8)
print(test)
print()

flip(test, 9)
print(test)
flip(test, 9)
print(test)
print()
'''

'''
#Quick Priority Queue Testing
q = PriorityQueue()

q.push([1,2,3,5,6,7,8,9,10], 0)
q.printHeap()

q.push([1,2,3,5,6,7,9,8,10], -1)
q.printHeap()

q.push([1,2,3,6,5,7,8,9,10], 3)
q.printHeap()

q.pop()
q.printHeap()

q.pop()

q.printHeap()

q.push([1,2,3,5,6,7,8,9,10], 4)
q.printHeap()

q.decreaseKey([1,2,3,5,6,7,8,9,10], -2)
q.printHeap()
'''