
import random
import sys

def factoriel (n) :
    if (n <= 1) : return 1
    else : return n * factoriel(n-1)
print ("factoriel 4 est %d " % factoriel (4), "\n terminé.")

# fonctions mathématiques

n = random.randrange(0 , 10)
print("n= %d" % n)

while (n != 9):
    print ('n= %d' % n)
    n= random.randrange(0 , 10)


i = 0;
while (i <=20) :  # afficher tout les nombres pairs <= 20
    if (i%2 ==0) :
        print (i)
    elif (i == 21) :
        break
    else :
        i += 1
        continue
    print("-----suite-----")
    i +=1

def add (a , b):
    return a + b

print("4 + 5 = %d" % add(4,5))

print("what's your name ?")
name = sys.stdin.readline()
print("hellow %s" % name)

# manipulation de chaines de caractères comme vecteurs

ch = "I'll get your work next week okay !"

print(ch[0:4]) # prints a 4 first characters
print(ch[-6:]) # prints a 6 last characters
print(ch[:-6]) # prints a string except a last 6 characters
print(ch[:4] + " be okay :-)") # prints 4 first characters concatenated with the added string
print("%c is my %s character and my number is %d is %.5f" % ('M',"favorite",23,.1))
#affichera 0.10000 :%.5f
str = "i'll catch you if you fall in the floor"
str2 = str.capitalize()
print("le resultat : \n %s \n capitalisée : %s " % (str,str2.upper()))
print ("le mot floor se trouve dans la position : ", str2.find("floor"))






