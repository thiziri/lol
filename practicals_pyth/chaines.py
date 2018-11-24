import sys
import io

ch = "youïç hdgcu ghsf"
print("alphanumérique : ",ch.isalnum())
print("decimale : ",ch.isdecimal())
print("alphabétique : ",ch.isalpha()) # est vrai si la chaine ne contient que des caractères alphabétiques sans
print(len("hello !"))
print("strip : ",ch.strip('f')) # retire la chaine en paramètre des extrémité de ch
print("split : ",ch.split())  # construit une liste des termes de la liste ch

