# extract performance results according to a given mesure for statistic test
from os import listdir 
from os.path import join
import os
import docopt


if __name__ == "__main__":
    print("\n------Begin------\n")
    args = docopt.docopt("""
        Usage:
            extract_mesure_results.py <evaluate_folder> <outputfolder> <mesure_to_extract>
        
        """)
    print (args)
    print("{mesure} extraction ...".format(mesure=args["<mesure_to_extract>"]))
    
    for f in listdir(args["<evaluate_folder>"]) :
        eval_file=join(args["<evaluate_folder>"],f)
        runf = open(eval_file, "r")
        res = runf.name.replace(args["<evaluate_folder>"], '')+"_queries_"+args["<mesure_to_extract>"]
        print("res= "+res)
        out = args["<outputfolder>"]+res
        print(out)
        results=open(out, "w")
        lines = runf.readlines()
        for l in lines :
            if (args["<mesure_to_extract>"] in l) and ("all" not in l) and (args["<mesure_to_extract>"]+"0" not in l):
                req=l.split()[1]
                val=l.split()[2]
                results.write(req+"\t"+val+"\n")
    print("Finished.")
    print("result in : " + out)


