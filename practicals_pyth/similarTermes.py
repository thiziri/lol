import sys
import os
from gensim import corpora, models, similarities, utils
from gensim.models import Word2Vec
import numpy
from math import *
from scipy import spatial
from operator import itemgetter
from os import listdir
from re import sub

def cosine (u,v):
    s = 0
    s1 = 0
    s2 = 0
    n = len(u)
    for i in range (0,n):
        s += u[i] * v[i]
    for e in u :
        s1 += e**2
    for m in v :
        s2 += m**2
    return (s/(sqrt(s1)*sqrt(s2)))

# calculer les termes simsilaires à une requête

print("Calculer les termes similaires à une requête via word2vec\n")
req = " " 
repReq = "C:/Users/Thiziri/Desktop/ColExt" # repertoire des requêtes text 
vocabulaire = "E:/RIBDM/M2RIT/Collection/Collection_Thiziri/coll_dkaki/word2vec/mesTests/Word2vec300_win15_min5.txt" #"chemin au vocabulaire word2vec"
#fichListTerm = "E:/RIBDM/M2RIT/Collection/topic201_300/reqExpansion/" # fichier resultat
fichListTerm= "C:/Users/Thiziri/Desktop/res/"
n = 20 # enregister les 20 top words
dimConcept = 300

# charger le vocabulaire sous forme de modèle
print("chargement du vocabulaire en cours ...\n ")
model = Word2Vec.load_word2vec_format(vocabulaire, binary=False)  # C text format

# ........évaluer le modèle avec modele.accuracy.........

print ("vocabulaire chargé\n")
for f in listdir(repReq):
	in_file=open(repReq+"/"+f, 'r')
	# req = input("Votre requête : ")
	req = in_file.read()
	in_file.close()
	req=sub(r'[^a-zA-Z]+',' ', req)
	req = req.lower()
	r = req.split() # liste des termes de la requête
	print("liste des termes : ",r)
	similarTerms = {}
	print("calcul des termes similaires en cours ...")
	for w in model.vocab :
		s = []
		wv = numpy.zeros(dimConcept)
		wv = numpy.array(model[w])
		for wq in r : 	#sim = 1- spatial.distance.cosine(w,wq)
			wqv = numpy.zeros(dimConcept)
			if(wq in model.vocab): 
				wqv = numpy.array(model[wq])
				sim = cosine(wv,wqv)
			else :
				sim = 0
			s.append(sim)
		# similarité avec le terme w est :
		#score = sum(s)/len(s)
		score = max (s)
		print("score = ",score)
		if (score !=0):
			similarTerms [w] = score
	print ("extension terminée\n")
	#similarTermsT = {}
	print("Trie des termes en cours ...\n")
	litem = similarTerms.items()
	li=list(litem)
	liT=sorted(li,key=itemgetter(1),reverse=True)
	print ("Termes triés avec succès. \n")
	#ntb = input("vous voulez affichez combien de termes : ")
	#nbt = int(ntb)
	#listTerm = list(similarTermsT.keys())
	print ("sauvegarde des %d premiers termes ... \n" %(n))
	out_file=open(fichListTerm+f+"_max.txt", 'w')
	out_file.write("query : %s"%(req))
	out_file.write("\n")
	for k in range(0,n): 
		# lire de 0 à n-1 : n n'est pas inclu
		# print(liT[k])
		out_file.write(str(liT[k]))
		out_file.write("\n")
	out_file.close()
	print ("extension de %s fini.\n" %(f))
print ("fin d'extension de toute les requêtes.\n")








