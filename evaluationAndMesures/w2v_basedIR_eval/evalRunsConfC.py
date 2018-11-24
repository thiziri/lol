
# evaluation with trec_eval9

from os import listdir 
from os.path import join
import os
import docopt


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return (s[start:end])
    except ValueError:
        return ("")


if __name__ == "__main__":
	print("\n------Begin------\n")
	args = docopt.docopt("""
	    Usage:
	        evalRuns.py <runs_folder> <trec_eval> <qrels> <outputfolder> <analyse_folder> <prefix>
	    
	    """)
	
	print("Evaluation of : ")
	print(args)

	print("---------\t BEGIN \t--------------\n")

	print("Evaluating ...")

	for f in listdir(args["<runs_folder>"]):
		fn=join(args["<runs_folder>"],f)
		if ("trie" in fn):  
			cmd1="./trec_eval -q "+args["<qrels>"]+" "+fn+" > "+join(args["<outputfolder>"],f)+"_eval"
			cmd2="./trec_eval -q -m ndcg_cut "+args["<qrels>"]+" "+fn+" >> "+join(args["<outputfolder>"],f)+"_eval"
			#os.system(cmd1)
			os.chdir(args["<trec_eval>"])
			os.system(cmd1)
			os.system(cmd2)

	print("Evaluation finished.")
	
	print("Analysing ...")
	#alpha=14

	for alpha in range(1,21):
		values={}
		lmda2=[]
		anFile=open(join(args["<analyse_folder>"],"analyse"+args["<prefix>"]+"alpha"+str(alpha)),"w")
		anFile.write("MAP\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		for f in listdir(args["<outputfolder>"]):
			#if (str(f).find("neg")!=-1 ) and (str(f).find("pos")==-1)and (str(f).find("impl1")!=-1) and (str(f).find("trie")!=-1):
			if (("trie" in str(f)) and ("alpha"+str(alpha)+"_" in str(f))):
				print("\n"+str(f)+"\n")
				lamb1=float(find_between(str(f),"lambda1_","_lambda2")[-3:]) # int between "alpha" and "_"
				lamb2=float(find_between(str(f),"lambda2_","_trie")) # "betha" or "Mlmbd"
				if lamb1 not in values:
					values[lamb1]={}
				if lamb2 not in lmda2:
					lmda2.append(lamb2)
				runf = open(join(args["<outputfolder>"],f),"r")
				lines = runf.readlines()
				map_value=""
				p_at5 = ""
				p_at10 = ""
				p_at20 = ""
				ndcg_20 = ""
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("map ")):
						map_value=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("P_5 ")):
						p_at5=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("P_10 ")):
						p_at10=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("P_20 ")):
						p_at20=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("ndcg_cut_20 ")):
						ndcg_20=line.split()[2]
				values[lamb1][lamb2]=map_value,p_at5,p_at10,p_at20,ndcg_20

		
		lamb1="lambda1\t"
		for a in sorted(values.keys()): 
			lamb1=lamb1+"\t"+str(a)

		anFile.write(lamb1+"\n")
		anFile.write("lambda2---------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		print(values.keys())
		#lamb_val=sorted(values[list(values.keys())[0]].keys())
		lamb_val=sorted(lmda2) #[0.1,0.2,0.3,0.4,0.5,0.6,0.7]
		#print("lambda2 : ",lamb_val)
		#print(values)
		#print(values[0.3][0.1])

		line_eval=''

		for lv in lamb_val:
			#if (lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in sorted(values.keys()): 
					try:
						map_value=values[av][lv][0]
					except:
						map_value=-1
					line_eval=line_eval+str(map_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@5\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		for lv in lamb_val:
			if (lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in sorted(values.keys()): 
					try:
						p5_value=values[av][lv][1]
					except:
						p5_value=-1
					line_eval=line_eval+str(p5_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@10\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		for lv in lamb_val:
			if (lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in sorted(values.keys()): 
					try:
						p10_value=values[av][lv][2]
					except:
						p10_value=-1
					line_eval=line_eval+str(p10_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@20\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")


		for lv in lamb_val:
			if (lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in sorted(values.keys()): 
					try:
						p20_value=values[av][lv][3]
					except:
						p20_value=-1
					line_eval=line_eval+str(p20_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("ndcg@20\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")


		for lv in lamb_val:
			if (lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in sorted(values.keys()): 
					try:
						ndcg_20=values[av][lv][4]
					except:
						ndcg_20=-1
					line_eval=line_eval+str(ndcg_20)+'\t'
				anFile.write(line_eval+"\n")

		anFile.close()
		

			
	print("---------\t ENDED. \t--------------")


