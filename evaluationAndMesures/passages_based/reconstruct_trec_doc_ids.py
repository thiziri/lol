import docopt
import os
from tqdm import tqdm
from os.path import join
from collections import defaultdict
from numpy import average as avg
import operator

def reconstruct(run_file, output, name):
    with open(join(output, "trec_" + name + ".txt"), 'w') as out_file:
        with open(run_file, 'r') as run:
            for line in tqdm(run):
                tokens = line.strip().split()
                q_id = tokens[0]
                # print(q_id)
                d_id = tokens[2]
                # print(d_id)
                new_line = line.replace(d_id, d_id.split("_")[0])
                # print(new_line)
                # break
                out_file.write("{l}".format(l=new_line))


def reconstruct_with_aggregation(run_file, output, name):
    uniques = defaultdict(dict)
    f = open(run_file, 'r')

    for line in f.readlines():
        if len(line.strip()) > 0:
            tokens = line.strip().split()
            doc_id, q_id = tokens[2].split('_')
            score = float(tokens[4])
            if doc_id not in uniques[q_id]:
                uniques[q_id][doc_id] = [score]
            else:
                uniques[q_id][doc_id].append(score)
    # average scores:
    scores = defaultdict(dict)
    for q in tqdm(uniques):
        for doc_id in uniques[q]:
            scores[q][doc_id] = round(avg(uniques[q][doc_id]), 6)
    # write results:
    with open(join(output, "trec_" + name + ".txt"), 'w') as out:
        sorted_scores = scores  # dict(sorted(scores.items(), key=lambda kv: kv[1]))
        for q in tqdm(sorted_scores):
            sorted_docs = sorted(sorted_scores[q].items(), key=operator.itemgetter(1), reverse=True)
            rank = range(1, len(sorted_docs) + 1)
            iter_rank = iter(rank)
            q_results = ["{q} Q0 {d} {i} {s} {m}".format(q=q, d=e[0], i=next(iter_rank), m=name,
                                                         s=e[1]) for e in sorted_docs]
            out.write('\n'.join(q_results) + '\n')


if __name__ == "__main__":
    args = docopt.docopt("""
           Usage:
              reconstruct_trec_doc_ids.py --r=<run_file_or_folder> --o=<output_directory>  [--n=<name>] [--tocheck=<clue>]

           Example:
              aggregate_passages.py --r=passages --o=path/to/output --n=documents.run 

           Options:
              --r=<passages_run_file>    TREC run file or folder of files of retrieved passages.
              --o=<output_directory>    Directory where final run will be stored.
              --n=<name>    Name of the model, optional.
              --tocheck=<clue>    Give the desired file name clue.
           """)

    if os.path.isfile(args["--r"]):
        print("Reading run file ...")
        reconstruct(args["--r"], args["--o"], args["--n"])
    else:
        print("Reading run files ...")
        for file in os.listdir(args["--r"]):
            if args["--tocheck"] in file and ".sh" not in file:
                print(file)
                name = file.split('.ranking')[0]  # .split('_')[0]
                reconstruct(os.path.join(args["--r"], file), args["--o"], name)

    print("Done.")
