from os.path import isfile, join
import re
import docopt

if __name__ == "__main__":
	args = docopt.docopt("""
	    Usage:
	        Top1000.py <run> <outputfolder> [--nres=<val>]
	    
	    Options:
	        --nres=<val>    number of results list [default : 1000].
	        
	    """)
	run=args["<run>"]
	nres=int(args["--nres"])
	outputfolder=args["<outputfolder>"]

	lines=open(run).readlines()
	topics=[x.split('\t')[0] for x in lines]
	topics=sorted(list(set(topics)))
	print(topics)
	for t in topics:
		f=open(join(outputfolder,t),'w')
		for i in range(0,nres):
			l=lines[i]
			topDoc=l.split('\t')[2]
			#print(t,topDoc)
			f.write(topDoc+"\n")
		f.close()



