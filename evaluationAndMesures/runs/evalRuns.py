
# evaluation with trec_eval9

from os import listdir 
from os.path import join, isfile
import os
import docopt
from tqdm import tqdm


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index(last, start)
        return (s[start:end])
    except ValueError:
        return ("")


if __name__ == "__main__":
    print("\n------Begin------\n")
    args = docopt.docopt("""
        Usage:
            evalRuns.py --r=<runs_folder> --te=<trec_eval> --rj=<qrels> --o=<outputfolder> [--c=<clue>]

        Options:
            --r=<runs_folder>    Give the folder of runs to be evaluated.
            --te=<trec_eval>    Give the path to trec_eval tool.
            --rj=<qrels>    The TREC like relevance judgements.
            --o=<outputfolder>    Where results will be stored.
            --c=<clue>    Facultataif, to distinguish desired files to evaluate.
        """)
    
    print("Evaluation of : ")
    print(args)
    print("---------\t BEGIN \t--------------\n")
    if not os.path.exists(args["--o"]):
        os.mkdir(args["--o"])

    print("Evaluating ...")

    for f in tqdm(listdir(args["--r"])):
        valid = False if bool(args["--c"]) else True
        if bool(args["--c"]) and args["--c"] in f:
            valid = True
        if isfile(join(args["--r"], f)) and valid:
            # construct the commande line 
            cmd1 = "./trec_eval"+" -q "+args["--rj"]+" "+join(args["--r"], f)+" > "+join(args["--o"], f)+".eval"
            cmd2 = "./trec_eval"+" -q -m ndcg_cut "+args["--rj"]+" "+join(args["--r"], f)+" >> "+join(args["--o"], f)+".eval"
            # run command in the corresponding directory
            os.chdir(args["--te"])
            os.system(cmd1)
            os.system(cmd2)

    print("Evaluation finished.")
