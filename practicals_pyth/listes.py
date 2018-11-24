import random
import sys
import os


list = ['juce', 2, '50', 3]
print("item 1: ", list[0])
print("item 2: ", list[1])
n = list[1]
print("nmbre ", n)
list[1] = 'jdbc'
print("item 2: ", list[1])

print(list[0:4])
print("list à %s" % len(list), "éléments")
print('\n' * 3)
list1 = [1, 2, 3]
list2 = [4, 5, 6, 7]
list = list1 + list2
print(list)
list3 = [list1, list2]
print(list3)
list3.append(8)
print(list3)
list.insert(0, "premier")
print(list)
list.remove("premier")
print(list)
list.reverse()
print(list)
list.sort()
print(list)
print("max(list)= %s" % max(list))
del list[2]
print(list)









