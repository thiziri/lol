import sys
import io

pi_tuple = (3,1,2,1,4)
print("tuple ", pi_tuple)
l1 = list(pi_tuple)
print("list ", l1)
n = pi_tuple.count(1)
print("1 apparais %d " % n, " fois")
ntuple = tuple(l1)
print("tuple créé ", ntuple)

# main functions with lists but we can't modify the tuple after creating it


# dictionnary in python

dicFrEn = {'good' : 'bien',
           'bad' : 'mauvais',
           'cat' : 'chat'}
# print(dicFrEn['chat'])  erreur l'interrogation se fais dans le sens opposé
print(dicFrEn['good'])
print("Dictionnaire Anglais Français : ",dicFrEn)
del dicFrEn['cat']
print("Dictionnaire Anglais Français : ",dicFrEn)
dicFrEn['bad'] = 'mauvaise'
print("Dictionnaire Anglais Français : ",dicFrEn)
print("dicFrEn a %d " % len(dicFrEn), "éléments \n ok")
cle = list(dicFrEn.keys())
print(cle, "\n")
print("valeurs ", dicFrEn.values(),"\n")
