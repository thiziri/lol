
#apprentissage utilusant gensim et NLTK avec python
#transformation du corps en phrases
#attention telecharger les ressources avec nltk.download()
#osirim ne possède pas nltk
#import nltk   
from os import listdir
from os.path import isfile, join
from re import sub
from gensim import corpora, models, similarities, utils
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
#from nltk.corpus import stopwords
import numpy
from scipy import spatial
#import pytrec_eval
from math import log10

def miseAZeroToutNegatif(mdl,dim):
	for w in mdl.vocab:
		for i in range(dim):
			if(mdl[w][i]<0.0):
				mdl[w][i]=0
				
def sortFile(run):
	print("fichier à trier: ", run)
	# file = input()
	f = open(run, 'r')
	out = f.read()
	f.close()
	lines = out.split('\n')  # donne la liste des tokens séparés par \n donc la liste des lignes
	# print("Fichier : \n", lines) 
	print("contient %d lignes" % (len(lines)))
	print("Tri en cours, patientez...\n")
	# print(sorted(lines))
	tf = sorted(lines)
	ft = open(run + "_trie", 'w')
	for l in tf:
		ft.write(l + '\n')
	ft.close()
	print("Fin, trié avec succès :)")
	
#stoplist = stopwords.words('english')
dimConcept=300
win=5
minc=5
tailles={}
doc_freq={}
nbDoc=0
avr_doc_len_d=0.0
k1=2
b=0.75
idf={}
lamda=0.6

#rep="/users/iris/tbelkace/mesPgmPython/sentensCorpus/"
rep="E:/RIBDM/M2RIT/Collection/Collection_Thiziri/coll_dkaki/word2vec/mesTests/AP-88-90-tests/models/"
#rep="C:/Users/Thiziri/Desktop/models/"
qrels="E:/RIBDM/M2RIT/Collection/Collection_Thiziri/coll_dkaki/word2vec/mesTests/AP-88-90-tests/runs/evaluation/qrels201-250-88-90"
documents={}
vocabulaire={}
out_file=open(rep+"APCorpusSentences_tf_idf.txt", 'w')
pathDoc="E:/TREC/SOURCE/APt/ap88-90"
#pathDoc="C:/Users/Thiziri/Desktop/ColExt"
pathTop="E:/TREC/TOPICS/201-250"
#pathTop="C:/Users/Thiziri/Desktop/req"

print('Extraction du vocabulaire de la collection en cours ...\n %s'%(pathDoc)) 
for f in listdir(pathDoc):
	if isfile(join(pathDoc,f)):
		in_file=open(join(pathDoc,f), 'r') 
		nbDoc+=1
		text = in_file.read()
		'''
		sents = nltk.sent_tokenize(text)
		in_file.close()
		doc_aux=[]
		for s in sents:
			s=sub(r'[^a-zA-Z]+',' ', s)
			s=s.lower()
			out_file.write("%s\n" %(s))
			
			d=[word for word in s.split()]
			doc_aux+=d
			'''
		in_file.close()
		doc_aux=[]
		s=text
		s=sub(r'[^a-zA-Z]+',' ', s)
		s=s.lower()
		out_file.write("%s\n" %(s))
			
		d=[word for word in s.split()]
		doc_aux+=d
		tailles[f]=len(doc_aux)
		avr_doc_len_d+=tailles[f]
		for w in doc_aux : doc={w:doc_aux.count(w)} # doc={w:doc_aux.count(w) for w in doc_aux}
		documents[f]=doc
		for word in doc:
			vocabulaire[word]=1
			if(word not in doc_freq):
				doc_freq[word]=1
			else:
				doc_freq[word]+=1
        #out_file.write("\n" %(s))	
print("vocabulaire OK")		
out_file.close()
avr_doc_len_d/=nbDoc

print("\n sentence generation ... \n")
out_file=open(rep+"tfidf_APCorpusSentences.txt", 'w') # où stocker le corpus sous-forme de phrases
for f in listdir(pathDoc): # repertoire des doc texte
	if isfile(join(pathDoc,f)):
		in_file=open(join(pathDoc,f), 'r') 
		nbDoc+=1
		text = in_file.read()
		print("document: %s"%(f))
		#sents = nltk.sent_tokenize(text)
		in_file.close()
		doc_aux=[]
		# avec nltk
		'''	for s in sents:
			s=sub(r'[^a-zA-Z]+',' ', s) # regette tout les caractéres non alphabétiques
			s=s.lower()
			out_file.write("%s\n" %(s))

			d=[word for word in s.split()]
			doc_aux+=d  # document oxiliaire 
			#out_file.write("%s " %(s))
		''' # fin avec nltk 
		s=text
		s=s.lower()
		out_file.write("%s\n" %(s))
		d=[word for word in s.split()]
		doc_aux+=d  # document oxiliaire
		tailles[f]=len(doc_aux)
		for w in doc_aux : doc={w:doc_aux.count(w)} # doc={w:doc_aux.count(w) for w in doc_aux}
		for word in doc:
			if(word not in doc_freq):
				doc_freq[word]=1
			else:
				doc_freq[word]+=1
        #out_file.write("\n" %(s))		
out_file.close()
print("corpus traité avec succès \n")

#3 apprentissage
print("Apprentissage en cours ...\n")
sentences = LineSentence(rep+"tfidf_APCorpusSentences.txt")
model = Word2Vec(sentences, size=dimConcept, window=win, min_count=minc, workers=10)
print("Apprentissage OK\n")

#representation des documents 
documentsV={}
print("construction des représentations des documents ... \n")
for f in listdir(pathDoc): # ici lire tte la collection 
	if isfile(join(pathDoc,f)):
		in_file=open(join(pathDoc,f), 'r') # sans stockage de la matrice
		text = in_file.read()
		#sents = nltk.sent_tokenize(text)
		in_file.close()
		vec_doc=numpy.zeros(dimConcept) # vecteur nule : initialisé a 0
		'''	for s in sents:
			s=sub(r'[^a-zA-Z]+',' ', s)
			s=s.lower()
			#d=[word for word in s.split() if word not in stoplist]
			d=[word for word in s.split()] # osirim 
			doc={w:d.count(w) for w in d} # crérer un dictionnaire dont l'entrée est le mot et la valeur est la freq exp {good : 2}
			for word in doc:
				if(word in model.vocab): # vecteurs pondérés des termes
					vec_doc+=doc[word]*numpy.array(model[word])/doc_freq[word]
		''' # par
		s=text
		s=sub(r'[^a-zA-Z]+',' ', s)
		s=s.lower()
		#d=[word for word in s.split() if word not in stoplist]
		d=[word for word in s.split()] # osirim 
		for w in d : doc={w:d.count(w)} # crérer un dictionnaire dont l'entrée est le mot et la valeur est la freq exp {good : 2}
		for word in doc:
			if(word in model.vocab)and (word in doc_freq): # vecteurs pondérés des termes
				vec_doc+=doc[word]*numpy.array(model[word])/doc_freq[word]
		# fin par
		if (list(vec_doc)==list(numpy.zeros(dimConcept))):
			for val in range(len(vec_doc)): 
				vec_doc[val]= 0.001
		#out_file.write("%s " %(f))
		documentsV[f]=vec_doc # matrice de la collection
print("documents representation ok \n")

#representation des topics
topicV={}
print("Construction des vecteurs topics ... \n %s"%(pathTop))
for f in listdir(pathTop): # repertoire des topics
	if isfile(join(pathTop,f)):
		in_file=open(join(pathTop,f), 'r') 
		text = in_file.read()
		#sents = nltk.sent_tokenize(text)
		in_file.close()
		taille_top=0
		vec_doc=numpy.zeros(dimConcept) # initialiser le vecteur de la requêtes à des 0
		'''	for s in sents:
			s=sub(r'[^a-zA-Z]+',' ', s)
			s=s.lower()
			#d=[word for word in s.split() if word not in stoplist] # élimination des mots vides du document
			d=[word for word in s.split()] #Osirim
			taille_top+=len(d)
			doc={w:d.count(w) for w in d} # dictionnaire du document, w : tf(w)
			for word in doc:
				if(word in model.vocab): # recherche dans le vocabulaire généré
					vec_doc+=doc[word]*numpy.array(model[word])/doc_freq[word] # construction du vecteur de topic : somme_de_tot_les_mots_du_topic(tf(mot)*vecteur(mot)/taille(topic)) 
		'''
		#----
		s=text
		s=sub(r'[^a-zA-Z]+',' ', s)
		s=s.lower()
		#d=[word for word in s.split() if word not in stoplist] # élimination des mots vides du document
		d=[word for word in s.split()] #Osirim
		taille_top+=len(d)
		for w in d : doc={w:d.count(w)} # dictionnaire du document, w : tf(w)
		for word in doc:
			if(word in model.vocab)and (word in doc_freq): # recherche dans le vocabulaire généré
				vec_doc+=doc[word]*numpy.array(model[word])/doc_freq[word] 
				# construction du vecteur de topic : 
				#somme_de_tot_les_mots_du_topic(tf(mot)*vecteur(mot)/taille(topic)) 
		#-----
		#out_file.write("%s " %(f))
		if (list(vec_doc)==list(numpy.zeros(dimConcept))):
			for val in range(len(vec_doc)): 
				vec_doc[val]= 0.001
		topicV[f]=vec_doc
print("Topic representation ok \n")

topics={}
print("Traitement des requêtes en cours ...\n %s"%(pathTop))
for f in listdir(pathTop):
	if isfile(join(pathTop,f)):
		in_file=open(join(pathTop,f), 'r') 
		text = in_file.read()
		#sents = nltk.sent_tokenize(text)
		in_file.close()
		taille_top=0
		vec_doc=numpy.zeros(dimConcept)
		d=[]
		'''	for s in sents:
			s=sub(r'[^a-zA-Z]+',' ', s)
			s=s.lower()
			#d+=[word for word in s.split() if word not in stoplist]
			d+=[word for word in s.split()] # Osirim
		'''
		s=text
		s=sub(r'[^a-zA-Z]+',' ', s)
		s=s.lower()
		#d+=[word for word in s.split() if word not in stoplist]
		d+=[word for word in s.split()] # Osirim
		taille_top=len(d)
		for w in d : doc={w:d.count(w)}
		topics[f]=doc
print("Requêtes OK")


print("Calcul IDF")
for w in vocabulaire:
	idf[w]=1.0/doc_freq[w]
print("IDF OK\n")

#miseAZeroToutNegatif(model,dimConcept)
run='E:/RIBDM/M2RIT/Collection/Collection_Thiziri/coll_dkaki/word2vec/mesTests/AP-88-90-tests/runs/'+'run_tf_idf_multipli_positive_cosine_word2vec_concept'+str(dimConcept)+'_lamda'+str(lamda)+'_win'+str(win)+'_min'+str(minc)
#run='C:/Users/Thiziri/Desktop/res/test'
out_file=open(run, 'w')

print("RI en cours ...\n")
for t in topics.keys():
	top=topics[t]
	topVec=topicV[t]
	print("traitement topic %s" %(t))
	for f in listdir(pathDoc):
		doc=documents[f] # dictionnaire term : freq
		vecDoc=documentsV[f]
		score=0.001
		for wt in top: # calculer la somme tf*idf des termes doc/req
			if(wt in doc):
				if (wt in idf):
					print("idf = %f" %(idf[wt]))
					print("tf = %f" %(doc[wt]))
					score+=(idf[wt]+0.001)*(doc[wt]+1) # +1 pour lissage et éviter score null
				else : 
					print("tf = %f" %(doc[wt]))
					score+=(doc[wt]+1)
			elif (wt in idf):
				print("tf = %f" %(idf[wt]))
				score+=idf[wt]+0.001
			else : score+=0.001
		# calculer le cosine (d,q)
		#score*=1.0-spatial.distance.cosine(topVec, vecDoc)
		#score=lamda*score+(1-lamda)*((2-spatial.distance.cosine(topVec, vecDoc))/2)  #tf*id+cos_positif
		score=score*((2-spatial.distance.cosine(topVec, vecDoc))/2)      #tf*id*cos_positif
		print("score = %f" %(score))
		out_file.write("%s\tQ0\t%s\t0\t%f\tWord2vec%d_%d_%d\n" %(t,f,score,dimConcept,win,minc))
print("RI OK\n")	
out_file.close()
sortFile(run)

print("trec_eval en cours ...\n")
trec_run = pytrec_eval.TrecRun(run)
trec_qrels = pytrec_eval.QRels(qrels)
m=["avgPrec", "ndcg","precisionAt10","precisionAt50","precisionAt100"]
metrics=[pytrec_eval.avgPrec, pytrec_eval.ndcg,pytrec_eval.precisionAt(10),pytrec_eval.precisionAt(50),pytrec_eval.precisionAt(100)]
res=pytrec_eval.evaluate(trec_run, trec_qrels, metrics)
for i in range(0,len(m)):
	print("%s:%f\n" %(m[i],res[i]))
print("trec_eval OK\n")



		


