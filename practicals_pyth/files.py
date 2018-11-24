import sys
import os

print("nom de votre fichier : ") #C:\Users\Thiziri\Desktop
nomF = sys.stdin.readline()
chemin = "C:/Users/Thiziri/Desktop/"
nomF = chemin + nomF
print("fichier à ouvrire : ",nomF)
f = open(nomF.strip('\n'),"a+")

'''
lors de la saisi en python, la chaine saisie contient toujours le caractère \n
donc il faut l'éliminer via la fonction : strip('\n')

modes d'ouverture : r, w, a (pour append : ajouter à la fin)
'''

f.write("chaine rajoutée\n")
# f.close()
f = open(nomF.strip('\n'),'r')
ligne = f.read()
print("contenu lu : ", ligne)

os.remove(chemin+"a.txt")




