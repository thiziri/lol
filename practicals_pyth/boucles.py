import os
import sys
import io

# if else elif
age = 25
if age < 18 :
    print("you are not allowed to drive")
else:
    print("OK to drive ! \n GOOD LUCK ;)")
if age >= 6 :
    print('you are old enough to go to school')
elif age > 25:
    print('ok')
# else : print('No')

# possibilité de faire des 'elif' ou 'if' sans 'else'

# if c1 and c2 or c3

age2 = 20
if (age==25) or age2>30 :
    print('OK \n')
else : print('NO')


#**********boucles : looping

# not ((c1) or (c2) and (c3))

for x in range (0,10) :
    print (x," ", end="")

print('\n')
l= ['e1', 'e2', 'e3', 4, 5]
for y in l :
    print (y,' ', end="")

l2= [[1,2,3],[4,5,6],['a','b','c']]

for x in range(0,3) :
    for y in range (0,3) :
        print (' ', l2[x][y],end="")

print('\n')

'''  ceci est  possible !!!!!!!

for x in range(0,3) :
    for y in  l2[x] :
        print (' ', y, end="")
'''







