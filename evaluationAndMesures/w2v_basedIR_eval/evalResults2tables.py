
# evaluation with trec_eval9

from os import listdir 
from os.path import join
import os
import docopt
from tqdm import tqdm
import operator

"""
Find a sub-string between first and last strings in s
return: string
"""
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
	        evalResults2tables.py <eval_folder> <analyse_folder> <prfix_model>
	    
	    """)
	
	print("Evaluation of : ")
	print(args)

	print("---------\t BEGIN \t--------------\n")

	print("Analysing ...")

	anFile=open(join(args["<analyse_folder>"],args["<prfix_model>"]+".analysis"),"w")
	
	if "eq2" in args["<prfix_model>"].lower():
		# confA
		anFile.write("alpha\tMAP\tP@5\tP@10\tP@20\tnDCG@10\tnDCG@20\n")
		values = {}
		for f in tqdm(listdir(args["<eval_folder>"])):
			if "eq2" in f.lower():
				alpha = find_between(f.lower(),"_alpha","stemmed")
				with open(join(args["<eval_folder>"],f),"r") as f_in:
					lines = [l.strip() for l in f_in]
				for line in tqdm(lines):
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
					if (line.find("all")!=-1 and line.startswith("ndcg_cut_10 ")):
						ndcg_10=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("ndcg_cut_20 ")):
						ndcg_20=line.split()[2]
				values[int(alpha)] = (map_value, p_at5, p_at10, p_at20, ndcg_10, ndcg_20)
		#print(sorted(values.items(),key=operator.itemgetter(0)))
		for a in sorted(values.items(),key=operator.itemgetter(0)):
			anFile.write("{a}\t{map}\t{p5}\t{p10}\t{p20}\t{ndcg10}\t{ndcg20}\n".format(a=str(a[0]),map=a[1][0],p5=a[1][1],p10=a[1][2],p20=a[1][3],ndcg10=a[1][4],ndcg20=a[1][5]))

	elif "eq3" in args["<prfix_model>"].lower():
		# confB
		values={}
		anFile.write("MAP\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		for f in tqdm(listdir(args["<eval_folder>"])):
			if ("eq3" in f.lower()):
				a=int(find_between(f.lower(),"_alpha","_")) 
				lamb=float(find_between(f.lower(),"_lambda","stemmed"))
				if a not in values:
					values[a]={}
				with open(join(args["<eval_folder>"],f),"r") as f_in:
					lines = [l.strip() for l in f_in]
				map_value=""
				p_at5 = ""
				p_at10 = ""
				p_at20 = ""
				ndcg_10 = ""
				ndcg_20 = ""
				for line in tqdm(lines):
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
					if (line.find("all")!=-1 and line.startswith("ndcg_cut_10 ")):
						ndcg_10=line.split()[2]
				for line in lines:
					if (line.find("all")!=-1 and line.startswith("ndcg_cut_20 ")):
						ndcg_20=line.split()[2]
				values[a][lamb]=map_value,p_at5,p_at10,p_at20,ndcg_10,ndcg_20		
		alpha="alpha\t" + "\t".join([str(a) for a in values.keys()])
		anFile.write(alpha+"\n")
		#anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		#print(values)
		lamb_val=sorted(values[list(values.keys())[0]].keys())
		print("lambda : ",lamb_val)

		#print(values)

		#print(lamb_val)

		line_eval=''

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					map_value=values[av][lv][0]
					line_eval=line_eval+str(map_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@5\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write(alpha+"\n")

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					p5_value=values[av][lv][1]
					line_eval=line_eval+str(p5_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@10\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write(alpha+"\n")

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					p10_value=values[av][lv][2]
					line_eval=line_eval+str(p10_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("P@20\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write(alpha+"\n")

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					p20_value=values[av][lv][3]
					line_eval=line_eval+str(p20_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("nDCG@10\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write(alpha+"\n")

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					ndcg10_value=values[av][lv][4]
					line_eval=line_eval+str(ndcg10_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

		anFile.write("nDCG@20\n")
		anFile.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
		anFile.write(alpha+"\n")

		for lv in lamb_val:
			if 1:#(lv!=1.0):
				line_eval=str(lv)+'\t'
				for av in values.keys(): 
					ndcg20_value=values[av][lv][5]
					line_eval=line_eval+str(ndcg20_value)+'\t'
				anFile.write(line_eval+"\n")

		anFile.close()
	else:
		# confC
		print("Analysis of Eq4 is not available yet.")

			
	print("---------\t ENDED. \t--------------")


