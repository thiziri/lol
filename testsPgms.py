# tests de fonctions et programmes
from os import listdir
from os.path import isfile, join
from re import sub
import ast
import numpy
import pyndri

collection='C:/Users/Thiziri/Desktop/govExt'
index = pyndri.Index(collection)

for document_id in range(index.document_base(), index.maximum_document()):
    print(index.document(document_id))
	
# Queries the index with 'hello world' and returns the first 1000 results.
results = index.query('hello world', results_requested=1000)

for int_document_id, score in results:
    ext_document_id, _ = index.document(int_document_id)
    print(ext_document_id, score)
	
token2id, id2token, id2df = index.get_dictionary()

id2tf = index.get_term_frequencies()